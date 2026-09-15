# Streetcraft Visual System 1.6.3 — Cheat Sheet

This file is the fast operational guide for everyday Streetcraft use.

Use **one profile command** plus optional modifiers.

## Quick start

If you do not know what to use, start with:

`/sc-2`

That invokes:
- **VP02**
- **T01**
- **Camera Auto**

## Core commands

| Command | Meaning | Typical use |
|---|---|---|
| `/sc-core` | VP00 + T01 + Camera Auto | faithful Streetcraft Core |
| `/sc-classic` | VP01 + T01 + Camera Auto | RDR Classic |
| `/sc-2` | VP02 + T01 + Camera Auto | everyday RDR 2.0 |
| `/sc-2a` | VP02 + T01 + CG-A | facade-dominant architectural view |
| `/sc-2b` | VP02 + T01 + CG-B | oblique street-level / corner view |
| `/sc-fear` | T06 + VP03 + CG-FC | confirmed Fear City |
| `/sc-fear2` | T06 + VP02 override for Fear City | Fear City with explicit RDR 2.0 override |

## Modifiers

| Command | Effect |
|---|---|
| `/sc-clean` | switches to T03 Clean Plate |
| `/sc-lock` | forces CG-S source-locked camera |
| `/sc-auto` | restores automatic camera choice |
| `/sc-preserve` | stronger source preservation |
| `/sc-noinvent` | preserve ambiguity, illegibility and unknown geometry |
| `/sc-status` | show resolved configuration before generation |
| `/sc-help` | show command reference |

## Best default combinations

### Standard use
`/sc-2`

### Standard use with extra caution
`/sc-2 /sc-preserve /sc-noinvent`

### Documentary / maximum fidelity
`/sc-core /sc-lock /sc-preserve /sc-noinvent`

### Facade-dominant scene
`/sc-2a`

### Corner / side-plane / stronger street depth
`/sc-2b`

### Clean plate
`/sc-2 /sc-clean`

### Clean plate with strict discipline
`/sc-2 /sc-clean /sc-preserve /sc-noinvent`

### Fear City
`/sc-fear`

### Fear City with explicit VP02 override
`/sc-fear2`

## How to choose CG-A vs CG-B

### Use `/sc-2a` when:
- the facade should dominate
- you want a near-elevation / frontal-oblique reading
- side depth should remain controlled
- the building is the protagonist

### Use `/sc-2b` when:
- the corner matters
- the side plane matters
- you want stronger street-level monumentality
- the scene should feel more spatially immersive

## Decision shortcuts

If unsure:
- start with `/sc-2`

If the image is delicate or documentary:
- use `/sc-core /sc-lock /sc-preserve /sc-noinvent`

If the scene is a corner:
- use `/sc-2b`

If the scene is a facade:
- use `/sc-2a`

If the source is Fear City:
- use `/sc-fear`

## Things to avoid

These are invalid or poor combinations:

- `/sc-core /sc-2`
- `/sc-classic /sc-2`
- `/sc-2a /sc-2b`
- `/sc-fear /sc-2`

Use `/sc-fear2` instead of mixing Fear City with `/sc-2`.

## Minimal examples

`/sc-2`

`/sc-2b /sc-preserve /sc-noinvent`

`/sc-core /sc-lock /sc-preserve /sc-noinvent`

`/sc-2 /sc-clean /sc-preserve /sc-noinvent`

`/sc-fear`

`/sc-fear2 /sc-status`

## Mental model

Streetcraft resolves requests approximately in this order:

1. source identity
2. user intent
3. mode
4. profile
5. camera
6. preservation / uncertainty modifiers

The commands are only a short invocation layer. They do not replace the Streetcraft system underneath.

## Recommended files to read if needed
- `STREETCRAFT.md`
- `command_invocation/COMMAND_INVOCATION_LAYER.md`
- `transform/AUTO_ROUTING.md`
- `transform/FEAR_CITY_IDENTITY_THRESHOLD.md`


## Archive-aware behavior (SVS 1.7)

No new command is required.

`/sc-2`, `/sc-2a`, `/sc-2b`, `/sc-fear`, etc. still work normally.

When the source has a legitimate documentary evidence deficit, SVS 1.7 can automatically create a scoped Reference Need and consult Streetcraft Archive V1.

Archive retrieval never means “make it look like this reference.” It means “use eligible evidence only for the declared missing domain.”
