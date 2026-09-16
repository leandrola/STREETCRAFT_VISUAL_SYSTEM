# Scene Action Resolver (SAR) 1.0

The Scene Action Resolver converts scene understanding into entity-level generation instructions.

## Actions

- `PRESERVE_EXACT`
- `PRESERVE_RELATIONSHIP`
- `PRESERVE_CHARACTER`
- `PRESERVE_CONTEXT`
- `TRANSFORM_SCOPED`
- `REMOVE_AUTHORIZED`
- `INFER_MINIMAL`
- `UNKNOWN_LOCKED`
- `FORBID_CHANGE`

## Resolution principles

### P0
Default: `PRESERVE_EXACT`.

### P1
Default: `PRESERVE_CHARACTER`.

### P2
Default: `PRESERVE_CONTEXT`.

### P3
Default: `TRANSFORM_SCOPED`.

### P4
`REMOVE_AUTHORIZED` only when the active task/mode actually authorizes removal.

### P5
- P5-A/P5-B may allow `INFER_MINIMAL` when evidence supports continuity/structure.
- P5-C remains conservative.
- P5-D becomes `UNKNOWN_LOCKED`.

## Mode rules

### T01
Observed people, vehicles and props remain source evidence even if a profile normally prefers their absence.

### T03
Authorized foreground removals may occur, but the revealed region receives only minimum evidence-compatible reconstruction.

### T06
Fear City authored geometry and protected relationships outrank aesthetic cleanup.

## Relationship escalation

An entity participating in PR0/PR1 can receive a relationship lock even when its own preservation level is lower.

Removal cannot silently break a protected relationship.
