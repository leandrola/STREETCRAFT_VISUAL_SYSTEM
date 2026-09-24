# VSG-2A · Generation Compiler Shadow

VSG-2A is **COMPLETED AND VALIDATED** over controlled structured snapshots. The
compiler creates a `VSG_GENERATION_CONTRACT` (`schema_version=2.0.0`,
`mode=SHADOW`, `governs_generation=false`). The preservation gate compares it
with the actual stable CGC plus the immutable source graph. A PASS is diagnostic
information, never permission to generate.

## Reproduce

Use the same Python environment as the unified regression (`jsonschema` and
Pillow installed). From the repository root:

```sh
python -m visual_scene_graph.run_generation_benchmark
python visual_scene_graph/test_generation_compiler.py
python -m visual_scene_graph.run_generation_benchmark --verify validation/VSG_2A_GENERATION_COMPILER_QA.json
python benchmark/run_regression_suite.py
```

The unified command writes `validation/INTEGRATION_QA.json`, as before. The
benchmark without `--output` is read-only. To persist fresh evidence:

```sh
python -m visual_scene_graph.run_generation_benchmark --output /tmp/vsg2a-qa.json
```

For caller-supplied snapshots, use `--input snapshots.json --output /tmp/report.json`.
The input object has `stable_cgc`, `sar2`, `expected_graph`, `candidate_graph`,
`generation_context`, and optional `causal_trace` plus `trace_artifacts`. A failed
preservation gate returns exit code 1. Malformed inputs are rejected, never
repaired or supplied with permissive defaults. The output includes the contract,
machine-readable comparison, and `summary` text.

## Explicit inputs and boundaries

The existing VSG-1 observer omits SAR2 preservation levels/actions and CGC request
policies. Altering that observer would change stable output. Instead,
`compile_generation_contract(vsg, *, sar2, generation_context, causal_trace=None,
trace_artifacts=None)` consumes a valid VSG-1 and explicit sidecars:

- SAR2 supplies entity priorities, resolved actions and source-only attributes,
  including roles and source invariants. Missing/duplicate mappings fail closed.
- VSG supplies node identities, properties, topology, spatial predicates,
  epistemic state, reference scope and effective Graph Locks.
- `generation_context.policies` supplies mode, profile, camera, text policy,
  material delta, occlusion policy, and any existing RR2/preflight/request policy
  fields. `generation_context.directives` explicitly provides all six request
  lists: preserve, transform, remove, infer, unknown and forbid. Empty lists must
  be explicit. Global policies are passthroughs, **not information inferred by
  VSG**. The benchmark captures them from actual stable orchestration and takes
  request directives from the request, independently of scene projection.

The compiler reuses SAR2's `project_scene_to_cgc` for directive encoding, VSG-1
lock construction/validation, and VSG-1.5 trace validation. It does not invoke
or modify generation. Contract node/edge values and membership come from the
candidate graph, never from the expected CGC. Every unique node is one required
source occurrence (cardinality 1..1); supplied physical counts/cardinalities in
properties or source attributes remain explicit and are retained separately.

`compare_generation_contract` additionally requires the **immutable source VSG**
(`expected_graph`). Stable CGC has no complete node-attribute or Graph Lock
ledger: those baseline restrictions therefore come from this separate source
snapshot. Callers must retain the original source snapshot; using the candidate
as its own baseline cannot establish preservation. This is an explicit trust
boundary, not a reconstructed source or a claim of image understanding.

## Semantic comparison and fail-closed gate

Constraints have stable IDs for nodes, actions, topology, relationships, locks,
references, unknowns, identity anchors, policies and directives. The comparator
reads stable `scene_intelligence.entity_actions` and `protected_relationships`,
checks their SAR2 mappings, and verifies that the corresponding executable CGC
preserve/unknown/forbid directives exist. It supplements these with source graph
restrictions. Unknown CGC fields and ambiguous mappings fail closed.

| Classification | Meaning |
| --- | --- |
| `equivalent` | Same typed value, priority and required lock association after normalization. |
| `omission` | Expected stable constraint has no candidate counterpart. |
| `weakening` | Lower action/relationship/lock strength, lost field/restriction/topology member, detached lock, lower minimum or higher maximum cardinality, or permissive unresolved state. |
| `contradiction` | Incompatible literal, type, identity, endpoint, spatial predicate or other exact value. |
| `unauthorized_addition` | New constraint, added lock association, directive or unsupported extra restriction. |

