# SVS 1.9.0 · R2b Critical Regression Report

**Decision: FAIL · DO NOT PROMOTE TO STABLE**

The critical run uses real individual source/candidate pairs available from the Streetcraft test history. Synthetic benchmark dashboards generated during the current run are excluded from evidence.

- Cases evaluated: 3
- Numeric average: 83.0/100
- S3 findings: 4
- Stable promotion: NO

The numeric average is informational only. R2b has a hard gate: any S3 = FAIL.

## R2B-FC-001 · Fear City identity / reference isolation
Score: **72/100** · Status: **FAIL**

- S3 `REGIONAL_LEAK`: Candidate introduces explicit New York identity (newspaper headline) not authorized by Fear City source.
- S3 `AUTHORED_WORLD_DRIFT`: Vehicle/prop and streetscape interpretation extends beyond authored-world evidence.
- S2 `MATERIAL_ATMOSPHERE_INFLATION`: Wet reflective pavement and cinematic realism intensify beyond source evidence.

Comparison: `R2B-FC-001_comparison.jpg`

## R2B-TXT-001 · Semantic Text Lock / CBGB
Score: **87/100** · Status: **FAIL**

- S3 `TEXT_MUTATION`: Visible source number 315 is changed to 313 at the Palace Hotel entrance.
- S2 `DETAIL_INVENTION`: Additional poster/graffiti micro-content is synthesized beyond legible source evidence.

Comparison: `R2B-TXT-001_comparison.jpg`

## R2B-OCC-TXT-001 · Occlusion + text discipline / laundry storefront
Score: **90/100** · Status: **FAIL**

- S3 `TEXT_INVENTION`: Small low-confidence storefront/product text is rendered as specific new readable semantics rather than preserving ambiguity.
- S1 `SOURCE_CLEANUP`: Material/detail cleanup is stronger than strictly necessary but does not dominate identity.

Comparison: `R2B-OCC-TXT-001_comparison.jpg`

## Patch targets for 1.9.1

1. Add a hard **Semantic Token Freeze** for P0/P1 text tokens and visible numerals.
2. Add **Fear City Geographic Null Lock**: external regional labels/names are forbidden unless source-authored.
3. Add **Reference Bleed Preflight** before generation, not only post-generation critique.
4. Add **Low-confidence Text Mask**: illegible microtext must remain graphic/ambiguous, never semantic.
5. Re-run the same R2b critical cases after patching; promotion requires S3=0 and global score >=90.
