# STREETCRAFT.md
## Entry point for AI agents
Version: SVS 1.6.3

Streetcraft is a visual transformation specification.

## Primary objective
Interpret a supplied source while preserving its authored or documentary identity. Transform only what the task authorizes.

## Authority hierarchy
1. Explicit user intent
2. P0 source invariants
3. Transformation Mode
4. Visual Profile
5. Camera Grammar / Auto-Routing constraints
6. Streetcraft Core Visual Grammar
7. Period and regional constraints
8. Creative preferences

## Camera routing summary
- CG-A: frontal-oblique architectural immersion
- CG-B: street-level oblique monumentality
- CG-S: source-locked camera
- CG-FC: Fear City authored-view camera

Confirmed Fear City defaults to:
`T06 → VP03 → CG-FC`

## Command Invocation Layer
This release includes CIL 1.0 with:
`/sc-core`, `/sc-classic`, `/sc-2`, `/sc-2a`, `/sc-2b`, `/sc-fear`, `/sc-fear2`, `/sc-clean`, `/sc-lock`, `/sc-auto`, `/sc-preserve`, `/sc-noinvent`, `/sc-status`, `/sc-help`

See `command_invocation/COMMAND_INVOCATION_LAYER.md`.
