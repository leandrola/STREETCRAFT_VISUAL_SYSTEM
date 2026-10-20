#!/usr/bin/env python3
"""Verify frozen cleanup hashes and the selected baseline in a disposable copy."""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/repository"
FROZEN = DOCS / "CLEANUP_2026_10_UNTOUCHABLE_HASHES.csv"
RESULT = DOCS / "CLEANUP_2026_10_FINAL_VERIFICATION.json"
CHECKS = [
    "command_invocation/test_commands.py", "command_invocation/test_backdrop_presets.py",
    "hardening/test_operational_hardening.py", "reference_runtime/test_archive_aware_runtime.py",
    "reference_runtime/test_reference_reasoning.py", "scene_intelligence/test_scene_intelligence.py",
    "integration/test_streetcraft_orchestrator.py", "validation/test_patch_1_9_1.py",
    "validation/test_single_client_1_10_0.py", "benchmark/check_r2_baseline.py",
    "validation/camera_routing/validate_matrix.py", "validation/camera_routing/validate_l3.py",
]
DOCUMENTED_MISSING_EXCEPTIONS = {
    "benchmark/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
    "benchmark/r2b_1_9_1/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
    "validation/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
    "validation/camera_routing/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
    "validation/cgc_e2e/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
    "validation/rr2_real_archive/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
    "visual_scene_graph/.DS_Store": "Finder metadata removed by Lean-authorized local cleanup; see docs/repository/ERRATA_DS_STORE_2026_10_20.md.",
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    frozen = list(csv.DictReader(FROZEN.open(encoding="utf-8")))
    mismatches, exceptions = [], []
    for row in frozen:
        path = ROOT / row["path"]
        actual = sha(path) if path.is_file() else "MISSING"
        if row["path"] in DOCUMENTED_MISSING_EXCEPTIONS and actual == "MISSING":
            exceptions.append({"path": row["path"], "expected": row["expected_sha256"],
                               "actual": actual, "reason": DOCUMENTED_MISSING_EXCEPTIONS[row["path"]]})
        elif actual != row["expected_sha256"]:
            mismatches.append({"path": row["path"], "expected": row["expected_sha256"], "actual": actual})
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().rstrip("\0").split("\0")
    checks: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="streetcraft-cleanup-final-") as temp_name:
        temp = Path(temp_name); checkout = temp / "repo"; checkout.mkdir(); tmp = temp / "tmp"; tmp.mkdir()
        for rel in paths:
            source, target = ROOT / rel, checkout / rel
            target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target, follow_symlinks=False)
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(tmp)}
        for rel in CHECKS:
            start = time.monotonic()
            run = subprocess.run([sys.executable, str(checkout / rel)], cwd=checkout, env=env,
                                 capture_output=True, text=True, timeout=90)
            checks.append({"name": rel, "status": "PASS" if run.returncode == 0 else "FAIL",
                           "exit_code": run.returncode, "elapsed_seconds": round(time.monotonic()-start, 3),
                           "stdout": run.stdout, "stderr": run.stderr})
            if run.returncode: break
        if all(c["status"] == "PASS" for c in checks):
            start = time.monotonic()
            run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_sc_supervisor.py", "-v"], cwd=checkout, env=env, capture_output=True, text=True, timeout=90)
            checks.append({"name": "SC03 supervisor unit tests", "status": "PASS" if run.returncode == 0 else "FAIL", "exit_code": run.returncode, "elapsed_seconds": round(time.monotonic()-start, 3), "stdout": run.stdout, "stderr": run.stderr})
    report = {"status": "PASS" if not mismatches and len(exceptions) == len(DOCUMENTED_MISSING_EXCEPTIONS) and len(checks) == 13 and all(c["status"] == "PASS" for c in checks) else "FAIL",
              "immutable_paths": len(frozen), "strict_immutable_paths": len(frozen)-len(exceptions),
              "strict_hash_matches": len(frozen)-len(exceptions)-len(mismatches),
              "documented_exceptions": exceptions, "hash_mismatches": mismatches,
              "copied_tracked_files": len(paths), "checks": checks,
              "method": "selected baseline checks ran in a TemporaryDirectory copy; the worktree was not a test target"}
    RESULT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "immutable_paths", "strict_immutable_paths", "strict_hash_matches", "copied_tracked_files")}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
