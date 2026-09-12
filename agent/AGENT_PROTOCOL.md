# Streetcraft Agent Execution Protocol (SAEP)

1. INGEST — identify source domain, user intent, requested output and constraints.
2. ANALYZE — run Visual Intelligence and produce SAR or FC-SAR.
3. RESOLVE — select Mode, Profile, P0–P5, PR, TB/DB, UB and overrides.
4. PLAN — produce a Transformation Plan with explicit preserve/change/remove/infer zones.
5. GENERATE — use a model adapter. Core SVS must remain vendor-agnostic.
6. INSPECT — run Visual Critic and gate-based compliance.
7. REVISE / DELIVER — invoke Self-Correction only when justified. Preserve BKO and stop on convergence.

## Adapter capability negotiation
image_input
image_edit
multi_reference
mask_edit
aspect_extension
seed_control
iterative_edit
locality_control
geometry_control
text_rendering

The adapter translates Streetcraft semantic contracts into model-specific syntax. Vendor parameters must not leak into the Core.
