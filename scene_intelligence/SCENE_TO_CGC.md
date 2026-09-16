# Scene Intelligence → Compact Generation Contract

SAR2 enriches the CGC with `scene_intelligence`.

Example:

```json
{
  "scene_intelligence": {
    "entities": [],
    "protected_relationships": [],
    "entity_actions": [],
    "identity_anchors": [],
    "unknown_locks": [],
    "reference_need_hints": []
  }
}
```

## Projection rules

CGC `preserve` receives:
- P0 actions
- P1 identity anchors
- PR0/PR1 relationship constraints

CGC `remove` receives only `REMOVE_AUTHORIZED`.

CGC `infer` receives only `INFER_MINIMAL` zones with evidence.

CGC `unknown` receives `UNKNOWN_LOCKED`.

CGC `forbid` receives hard relationship, semantic, geographic and authorship prohibitions.

## Benefit

The generator receives precise entity-level instructions instead of broad prompts such as “preserve the architecture.”
