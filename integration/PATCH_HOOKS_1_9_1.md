# Patch Hooks for SVS 1.9.0

When applying this overlay to the complete 1.9.0 tree, load the patch at these hooks:

1. **After SAR2**: classify all visible text tokens with STF/LCTM.
2. **Before Archive projection**: mark confirmed Fear City with `geographic_identity = NULL_EXTERNAL`.
3. **After Evidence Admission**: run RBP on each transferable feature.
4. **Before final CGC**: run AMCG against source atmosphere/material states.
5. **Before GENERATE**: `patch_pre_generation_gate` must return `PASS`.
6. **Critic**: any exact-token mismatch, external Fear City geography, or semantic text invented from masked regions is S3.

Camera Grammar and profiles are not patched.
