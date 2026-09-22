"""Controlled Causal Trace corpus; reuses VSG-0.5 injection and Kenny's fixtures."""
from copy import deepcopy
import json
from pathlib import Path

from .diagnostic_benchmark.run_benchmark import (
    _base_rr, build_case_snapshots, build_scene_analysis_record, build_visual_scene_graph,
)
from .diagnostic_benchmark.diagnostic_engine import (
    ORIGIN_TO_STAGE, check_causal_graph_locks, diagnose_causal_snapshots,
)
from .causal_trace import build_causal_trace, canonical_sha256, validate_causal_trace

ROOT = Path(__file__).resolve().parents[1]
ADDITIONAL = [
    {"case_id": "VSG-TRACE-14", "title": "Semantic lock: observed Kenny's text changed",
     "mutation": "semantic", "expected": {"stage": "OBSERVED_OUTPUT", "code": "OUTPUT_SEMANTIC_MUTATION",
     "artifact_id": "sign_01", "lock_id": "GL-SEM-SIGN_01"}},
    {"case_id": "VSG-TRACE-15", "title": "Geometry lock: VSG changes building type",
     "mutation": "geometry", "expected": {"stage": "VSG", "code": "GEOMETRY_TYPE_CHANGED",
     "artifact_id": "building_01", "lock_id": "GL-GEO-BUILDING_01"}},
    {"case_id": "VSG-TRACE-16", "title": "Occlusion lock: observed relation changed",
     "mutation": "occlusion", "expected": {"stage": "OBSERVED_OUTPUT", "code": "OUTPUT_RELATION_MISMATCH",
     "artifact_id": "rel_parapet_occludes", "lock_id": "GL-OCC-REL_PARAPET_OCCLUDES"}},
    {"case_id": "VSG-TRACE-17", "title": "Reference Isolation: forbidden geometry transferred in VSG",
     "mutation": "reference", "expected": {"stage": "VSG", "code": "REFERENCE_ISOLATION_VIOLATION",
     "artifact_id": "N-ROOF", "lock_id": "GL-REF-N-ROOF-ROOF_01"}},
    {"case_id": "VSG-TRACE-18", "title": "Ledger loses a semantic Graph Lock",
     "mutation": "ledger", "expected": {"stage": "GRAPH_LOCKS", "code": "GRAPH_LOCK_MISSING",
     "artifact_id": "GL-SEM-SIGN_01", "lock_id": "GL-SEM-SIGN_01"}},
    {"case_id": "VSG-TRACE-19", "title": "Shadow contract drops a Graph Lock requirement",
     "mutation": "shadow", "expected": {"stage": "SHADOW_COMPILER", "code": "SHADOW_LOCK_OMISSION",
     "artifact_id": "GL-SEM-SIGN_01", "lock_id": "GL-SEM-SIGN_01"}},
]


def complete_artifacts(snapshots):
    """Collect actual diagnostic reports for these controlled input snapshots."""
    data = deepcopy(snapshots)
    data["graph_lock_validation"] = check_causal_graph_locks(**snapshots)
    data["diagnosis"] = diagnose_causal_snapshots(**snapshots)
    return data


