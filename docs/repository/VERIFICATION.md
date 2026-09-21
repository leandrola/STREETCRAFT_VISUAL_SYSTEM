# Repository verification

Baseline: **SVS 1.10.0 STABLE**. Housekeeping does not change the release or its runtime.

## Environment and isolation

Use Python 3.10+ (the runtime uses modern union type annotations), Pillow and jsonschema. This cleanup was checked with Python 3.14.5; exact installed dependency versions and captured results are in [CLEANUP_VERIFICATION.json](CLEANUP_VERIFICATION.json).

Several existing runners write directly into `validation/`. Run them in a disposable copy of repository content, outside the checkout, with a separate virtual environment. Exclude `.git`, `.venv`, `.browser-profile`, caches and local output directories. Include current modified documentation and fixtures in that copy. This is test isolation, not another Streetcraft client or product runtime.

For example, from that temporary copy, using the absolute path to its test interpreter:

```sh
PYTHONDONTWRITEBYTECODE=1 /path/to/test-env/bin/python benchmark/run_regression_suite.py
PYTHONDONTWRITEBYTECODE=1 /path/to/test-env/bin/python validation/camera_routing/validate_matrix.py
PYTHONDONTWRITEBYTECODE=1 /path/to/test-env/bin/python validation/camera_routing/validate_l3.py
```

The unified runner executes CIL, operational hardening, Archive-aware unit tests, RR2, scene intelligence, orchestrator, patch and single-client governance tests. It also checks JSON, Python syntax, embedded assets, golden fixtures and the R2 baseline. Its RR2-real and CGC-real summary fields read **stored reports**; they do not themselves rerun the external Archive cases.

Validate all 16 schema definitions (`schemas/` plus `reference/manifest.schema.json`) with `jsonschema.validators.validator_for(schema).check_schema(schema)`. Validate the reference manifest and the stored `sar2`, `cgc_draft` and `cgc_final` objects against their respective schemas. These checks are recorded separately from runtime tests.

## External Archive re-execution

Supply a real `STREETCRAFT_ARCHIVE_V1_FINAL` checkout/package. Before execution, compare its 20 runtime module SHA-256 values with [ARCHIVE_RUNTIME_IDENTITY.json](../../validation/rr2_real_archive/ARCHIVE_RUNTIME_IDENTITY.json). Do not substitute mock code or infer identity from a directory name.

In the temporary test copy:

```sh
python reference_runtime/check_archive_v1_integration.py /path/to/STREETCRAFT_ARCHIVE_V1_FINAL
python reference_runtime/check_reference_archive_integration.py /path/to/STREETCRAFT_ARCHIVE_V1_FINAL
python validation/run_cgc_e2e_real_archive.py --archive-root /path/to/STREETCRAFT_ARCHIVE_V1_FINAL
```

For each of the eight RR2 request files, invoke the existing runner:

```sh
python reference_runtime/run_reference_archive.py \
  --archive-root /path/to/STREETCRAFT_ARCHIVE_V1_FINAL \
  --evidence reference_runtime/real_catalog/REAL_EVIDENCE_CATALOG_V1.json \
  --request validation/rr2_real_archive/requests/RR2-REAL-01.json \
  --output /path/to/disposable-results/RR2-REAL-01.json
```

Repeat for `RR2-REAL-02` through `RR2-REAL-08`. Compare status, query budget, projections, duplicate rejection, contradictions, locks and bundle/provenance fields against the expectations in [REAL_CASES_V1.json](../../reference_runtime/real_catalog/REAL_CASES_V1.json). Exit 2 is expected for deliberately blocked RR2 cases; it is not sufficient by itself to classify the test as a failure. E2E requests likewise include expected blocked/review outcomes.

The cleanup environment did not contain the external Archive runtime. Stored results and provenance were verified, but real Archive re-execution remains unverified here. This local dependency gap does not reopen the completed 21/9 release roadmap.

## Evidence and package integrity

The original [release checksum manifest](../../SVS_1_10_0_SHA256SUMS.json) and [release integrity report](../../validation/FINAL_PACKAGE_INTEGRITY_2026_09_21.json) remain unchanged. They describe the promotion snapshot. Documentation edits naturally differ from their original hashes; the exact old/new hashes are recorded in [CLEANUP_VERIFICATION.json](CLEANUP_VERIFICATION.json).

[CLEANUP_SHA256SUMS.json](CLEANUP_SHA256SUMS.json) records the current repository content after housekeeping. Its scope excludes Git internals, virtual environments, browser state and itself. Verify every listed path against SHA-256; compare file membership as well as hashes. It supplements the original manifest rather than rewriting release history.

The R2b final report lists 14 evidence files with hashes and sizes. Check all 14, the six final verdicts and score arithmetic. This verifies existing evidence; it does not regenerate images or repeat human visual scoring.

For RR2/CGC, verify each stored result's request/evidence hashes and recorded Archive module map, plus traces and bundle IDs. Without external runtime bytes this proves consistency of preserved provenance, not a new runtime identity check.
