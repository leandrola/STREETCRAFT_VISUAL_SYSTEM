#!/usr/bin/env python3
"""Run VSG-0.5 controlled causal diagnostic cases."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
for rel in ("scene_intelligence", "visual_scene_graph", "visual_scene_graph/diagnostic_benchmark"):
    sys.path.insert(0, str(ROOT / rel))

from scene_intelligence import build_scene_analysis_record
from vsg_observer import build_visual_scene_graph
from diagnostic_engine import diagnose_pipeline


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _base_rr() -> tuple[dict, list[dict]]:
    rr = {
        "status": "READY",
        "trace": [{"need_id": "N-ROOF", "evidence_bundle_ids": ["EB-DIAG-ROOF"]}],
        "generation_projection": [{"need_id": "N-ROOF", "evidence_unit_id": "EU-DIAG-ROOF"}],
    }
    needs = [{"need_id": "N-ROOF", "target_entity_id": "roof_01"}]
    return rr, needs


def _contract_from_vsg(vsg: dict) -> dict:
    semantic_text = {}
    for node in vsg.get("nodes", []):
        text = node.get("properties", {}).get("text")
        if node.get("locks", {}).get("semantic") and text is not None:
            semantic_text[node["id"]] = text
    return {
        "kind": "VSG_0_5_SHADOW_CONTRACT",
        "governs_generation": False,
        "required_nodes": sorted(node["id"] for node in vsg.get("nodes", [])),
        "required_edges": sorted(edge["id"] for edge in vsg.get("edges", [])),
        "semantic_text": semantic_text,
    }


def _output_from_contract(vsg: dict, contract: dict) -> dict:
    nodes_by_id = {node["id"]: deepcopy(node) for node in vsg.get("nodes", [])}
    edges_by_id = {edge["id"]: deepcopy(edge) for edge in vsg.get("edges", [])}
    return {
        "nodes": [nodes_by_id[node_id] for node_id in contract["required_nodes"] if node_id in nodes_by_id],
        "edges": [edges_by_id[edge_id] for edge_id in contract["required_edges"] if edge_id in edges_by_id],
    }


def _drop_node(container: dict, collection: str, key: str, target: str) -> None:
    container[collection] = [item for item in container[collection] if item.get(key) != target]


def _apply_case(base_scene: dict, expected_graph: dict, case: dict) -> dict:
    scene = deepcopy(base_scene)
    rr, needs = _base_rr()
    mutation = case["mutation"]
    stage, operation, target = mutation["stage"], mutation["operation"], mutation["target"]

    if stage == "PERCEPTION" and operation == "drop_node":
        _drop_node(scene, "entities", "entity_id", target)
        scene["relationships"] = [
            rel for rel in scene["relationships"]
            if target not in {rel.get("subject"), rel.get("object")}
        ]
    elif stage == "PERCEPTION" and operation == "drop_edge":
        _drop_node(scene, "relationships", "relationship_id", target)

    sar2 = build_scene_analysis_record(**scene)

    if stage == "REFERENCE_REASONING" and operation == "drop_projection":
        rr["generation_projection"] = [
            item for item in rr["generation_projection"] if item.get("need_id") != target
        ]
        rr["trace"] = [{"need_id": target, "reason": "NO_MATCH", "evidence_bundle_ids": []}]

    vsg = build_visual_scene_graph(sar2, reference_reasoning=rr, reference_needs=needs)
    if stage == "GRAPH_PROJECTION" and operation == "drop_node":
        _drop_node(vsg, "nodes", "id", target)
        vsg["edges"] = [
            edge for edge in vsg["edges"]
            if target not in {edge.get("from"), edge.get("to")}
        ]
    elif stage == "GRAPH_PROJECTION" and operation == "drop_edge":
        _drop_node(vsg, "edges", "id", target)
    elif stage == "GRAPH_PROJECTION" and operation == "drop_reference_observation":
        _drop_node(vsg, "reference_observations", "need_id", target)

    contract = _contract_from_vsg(vsg)
    if stage == "COMPILER" and operation == "drop_node":
        contract["required_nodes"] = [node_id for node_id in contract["required_nodes"] if node_id != target]
    elif stage == "COMPILER" and operation == "drop_edge":
        contract["required_edges"] = [edge_id for edge_id in contract["required_edges"] if edge_id != target]
    elif stage == "COMPILER" and operation == "drop_semantic_text":
        contract["semantic_text"].pop(target, None)

    output = _output_from_contract(vsg, contract)
    if stage == "GENERATION" and operation == "drop_node":
        _drop_node(output, "nodes", "id", target)
        output["edges"] = [
            edge for edge in output["edges"]
            if target not in {edge.get("from"), edge.get("to")}
        ]
    elif stage == "GENERATION" and operation == "replace_edge_type":
        for edge in output["edges"]:
            if edge.get("id") == target:
                edge["type"] = mutation["value"]
    elif stage == "GENERATION" and operation == "replace_text":
        for node in output["nodes"]:
            if node.get("id") == target:
                node.setdefault("properties", {})["text"] = mutation["value"]

    diagnosis = diagnose_pipeline(
        expected_graph=expected_graph,
        sar2=sar2,
        reference_reasoning=rr,
        vsg=vsg,
        generation_contract=contract,
        observed_output_graph=output,
    )
    actual = diagnosis["primary_diagnosis"]
    expected = case["expected"]
    passed = actual["origin"] == expected["origin"] and actual["code"] == expected["code"]
    return {
        "case_id": case["case_id"],
        "title": case["title"],
        "mutation": mutation,
        "expected": expected,
        "actual": {"origin": actual["origin"], "code": actual["code"], "target": actual["target"]},
        "status": "PASS" if passed else "FAIL",
        "finding_count": diagnosis["finding_count"],
        "origin_counts": diagnosis["origin_counts"],
    }


def run(cases_path: Path, fixture_path: Path) -> dict:
    spec = json.loads(cases_path.read_text())
    base_scene = json.loads(fixture_path.read_text())
    base_sar2 = build_scene_analysis_record(**base_scene)
    rr, needs = _base_rr()
    expected_graph = build_visual_scene_graph(base_sar2, reference_reasoning=rr, reference_needs=needs)
    results = [_apply_case(base_scene, expected_graph, case) for case in spec["cases"]]
    passed = sum(result["status"] == "PASS" for result in results)
    accuracy = passed / len(results) if results else 0.0
    covered = sorted({result["actual"]["origin"] for result in results if result["status"] == "PASS"})
    missing_origins = sorted(set(spec["required_origins"]) - set(covered))
    healthy = next(result for result in results if result["case_id"] == "VSG-DIAG-13")
    gate_pass = accuracy >= spec["minimum_accuracy"] and not missing_origins and healthy["status"] == "PASS"
    return {
        "suite": spec["suite"],
        "version": spec["version"],
        "method": spec["method"],
        "status": "PASS" if gate_pass else "FAIL",
        "gate": {
            "minimum_accuracy": spec["minimum_accuracy"],
            "actual_accuracy": round(accuracy, 4),
            "cases_passed": passed,
            "cases_total": len(results),
            "required_origins": spec["required_origins"],
            "covered_origins": covered,
            "missing_origins": missing_origins,
            "healthy_control": healthy["status"],
        },
        "limitations": [
            "Controlled stage-fault injection; not a claim of pixel-level output understanding.",
            "The generation contract used here is a non-governing shadow benchmark artifact, not VSG-2.",
        ],
        "provenance": {
            "cases_sha256": _sha(cases_path),
            "fixture_sha256": _sha(fixture_path),
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--fixture", type=Path, default=ROOT / "visual_scene_graph/fixtures/kennys_rooftop_vsg0.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run(args.cases, args.fixture)
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
