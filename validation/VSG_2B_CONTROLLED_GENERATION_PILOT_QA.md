# VSG-2B controlled generation pilot · 2026-09-29

**General status: BLOCKED / PENDING_VISUAL.** Technical dry-run results are separate by fixture:

- **R2B-191-D: CORPUS_RECOVERY_DRY_RUN_PASS**; delta `6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`.
- **R2B-191-E: CORPUS_RECOVERY_DRY_RUN_PASS**; delta `a282bbee73b6613ce2d5ad0737065f3e2332ebce020e664161f38cc43fd17458`.
- **KENNYS-ROOFTOP: CORPUS_RECOVERY_DRY_RUN_PASS**; delta `d04d58135715c95be089344674a99f51b78d8bb4a6ebd08da2194e2b97cc0e17`.

- Deterministic controls: **74/74 PASS** (32 original + 16 E + 26 Kenny controls).
- Current VSG-2A replay: **25/25 PASS**, 42 files verified; historical suite unchanged.
- Unified regression: **PASS** (23 checks).
- Dependencies: Python 3.14.5, jsonschema 4.26.0, Pillow 12.3.0.
- Generation attempts / fresh images / valid pairs: **0 / 0 / 0**.

Each successful real-source run reports **INCONCLUSIVE / DRY_RUN_NO_IMAGES**. The separate automated review checks persisted A/B equality, frozen restrictions, source bytes and delta hashes; it is neither a human review nor evidence of visual improvement.

E keeps the foreground occluder and its behind-content UNKNOWN_LOCKED, with no hidden object assertion or reconstruction authorization. P0 9/9, PR0 1/1, LOCK 4/4 are exercised; **PR1 0/0 is unexercised**, despite the comparator's conventional ratio 1.0. RR2 records one blocked hint and zero queryable needs, Archive queries, admissions or projections. Darkness, cropping and low resolution are distinguished from occlusion in its source provenance.

D/E original fixtures and historical UUID directories remain byte-for-byte intact; their deltas are unchanged. All three bindings are prospective annotations. C remains RECEIVED_UNBOUND / NO_GO_C0_UNVERIFIED; F remains conditional. Provider/model/quality remain dry-run placeholders. Zero production promotion or VSG-3A claim.

Kenny: **K1_CORPUS_RECOVERY_DRY_RUN_PASS**. Source VSG-2A and separate design authority/integrity are checked by the blocking verifier and persisted-byte review. Visual rubric remains **PENDING**. Source coverage: P0 21/21, PR0 7/7, PR1 3/3, LOCK 7/7; design: 3 required nodes and 4 required relations. Rooftop Graph Locks **0/0 NOT_EXERCISED**. Identical design directives travel in A/B common; only source topology/locks differ in serialization. Six sidecars (including K0, reception and design) are frozen and revalidated without checkout fallback. Plan Limits initial/final and consumption **UNKNOWN**; no numeric budget compliance claim.

[Kenny runbook](../visual_scene_graph/pilot/fixtures/kennys_new_01/RUNBOOK.md).

[E runbook](../visual_scene_graph/pilot/fixtures/r2b_e_new_01/RUNBOOK.md) · [D runbook](../visual_scene_graph/pilot/fixtures/r2b_d_new_01/RUNBOOK.md) · [Full QA](VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) · [Corpus audit](vsg_2b/corpus_audit.json) · [Controls](vsg_2b/controls.json) · [Regression](vsg_2b/regression.json).
