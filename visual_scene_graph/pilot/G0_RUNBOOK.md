# VSG-2B / G0 · campaign gate and provider readiness

Execution date: 2026-09-30. **G0_CAMPAIGN_GATE_READY_PROVIDER_UNCONFIGURED**.
Technical outcome is recorded in
[`validation/vsg_2b/G0_RESULT.json`](../../validation/vsg_2b/G0_RESULT.json).
This is a technical gate, never a visual PASS. VSG-2B remains **BLOCKED / PENDING_VISUAL**;
`production_authorized=false`.

## Entry and scope

Initial and final HEAD: `14641922fc185a809885730899f1e1cb80d8fc42`.
The checkout matches the spec's inspected commit; no intervening commits. Entry tree
was clean. Changes are left in the working tree, without a commit or publication.
No applicable AGENTS.md was found in the checkout or parent directories.

The operator replied `go` after the reasoning-level checkpoint. The selected UI
reasoning setting and Plan Limits are not exposed through this session. Five-hour
and weekly balances, initial/final and after audit, implementation, validation and
closure: **UNKNOWN**. Consumption: **UNKNOWN**. The spec's 40-percentage-point ceiling
is retained as a limit, not a target; numeric compliance cannot be certified.
No quota values are inferred from elapsed time or test counts.

Entry `check_preconditions()` passed against current bytes. Historical evidence at
that HEAD records 74 controls, 25 VSG-2A cases, 42 replay file hashes, 23 regression
checks and zero generation attempts/images/pairs. These are distinguished from the
new results below. The original snapshots, K0, K1 sidecars, C decision and historical
dry-run UUID directories are preserved.

## Coverage and campaign policy

[Policy 1.0.0](campaign_policy.json) is machine-validated by
[the campaign schema](../../schemas/vsg-pilot-campaign.schema.json).
Its canonical hash is recorded in G0_RESULT and current QA. Policy and schema bytes
are included in the existing preconditions file-hash checks.

| Fixture | Phenomenon | Technical eligibility now | Global closure contribution |
| --- | --- | --- | --- |
| D | Semantic Text Lock | Admitted prospective binding; dry run only | `lock:GL-SEM-SIGN_01`, with real A/B observations and preservation in B |
| E | Occlusion Lock | Admitted prospective binding; dry run only | `lock:GL-OCC-REL_FOREGROUND_OCCLUDES_UNKNOWN`; hidden content remains UNKNOWN_LOCKED |
| Kenny | Source preservation and authorized design | Admitted source/design separation; dry run only | Source identity plus all 10 frozen design rubric criteria, including 3 components and 4 relations |
| C | Reference Isolation | BLOCKED / RECEIVED_UNBOUND / NO_GO_C0_UNVERIFIED | Mandatory critical phenomenon; no coverage until documented source binding, admission and valid reviewed pair |
| F | CG-F camera | Conditional, not selected or admitted | Does not replace C; cannot automatically become the fourth or fifth pair |

Global selection is exactly D/E/Kenny/C: minimum four distinct pairs, one A/B pair
per fixture, eight attempted calls maximum in one campaign directory. Every required
phenomenon needs at least one admitted pair with nonempty criteria bound to the frozen
rubric and favorable B observations. Empty criteria and 0/0 coverage do not count.
E PR1 0/0 and Kenny rooftop source Graph Locks 0/0 remain **NOT_EXERCISED**.

D/E/Kenny alone can establish only a partial subpilot (`PARTIAL_D_E_KENNY`, global
status `INCONCLUSIVE`). Technical admission does not authorize generation under the
current placeholder settings. A future policy/version change, backed by new evidence,
is required for a replacement fixture or scope change; a camera case alone does not
establish Reference Isolation. C's valid image hash does not prove Fear City ↔ CG-FC.

## Code changes

- `campaign.py` loads policy and registry and replays current admission/preconditions,
  frozen artifacts and K1 sidecars, payloads/comparison, attempted inputs, receipts,
  image bytes, metadata and submitted review before considering global PASS.
- `evaluation.py` separates read-only `assess_review` from append-only `evaluate`.
  Closure recomputes findings and compares the saved evaluation; it never fabricates
  or writes a human review. S3, protected loss and regression rules remain unchanged.
- Closure checks one campaign directory, all attempt files including omitted/failed
  runs, the eight-call cap, unique selection/results, STOP, exact policy manifest
  admission, minimum pairs, required phenomena, a verified improvement, controlled
  seeds and regression. Missing or malformed evidence closes inconclusively;
  validated visual failures remain FAIL. No production promotion is possible.
- `CommandGenerator` requires actual provider/model/seed/parameters metadata,
  including an explicit null seed when unavailable, and a nonempty string generation
  ID. Unsupported/mismatched settings fail. No real bridge was added or invoked.
- `test_campaign.py` covers policy and closure with synthetic temporary fixtures,
  fake outputs and explicitly synthetic reviews. The positive PASS test establishes
  logical reachability only; its IDs are prefixed `SYNTHETIC-` and it is not evidence
  about D/E/Kenny/C. Existing K1 checks remain active for real Kenny IDs.
- The regression runner and validation refresh include G0 controls and policy
  metadata. The stable client and normal orchestration were not changed.

## Provider inventory: PROVIDER_UNCONFIGURED