def corpus():
    cases = json.loads((ROOT / "visual_scene_graph/diagnostic_benchmark/cases.json").read_text())["cases"]
    scene = json.loads((ROOT / "visual_scene_graph/fixtures/kennys_rooftop_vsg0.json").read_text())
    rr, needs = _base_rr()
    expected = build_visual_scene_graph(build_scene_analysis_record(**scene), reference_reasoning=rr, reference_needs=needs)
    rows = []
    for case in cases:
        data = build_case_snapshots(scene, expected, case, trace_artifacts=True)
        target = case["mutation"]["target"]
        rows.append(({"case_id": case["case_id"], "title": case["title"], "expected": {
            "stage": ORIGIN_TO_STAGE.get(case["expected"]["origin"]),
            "code": case["expected"]["code"], "artifact_id": target}}, complete_artifacts(data)))

    scene = json.loads((ROOT / "visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json").read_text())
    # Same RR2 IDs and scope as the existing Graph Locks fixture tests.
    rr = {"status": "READY", "trace": [{"need_id": "N-ROOF", "evidence_bundle_ids": ["EB-ROOF"]}],
          "generation_projection": [{"need_id": "N-ROOF", "evidence_unit_id": "EU-ROOF",
             "permitted_learning": ["material family", "equipment family"],
             "forbidden_transfer": ["exact geometry", "source signage"]}]}
    expected = build_visual_scene_graph(build_scene_analysis_record(**scene), reference_reasoning=rr, reference_needs=needs)
    for case in ADDITIONAL:
        data = build_case_snapshots(scene, expected, cases[-1], trace_artifacts=True)
        # The shared runner's default RR2 is VSG-0.5's roof observation; replace
        # it explicitly with the VSG-1 fixture's scoped diagnostic observation.
        data["reference_reasoning"] = deepcopy(rr)
        data["vsg"] = deepcopy(expected)
        data["observed_output_graph"] = {k: deepcopy(expected[k]) for k in ("nodes", "edges", "reference_observations")}
        op = case["mutation"]
        if op == "semantic":
            next(n for n in data["observed_output_graph"]["nodes"] if n["id"] == "sign_01")["properties"]["text"] = "KENNYS"
        elif op == "geometry":
            for snapshot in (data["vsg"], data["observed_output_graph"]):
                next(n for n in snapshot["nodes"] if n["id"] == "building_01")["type"] = "facade"
        elif op == "occlusion":
            next(e for e in data["observed_output_graph"]["edges"] if e["id"] == "rel_parapet_occludes")["type"] = "IN_FRONT_OF"
        elif op == "reference":
            for snapshot in (data["vsg"], data["observed_output_graph"]):
                snapshot["reference_observations"][0]["applied_transfers"] = ["exact geometry"]
        elif op == "ledger":
            data["vsg"]["graph_locks"]["items"] = [l for l in data["vsg"]["graph_locks"]["items"] if l["id"] != "GL-SEM-SIGN_01"]
        elif op == "shadow":
            data["shadow_contract"]["required_locks"].remove("GL-SEM-SIGN_01")
        rows.append((case, complete_artifacts(data)))
    return rows


def run_causal_cases():
    results = []
    for case, artifacts in corpus():
        input_hash = canonical_sha256(artifacts)
        trace = build_causal_trace(**artifacts)
        validation = validate_causal_trace(trace, artifacts)
        root = trace["root_cause"]
        expected = case["expected"]
        healthy = expected["stage"] is None
        correct = (trace["status"] == "HEALTHY" and root is None and not trace["symptoms"]) if healthy else (
            trace["status"] == "FAILURE_LOCALIZED" and all(root[k] == expected[k] for k in ("stage", "code", "artifact_id")))
        if "lock_id" in expected:
            correct = correct and expected["lock_id"] in root["lock_ids"]
        repeat = build_causal_trace(**deepcopy(artifacts))
        checks = {"expected_root_cause": correct, "resolvable_acyclic_trace": validation["status"] == "PASS",
                  "deterministic": repeat == trace, "inputs_unchanged": input_hash == canonical_sha256(artifacts)}
        results.append({"case_id": case["case_id"], "expected": expected,
                        "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
                        "validation": validation, "artifacts": artifacts, "trace": trace})
    return {"suite": "VSG-1.5 Causal Trace", "version": "1.5.0", "mode": "TRACE_ONLY",
            "governs_generation": False, "status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
            "cases": len(results), "passed": sum(r["status"] == "PASS" for r in results),
            "causal_accuracy": sum(r["checks"]["expected_root_cause"] for r in results) / len(results),
            "cycle_count": sum(r["validation"]["cycle_count"] for r in results),
            "unresolved_references": sum(r["validation"]["unresolved_references"] for r in results),
            "healthy_control_false_positives": sum(r["trace"]["status"] != "HEALTHY" or r["trace"]["root_cause"] is not None
                                                    for r in results if r["expected"]["stage"] is None),
            "results": results}
