# VSG-2B controlled generation harness

Status: **BLOCKED: MISSING_FROZEN_SOURCE_BINDINGS**. Infrastructure and deterministic controls are implemented. Zero pilot images and zero visual comparisons have been produced. The user confirmed on 2026-09-29 that the missing snapshots / Kenny source are unavailable. The session has image-generation capability, so this is not a claim of `NO_GENERATOR`.

The stable client still ends at `GENERATION_READY`. Nothing in normal orchestration imports this package. Explicit invocation is `python -m visual_scene_graph.pilot`; the checked-in registry admits no fixtures. VSG-3A, 3B, correction and BK work are outside this implementation.

## Frozen fixture contract

To refresh technical evidence after an intentional change, run `.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation`. This does not admit fixtures or generate images.

The strict [manifest schema](../../schemas/vsg-pilot-manifest.schema.json) requires:

- A version, allowlisted fixture ID and explicit `pilot_enabled=true` (disabled unless supplied).
- Separate, SHA-256-bound request, runtime, SAR2, RR2, final CGC, expected graph, candidate graph, policy/directive sidecar, compiled contract and original source image files. Every file has a provenance description. Paths stay inside the repository.
- A source-identity attestation with author and evidence. A hash proves bytes; the attestation must establish that the snapshots describe this particular source. Historical generated outputs are not source photographs.
- Required nonempty P0/PR0/PR1/LOCK denominators, generation provider/model/seed/size/quality/format and a frozen visual rubric. The rubric covers all protected constraints and required relations, identity, and unauthorized changes.

Admission requires adding the exact canonical manifest SHA-256 to `allowlist.json` with `status=ADMITTED`. Registry changes require rerunning controls and freezing preconditions. Expected and candidate graph files must be separate. The expected graph replays from frozen SAR2/RR2; SAR2 replays from the request and resolved configuration. Runtime status, CGC and sidecars must agree. VSG-2A validates schemas, replay, canonical ordering, mapping, policies, all constraint equivalences and preservation coverage. Neither shadow `governs_generation=false` nor a historical visual PASS grants admission.

`check_preconditions()` verifies the current VSG-2A replay QA, unified regression and pilot-control evidence. Their hashes and current code/schema/fixture hashes are in `validation/vsg_2b/preconditions.json`. Code or registry changes invalidate this evidence.

## A/B renderer

There was no existing image-provider renderer in the stable runtime. This pilot defines an explicit CGC handoff renderer, `CGC + frozen source restrictions`, for both branches:

- Shared content is the entire stable CGC plus approved source constraints outside relationship/topology/lock records. This includes identical source identity, policies, directives, references, profile, mode, camera and format.
- A reads the stable CGC through the existing independent `stable_constraints` projection, which supplements restrictions absent from CGC with the frozen source graph. It serializes relationship/topology/lock records individually as canonical JSON lines in a string.
- B reads equivalent records from the compiled contract and expresses those same records as a structured array. The compiler contract is never sent as a CGC.

Both branches retain every constraint's ID, priority, value and lock IDs. The renderer compares the complete semantic projections, then parses A's relationship string back and requires exact equality with B's array. No additional facts, references or constraints are introduced. Unsupported fields or any loss fail closed. This tests a specific structured-expression delta; it does not compare against an undocumented historical prompting practice.

A dry run writes both effective payloads, manifest, comparison, frozen artifact bytes and a `delta_sha256` binding the manifest and payloads. It makes no provider calls and reports `INCONCLUSIVE / DRY_RUN_NO_IMAGES`. A real corpus dry run is currently blocked; the persisted control renderer preview uses a synthetic test fixture and is not visual evidence.

```sh
.venv-sc/bin/python -m visual_scene_graph.pilot path/to/frozen-manifest.json --output outputs/vsg-2b-campaign
```

## Provider adapter and execution

`CommandGenerator` runs an explicitly configured trusted local argv without a shell. No executable comes from a fixture. JSON on stdin contains exactly `source_base64`, `payload`, `provider`, `model`, `seed`, and `parameters`. A bridge must call a real image provider and return JSON with `image_base64` and `metadata`. Metadata must include provider, model, a fresh generation ID, seed (including null when unavailable), parameters and may include other provider receipts. It must report the provider's actual settings; unsupported parameters must fail rather than be silently dropped.

