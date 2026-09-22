import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "visual_scene_graph/diagnostic_benchmark"))

from run_benchmark import run

cases = ROOT / "visual_scene_graph/diagnostic_benchmark/cases.json"
fixture = ROOT / "visual_scene_graph/fixtures/kennys_rooftop_vsg0.json"
report = run(cases, fixture)

assert report["status"] == "PASS"
assert report["gate"]["cases_passed"] == 13
assert report["gate"]["cases_total"] == 13
assert report["gate"]["actual_accuracy"] == 1.0
assert report["gate"]["missing_origins"] == []
assert report["gate"]["healthy_control"] == "PASS"
assert set(report["gate"]["covered_origins"]) == {
    "PERCEPTION", "REFERENCE_REASONING", "GRAPH_PROJECTION", "COMPILER", "GENERATION", "NONE"
}
assert all(result["status"] == "PASS" for result in report["results"])
assert report["results"][-1]["actual"]["code"] == "NO_FAILURE"

print("PASS 9/9 VSG-0.5 diagnostic benchmark tests")
