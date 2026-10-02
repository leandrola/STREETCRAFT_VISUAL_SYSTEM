"""Read-only stdlib evidence checks. Does not import or execute Streetcraft models."""
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASELINE = "2a489a6e6868bfe8473ceb6b4f4228e0d2cc8b88"
SPEC_HASH = "89123ca72cc8f3477d14cb57715785b3fe58326fd09dd15e261760a86d63438b"


def main():
    checks = []
    hash_rows = []

    def check(name, ok, detail):
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    def read(path):
        return json.loads((ROOT / path).read_text())

    def verify(path, expected, source):
        p = Path(path)
        if not p.is_absolute():
            p = ROOT / p
        actual = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        hash_rows.append({"source": source, "path": path, "expected": expected,
                          "actual": actual, "status": "PASS" if actual == expected else "FAIL"})

    def declared(x, source):
        if isinstance(x, dict):
            if "sha256" in x and ("path" in x or "local_path" in x):
                verify(x.get("local_path", x.get("path")), x["sha256"], source)
            for k, v in x.items():
                if "/" in k and isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v):
                    verify(k, v, source)
                declared(v, source)
        elif isinstance(x, list):
            for v in x:
                declared(v, source)

    sources = ["validation/vsg_2b/N4S_RESULT.json", "validation/vsg_2b/n4s/INPUT_MANIFEST.json",
               "validation/vsg_2b/N5PV_RESULT.json", "validation/vsg_2b/n5pv/INPUT_MANIFEST.json"]
    for source in sources:
        doc = read(source)
        declared(doc, source)
        inventory = doc.get("existing_files", {})
        for path, meta in inventory.items():
            verify(path, meta["sha256"], source + "#/existing_files")
        if inventory:
            check(source + " inventory count", len(inventory) == doc["existing_file_count"], len(inventory))
    spec = "validation/vsg_2b/orchestration_pilot/VSG_2B_N5P_N5V_PREEXECUTION_SPEC.md"
    verify(spec, SPEC_HASH, "bootstrap")
    check("declared hashes", all(r["status"] == "PASS" for r in hash_rows),
          {"checked": len(hash_rows), "failed": [r for r in hash_rows if r["status"] != "PASS"]})

    baseline_paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASELINE], cwd=ROOT, text=True).splitlines()
    changed = subprocess.check_output(["git", "diff", "--name-only", BASELINE, "--", *baseline_paths], cwd=ROOT, text=True).splitlines()
    check("historical tracked contents preserved", not changed, {"baseline_files": len(baseline_paths), "changed": changed})

    result = read("validation/vsg_2b/N5PV_RESULT.json")
    missing = [p for p in result["files_new"] if not (ROOT / p).is_file()]
    check("declared deliverables exist now", not missing, missing)
    names = ["N5P_IMPLEMENTATION_AND_RESOURCES_PLAN.md", "N5V_SEMANTIC_VALIDATION_PREREGISTRATION.md", "N5PV_WORK_MODE_NEXT_STEPS.md"]
    for name in names:
        path = ROOT / "visual_scene_graph/pilot" / name
        check(name + " provenance", "RECONSTRUCTION DRAFT" in path.read_text(), "Labeled draft; historical original unavailable")
    audit = read("validation/vsg_2b/orchestration_pilot/AUDIT.json")
    for path, meta in audit["reconstructed_documents"].items():
        verify(path, meta["sha256"], "reconciliation audit")
    historical_missing = audit["readiness_correction"]["baseline_absent_declared_deliverables"]
    check("correction baseline availability", all(
        subprocess.run(["git", "cat-file", "-e", BASELINE + ":" + path], cwd=ROOT,
                       capture_output=True).returncode != 0 for path in historical_missing)
        and not audit["historical_originals_available"]
        and not audit["readiness_correction"]["historical_records_rewritten"], historical_missing)

    budget = read("validation/vsg_2b/n5pv/EXECUTION_BUDGET_PROPOSAL.json")
    scenario = budget["selected_diagnostic_scenario"]
    receipts = scenario["receipts"]
    ids = [r["id"] for r in receipts]
    check("unique receipt IDs", len(set(ids)) == len(ids), ids)
    visited = set()
    dag_ok = True
    for receipt in receipts:
        dag_ok &= set(receipt["depends_on"]).issubset(visited)
        visited.add(receipt["id"])
    check("receipt DAG topological order", dag_ok, "All dependencies precede use")
    for field, cap, total in [("module_invocations", "module_invocation_caps", "total_learned_invocations"),
                              ("processed_batch_units", "processed_batch_unit_caps", "total_processed_batch_units")]:
        computed = Counter()
        for receipt in receipts:
            for module, count in receipt[field].items():
                computed[module] += count * receipt["maximum_executions"]
        check(field + " arithmetic", dict(computed) == scenario[cap] and sum(computed.values()) == scenario[total], dict(computed))
    check("trajectory/decode/attempt counts", sum(r.get("attempt_reservations_proposed", 0) for r in receipts) == 7
          and sum(r.get("maximum_outputs", 0) for r in receipts) == 5
          and sum(r["stage"] == "trajectory" for r in receipts) == 7, "7 trajectories/attempt charges; 5 outputs proposed")
    training = budget["training_scenario"]
    train_calls = training["CLIP_preparation"]["invocations"] + training["VAE_preparation"]["invocations"] + sum(training["training_validation_calls"].values())
    check("training arithmetic", train_calls == training["module_execution_cap"] == 93121
          and train_calls + scenario["total_learned_invocations"] == budget["all_tranches_learned_invocations_cap"] == 93546
          and training["microsteps_training"] // training["gradient_accumulation"] == training["optimizer_steps_cap"], train_calls)
    matrix = read("validation/vsg_2b/n5pv/VALIDATION_MATRIX.json")
    check("eight matrix tests and receipt references", len(matrix["tests"]) == 8
          and {t["id"] for t in matrix["tests"]} == {t["id"] for t in result["model_tests"]}
          and all(set(t["receipts"]).issubset(visited) for t in matrix["tests"]), "Eight inherited tests mapped to existing receipt IDs")
    frozen = matrix["frozen_rubric"]
    manifest = read(frozen["path"])
    verify(frozen["path"], frozen["sha256"], "matrix rubric")
    # The frozen manifest supplies the actual rubric; inspect its shape without model imports.
    def find_rows(value):
        if isinstance(value, list) and value and all(isinstance(v, dict) and "constraint_id" in v for v in value):
            return value
        if isinstance(value, dict):
            for v in value.values():
                found = find_rows(v)
                if found is not None:
                    return found
        return None
    check("frozen rubric exact rows", frozen["rows"] == find_rows(manifest), {"rows": len(frozen["rows"])})
    policy = read("visual_scene_graph/pilot/campaign_policy.json")
    conflict = budget["campaign_policy_conflict"]
    check("campaign quota conflict preserved", policy["maximum_generation_attempts"] == conflict["current_max_attempts"] == 8
          and policy["minimum_pairs"] == 4 and conflict["diagnostic_and_official_unique_attempts"] == 7 + 6 == 13,
          "13 exceeds 8; D-only diagnostic proposal is not campaign closure")
    check("authorization and NOT_RUN invariants", not matrix["execution_authorized"] and not matrix["semantic_criteria_frozen"]
          and not budget["all_execution_authorized"] and not budget["execution_budget_complete"]
          and all(v == 0 for v in budget["approved_caps"].values())
          and all(t["status"] == "NOT_RUN" for t in matrix["tests"] + result["model_tests"])
          and all(r["status"] == "NOT_RUN" for r in receipts)
          and not result["settings_applied"] and not result["implementation_authorized"] and not result["execution_authorized"], "No execution readiness inferred")
    checkpoint = read("development/coordination/CHECKPOINT.json")
    check("checkpoint gate", checkpoint["milestones"]["M1"]["status"] == "CLOSED"
          and checkpoint["milestones"]["M3"]["status"] == "BLOCKED"
          and all(v == "PENDING" for v in checkpoint["decisions"].values())
          and checkpoint["generated_images"] == 0 and checkpoint["model_tests"] == "NOT_RUN", "M1 closed; D1-D4 pending; M3 blocked")
    broken = []
    for p in [ROOT / "development/coordination/README.md"] + [ROOT / "visual_scene_graph/pilot" / n for n in names]:
        for target in re.findall(r"\]\(([^)]+)\)", p.read_text()):
            if not target.startswith(("https:", "http:")) and not (p.parent / target.split("#")[0]).exists():
                broken.append({"file": str(p.relative_to(ROOT)), "target": target})
    check("document links", not broken, broken)
    check("final declared hashes", all(r["status"] == "PASS" for r in hash_rows),
          {"checked": len(hash_rows), "failed": [r for r in hash_rows if r["status"] != "PASS"]})
    output = {"status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
              "scope": "STATIC_DOCUMENTARY_ONLY", "checks": checks, "hash_evidence": hash_rows,
              "model_tests": "NOT_RUN", "generated_images": 0}
    print(json.dumps(output, indent=2))
    return 0 if output["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
