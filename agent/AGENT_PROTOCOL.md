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

## SVS 1.6.4 Compact Contract Gate
Before generation, resolve a Compact Generation Contract. If preserve/transform/remove/infer/unknown/forbid cannot be made internally consistent, do not generate until the conflict is resolved.

## SVS 1.7 Archive-Aware Reference Gate
After the Compact Generation Contract is drafted, evaluate Reference Need before generation.

Sequence:
1. classify Reference Need;
2. skip Archive when `RN_NONE`;
3. preserve unknown without retrieval when `RN_BLOCKED`;
4. query Archive for `RN_SUPPORT` or `RN_REQUIRED`;
5. admit evidence through EAP 1.0;
6. enrich the CGC with only scoped admitted evidence;
7. generate;
8. inspect for reference bleed with Visual Critic and Micro-Drift Critic.

Archive evidence never changes Mode/Profile/Camera by itself.
