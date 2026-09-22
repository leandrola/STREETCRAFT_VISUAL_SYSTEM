import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scene_intelligence"))
sys.path.insert(0, str(ROOT / "visual_scene_graph"))

from scene_intelligence import build_scene_analysis_record
from vsg_observer import build_visual_scene_graph


fixture = json.loads((ROOT / "visual_scene_graph/fixtures/kennys_rooftop_vsg0.json").read_text())
sar2 = build_scene_analysis_record(**fixture)
graph = build_visual_scene_graph(
    sar2,
    reference_id="R2B-KENNYS",
    reference_sha256="a" * 64,
)

assert graph["mode"] == "OBSERVER"
assert graph["governs_generation"] is False
assert graph["provenance"]["node_count"] == 9
assert graph["provenance"]["edge_count"] == 7
assert graph["provenance"]["reference_sha256"] == "a" * 64
assert graph["diagnostics"] == {
    "unclassified_nodes": [], "unsupported_relations": [], "dangling_relations": []
}
assert graph["reference_observations"] == []
assert graph["provenance"]["rr_status"] == "NOT_SUPPLIED"

nodes = {node["id"]: node for node in graph["nodes"]}
assert nodes["sign_01"]["type"] == "sign"
assert nodes["sign_01"]["properties"]["text"] == "KENNY'S"
assert nodes["sign_01"]["locks"]["semantic"] is True
assert nodes["building_01"]["locks"]["geometry"] is True
assert nodes["hvac_01"]["confidence"] == 0.65

edges = {edge["id"]: edge for edge in graph["edges"]}
assert edges["rel_hvac_behind"]["type"] == "BEHIND"
assert edges["rel_hvac_behind"]["from"] == "hvac_01"
assert edges["rel_hvac_behind"]["to"] == "parapet_01"

circuits = {circuit["name"]: circuit for circuit in graph["functional_subgraphs"]}
assert "sign_01" in circuits["semantic_text"]["nodes"]
assert set(circuits["rooftop"]["nodes"]) == {
    "roof_01", "parapet_01", "hvac_01", "chimney_01", "skylight_01", "access_bulkhead_01"
}
assert "rel_hvac_behind" in circuits["rooftop"]["edges"]

again = build_visual_scene_graph(sar2, reference_id="R2B-KENNYS", reference_sha256="a" * 64)
assert graph == again

rr_graph = build_visual_scene_graph(
    sar2,
    reference_reasoning={
        "status": "READY",
        "trace": [{"need_id": "N-ROOF", "evidence_bundle_ids": ["EB-1"]}],
        "generation_projection": [{"need_id": "N-ROOF", "evidence_unit_id": "EU-1"}],
    },
    reference_needs=[{"need_id": "N-ROOF", "target_entity_id": "roof_01"}],
)
observation = rr_graph["reference_observations"][0]
assert rr_graph["provenance"]["rr_status"] == "READY"
assert observation["target_node_id"] == "roof_01"
assert observation["evidence_unit_ids"] == ["EU-1"]
assert observation["evidence_bundle_ids"] == ["EB-1"]

print("PASS 24/24 VSG-0 Observer tests")
