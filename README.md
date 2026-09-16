# Streetcraft Visual System (SVS) 1.9.0

SVS 1.9 introduces **Scene Intelligence**.

Streetcraft now represents a source explicitly as:
- entities
- scene roles
- protected relationships
- preservation authority
- salience
- entity-level actions
- unknown locks
- scoped Reference Need hints

The objective is to improve decisions before generation, not to add another visual style.

## New runtime layer
`SOURCE → SAR2 Scene Intelligence → CGC → Archive-Aware Runtime → Generation → Critic`

## Release status
Implementation and automated regression are complete.

Because Scene Intelligence changes pre-generation behavior, the SVS 1.8 benchmark policy requires a fresh R2b visual candidate regression before 1.9 can be promoted to fully stable.
