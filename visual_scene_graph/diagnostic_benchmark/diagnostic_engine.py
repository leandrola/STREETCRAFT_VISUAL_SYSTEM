#!/usr/bin/env python3
"""Causal stage diagnosis for the VSG-0.5 controlled benchmark."""
from __future__ import annotations

from collections import Counter
import hashlib
import json

STAGE_ORDER = {
    "PERCEPTION": 0,
    "REFERENCE_REASONING": 1,
    "GRAPH_PROJECTION": 2,
    "COMPILER": 3,
    "GENERATION": 4,
    "NONE": 5,
}


def _by_id(items: list[dict], key: str = "id") -> dict[str, dict]:
    return {item[key]: item for item in items if item.get(key)}


def _finding(origin: str, code: str, target: str, expected=None, observed=None) -> dict:
    finding = {"origin": origin, "code": code, "target": target}
    if expected is not None:
        finding["expected"] = expected
    if observed is not None:
        finding["observed"] = observed
    return finding


def diagnose_pipeline(
    *,
    expected_graph: dict,
    sar2: dict,
    reference_reasoning: dict,
    vsg: dict,
    generation_contract: dict,
    observed_output_graph: dict,
) -> dict:
    """Locate the earliest stage that can explain each observed delta."""
    findings = []

    expected_nodes = _by_id(expected_graph.get("nodes", []))
    expected_edges = _by_id(expected_graph.get("edges", []))
    sar_nodes = _by_id(sar2.get("entities", []), "entity_id")
    sar_edges = _by_id(sar2.get("relationships", []), "relationship_id")
    vsg_nodes = _by_id(vsg.get("nodes", []))
    vsg_edges = _by_id(vsg.get("edges", []))

    # Stage 1: source interpretation / SAR2.
    for node_id in sorted(set(expected_nodes) - set(sar_nodes)):
        findings.append(_finding("PERCEPTION", "PERCEPTION_NODE_MISSING", node_id))
    for edge_id in sorted(set(expected_edges) - set(sar_edges)):
        findings.append(_finding("PERCEPTION", "PERCEPTION_RELATION_MISSING", edge_id))

    # Stage 2: RR2 admission. Only expected ADMITTED observations are normative.
    rr_projection = {
        item.get("need_id") for item in reference_reasoning.get("generation_projection", [])
        if item.get("need_id")
    }
    expected_admissions = {
        item.get("need_id") for item in expected_graph.get("reference_observations", [])
        if item.get("result") == "ADMITTED"
    }
    for need_id in sorted(expected_admissions - rr_projection):
        findings.append(_finding("REFERENCE_REASONING", "RR2_EXPECTED_ADMISSION_MISSING", need_id))

    # Stage 3: SAR2/RR2 -> VSG projection.
    for node_id in sorted(set(sar_nodes) - set(vsg_nodes)):
        findings.append(_finding("GRAPH_PROJECTION", "VSG_NODE_OMISSION", node_id))
    for edge_id in sorted(set(sar_edges) - set(vsg_edges)):
        findings.append(_finding("GRAPH_PROJECTION", "VSG_RELATION_OMISSION", edge_id))
    vsg_observations = {
        item.get("need_id") for item in vsg.get("reference_observations", [])
        if item.get("result") == "ADMITTED"
    }
    for need_id in sorted(rr_projection - vsg_observations):
        findings.append(_finding("GRAPH_PROJECTION", "VSG_RR_OBSERVATION_MISSING", need_id))

    # Stage 4: VSG -> generation contract shadow projection.
    contract_nodes = set(generation_contract.get("required_nodes", []))
    contract_edges = set(generation_contract.get("required_edges", []))
    for node_id in sorted(set(vsg_nodes) - contract_nodes):
        findings.append(_finding("COMPILER", "COMPILER_NODE_OMISSION", node_id))
    for edge_id in sorted(set(vsg_edges) - contract_edges):
        findings.append(_finding("COMPILER", "COMPILER_RELATION_OMISSION", edge_id))
    contract_text = generation_contract.get("semantic_text", {})
    for node_id, node in sorted(vsg_nodes.items()):
        if not node.get("locks", {}).get("semantic"):
            continue
        expected_text = node.get("properties", {}).get("text")
        if expected_text is not None and contract_text.get(node_id) != expected_text:
            findings.append(_finding(
                "COMPILER", "COMPILER_SEMANTIC_LOCK_OMISSION", node_id,
                expected=expected_text, observed=contract_text.get(node_id),
            ))

    # Stage 5: generation contract -> observed output graph.
    output_nodes = _by_id(observed_output_graph.get("nodes", []))
    output_edges = _by_id(observed_output_graph.get("edges", []))
    for node_id in sorted(contract_nodes - set(output_nodes)):
        findings.append(_finding("GENERATION", "OUTPUT_NODE_MISSING", node_id))
    for edge_id in sorted(contract_edges):
        expected_edge = vsg_edges.get(edge_id)
        observed_edge = output_edges.get(edge_id)
        if observed_edge is None:
            findings.append(_finding("GENERATION", "OUTPUT_RELATION_MISSING", edge_id))
        elif expected_edge is not None:
            expected_tuple = (expected_edge.get("type"), expected_edge.get("from"), expected_edge.get("to"))
            observed_tuple = (observed_edge.get("type"), observed_edge.get("from"), observed_edge.get("to"))
            if expected_tuple != observed_tuple:
                findings.append(_finding(
                    "GENERATION", "OUTPUT_RELATION_MISMATCH", edge_id,
                    expected=expected_tuple, observed=observed_tuple,
                ))
    for node_id, expected_text in sorted(contract_text.items()):
        if node_id not in output_nodes:
            continue
        observed_text = output_nodes[node_id].get("properties", {}).get("text")
        if observed_text != expected_text:
            findings.append(_finding(
                "GENERATION", "OUTPUT_SEMANTIC_MUTATION", node_id,
                expected=expected_text, observed=observed_text,
            ))

    findings.sort(key=lambda item: (STAGE_ORDER[item["origin"]], item["code"], item["target"]))
    primary = findings[0] if findings else {
        "origin": "NONE", "code": "NO_FAILURE", "target": "pipeline"
    }
    return {
        "status": "FAILURE_LOCALIZED" if findings else "NO_FAILURE",
        "primary_diagnosis": primary,
        "findings": findings,
        "finding_count": len(findings),
        "origin_counts": dict(sorted(Counter(item["origin"] for item in findings).items())),
    }