The bridge is deliberately external: no API, credentials or provider model is invented. No local bridge is configured in this checkout. A valid, reviewed fixture without a bridge returns `BLOCKED: NO_GENERATOR`. The session image tool cannot bypass fixture admission; its availability does not cure missing source bindings.

```sh
.venv-sc/bin/python -m visual_scene_graph.pilot path/to/frozen-manifest.json \
  --output outputs/vsg-2b-campaign --generate --reviewed-delta HASH_FROM_REVIEWED_DRY_RUN \
  --adapter-command /absolute/path/to/trusted-provider-bridge
```

`--reviewed-delta` records the operator's review of the concrete dry-run payloads before spending generation. It is not derived from the comparison PASS. Review whether the provider supports the supplied settings and approved reference representation before configuring it.

All runs have fresh UUID directories, exclusive file creation and immutable input snapshots. Each attempted call is recorded before invocation and consumes budget even on crash. Provider responses, output hashes, metadata, decoded image dimensions and input hashes are persisted. Invalid bytes remain available for technical triage. Calls stop on the first error. Both images must have matching dimensions/format, with settings equal to the frozen request. Reused generation IDs within a pair are rejected.

Use one campaign directory for the selected corpus. An OS lock serializes generation; the hard cap is eight calls (four pairs), with no automatic retries. The previous pair must have a completed review before another pair begins. Critical visual failure writes `STOP`; technical failure/interruption blocks further calls pending triage. Repeated fixtures are rejected. A fifth pair or retry requires an explicit, versioned budget/selection change; this implementation does not automatically authorize either. Starting another directory is a new campaign, not a way to extend this campaign's budget.

## Independent visual review and closure

Only copy the `review_packet/` directory to the reviewer. It contains the original source, randomly ordered anonymous outputs and frozen rubric. Keep the parent run directory (including the branch map, prompts and provider metadata) private during review. The provider never receives the rubric, expected verdict, review, or other branch's image.

A separately authored review follows [the review schema](../../schemas/vsg-pilot-review.schema.json). Each output must have one observation per rubric item, a source-relative preservation judgment, S0–S3 severity, normalized bounding box `[x0,y0,x1,y1]`, and a visual justification. Source/output hashes bind the review to real artifacts. Any reviewer disagreement must be resolved by a named human and documented in `disagreements`; unresolved disagreements must not be submitted as settled observations.

```python
from visual_scene_graph.pilot.evaluation import evaluate, close_campaign
result = evaluate(run_directory, independently_authored_blind_review)
summary = close_campaign(run_directories, selected_fixture_ids, regression_passed=True)
```

The evaluator checks the review evidence, unmasks A/B afterward and returns `BETTER`, `TIE`, `WORSE` or `INDETERMINATE`. S3, protected loss or regression fails. Unknown findings and uncontrolled seeds conservatively prevent PASS. Ties cannot establish improvement. Campaign PASS requires all selected fixtures, a verified improvement, no failures or unresolved results, and stable regression PASS. Human visual findings, not contract similarity, determine these results. Technical errors never count as valid pairs.

## Reproduction and evidence

```sh
.venv-sc/bin/python -m unittest visual_scene_graph.pilot.test_pilot -v
.venv-sc/bin/python benchmark/run_regression_suite.py
.venv-sc/bin/python -m visual_scene_graph.run_generation_benchmark --verify validation/vsg_2b/VSG_2A_REPLAY_QA.json
.venv-sc/bin/python -m visual_scene_graph.pilot.audit_corpus
```

The initial 2A verification matched all 42 original file hashes before edits. README, roadmap, changelog and regression-runner updates necessarily invalidate that historical report's checkout hashes. The original report is retained unchanged; the new replay evidence records the current checkout. The original baseline verification is preserved separately.

See [pilot QA](../../validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) and [summary](../../validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.md). Tests use synthetic images and a fake adapter only for control behavior; those outputs are never pilot evidence. No quota counters are available through this harness; the percentages in the proposed spec are historical observations, not reserved capacity.
