"""Causal fidelity, adversarial validation, incompleteness and non-interference."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from visual_scene_graph.causal_cases import corpus, complete_artifacts, run_causal_cases
from visual_scene_graph.causal_trace import (
    INPUTS, build_causal_trace, canonical_sha256, render_causal_trace,
    resolve_artifact_ref, trace_sha256, validate_causal_trace,
)


def refresh(artifacts):
    return complete_artifacts({k: v for k, v in artifacts.items() if k not in {"diagnosis", "graph_lock_validation"}})


class CausalTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = corpus()
        cls.report = run_causal_cases()

    def assertRejected(self, trace, artifacts, error=None):
        trace["trace_sha256"] = trace_sha256(trace)
        validation = validate_causal_trace(trace, artifacts)
        self.assertEqual(validation["status"], "FAIL")
        if error:
            self.assertIn(error, validation["errors"])

    def test_nineteen_controlled_roots_and_real_paths(self):
        self.assertEqual(self.report["passed"], 19)
        self.assertEqual(self.report["causal_accuracy"], 1.0)
        for row in self.report["results"]:
            with self.subTest(case=row["case_id"]):
                self.assertEqual(row["status"], "PASS")
                trace = row["trace"]
                self.assertFalse(trace["governs_generation"])
                root = trace["root_cause"]
                if root:
                    events = {e["event_id"]: e for e in trace["events"]}
                    pairs = {(e["from_event"], e["to_event"]) for e in trace["causal_edges"]}
                    path = root["causal_path"]
                    self.assertEqual(events[path[0]]["stage"], "SOURCE_EVIDENCE")
                    self.assertEqual(path[-2], root["event_id"])
                    self.assertEqual(path[-1], root["diagnostic_event"])
                    self.assertTrue(all((a, b) in pairs for a, b in zip(path, path[1:])))
                    resolve_artifact_ref(root["artifact_ref"], row["artifacts"])

    def test_healthy_control(self):
        row = self.report["results"][12]
        self.assertEqual(row["trace"]["status"], "HEALTHY")
        self.assertIsNone(row["trace"]["root_cause"])
        self.assertEqual(row["trace"]["symptoms"], [])
        self.assertEqual(row["trace"]["independent_findings"], [])

    def test_exact_four_lock_ids(self):
        for row in self.report["results"][13:17]:
            self.assertIn(row["expected"]["lock_id"], row["trace"]["root_cause"]["lock_ids"])
            self.assertTrue(any(row["expected"]["lock_id"] in e["lock_ids"] for e in row["trace"]["events"]))

    def test_earlier_omission_explains_downstream_absence(self):
        row = self.report["results"][0]
        self.assertEqual(row["trace"]["root_cause"]["stage"], "SAR2")
        self.assertTrue(any(s["stage"] == "OBSERVED_OUTPUT" and s["artifact_id"] == "hvac_01" for s in row["trace"]["symptoms"]))

    def test_every_missing_snapshot_is_incomplete(self):
        for key in INPUTS:
            with self.subTest(snapshot=key):
                artifacts = deepcopy(self.cases[0][1]); artifacts[key] = None
                trace = build_causal_trace(**artifacts)
                self.assertEqual(trace["status"], "INCOMPLETE")
                self.assertIsNone(trace["root_cause"])
                self.assertTrue(any(i["artifact"] == key for i in trace["unresolved_inputs"]))
                self.assertNotIn(key, trace["provenance"])
                self.assertEqual(validate_causal_trace(trace, artifacts)["status"], "PASS")

    def test_missing_lock_snapshot_is_not_an_empty_ledger(self):
        artifacts = deepcopy(self.cases[12][1]); del artifacts["vsg"]["graph_locks"]
        self.assertEqual(build_causal_trace(**artifacts)["status"], "INCOMPLETE")

    def test_stale_diagnosis_and_lock_findings_are_not_trusted(self):
        for name in ("diagnosis", "graph_lock_validation"):
            artifacts = deepcopy(self.cases[0][1]); artifacts[name] = deepcopy(self.cases[12][1][name])
            trace = build_causal_trace(**artifacts)
            self.assertEqual(trace["status"], "INCOMPLETE")
            self.assertTrue(any(i["artifact"] == name for i in trace["unresolved_inputs"]))

    def test_duplicate_snapshot_ids_are_explicitly_incomplete(self):
        artifacts = deepcopy(self.cases[12][1]); artifacts["sar2"]["entities"].append(deepcopy(artifacts["sar2"]["entities"][0]))
        self.assertEqual(build_causal_trace(**artifacts)["status"], "INCOMPLETE")

    def test_duplicate_event_ids(self):
        a = self.cases[0][1]; t = build_causal_trace(**a); t["events"].append(deepcopy(t["events"][0]))
        self.assertRejected(t, a, "DUPLICATE_EVENT_ID")

    def test_unresolved_artifact_and_event_references(self):
        a = self.cases[0][1]
        for kind in ("artifact", "event", "root"):
            t = build_causal_trace(**a)
            if kind == "artifact": t["events"][0]["artifact_ref"] = "sar2#/entities/9999"
            elif kind == "event": t["causal_edges"][0]["to_event"] = "EV-DOES-NOT-EXIST"
            else: t["root_cause"]["event_id"] = "EV-DOES-NOT-EXIST"
            self.assertRejected(t, a)
            self.assertGreater(validate_causal_trace(t, a)["unresolved_references"], 0)

    def test_cycle_and_reverse_order(self):
        a = self.cases[0][1]; t = build_causal_trace(**a); e = t["causal_edges"][0]
        t["causal_edges"].append({"from_event": e["to_event"], "to_event": e["from_event"], "relation": "CAUSED"})
        self.assertRejected(t, a, "CAUSAL_CYCLE")
        self.assertIn("REVERSED_CAUSAL_ORDER", validate_causal_trace(t, a)["errors"])

    def test_later_symptom_cannot_be_promoted_to_root(self):
        a = self.cases[0][1]; t = build_causal_trace(**a)
        t["root_cause"] = deepcopy(next(s for s in t["symptoms"] if s["stage"] == "OBSERVED_OUTPUT"))
        self.assertRejected(t, a, "TRACE_REPLAY_MISMATCH")

    def test_root_required_and_healthy_root_forbidden(self):
        a = self.cases[0][1]; t = build_causal_trace(**a); t["root_cause"] = None
        self.assertRejected(t, a, "PRIMARY_ROOT_REQUIRED")
        a = self.cases[12][1]; t = build_causal_trace(**a); t["root_cause"] = deepcopy(self.report["results"][0]["trace"]["root_cause"])
        self.assertRejected(t, a, "UNSUPPORTED_ROOT_CAUSE")

    def test_lock_identity_cannot_be_replaced_even_with_new_hash(self):
        a = self.cases[13][1]; t = build_causal_trace(**a)
        t["root_cause"]["lock_ids"] = ["GL-FABRICATED"]
        self.assertRejected(t, a, "TRACE_REPLAY_MISMATCH")

    def test_tampered_hash_and_provenance(self):
        a = self.cases[0][1]; t = build_causal_trace(**a); t["trace_sha256"] = "0" * 64
        self.assertIn("HASH_MISMATCH", validate_causal_trace(t, a)["errors"])
        t = build_causal_trace(**a); t["provenance"]["sar2"]["sha256"] = "0" * 64
        self.assertRejected(t, a, "TRACE_REPLAY_MISMATCH")

    def test_determinism_key_order_and_no_input_mutation(self):
        for _, a in self.cases:
            before = deepcopy(a); t = build_causal_trace(**a)
            reversed_keys = json.loads(json.dumps(a, sort_keys=True))
            self.assertEqual(t, build_causal_trace(**reversed_keys))
            self.assertEqual(a, before)
            self.assertEqual(t["trace_sha256"], trace_sha256(t))

    def test_independent_fault_is_not_a_symptom_of_unrelated_root(self):
        a = deepcopy(self.cases[0][1])
        next(n for n in a["observed_output_graph"]["nodes"] if n["id"] == "sign_01")["properties"]["text"] = "OTHER"
        a = refresh(a); t = build_causal_trace(**a)
        self.assertEqual(t["root_cause"]["stage"], "SAR2")
        self.assertTrue(any(f["artifact_id"] == "sign_01" for f in t["independent_findings"]))
        self.assertFalse(any(f["artifact_id"] == "sign_01" for f in t["symptoms"]))

    def test_trace_call_does_not_change_stable_or_observer_orchestration(self):
        sys.path.insert(0, str(ROOT / "integration"))
        from streetcraft_orchestrator import orchestrate
        scene = json.loads((ROOT / "visual_scene_graph/fixtures/kennys_rooftop_vsg0.json").read_text())
        for observer in (False, True):
            request = {"command_text": "/sc-2a", "scene": scene}
            if observer: request["vsg"] = {"mode": "OBSERVER"}
            before = orchestrate(deepcopy(request), archive_retriever=None)
            a = self.cases[0][1]; build_causal_trace(**a)
            after = orchestrate(deepcopy(request), archive_retriever=None)
            self.assertEqual(canonical_sha256(before), canonical_sha256(after))
            self.assertNotIn("causal_trace", after)

    def test_readable_summary_and_schema(self):
        import jsonschema
        schema = json.loads((ROOT / "schemas/vsg-causal-trace.schema.json").read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        for row in self.report["results"]:
            jsonschema.validate(row["trace"], schema)
        text = render_causal_trace(self.report["results"][0]["trace"])
        self.assertIn("SAR2 / PERCEPTION_NODE_MISSING / hvac_01", text)
        a = deepcopy(self.cases[0][1]); a["sar2"] = None
        incomplete = build_causal_trace(**a)
        jsonschema.validate(incomplete, schema)
        self.assertIn("sar2", render_causal_trace(incomplete))


if __name__ == "__main__":
    unittest.main()
