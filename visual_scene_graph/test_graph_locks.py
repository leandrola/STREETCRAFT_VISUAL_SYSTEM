from copy import deepcopy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scene_intelligence"))
sys.path.insert(0, str(ROOT / "visual_scene_graph"))

from scene_intelligence import build_scene_analysis_record
from graph_locks import build_graph_locks, validate_graph_locks
from vsg_observer import build_visual_scene_graph

fixture = json.loads((ROOT / "visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json").read_text())
sar2 = build_scene_analysis_record(**fixture)
rr = {
    "status": "READY",
    "trace": [{"need_id": "N-ROOF", "evidence_bundle_ids": ["EB-ROOF"]}],
    "generation_projection": [{
        "need_id": "N-ROOF", "evidence_unit_id": "EU-ROOF",
        "permitted_learning": ["material family", "equipment family"],
        "forbidden_transfer": ["exact geometry", "source signage"],
    }],
}
needs = [{"need_id": "N-ROOF", "target_entity_id": "roof_01"}]
graph = build_visual_scene_graph(sar2, reference_reasoning=rr, reference_needs=needs)

assert graph["schema_version"] == "1.0.0"
assert graph["governs_generation"] is False
ledger = graph["graph_locks"]
assert ledger["version"] == "1.0.0"
assert ledger["mode"] == "VALIDATE_ONLY"
assert ledger["governs_generation"] is False
assert ledger["summary"]["total"] == 5
assert ledger["summary"]["by_type"] == {
    "GEOMETRY_LOCK": 2,
    "OCCLUSION_LOCK": 1,
    "REFERENCE_ISOLATION_LOCK": 1,
    "SEMANTIC_TEXT_LOCK": 1,
}
assert ledger["summary"]["warnings"] == []
assert len({lock["id"] for lock in ledger["items"]}) == 5
assert all(lock["enforcement"] == "VALIDATE_ONLY" for lock in ledger["items"])
assert len(ledger["ledger_sha256"]) == 64
assert build_graph_locks(graph) == ledger

lock_by_type = {lock["type"]: lock for lock in ledger["items"] if lock["type"] != "GEOMETRY_LOCK"}
assert lock_by_type["SEMANTIC_TEXT_LOCK"]["expected"]["text"] == "KENNY'S"
assert lock_by_type["OCCLUSION_LOCK"]["expected"]["edge"]["type"] == "OCCLUDES"
assert lock_by_type["REFERENCE_ISOLATION_LOCK"]["expected"]["forbidden_transfer"] == ["exact geometry", "source signage"]
assert validate_graph_locks(graph)["status"] == "PASS"

semantic = deepcopy(graph)
next(node for node in semantic["nodes"] if node["id"] == "sign_01")["properties"]["text"] = "KENNYS"
semantic_result = validate_graph_locks(graph, semantic)
assert semantic_result["status"] == "FAIL"
assert any(item["code"] == "SEMANTIC_TEXT_LOCK_VIOLATION" for item in semantic_result["findings"])

geometry = deepcopy(graph)
next(node for node in geometry["nodes"] if node["id"] == "building_01")["type"] = "facade"
geometry_result = validate_graph_locks(graph, geometry)
assert any(item["code"] == "GEOMETRY_TYPE_CHANGED" for item in geometry_result["findings"])

missing_geometry = deepcopy(graph)
missing_geometry["nodes"] = [node for node in missing_geometry["nodes"] if node["id"] != "roof_01"]
missing_result = validate_graph_locks(graph, missing_geometry)
assert any(item["code"] == "GEOMETRY_NODE_MISSING" for item in missing_result["findings"])

occlusion = deepcopy(graph)
next(edge for edge in occlusion["edges"] if edge["id"] == "rel_parapet_occludes")["type"] = "IN_FRONT_OF"
occlusion_result = validate_graph_locks(graph, occlusion)
assert any(item["code"] == "OCCLUSION_RELATION_CHANGED" for item in occlusion_result["findings"])

reference = deepcopy(graph)
reference["reference_observations"][0]["applied_transfers"] = ["exact geometry"]
reference_result = validate_graph_locks(graph, reference)
assert any(item["code"] == "REFERENCE_ISOLATION_VIOLATION" for item in reference_result["findings"])
assert reference_result["s3_count"] == 1

reference_missing = deepcopy(graph)
reference_missing["reference_observations"] = []
reference_missing_result = validate_graph_locks(graph, reference_missing)
assert any(item["code"] == "REFERENCE_OBSERVATION_MISSING" for item in reference_missing_result["findings"])

assert validate_graph_locks(graph, deepcopy(graph)) == validate_graph_locks(graph, deepcopy(graph))

print("PASS 25/25 VSG-1 Graph Locks tests")
