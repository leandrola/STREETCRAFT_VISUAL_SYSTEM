#!/usr/bin/env python3
"""Causal stage diagnosis for the VSG-0.5 controlled benchmark."""
from __future__ import annotations

from collections import Counter

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
