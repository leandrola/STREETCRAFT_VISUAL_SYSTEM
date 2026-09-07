# Streetcraft Agent Execution Protocol (SAEP)

1. INGEST — identify source domain, user intent, requested output and constraints.
2. ANALYZE — run Visual Intelligence and produce SAR or FC-SAR; build Source Evidence Map.
3. INFER — attempt conservative internal inference before external retrieval; preserve provenance/confidence.
4. REFERENCE-REASON — build RNM. Return NRN when sufficient. Otherwise choose RM1/RM2/RM3, apply eligibility gates, retrieve minimum sufficient set, build RAM/RTC/SLM/ETO and Conflict Ledger.
5. RESOLVE — select Mode, Profile, P0–P5, PR, TB/DB, UB and narrow overrides.
6. PLAN — produce Transformation Plan with explicit preserve/change/remove/infer zones plus property-level reference permissions.
7. GENERATE — use a model adapter. Core SVS remains vendor-agnostic. Adapter receives authorized knowledge, not a generic instruction to imitate references.
8. INSPECT — run Visual Critic, reference-leakage checks and gate-based compliance.
9. REVISE / DELIVER — invoke Self-Correction only when justified. Preserve BKO and stop on convergence.

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
reference_scope_control

The adapter translates Streetcraft semantic contracts into model-specific syntax. Vendor parameters must not leak into Core. When the target model cannot enforce reference locality/scope, compensate with stricter RTC, Source Locks, lower Reference Debt and stronger post-generation leakage inspection.
