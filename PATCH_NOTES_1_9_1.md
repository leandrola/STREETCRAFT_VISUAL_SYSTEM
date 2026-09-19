# Streetcraft SVS 1.9.1 Patch

**Base:** SVS 1.9.0 Candidate Release  
**Patch focus:** R2b critical regression hardening  
**Status:** PATCH_IMPLEMENTED / R2B_RETEST_REQUIRED

This patch responds directly to the three critical R2b failures recorded for SVS 1.9.0:

- Fear City regional/reference bleed
- exact text mutation (`315` → `313`)
- low-confidence text becoming invented readable semantics

## Added gates

1. Semantic Token Freeze (STF)
2. Low-Confidence Text Mask (LCTM)
3. Fear City Geographic Null Lock (FC-GNL)
4. Reference Bleed Preflight (RBP)
5. Atmosphere/Material Carryover Guard (AMCG)

The patch does not alter Camera Grammar, Visual Profiles, Canon authority, CIL syntax, or Archive ownership boundaries.
