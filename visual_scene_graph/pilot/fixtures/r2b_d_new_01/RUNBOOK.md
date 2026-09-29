# VSG2B-R2B-D-NEW-01 · prospective binding v1

This is a **new annotation and orchestration** of the existing R2B D photograph, dated 2026-09-29. Registry compatibility key: `R2B-191-D`. No historical request or generation snapshots were recovered. The original photograph remains at `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg` with SHA-256 `282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc` (JPEG 347 × 389).

Implementation started at HEAD `ab04e1af0f5f7bf5e4ceed9431d02bc7977ce24d`; the difference from the spec baseline `ede34f6418dba617ab0b613046f9be2a6e9c5997` is the already-added Kenny JPEG. Quota counters were unavailable; timestamp and UNKNOWN five-hour/weekly balances are in `source_provenance.json`.

## Source annotation and review

Codex inspected the decoded original image and authored the current annotation; this is not attribution of the photograph. Photographer and capture date remain unknown. `source_provenance.json` records normalized source regions and a completed checklist for every entity and relationship; its SHA-256 is bound in the manifest attestation.

- Yellow sign: `TERMINAL DINER`, two lines, at `[0.455, 0.527, 0.600, 0.628]`; only exact transcription in this fixture.
- Visible sign is above the diner storefront (PR0). Left masonry facade is left of the diner (PR1). No concealed attachment or building ownership is asserted.
- Left storefront lettering is uncertain. Upper advertisement wording is deliberately untranscribed, not declared wholly illegible. Preserve their graphic layouts without inventing readings.
- No hidden architecture, rooftop, geographical identity, author, or capture date is inferred.

Task authorization is the user's instruction to implement the prospective dry-run spec. Conservative operation `/sc-core /sc-lock` resolves to VP00 / T01 / CG-S, with zero material change and the original camera held. Original preserve/unknown/forbid directives are frozen in `request.json`; no objective was changed after output inspection. The manifest rubric covers all 14 protected constraints plus identity and unauthorized changes and contains no branch assignment.

## Replay and dry run

Run from the repository root:

```sh
.venv-sc/bin/python -m visual_scene_graph.pilot.bind_d
.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation
.venv-sc/bin/python -m visual_scene_graph.run_generation_benchmark --verify validation/vsg_2b/VSG_2A_REPLAY_QA.json
.venv-sc/bin/python -m visual_scene_graph.pilot visual_scene_graph/pilot/fixtures/r2b_d_new_01/manifest.json --output outputs/vsg-2b-campaign
.venv-sc/bin/python -m visual_scene_graph.pilot.review_dry_run outputs/vsg-2b-campaign/RUN_UUID_FROM_PREVIOUS_COMMAND
```

`bind_d` re-executes the actual orchestrator with the frozen request and compares all eight derived snapshots; it checks source bytes and dimensions. The retriever rejects unexpected Archive queries: this fixture has zero reference needs, queries, admissions and projections. `--freeze` was used once to create the initial snapshots with exclusive writes. It cannot overwrite them and never changes the allowlist. Future annotation changes require a new fixture version, manifest hashes, reviewed admission, refreshed preconditions and another dry run.

Expected graph is rebuilt by the observer from SAR2, RR2 and runtime reference needs. Candidate is an equivalent input graph stored independently, not an output-image annotation. Context uses final CGC policies and original request directives; contract uses VSG-2A. Required preservation counts: P0 9/9, PR0 1/1, PR1 1/1, LOCK 3/3, zero unresolved mappings. These do not establish rooftop, occlusion, reference-transfer or visual coverage.

Validation refreshes controls, regression, replay and preconditions **before** invoking D's harness. It persists an append-only real dry run under `validation/vsg_2b/dry_runs/` and reviews the saved JSON through the separate `review_dry_run.py` implementation. This review checks parsed A records against B, all contract records, common equality, snapshot bytes and delta digest. Codex is responsible for the technical review; it is explicitly automated, not claimed to be a human or blind visual review. `delta_review.json` includes HEAD, date, hashes, command, checks and limitations. Current evidence paths are in `validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json`. Subsequent explicit CLI runs create new UUID directories; they do not replace the archived validation run.

Provider/model/quality use `DRY_RUN_ONLY` placeholders; size 347×389 and PNG are provisional requested settings, not a claim of provider support. Seed is null. The harness rejects real execution with these placeholders even if a bridge and reviewed delta are supplied. Before any later generation, operational settings must be supported, versioned, hashed, re-admitted and revalidated. This task ends at the dry run, with **zero provider calls, zero new images and zero valid visual pairs**.

## Checkpoint

Technical target: `CORPUS_RECOVERY_DRY_RUN_PASS`. Visual result: **INCONCLUSIVE / DRY_RUN_NO_IMAGES**. Overall VSG-2B remains **BLOCKED / PENDING_VISUAL**. Controls remain synthetic; their renderer preview is separate from this real-source dry run. Stable orchestration is unchanged, and no VSG-3A work is authorized by this evidence.

Kenny reception and observed/inferred scope are recorded separately in `../kennys/reception.json`. Kenny remains `RECEIVED_UNBOUND`; historical synthetic rooftop fixtures are not photographic observations. A separate versioned observation/design graph and tests are required before its admission. C/E binding and conditional F coverage remain later work.
