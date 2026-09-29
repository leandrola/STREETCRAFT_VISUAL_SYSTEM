# VSG-2B controlled generation pilot · 2026-09-29

**BLOCKED: MISSING_FROZEN_SOURCE_BINDINGS.** The user confirmed that the missing snapshots / Kenny source are unavailable. The isolated harness is implemented; the visual pilot is not complete and production is not authorized.

- Deterministic pilot controls: **32/32 PASS**.
- VSG-2A replay: **25/25 PASS**, current 42-file manifest verified. Original baseline also verified before edits; historical QA retained unchanged.
- Unified regression: **PASS** (21 checks).
- Dependencies: Python 3.14.5, jsonschema 4.26.0, Pillow 12.3.0.
- Generation attempts / fresh images / valid pairs: **0 / 0 / 0**. Technical failure rate and visual scores are not applicable.
- Real-corpus dry run: **BLOCKED**. Synthetic control renderer preview: **PASS**, no generation authorization or visual evidence.

R2B C/D/E/F original source files have recorded SHA-256 hashes, but lack frozen request/SAR2/RR2/CGC bindings. Kenny has structured fixtures but no traceable source image. No defensible substitution was found. All five registry entries remain `PENDING_EVIDENCE`.

The session has image-generation capability. Missing corpus evidence is the primary blocker; `NO_GENERATOR` is only the harness result for an otherwise admissible run without a configured local bridge.

The provider adapter uses an explicit local JSON protocol; it has not been exercised against a real image provider. Blind review and closure controls have deterministic tests only. Resume by supplying source-bound snapshots and an attested manifest, admitting its hash, refreshing preconditions, reviewing the dry-run payload delta, configuring a real provider bridge, then generating and reviewing each pair within the eight-image budget. Do not infer visual PASS from the technical checks.

[Harness / operational specification](../visual_scene_graph/pilot/README.md) · [Full QA](VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) · [Corpus audit](vsg_2b/corpus_audit.json) · [Controls](vsg_2b/controls.json) · [Regression](vsg_2b/regression.json) · [Current VSG-2A replay](vsg_2b/VSG_2A_REPLAY_QA.json) · [Control-only payload preview](vsg_2b/CONTROL_RENDERER_PREVIEW.json).
