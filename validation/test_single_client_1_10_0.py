#!/usr/bin/env python3
"""Guard the single-client versioning decision for current governing files."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
GOVERNING = [
    "README.md",
    "STREETCRAFT.md",
    "ROADMAP.md",
    "PACKAGE_MANIFEST.json",
    "reference_runtime/REFERENCE_REASONING_2.md",
    "REFERENCE_REASONING_ARCHIVE_INTEGRATION.md",
]
FORBIDDEN = (
    "1.10.0-dev",
    "dev2",
    "experimental opt-in",
    "runtime anterior permanece",
    "no se realizó push",
    "no se hizo push",
)

errors = []
for relative in GOVERNING:
    text = (ROOT / relative).read_text(encoding="utf-8").lower()
    for token in FORBIDDEN:
        if token in text:
            errors.append(f"{relative}: forbidden current-release label {token!r}")

manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
if manifest.get("version") != "1.10.0":
    errors.append("PACKAGE_MANIFEST.json: version must be 1.10.0")
if manifest.get("single_client") is not True:
    errors.append("PACKAGE_MANIFEST.json: single_client must be true")
if manifest.get("parallel_product_runtimes") is not False:
    errors.append("PACKAGE_MANIFEST.json: parallel_product_runtimes must be false")
entry = manifest.get("reference_reasoning", {}).get("entry_point")
if entry != "reference_runtime/reference_reasoning.py":
    errors.append("PACKAGE_MANIFEST.json: primary reference entry point is incorrect")

decision = json.loads((ROOT / "release_decisions/SVS_1_10_0_SINGLE_CLIENT.json").read_text(encoding="utf-8"))
gate = decision.get("promotion_gate", {})
if gate != {"r2b_cases": 6, "s3_violations": 0, "minimum_global_score": 90}:
    errors.append("single-client decision: promotion gate changed")

if errors:
    print("FAIL single-client governance")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print("PASS single-client governance 1.10.0")
