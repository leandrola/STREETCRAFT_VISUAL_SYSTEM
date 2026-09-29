# VSG2B-R2B-E-NEW-01 · prospective Occlusion Lock binding v1

This fixture is a **new annotation and orchestration** of the original E photograph, dated 2026-09-29. Compatible registry key: `R2B-191-E`. No historical request or snapshots were recovered. The photograph remains at `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-E_source.jpg`, SHA-256 `f0ba6e1f5bb5e3f40f39c0847f3d980e25c8c110b15b932cb1b3a10984a62860`, JPEG 500 × 454. No historical candidate is used as source or output.

HEAD at start: `0cb920c95b3f3f20814b376bbf3a7bf086733c03`, matching the spec baseline, with a clean tree. The required initial pause recommended High reasoning; the user replied “go”. Five-hour and weekly counters were UNKNOWN, with the inspection timestamp recorded in `source_provenance.json`; historical percentages were not reused. Scope is the E dry run, with zero image calls and the visual budget reserved for a later session.

## Annotation and scope review

Codex opened the original JPEG at native resolution, checked its dimensions/hash, and authored the current annotation. Photographer and capture date remain UNKNOWN. The manifest attestation binds the source and the SHA-256 of `source_provenance.json`, which contains per-entity/relationship evidence, a completed checklist, uncertainty states and prohibited inferences.

| Record | Normalized region | Meaning |
| --- | --- | --- |
| `left_facades_01` | `[0,0,0.438,0.872]` | Visible facade contours; a coarse support region, not complete inferred geometry. |
| `right_facades_01` | `[0.638,0,1,0.861]` | Visible right facade contours, clipped at photo edges. |
| `occluder_01` | `[0.496,0.819,0.790,0.969]` | Observed dark textured foreground silhouette, with an approximate polygon in provenance/request. Physical object identity is deliberately unassigned. |
| `hidden_01` | `[0.530,0.874,0.742,0.949]` | Screen-space non-revelation review mask behind the silhouette; not a measured hidden object or hidden geometry. |

The foreground surface has a visible edge against lighter pavement and pale horizontal forms; visibility behind it is interrupted. The relation `occluder_01 OCCLUDES hidden_01` is PR0 because preserving this visibility barrier is the critical source restriction. That relational observation does **not** identify anything behind it. No PR1 relationship is manufactured for coverage.

Dark distant surfaces, small details limited by resolution, buildings cut by the photo boundary and absent evidence are recorded separately from occlusion. No exact text is transcribed. Bounding boxes/polygon are approximate manual evidence regions, not a segmentation claim. Preserve the pixels and uncertainty; do not infer occluder species/type, hidden vehicles, facade openings, street geometry or exact wording.

`/sc-core /sc-lock` resolves VP00 / T01 / CG-S. It holds the source composition and camera. `hidden_01` uses P5-D and resolves to `UNKNOWN_LOCKED`; its observed flag is false. No reconstruction, including minimal-continuity synthesis, is authorized. SAR2-derived CGC policies contain the hidden occlusion lock and forbid exact resolution. Semantic Text Lock remains STRICT. Original request directives are frozen before any A/B payload is seen.

The effective ledger contains absolute `GL-OCC-REL_FOREGROUND_OCCLUDES_UNKNOWN`, targeting the occlusion edge, with endpoints `occluder_01` and `hidden_01` and source-region provenance. Three additional geometry locks protect visible facade groups and occluder geometry. Tests validate the effective unknown action/flag/edge lock even with an ordinary node type; no gate depends on forcing `unknown_region`.

## Replay and admission

Initial creation was `.venv-sc/bin/python -m visual_scene_graph.pilot.bind_e --freeze`. It uses exclusive writes and refuses to overwrite any existing snapshot/manifest. Future versions need a new fixture directory; do not edit this admitted version in place. The original source is referenced without changing its bytes.

The binder executes the real orchestrator once per reconstruction, and all runtime/SAR2/RR2/CGC snapshots come from that same run. The observer derives expected graph from SAR2, RR2 and runtime reference needs. Candidate graph is an equivalent input in a separate file, not a generated-image observation. Context contains final CGC policies and original request directives. VSG-2A compiles and compares against the immutable source graph.

