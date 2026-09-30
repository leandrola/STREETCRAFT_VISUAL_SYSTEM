# K1 · Kenny source/design binding and technical dry run

**K1_CORPUS_RECOVERY_DRY_RUN_PASS**. Current validation: 74/74 pilot controls,
23/23 unified regression checks, VSG-2A 25/25 cases and 42 files verified.
Source P0 21/21, PR0 7/7, PR1 3/3, LOCK 7/7; design gate 3/3 nodes, 4/4 relations.

Executed: `bind_kenny` replay PASS; combined pilot unittest command 74 tests PASS;
`run_validation` PASS with new D/E/Kenny dry runs and independent delta reviews.
Kenny run: `validation/vsg_2b/dry_runs/ffec337b-31af-471a-bb9b-9a0c91413c7c/`.
Canonical manifest SHA-256:
`f628730fb1dd043c6df5cdf2d47d76002b3266be21b8a97204d54914674b5c79`.
Delta SHA-256:
`d04d58135715c95be089344674a99f51b78d8bb4a6ebd08da2194e2b97cc0e17`.
Design sidecar SHA-256:
`c09e93d07aebd51203e08d385a82c49918f318e47f60f51f3b672077cd98ee4e`.

This is a prospective annotation of the original 736 × 414 JPEG and a separately
authorized rooftop composition. It is not historical snapshot recovery, rooftop
observation or a claim about the original roof. The authoritative K0 is the
punctuation-corrected contract at the starting HEAD
`b36afe7dec67ee5a1778757011d7af89297f3645`, SHA-256
`ed8f17f1204d041d47f0618378e7056b9d0d95fc4b67aa9d4203003b75194f90`.
K0's earlier annotation HEAD is provenance, not a requirement to discard later
compatible commits. No pre-existing working changes were present.

## Frozen scope and authority

- Source: `../kennys/source/kennys-shop.jpg`, SHA-256
  `45b8bff5c33ea411ffef3c88db99d757ce462a7f13b56df3f2fbc62b994357b2`.
- `observations.json`: KOBS-01…12, KSR-01…10, regions, literals and uncertainty.
  Eleven observed source nodes; KOBS-12 records a capture limit, not an observed
  roof node. Exact locks only for the main sign and banner. The sale strip is a
  visual surface with a partial text token; punctuation remains unresolved.
- `design.json`: `KENNYS_ROOFTOP_DESIGN_V1`, AUTHORIZED_INFERENCE, observed=false,
  three required nodes and four required relations. Roof, parapet and one HVAC
  are mandatory; skylight, chimney, water tank and access bulkhead excluded.
  Only KDR-01 crosses to the read-only facade anchor.
- T04 / VP00 / CG-B, explicitly authorized moderate elevation and upward framing
  extension. CG-B's source/mode-authority exception is used for a prospective
  view, not attributed to the photograph. No source camera lock was removed.
  Original rooftop, unseen sides/interiors and historical depth remain unknown.
- `request.json` pins six sidecars: observations, design, source provenance,
  preservation baseline, K0 Markdown and reception. Original design directives
  are frozen before orchestration. CIL preserve/unknown prohibitions are also
  explicit original directives so compilation cannot silently omit them.
- Nine JSON artifacts plus the unchanged source form manifest v1's ten artifacts.
  The six extra sidecars retain their own filenames and exact bytes under each
  run's `sidecars/`; the schema is unchanged. Candidate graph is an equivalent
  input encoding, never an observed generated result.

## Blocking boundary

`../../kenny_binding.py` pins the reviewed authority bytes independently of the
request. It checks exact design structure, source/design IDs, immutable facade
annotation, uncertainty, directives and deterministic runtime/contract replay.
`../../bind_kenny.py` creates or replays this fixture. Both shared fixture replay
and harness prepare invoke the same verifier. Execution rechecks the frozen
bundle and common CGC; persisted review reads only the run's sidecars, without
falling back to checkout copies. Renaming Kenny's fixture ID does not bypass the
gate when source hash or binding identifies Kenny. Tests use temporary admission
and mocked preconditions only to avoid circular regression evidence; actual dry
runs use the refreshed real preconditions.

The independent delta reviewer checks A/B common equality, serialized A versus
structured B, frozen restrictions, artifact hashes and delta hash. Design
instructions are identical in common. A/B exercises **source** relations and
locks; **rooftop Graph Locks are 0/0, NOT_EXERCISED**. Design authority/integrity
(3 nodes, 4 relations) is a separate gate. The visual rubric remains PENDING.

## Reproduction from repository root

```sh
.venv-sc/bin/python -m visual_scene_graph.pilot.bind_kenny
.venv-sc/bin/python -m unittest visual_scene_graph.pilot.test_pilot visual_scene_graph.pilot.test_e_binding visual_scene_graph.pilot.test_kenny_binding
.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation
.venv-sc/bin/python -m visual_scene_graph.pilot visual_scene_graph/pilot/fixtures/kennys_new_01/manifest.json --output outputs/vsg-2b-campaign
.venv-sc/bin/python -m visual_scene_graph.pilot.review_dry_run <persisted-run-directory>
```

The unified validator explicitly selects D → E → Kenny, refreshes preconditions
after code/fixture/allowlist changes and archives new UUID runs. It never replaces
historical run directories. `preservation_baseline.json` hashes every starting
D/E fixture, C decision, original Kenny record and historical dry-run file; D/E
canonical delta hashes must also remain unchanged. `--freeze` refuses an existing
manifest; use a new version for a new annotation. Do not edit pins to readmit
mutated evidence. Do not use `--generate`: provider/model/quality are deliberate
DRY_RUN_ONLY placeholders and seed is null.

Current machine-readable results and run links are in
`validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json` and
`validation/vsg_2b/corpus_audit.json` (repository-relative paths). A technical K1
PASS requires current regression, source comparison, design gate, preconditions,
D/E preservation and independent persisted-byte review all to pass. Harness
status remains INCONCLUSIVE / DRY_RUN_NO_IMAGES; global status remains
BLOCKED / PENDING_VISUAL. C remains RECEIVED_UNBOUND / NO_GO_C0_UNVERIFIED.

## Budget and scope

Plan Limits initial, Gate A, Gate B, Gate C and final: five-hour UNKNOWN, Weekly
UNKNOWN, observed consumption UNKNOWN. No numerical certification of the
40-percentage-point cap is possible. Work is limited to K1's specified gates;
no K2, provider setup, images or visual review. New Archive calls / generator
calls / images / visual pairs: 0 / 0 / 0 / 0.
