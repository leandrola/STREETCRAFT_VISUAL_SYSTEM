# M3 / D2 isolated scaffold v0.1.0

User approval on 2026-10-02 accepts D1 as a design basis for
`VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0` and D2 exclusively for this scaffold.
The full approval, cited proposal hash, caps and resume state are recorded in
[CHECKPOINT](../../../development/coordination/CHECKPOINT.json).
The independent verifier approved the eight-file/sixteen-check allowlist before
implementation. Limits: eight new files, sixteen acceptance checks, forty engineering
hours maximum; model calls, attempts and images zero. D3/D4 remain pending.

This is a stdlib validation/log scaffold, without a consumer, model patch, runtime
registration, provider, tokenization, tensor/RNG creation, training or generation.
No settings are applied. No campaign policy, frozen inputs, manifest, admission,
historical result, approval proposal or image-generation protocol is changed.

`contract.py` validates seven-field envelopes against pinned source and payload
bytes. A text is canonical common + newline + exact persisted JSONL and has no R.
B text is common only; R is a separate array with the ten original typed records:
two edges, three VALIDATE_ONLY locks and five topology rows. A JSONL is never parsed
to create R. Inverse predicates have valid syntax but a mutated D envelope still
fails exact frozen truth. Missing/unknown fields, duplicate JSON keys, non-finite
values, changed locks/authority and hashes fail closed. Validation returns a fresh
copy and produces no side effects. It asserts documentary identity, not semantics.

`settings.py` compares the complete explicit candidate or negative-control
configuration with the pinned proposal: ID/version/kind, every setting, RNG design
text and relation-active-loop list. It returns immutable serialized design data and
a digest, with settings_applied/execution_authorized=false. Paired A/B configurations
must be identical. No defaults, settings application or runtime instantiation exists.

`ledger.py` is an in-memory static simulation with immutable zero caps and event
snapshots. Only all-zero reservations are allowed. A failure appends an event without
deleting its original reservation; an ID can never be retried. These are simulated
log transitions, not campaign attempts or learned calls. It has no persistence or
dispatch method and cannot reserve positive real work.

Run the sixteen acceptance checks directly, avoiding the outer Streetcraft package
initializers, from any working directory:

```sh
python3 -B visual_scene_graph/pilot/n5_scaffold/static_checks.py --verify-only
```

Use an absolute script path when outside the repository. To publish local evidence,
run from the repository root:

```sh
python3 -B visual_scene_graph/pilot/n5_scaffold/static_checks.py --output validation/vsg_2b/n5_scaffold/STATIC_RESULT.json
```

The runner only imports stdlib and the three sibling scaffold modules; git calls
read the fixed M3 baseline and never mutate the checkout. `--output` accepts only
the approved evidence path. No packages, source artifacts or weights are downloaded.
`fixtures.json` records frozen repository inputs and versioned acceptance definitions,
without copying or altering D truth. The sixteenth check validates imports/AST,
eight-file scope and byte preservation of all previous files except the two authorized
coordination updates. Historical M2 checker/report remain frozen evidence at `8ca0422`;
their checkpoint assertion describes that earlier approval state, not current M3.

Acceptance evidence and independent review are in
[STATIC_RESULT](../../../validation/vsg_2b/n5_scaffold/STATIC_RESULT.json).
PASS certifies sixteen static checks only. M3 closes after actual independent review
and checkpoint update. VSG-2B stays BLOCKED / PENDING_VISUAL, model tests NOT_RUN,
generated images0, production/provider_READY=false. Usage percentages are UNKNOWN.
Rollback is removal of this isolated scaffold under a later authorized change;
retain its evidence and historical counters. There is no operational integration
to disable or backend to restore.
