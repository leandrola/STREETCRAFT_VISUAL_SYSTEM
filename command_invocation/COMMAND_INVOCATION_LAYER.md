# Streetcraft Command Invocation Layer (CIL) 1.1

CIL is the short human-facing invocation layer for Streetcraft. Commands are turn-scoped and expand into valid Mode/Profile/Camera configuration. CIL never weakens source authority.

## Primary commands
`/sc-core`, `/sc-classic`, `/sc-2`, `/sc-2a`, `/sc-2b`, `/sc-rdr2-elevation`, `/sc-fear`, `/sc-fear2`.

## Camera / mode modifiers
`/sc-clean`, `/sc-lock`, `/sc-auto`, `/sc-front`.

## Safety modifiers
`/sc-preserve`, `/sc-noinvent`.

## Diagnostics
`/sc-status`, `/sc-help`.

## CIL 1.1 elevation macro
`/sc-rdr2-elevation` resolves to:

`VP02 + T02 + CG-F`

with:
- Identity Lock: `STRICT`
- Occlusion Lock: `LOCKED_UNKNOWN`
- frontalization: `STRICT`
- aspect ratio: `16:9`
- street presence: `MINIMAL`

Aliases: `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`.

`/sc-front` is a camera modifier selecting `CG-F` with strict frontalization while leaving the current Profile/Mode intact.

Multiple profile macros are invalid. Use `/sc-fear2` for explicit VP02-on-Fear-City override.

See `CG_F_FRONTAL_ELEVATION.md` for the operational camera contract.