All non-equivalent findings fail the gate, including changes outside P0/PR0/PR1.
Opaque/free-text restrictions require exact content: this compiler does not
interpret natural-language paraphrases as equivalent or authorize strengthening.
Unknowns require an explicit unknown action, epistemic state and occlusion lock;
resolving them, detaching the lock or substituting inference fails.

Reports include source/target values, priority, affected stable CGC location or
source restriction, expected/actual lock IDs, source/candidate references and
optional verified trace-event IDs. `render_comparison` produces a readable summary.

Coverage is `equivalent required constraints / all expected required constraints`
for each of P0, PR0, PR1 and LOCK. The Kenny control has **9/9 P0 constraints**
(three nodes, each with node/action/topology constraints), **2/2 PR0**, **3/3 PR1**,
and **6/6 Graph Locks**, covering all four lock types. An empty category has ratio
1.0 with denominator zero; it is not evidence that the category was exercised.
The controlled corpus exercises all categories with nonzero denominators.
PASS additionally requires zero discrepancies and zero unresolved mappings;
coverage alone cannot override an invalid baseline, replay or lineage failure.

## Canonical content and lineage

Canonical UTF-8 JSON uses sorted keys, compact separators, no timestamps and no
NaN/Infinity. Named set collections are sorted; arbitrary property arrays such
as coordinates retain their meaningful order. Equivalent reordering of nodes,
edges, source entities, action mappings and lock ledgers produces identical
bytes. Duplicate IDs are rejected rather than deduplicated.

Source references use `{artifact, collection, id}` selectors instead of positional
array offsets, so reordering does not change lineage. `resolve_ref` resolves
these against supplied artifacts. Multiple nodes and edges support one topology
constraint; one node supports several constraints. Evidence remains reachable
through the original elements, including source attributes and lock provenance.
Observer input hashes and ledger checksum caches are excluded from the semantic
source hash because those legacy caches depend on ordering; their complete
underlying content is retained and hashed instead.

A supplied VSG-1.5 trace must validate by replay against its complete artifacts
and match both VSG and SAR2. Event references retain exact existing IDs and the
trace digest. Missing or mismatched trace evidence is rejected. When no trace
is supplied, provenance says `causal_trace: null`; no causal events are invented.
A regenerated trace with different provenance is a different input artifact.

`contract_sha256` and `report_sha256` exclude only their own digest fields.
`validate_generation_contract` checks schema, canonical form, references and
complete compiler replay. Rehashing a forged contract does not make it valid.
The QA verification command checks all recorded file hashes and replays every
controlled case; extra regression evidence is also bound by the QA digest.

## Validation and generation isolation

The corpus contains **25/25 passing expectations**, including deliberately
failing contracts. Tests cover healthy equivalence, all required fault classes,
locked/permissive unknowns, reordering, many-to-one and one-to-many lineage,
verified Causal Trace, unsupported policies, ambiguity and tampered provenance.
There are **24 automated tests**, with shuffled inputs tested across ten seeds.
Five persisted final CGCs are also compared successfully, including the locked
unknown building and blocked-preflight snapshot. Three blocked-reference records
have no final CGC and are reported `UNAVAILABLE`, never counted as successful
comparisons. This replay uses stored evidence and does not rerun the external
Archive. Global policies and non-scene directives are captured passthroughs;
scene constraints are independently projected from the persisted SAR2/RR2.
An unknown need not have node type `unknown_region`: a SAR2 unknown action plus
its VSG occlusion flag preserves the restriction, with the CGC unknown/occlusion
policies checked separately. Every applicable ledger lock remains mandatory.

The production orchestrator, CGC schema, generator/preflight/readiness code,
observer, SAR2 and Reference Reasoning remain unchanged. The new contract also
fails the stable CGC schema, so it cannot masquerade as a valid stable CGC.
There is no routing/import from production into the compiler. Regression tests
compare the complete effective orchestration output before/after shadow analysis,
for observer on/off and ready/blocked cases, including a supplied shadow artifact
that production does not consume. Full unified regression passes; VSG-0.5 remains
13/13, VSG-1.5 remains 19/19, and R2b remains 91.0 with S3=0.

Evidence: [VSG-2A QA](../validation/VSG_2A_GENERATION_COMPILER_QA.json).
The prior Causal Trace QA hashes are refreshed against the final shared docs and
regression runner; its original 19-case expectations remain unchanged.

No production VSG compiler, pixel extractor, regeneration, self-correction or
Build Kit integration is introduced. A future production integration requires a
separate authorization and gate; VSG-2A does not enable it.
