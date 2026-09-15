# Streetcraft Command Invocation Layer (CIL) 1.0

CIL is the short human-facing invocation layer for Streetcraft.

Commands apply to the **current request only**. There is no hidden persistent configuration in CIL 1.0.

## Primary commands

| Command | Expansion |
|---|---|
| `/sc-core` | VP00 + T01 + camera AUTO |
| `/sc-classic` | VP01 + T01 + camera AUTO |
| `/sc-2` | VP02 + T01 + camera AUTO |
| `/sc-2a` | VP02 + T01 + CG-A |
| `/sc-2b` | VP02 + T01 + CG-B |
| `/sc-fear` | T06 + VP03 + CG-FC |
| `/sc-fear2` | T06 + VP02 explicit Fear City override |

## Modifiers

| Command | Effect |
|---|---|
| `/sc-clean` | T03 Clean Plate |
| `/sc-lock` | CG-S source-lock |
| `/sc-auto` | automatic camera resolution |
| `/sc-preserve` | strict observed-evidence preservation |
| `/sc-noinvent` | strict uncertainty preservation |

## Diagnostics
- `/sc-status` reports the resolved configuration before generation.
- `/sc-help` shows this command vocabulary.

## Examples

`/sc-2`

`/sc-2b`

`/sc-2 /sc-clean`

`/sc-core /sc-lock /sc-preserve /sc-noinvent`

`/sc-fear`

`/sc-fear2`

## Conflict rules

Multiple ordinary profile macros are invalid:
`/sc-core /sc-2`

Fear City plus an ordinary profile macro is also invalid:
`/sc-fear /sc-2`

Use `/sc-fear2` for the explicit VP02 override.

Modifiers override macro defaults but do not override hard source-authority constraints. A requested CG-A/CG-B may still resolve to CG-S when Source Identity Preservation requires it.

## Precedence

1. Source identity and hard preservation invariants
2. Explicit natural-language user override
3. Fear City identity/routing constraints
4. Mode modifier
5. Profile macro
6. Camera modifier
7. Safety modifiers
8. Streetcraft defaults

CIL is a Streetcraft convention, not a native ChatGPT slash-command feature. A compatible Streetcraft agent or wrapper interprets it.
