#!/usr/bin/env python3
"""Build current SVS 1.10.0 QA summaries and repository checksums."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(relative, cwd=None):
    path = ROOT / relative
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(cwd or path.parent),
        capture_output=True,
        text=True,
    )
    return {
        "test": relative,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


reference = run("reference_runtime/test_reference_reasoning.py", ROOT / "reference_runtime")
governance = run("validation/test_single_client_1_10_0.py", ROOT)
regression = run("benchmark/run_regression_suite.py", ROOT)

reference_report = {
    "version": "1.10.0",
    "capability": "Reference Reasoning 2.0",
    "status": "AUTOMATED_CHECKS_PASS" if reference["status"] == "PASS" else "FAIL",
    "primary_entry_point": "reference_runtime/reference_reasoning.py",
    "unit_tests": 16,
    "integrated_automated_tests": 106,
    "archive_software_checks": 12,
    "archive_evidence_scope": "SYNTHETIC_TEST_EVIDENCE",
    "real_catalog_validation": "PENDING_CLASSIFIED_CATALOG",
    "visual_validation": "R2B_REQUIRED_PENDING",
    "result": reference,
}
(ROOT / "validation/SVS_1_10_0_REFERENCE_QA.json").write_text(
    json.dumps(reference_report, indent=2) + "\n", encoding="utf-8"
)

qa_report = {
    "version": "1.10.0",
    "client_model": "SINGLE_STREETCRAFT_CLIENT",
    "status": "PASS" if all(x["status"] == "PASS" for x in (reference, governance, regression)) else "FAIL",
    "base_release": "SVS 1.9.1 / CIL 1.1",
    "reference_reasoning": "INTEGRATED_MAINLINE_IN_PROGRESS",
    "stable_promotion": False,
    "promotion_gate": {
        "r2b_cases": 6,
        "s3_violations": 0,
        "minimum_global_score": 90,
        "status": "PENDING",
    },
    "pending": [
        "classified real Archive catalog",
        "full CGC orchestration projection",
        "formal visual R2b evaluation",
    ],
    "results": [reference, governance, regression],
}
(ROOT / "validation/SVS_1_10_0_QA.json").write_text(
    json.dumps(qa_report, indent=2) + "\n", encoding="utf-8"
)

checksum_path = ROOT / "SVS_1_10_0_SHA256SUMS.json"
excluded_parts = {".git", "__pycache__", ".pytest_cache"}
files = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path == checksum_path:
        continue
    if any(part in excluded_parts for part in path.parts):
        continue
    files.append(path)
checksums = {
    str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(files)
}
checksum_path.write_text(json.dumps(checksums, indent=2) + "\n", encoding="utf-8")

print(json.dumps({
    "status": qa_report["status"],
    "reference_tests": reference["status"],
    "single_client_governance": governance["status"],
    "integrated_regression": regression["status"],
    "checksums": len(checksums),
}, indent=2))
raise SystemExit(0 if qa_report["status"] == "PASS" else 1)