def snapshot_sha256(value):
    """Canonical structured-snapshot hash; shared with Causal Trace."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


# VSG-1.5 enriches diagnostic snapshots; the VSG-0.5 API above is unchanged.
TRACE_STAGES = ("SOURCE_EVIDENCE", "SAR2", "RR2", "VSG", "GRAPH_LOCKS",
                "SHADOW_COMPILER", "OBSERVED_OUTPUT", "DIAGNOSTIC")
ORIGIN_TO_STAGE = {"PERCEPTION": "SAR2", "REFERENCE_REASONING": "RR2",
                   "GRAPH_PROJECTION": "VSG", "COMPILER": "SHADOW_COMPILER",
                   "GENERATION": "OBSERVED_OUTPUT"}


def check_causal_graph_locks(*, expected_graph, sar2, reference_reasoning,
                            vsg, shadow_contract, observed_output_graph):
    """Recheck immutable expected locks at each *supplied* diagnostic transition."""
    try:
        from ..graph_locks import validate_graph_locks
        from ..vsg_observer import build_visual_scene_graph
    except ImportError:
        from graph_locks import validate_graph_locks
        from vsg_observer import build_visual_scene_graph

    input_sha256 = {k: snapshot_sha256(v) for k, v in {
        "expected_graph": expected_graph, "sar2": sar2, "reference_reasoning": reference_reasoning,
        "vsg": vsg, "shadow_contract": shadow_contract, "observed_output_graph": observed_output_graph}.items()}
    needs = [{"need_id": o["need_id"], "target_entity_id": o.get("target_node_id")}
             for o in expected_graph["reference_observations"]]
    interpreted = build_visual_scene_graph(sar2, reference_reasoning=reference_reasoning,
                                          reference_needs=needs)
    findings = []
    for stage, candidate in (("SAR2", interpreted), ("VSG", vsg),
                             ("OBSERVED_OUTPUT", observed_output_graph)):
        for finding in validate_graph_locks(expected_graph, candidate)["findings"]:
            # RR2 admission does not belong to source perception.
            if stage == "SAR2" and finding["lock_type"] == "REFERENCE_ISOLATION_LOCK":
                continue
            findings.append({"stage": stage, **finding})
    expected = _by_id(expected_graph["graph_locks"]["items"])
    actual = _by_id(vsg["graph_locks"]["items"])
    for lock_id, lock in sorted(expected.items()):
        if actual.get(lock_id) != lock:
            findings.append({"stage": "GRAPH_LOCKS", "lock_id": lock_id,
                             "lock_type": lock["type"], "target": lock["target"],
                             "code": "GRAPH_LOCK_MISSING" if lock_id not in actual else "GRAPH_LOCK_ALTERED"})
        if lock_id not in shadow_contract["required_locks"]:
            findings.append({"stage": "SHADOW_COMPILER", "lock_id": lock_id,
                             "lock_type": lock["type"], "target": lock["target"],
                             "code": "SHADOW_LOCK_OMISSION"})
    return {"mode": "VALIDATE_ONLY", "governs_generation": False,
            "status": "FAIL" if findings else "PASS", "findings": findings, "input_sha256": input_sha256}


def diagnose_causal_snapshots(*, expected_graph, sar2, reference_reasoning,
                             vsg, shadow_contract, observed_output_graph):
    """Benchmark source of truth, with lock-aware checks between its stages.

    Existing VSG-0.5 diagnoses take precedence within the same stage. Lock IDs
    annotate those diagnoses rather than replacing an earlier causal transition.
    """
    from copy import deepcopy
    legacy = diagnose_pipeline(expected_graph=expected_graph, sar2=sar2,
                               reference_reasoning=reference_reasoning, vsg=vsg,
                               generation_contract=shadow_contract,
                               observed_output_graph=observed_output_graph)
    lock_check = check_causal_graph_locks(
        expected_graph=expected_graph, sar2=sar2, reference_reasoning=reference_reasoning,
        vsg=vsg, shadow_contract=shadow_contract, observed_output_graph=observed_output_graph)
    kinds = {n["id"]: "NODE" for n in expected_graph["nodes"]}
    kinds.update({e["id"]: "EDGE" for e in expected_graph["edges"]})
    findings = []
    for f in legacy["findings"]:
        findings.append({**deepcopy(f), "stage": ORIGIN_TO_STAGE[f["origin"]],
                         "target_kind": kinds.get(f["target"], "REFERENCE"),
                         "diagnostic_source": "VSG_0_5", "lock_ids": []})
    locks = _by_id(expected_graph["graph_locks"]["items"])
    for f in lock_check["findings"]:
        lock = locks.get(f["lock_id"], {})
        target = f["target"]["id"]
        kind = f["target"]["kind"]
        if f["lock_type"] == "REFERENCE_ISOLATION_LOCK":
            target, kind = lock["expected"]["need_id"], "REFERENCE"
        if f["stage"] == "GRAPH_LOCKS" or f["code"] == "SHADOW_LOCK_OMISSION":
            target, kind = f["lock_id"], "LOCK"
        # Topology failures concern the edge, not just the owner of its lock.
        if f["code"] == "GEOMETRY_TOPOLOGY_MISSING":
            target, kind = f["observed"], "EDGE"
        elif f["code"] == "GEOMETRY_TOPOLOGY_CHANGED":
            target, kind = f["observed"]["id"], "EDGE"
        matches = [x for x in findings if x["stage"] == f["stage"]
                   and x["target"] == target and x["target_kind"] == kind]
        if matches:
            for x in matches:
                x["lock_ids"] = sorted(set(x["lock_ids"] + [f["lock_id"]]))
        else:
            findings.append({"stage": f["stage"], "code": f["code"], "target": target,
                             "target_kind": kind, "diagnostic_source": "GRAPH_LOCKS",
                             "lock_ids": [f["lock_id"]]})
    # Retain downstream disappearance even when an earlier omission meant the
    # shadow contract never requested that element. These are symptoms, not a
    # replacement for the benchmark's earlier primary stage.
    for field, key, kind in (("nodes", "id", "NODE"), ("edges", "id", "EDGE"),
                              ("reference_observations", "need_id", "REFERENCE")):
        expected_ids = {row[key] for row in expected_graph[field]
                        if kind != "REFERENCE" or row.get("result") == "ADMITTED"}
        observed_ids = {row[key] for row in observed_output_graph[field]
                        if kind != "REFERENCE" or row.get("result") == "ADMITTED"}
        for target in sorted(expected_ids - observed_ids):
            if not any(f["stage"] == "OBSERVED_OUTPUT" and f["target"] == target
                       and f["target_kind"] == kind for f in findings):
                findings.append({"stage": "OBSERVED_OUTPUT", "code": f"OUTPUT_EXPECTED_{kind}_ABSENT",
                                 "target": target, "target_kind": kind,
                                 "diagnostic_source": "EXPECTED_OUTPUT_COMPARISON", "lock_ids": []})
    findings.sort(key=lambda f: (TRACE_STAGES.index(f["stage"]),
                                f["diagnostic_source"] != "VSG_0_5", f["code"], f["target"]))
    return {"status": "FAILURE_LOCALIZED" if findings else "NO_FAILURE",
            "primary_diagnosis": deepcopy(findings[0]) if findings else None,
            "findings": findings, "finding_count": len(findings), "input_sha256": lock_check["input_sha256"]}
