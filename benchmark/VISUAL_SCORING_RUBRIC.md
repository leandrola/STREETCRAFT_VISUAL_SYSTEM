# Visual Benchmark Scoring Rubric

Each generated candidate is scored out of 100.

| Dimension | Weight |
|---|---:|
| Source / authored-world identity | 25 |
| Geometry & protected relationships | 15 |
| Camera compliance | 15 |
| Semantic text fidelity | 10 |
| Material intensity discipline | 10 |
| Occlusion discipline | 10 |
| Reference isolation / no evidence bleed | 10 |
| Atmosphere / profile compliance | 5 |

## Critical invariants

The following are binary release gates:
- no source identity replacement
- no semantic text invention
- no S3 geometry drift
- no Fear City geographic import
- no locked occlusion invention
- no camera override of CG-S/CG-FC without authority
- no Canon-by-similarity
- no reference-specific geometry copied outside scope

A candidate with any critical failure receives `FAIL` regardless of numeric score.

## Severity

- S0: no issue
- S1: cosmetic
- S2: meaningful drift
- S3: identity/authority violation

## Benchmark thresholds

- 90–100: PASS
- 85–89: REVIEW
- <85: FAIL

Multiple S2 findings may force REVIEW/FAIL even above 90.
