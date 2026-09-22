# VSG-0 · Observer

VSG-0 projects the existing SAR2 scene model into a deterministic, inspectable
graph. It is an observer only: it cannot alter RR2, CGC, preflight, adapters, or
the `generation_ready` decision.

Enable it per request:

```json
{
  "vsg": {
    "mode": "OBSERVER",
    "reference_id": "R2B-KENNYS",
    "reference_sha256": "<sha256>"
  }
}
```

The orchestration result then includes `visual_scene_graph`. With `vsg` absent
or `mode` set to `OFF`, the stable runtime output remains unchanged.

VSG-0 consumes SAR2 as its scene source and retains RR2 outcomes as passive
`reference_observations`. It does not redetect objects and does not query
Archive. Stable entity IDs become graph node IDs; supported SAR2 relationships
become explicit edges. Unsupported or dangling observations are reported under
`diagnostics` instead of being invented or silently promoted.

Four initial functional subgraphs are emitted: `semantic_text`, `rooftop`,
`geometry`, and `occlusion`. These circuits are diagnostic views over the same
graph, not separate sources of truth.

The first fixture is Kenny's Shop because it exercises facade identity,
Semantic Text Lock, a volumetric rooftop, separated rooftop pieces, and depth
relations in one compact case.

VSG-1 extends this observer output with `graph_locks`; VSG-0 remains the
historical non-governing foundation.
