# RR2 Real Catalog V1

This package replaces synthetic-only Evidence Unit testing with a first classified catalog made from actual Streetcraft project evidence.

Sources include:
- user-supplied R2b source/candidate evidence from 2026-09-21;
- versioned R2b source fixtures already stored in the repository;
- confirmed Fear City authored-world evidence;
- versioned project reference/golden assets.

The catalog is metadata-only. Archive retrieval reasons over classified Evidence Units; source images remain at the recorded repository path or provenance reference.

`REAL_CASES_V1.json` contains real scenarios covering:
- required/support needs;
- query budget;
- cache reuse;
- provenance floors;
- cross-ID duplicate content;
- structured contradictions;
- strict semantic text lock;
- Fear City geographic isolation;
- locked unknowns.

## Validation and runtime dependency

Real validation is complete: [8/8 RR2 cases](../../validation/RR2_REAL_ARCHIVE_VALIDATION_V1.json) and [8/8 CGC E2E cases](../../validation/CGC_END_TO_END_REAL_ARCHIVE_V1.json) passed for SVS 1.10.0 STABLE. Requests, results, bundles and traces remain under `validation/rr2_real_archive/` and `validation/cgc_e2e/` at the repository root.

Re-execution requires an external `STREETCRAFT_ARCHIVE_V1_FINAL` runtime matching the [recorded module identity](../../validation/rr2_real_archive/ARCHIVE_RUNTIME_IDENTITY.json). The catalog is not a replacement for that software. See [verification instructions](../../docs/repository/VERIFICATION.md).