The CLI accepts an explicit `--adapter-command` argv and does not discover a provider
from credentials or environment variables. None was supplied. The checkout has no
image-provider implementation or declared executable bridge; `adapters/README.md`
is an interface outline. D/E/Kenny manifests all retain `DRY_RUN_ONLY` provider,
model and quality, and seed null. This proves no usable local bridge configuration
for this run; it does not claim that no external service exists. No credential files
or secret environment values were searched, printed or persisted.

| Capability | Required contract | Verified local support |
| --- | --- | --- |
| Source image | `source_base64` containing the frozen original | Protocol tested with fake bridge; real support UNKNOWN |
| A/B payloads | Same `common`; A relation string / B structured array | Fake JSON stdin/stdout only; real support UNKNOWN |
| Resolution/aspect | Provider-supported `parameters.size`, documented handling of source aspect | UNKNOWN; D 347x389, E 500x454 and Kenny settings are provisional |
| Output format | Image bytes encoded as `image_base64`; requested format in metadata | Fake protocol and existing image-decoding controls; real support UNKNOWN |
| Quality | Explicit supported quality; no silent omission | UNKNOWN |
| Seed | Actual reproducible seed or explicit null | Metadata contract checked; reproducibility UNKNOWN; null prevents global PASS |
| IDs/receipts | Fresh generation ID, actual provider/model/settings, bound inputs and outputs | Fake protocol and receipt tamper controls only; no real receipts |
| Authentication | Local authentication used by the trusted executable | UNCONFIGURED; no credentials inspected |

Exact missing inputs are: provider and model identifiers; documented source-image and
A/B payload support; trusted executable absolute path and argv; local authentication
mechanism (reference/name only, never credential contents); supported size/aspect,
format, quality and all additional parameters; actual seed semantics; and the real
response/receipt contract with generation IDs. Documentation or bridge inspection
must establish support without a live call before calling this provider READY.
A manually supplied output does not replace two fresh outputs and receipts from the
same bridge. D's source photograph is already present.

## Proposed next first pair: D, still not authorized here

1. Supply and verify the above real bridge capabilities. Resolve seed reproducibility;
   a provider without controlled seed can explore variation but cannot yield global
   PASS under this policy.
2. Preserve `fixtures/r2b_d_new_01/` and create a new versioned D manifest/configuration
   (proposed location `fixtures/r2b_d_provider_v1/manifest.json`). Retain source and
   frozen semantics. Specify supported provider/model/size/quality/format/seed and
   parameters; do not assume the provisional 347x389 size is supported.
3. Recompute the canonical manifest hash, explicitly version/update allowlist and
   campaign policy admission, and adapt replay/refresh to the new configuration.
   Refresh preconditions/regression using the repository flow. Do not edit historical
   manifests merely to bypass admission.
4. Run a new D dry run in the intended campaign and review its concrete A/B payloads.
   Recompute `delta_sha256 = digest({manifest, payloads})`; the old D delta is historical
   and cannot authorize changed provider, size, seed or parameters. Settings are not
   frozen yet, so there is no honest operational manifest/delta hash to publish now.
5. A subsequent authorized spec may spend two of eight attempts in a single proposed
   campaign directory `outputs/vsg-2b-g0-provider-v1`. Use the fresh reviewed delta and
   configured executable. Then provide only `review_packet/` to an independent blind
   reviewer before any next pair. C provenance/admission remains separately necessary
   to close the full campaign; completing D never resolves it.

## Reproduction and evidence

```sh
.venv-sc/bin/python -m unittest visual_scene_graph.pilot.test_campaign visual_scene_graph.pilot.test_pilot
.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation
```

The first command checks G0 plus original controls; the second runs required unified
regression, refreshes preconditions and VSG-2A replay, then saves separate new technical
D/E/Kenny dry runs and persisted delta reviews. No `--generate` or live provider call
is part of either command. Synthetic fake calls/images exist only inside control tests
and temporary directories; they are not campaign generation or visual evidence.

Fresh results: **58/58 focused tests**, **100/100 pilot controls** (32 original,
16 E, 26 Kenny, 26 G0), **25/25 VSG-2A cases** with 42 replay hashes, and
**24/24 unified regression checks**, all PASS. Final `check_preconditions()` passed;
`git diff --check` passed. All **263 protected existing files** are byte-identical.
D/E/Kenny replay and new technical dry runs passed with all three prior deltas
unchanged. The real empty campaign correctly closes INCONCLUSIVE, with C admission,
minimum pairs, required phenomena and verified improvement still missing.

New terminal results, exact hashes, invariance checks, limits checkpoints and the
three new dry-run artifact paths are in [G0_RESULT](../../validation/vsg_2b/G0_RESULT.json).
Current [QA](../../validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json),
[controls](../../validation/vsg_2b/controls.json),
[regression](../../validation/vsg_2b/regression.json) and
[preconditions](../../validation/vsg_2b/preconditions.json) are regenerated evidence.
Historical reports and dry-run UUIDs are retained. The first development test run
failed because synthetic fixtures used the real Kenny ID; the corrected controls
use separate synthetic identities and preserve the K1 verifier.

Terminal state is **G0_CAMPAIGN_GATE_READY_PROVIDER_UNCONFIGURED**.
Provider readiness is the remaining
G0 prerequisite; C provenance and all visual pairs/reviews remain prerequisites for
VSG-2B. Real Archive calls / generation calls / new images / visual pairs: **0/0/0/0**.
