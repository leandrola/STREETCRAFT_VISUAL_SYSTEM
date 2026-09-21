# Hito 2 · RR2 / Archive synthetic → real

> Historical pre-validation implementation checklist. All steps below were subsequently completed; the patch was integrated and is not a required local input. Current results: [RR2 real 8/8 PASS](../../validation/RR2_REAL_ARCHIVE_VALIDATION_V1.json), [CGC E2E 8/8 PASS](../../validation/CGC_END_TO_END_REAL_ARCHIVE_V1.json). Current executable: [run_reference_archive.py](../../reference_runtime/run_reference_archive.py).

## Implemented in this patch

- First real classified Evidence Unit catalog: 10 units.
- Eight real RR2 validation scenarios.
- Real-source/candidate contradiction fixture from R2B-191-A.
- Cross-ID content dedupe using a known pixel-identical Streetcraft pair (RDR-F01 / RDR-F07).
- Structured contradiction detection via `claim_key` / `claim_value`.
- Provenance, semantic-text, Fear City, query-budget, cache and locked-unknown coverage.

## Still required for final PASS

1. Apply `RR2_REAL_CATALOG_CODE.patch` to the repository.
2. Run the existing unit suite. Expected count becomes 18 RR2 tests (16 existing + 2 new).
3. Run the eight real cases through `STREETCRAFT_ARCHIVE_V1_FINAL` using `run_reference_archive.py`.
4. Persist the resulting bundles/traces and SHA-256 input provenance.
5. Only after that mark Archive real validation PASS.

## Environment limitation encountered

The connected GitHub app could read `main` but returned HTTP 403 on `update_file`. No repository write was performed. The Archive V1 Final package was also not discoverable in connected conversation/library files, so a live Archive execution would be fabricated if claimed here.