E naturally creates **one RN_BLOCKED reference hint** for `hidden_01`. It is not an Archive query authorization: there are zero queryable needs, zero queries, no admissions/projection, and `NO_QUERY_LOCKED_UNKNOWN` in RR2. The retriever raises on unexpected calls; query budget is zero. Reporting “zero total needs” would be incorrect.

Replay and source annotation review preceded admission of canonical manifest digest `6568570352087407c7f6f23955ffe6e4f6381c6861bdd674d78baaa16197b275`. Manifest has all ten required artifacts, SHA-256/provenance, nonempty P0/LOCK requirements, and a rubric covering the protected constraints plus explicit unknown/inference/reference restrictions. Rubric contains no A/B branch mapping.

| Priority | Required | Preserved | Coverage claim |
| --- | ---: | ---: | --- |
| P0 | 9 | 9 | Exercised |
| PR0 | 1 | 1 | Exercised |
| PR1 | 0 | 0 | **Unexercised**; comparator ratio 1.0 is not evidence |
| LOCK | 4 | 4 | Exercised |

Comparison has zero discrepancies and unresolved mappings. Provider/model/quality are explicit `DRY_RUN_ONLY` placeholders; size 500×454, PNG and null seed are provisional requests, not asserted provider capabilities. Existing harness guards reject real generation with these settings.

## Reproducible commands

From repository root:

```sh
.venv-sc/bin/python -m visual_scene_graph.pilot.bind_e
.venv-sc/bin/python -m visual_scene_graph.pilot.bind_d
.venv-sc/bin/python -m unittest visual_scene_graph.pilot.test_e_binding -v
.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation
.venv-sc/bin/python -m visual_scene_graph.run_generation_benchmark --verify validation/vsg_2b/VSG_2A_REPLAY_QA.json
.venv-sc/bin/python -m visual_scene_graph.pilot visual_scene_graph/pilot/fixtures/r2b_e_new_01/manifest.json --output outputs/vsg-2b-campaign
.venv-sc/bin/python -m visual_scene_graph.pilot.review_dry_run outputs/vsg-2b-campaign/RUN_UUID_FROM_PREVIOUS_COMMAND
```

Validation runs the original 32 controls plus 16 E mutation/replay checks, unified regression and current VSG-2A replay. It refreshes preconditions **before** invoking the harness. Explicit deterministic selection is D then E, each with a separate result under QA `dry_run.fixtures`. Each successful run creates a fresh UUID under `validation/vsg_2b/dry_runs/`, never overwriting an earlier run. It saves frozen bytes, manifest, comparison, effective A/B payloads, report and `delta_review.json`.

The separate reviewer reads persisted bytes, checks identical common content, parsed A records versus structured B, all contract locks/restrictions, nonempty required coverage, source/artifact hashes and delta digest. Review records HEAD/date/commands, precondition hash, all priority denominators and zero call/image counts. It is an **automated technical review**, not a human or visual review. Exact archived paths and hashes are in `validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json`.

## D protection and checkpoint

`d_preservation_baseline.json` freezes hashes for all 42 existing D fixture/history files at starting HEAD. E provenance binds that baseline. Every E replay and the mutation suite check them. D's binder and original fixture remain untouched; validation requires its new payload delta to equal `6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`, with unchanged manifest digest `d258f4784d7f27cabec9b6044142cdc809e19a9552e72924468e20d55dc3d3ec`. New D UUIDs are additional evidence, not replacements.

The expected technical checkpoint is E `CORPUS_RECOVERY_DRY_RUN_PASS`, with D preserved/revalidated. Harness result is **INCONCLUSIVE / DRY_RUN_NO_IMAGES**. Overall VSG-2B remains **BLOCKED / PENDING_VISUAL**: zero provider calls, zero new images, zero valid visual pairs, no visual merit or production promotion claim. C and Kenny remain pending; F remains conditional. No bridge selection, visual-budget spending or VSG-3A work belongs to this advance.
