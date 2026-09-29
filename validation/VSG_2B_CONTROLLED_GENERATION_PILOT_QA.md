# VSG-2B controlled generation pilot · 2026-09-29

**General status: BLOCKED / PENDING_VISUAL.** Technical dry-run results are separate by fixture:

- **R2B-191-D: CORPUS_RECOVERY_DRY_RUN_PASS**; delta `6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`.
- **R2B-191-E: CORPUS_RECOVERY_DRY_RUN_PASS**; delta `a282bbee73b6613ce2d5ad0737065f3e2332ebce020e664161f38cc43fd17458`.

- Deterministic controls: **48/48 PASS** (32 original controls + 16 E binding/mutation checks).
- Current VSG-2A replay: **25/25 PASS**, 42 files verified; historical suite unchanged.
- Unified regression: **PASS** (22 checks).
- Dependencies: Python 3.14.5, jsonschema 4.26.0, Pillow 12.3.0.
- Generation attempts / fresh images / valid pairs: **0 / 0 / 0**.

Each successful real-source run reports **INCONCLUSIVE / DRY_RUN_NO_IMAGES**. The separate automated review checks persisted A/B equality, frozen restrictions, source bytes and delta hashes; it is neither a human review nor evidence of visual improvement.

E keeps the foreground occluder and its behind-content UNKNOWN_LOCKED, with no hidden object assertion or reconstruction authorization. P0 9/9, PR0 1/1, LOCK 4/4 are exercised; **PR1 0/0 is unexercised**, despite the comparator's conventional ratio 1.0. RR2 records one blocked hint and zero queryable needs, Archive queries, admissions or projections. Darkness, cropping and low resolution are distinguished from occlusion in its source provenance.

D's original snapshots, manifest, historical UUID directories and delta are preserved byte-for-byte and replayed. Both bindings are new prospective annotations; no historical requests were recovered. Kenny remains RECEIVED_UNBOUND, C remains pending, and F depends on coverage/budget review. Provider/model/quality remain dry-run placeholders. Operational generation requires complete critical corpus, supported settings, versioned readmission, fresh validation/dry runs and reviewed deltas; the eight-call visual budget remains unused. No production promotion or VSG-3A claim.

[E runbook](../visual_scene_graph/pilot/fixtures/r2b_e_new_01/RUNBOOK.md) · [D runbook](../visual_scene_graph/pilot/fixtures/r2b_d_new_01/RUNBOOK.md) · [Full QA](VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) · [Corpus audit](vsg_2b/corpus_audit.json) · [Controls](vsg_2b/controls.json) · [Regression](vsg_2b/regression.json).
