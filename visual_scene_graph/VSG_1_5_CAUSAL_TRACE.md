# VSG-1.5 · Causal Trace

VSG-1.5 reconstructs the first incorrect transition across **supplied structured snapshots**. It is diagnostic: `mode=TRACE_ONLY`, `governs_generation=false`. It does not call a generator, modify CGC, change `generation_ready`, affect preflight, alter adapter input, rewrite RR2 or repair Graph Locks. The stable orchestration entrypoint is unchanged; Causal Trace is an explicitly called API, not another client.

## API and artifacts

```python
from visual_scene_graph.causal_trace import (
    build_causal_trace, validate_causal_trace, render_causal_trace,
)
trace = build_causal_trace(
    expected_graph=expected_graph,
    sar2=sar2,
    reference_reasoning=reference_reasoning,
    vsg=vsg,
    graph_lock_validation=graph_lock_validation,
    shadow_contract=shadow_contract,
    observed_output_graph=observed_output_graph,
    diagnosis=diagnosis,
)
validation = validate_causal_trace(trace, artifacts)
print(render_causal_trace(trace))
```

`artifacts` is a dictionary with those same eight named inputs. Pass `None` for a missing snapshot. Missing required fields, ambiguous identities, mismatched scene IDs or diagnostic reports that do not match the supplied snapshots yield `INCOMPLETE`, explicit `unresolved_inputs`, and no asserted root cause. Available snapshots still retain provenance. An empty list inside a supplied stage is an observed absence; an unavailable stage is not replaced with an empty list.

The expected graph is the structured source-evidence expectation. It is **not** evidence that this module inspected image pixels. SAR2 uses its existing entity/relationship IDs; RR2 retains need IDs, Evidence Unit IDs and bundle IDs. VSG and expected locks keep their existing IDs.

The VSG-0.5 shadow snapshot supplies `required_nodes`, `required_edges`, `semantic_text` and, for tracing lock projection, `required_locks`. The controlled corpus exposes those explicit diagnostic requirements through the existing benchmark builder. Observed snapshots provide nodes, edges and reference observations. Neither snapshot is a VSG-2 compiler or VSG-3 image extractor.

Generate the two diagnostic input reports using [diagnostic_engine.py](diagnostic_benchmark/diagnostic_engine.py): `check_causal_graph_locks(**snapshots)` and `diagnose_causal_snapshots(**snapshots)`, where `snapshots` contains the six non-report inputs. Both reports bind themselves to those six input hashes. The trace rechecks their agreement rather than trusting a supplied stage label.

## Causal model

```text
SOURCE_EVIDENCE → SAR2 → VSG → GRAPH_LOCKS → SHADOW_COMPILER → OBSERVED_OUTPUT
        └──────→ RR2 ────┘                                       ↓
                                                              DIAGNOSTIC
```

Events carry typed stages, operations, presence/change/admission status, existing artifact IDs, evidence references and confidence. Stable event IDs derive from scene, stage, kind and artifact identity. Directed edges describe production, projection, locking, requirements, observation and causal findings. Edges also depend on their endpoint entities.

References use `artifact-name#JSON-pointer`, for example `sar2#/entities/3`. An absent element references its existing collection, together with the missing `artifact_id`; no pointer is invented for an object that does not exist. Source/evidence references point to supplied objects, including RR2 trace records containing the original bundle IDs. Raw bundle contents or image regions that were not supplied are not fabricated.

The benchmark remains the attribution authority. The original VSG-0.5 `diagnose_pipeline` behavior and all 13 cases are retained. Its origins map to trace stages:

| Benchmark origin | Trace stage |
| --- | --- |
| PERCEPTION | SAR2 |
| REFERENCE_REASONING | RR2 |
| GRAPH_PROJECTION | VSG |
| COMPILER | SHADOW_COMPILER |
| GENERATION | OBSERVED_OUTPUT |

The diagnostic extension reuses the observer and Graph Lock validator to inspect lock violations at supplied stages, expected-versus-actual ledger entries and shadow lock requirements. Within a stage, existing benchmark findings take precedence; matching lock findings annotate them with exact `lock_id` values. A lost ledger entry is attributed to `GRAPH_LOCKS`; a lost shadow lock requirement to `SHADOW_COMPILER`.

There is one deterministic primary root cause: the earliest incorrect stage, with the benchmark's stable ordering for ties. Reachable downstream findings are `symptoms`; unrelated findings remain `independent_findings`, not asserted consequences of that root. Every root and finding includes an explicit source-to-finding `causal_path`. This is structured dependency attribution, not a proof of physical causation beyond the supplied snapshots.

## Examples from the controlled corpus

| Observation | First incorrect transition | Evidence |
| --- | --- | --- |
| HVAC absent after SAR2 omitted it | SAR2 / `PERCEPTION_NODE_MISSING` | Expected `hvac_01`, absence in SAR2, downstream output absence as a symptom |
| `BEHIND` requirement lost in the shadow contract | SHADOW_COMPILER / `COMPILER_RELATION_OMISSION` | `rel_hvac_behind` exists upstream, absent from required edges |
| Kenny's text changed only in observed output | OBSERVED_OUTPUT / `OUTPUT_SEMANTIC_MUTATION` | `sign_01`, `GL-SEM-SIGN_01`, original text and contract requirement |
| Semantic lock removed from the ledger | GRAPH_LOCKS / `GRAPH_LOCK_MISSING` | Expected `GL-SEM-SIGN_01`, missing ledger item |

## Validation and deterministic hashes

[The schema](../schemas/vsg-causal-trace.schema.json) defines the public trace shape. `validate_causal_trace` checks event uniqueness, resolvable pointers and event references, stage ordering, acyclicity, primary-root rules and hash validity. It also deterministically replays the benchmark and trace construction against the artifacts. A forged later root, omitted symptom, altered lock ID, reordered causal content or stale provenance fails replay even if an attacker recomputes the outer hash.

Canonical hashing uses UTF-8 JSON with sorted keys, compact separators, literal Unicode and finite numbers. `trace_sha256` excludes **only** its own field. Provenance hashes each supplied artifact separately. Confidence `1.0` means an exact structured comparison, not certainty about pixel evidence or the completeness of the source interpretation.

```sh
python visual_scene_graph/test_causal_trace.py
python -m visual_scene_graph.run_causal_benchmark --output /tmp/vsg-causal-qa.json
python -m visual_scene_graph.run_causal_benchmark --verify validation/VSG_1_5_CAUSAL_TRACE_QA.json
```

The corpus reuses all 13 VSG-0.5 cases, plus Semantic Text, Geometry, Occlusion and Reference Isolation violations, a missing ledger lock and a missing shadow lock requirement: **19 cases**. [QA evidence](../validation/VSG_1_5_CAUSAL_TRACE_QA.json) includes snapshots, full traces, expected roots, validation results and hashes of the final implementation/metadata files. The QA file does not hash itself. Replay checks nested artifact/trace hashes and all listed file hashes.

Milestone: **COMPLETED AND VALIDATED**. Next: **VSG-2A Generation Compiler Shadow**. No production compiler, automatic regeneration, real-image Graph Delta, self-correction loop or Build Kit integration is implemented here.
