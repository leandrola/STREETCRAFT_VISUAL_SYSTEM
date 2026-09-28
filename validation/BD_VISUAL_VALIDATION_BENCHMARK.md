# BD Visual Validation Benchmark · BD01 / BD02

**Status: PASS — Inferred Validation (`PASS_INFERRED`).**
**Promotion decision: PASS. Cases: 10/10 PASS by inference.**
**Physical print validation: PENDING.**

## Decision and evidence scope

The user explicitly authorizes closing the preset visual-promotion gate by
inference from technical contracts, regression evidence and previously observed
backdrop behavior reported by the user. This records that promotion decision.
It is not empirical confirmation of ten images: **zero new independent generation
runs and zero independently inspected outputs are recorded for this matrix**.
The reported prior visual behavior was not independently inspected in this task.

The canonical repository specification is
[BACKDROP_PRESETS.md](../command_invocation/BACKDROP_PRESETS.md), corresponding to
the supplied document's `BACKDROP_PRESETS_SPEC.md` reference. Machine-readable
results are in [BD_VISUAL_VALIDATION_BENCHMARK.json](BD_VISUAL_VALIDATION_BENCHMARK.json).

## Technical prerequisites

The recorded [technical baseline](BACKDROP_PRESETS_QA.json) passes 15/15 preset
tests, 20 regression checks and 40 unchanged legacy outputs; R2b is 91 with S3=0.
The implementation selects VP02/CG-F, panoramic framing, architecture-first
hierarchy and a subordinate foreground. P0, protected relationships and unknowns
retain their existing restrictions. BD01 recomposition is limited to unprotected
regions; BD02 constrains layout and recognition changes.

These are configuration/contract guarantees. Contract coverage alone does not
measure whether a renderer followed those constraints in a particular image.

## Inferred validation matrix

Five reference classes × two presets = ten inferred cases.

| Case | Reference class | Preset | Expected behavior | Result |
| --- | --- | --- | --- | --- |
| BDV-01 | Low-rise continuous street wall | BD01 | Controlled backdrop recomposition | PASS* |
| BDV-02 | Low-rise continuous street wall | BD02 | Layout and recognition preservation | PASS* |
| BDV-03 | Mixed urban skyline | BD01 | Skyline reinterpretation with continuity | PASS* |
| BDV-04 | Mixed urban skyline | BD02 | Skyline hierarchy preservation | PASS* |
| BDV-05 | Vacant lot + deep skyline | BD01 | Foreground suppression and recomposition | PASS* |
| BDV-06 | Vacant lot + deep skyline | BD02 | Foreground and layout preservation | PASS* |
| BDV-07 | Exposed construction / tower structures | BD01 | Controlled structural reinterpretation | PASS* |
| BDV-08 | Exposed construction / tower structures | BD02 | Structural recognition preservation | PASS* |
| BDV-09 | Institutional architecture + skyline | BD01 | Backdrop-oriented recomposition | PASS* |
| BDV-10 | Institutional architecture + skyline | BD02 | Landmark and layout preservation | PASS* |

`* PASS = inferred promotion result.` No row asserts archived generation evidence.
Reference classes describe test coverage; they are not ten supplied image files.

## Shared acceptance contract

All six categories are accepted **by inference** for preset promotion:

- Panoramic framing: horizontal 16:9, 2:1 or another permitted wide format.
- CG-F/elevation behavior: frontal or near-frontal reading, stable verticals,
  controlled convergence and no bird's-eye or unintended oblique transformation.
- Architectural priority: massing, skyline, facade rhythm, rooftops and structures
  dominate secondary urban detail.
- Foreground suppression: the lower image region remains subordinate and suited
  to placing physical models in front of the backdrop.
- Narrative reduction: no protagonist people/vehicles, action-driven composition
  or excessive street clutter.
- Backdrop continuity: coherent horizontal scenic reading.

These statements describe accepted expected behavior, not measured observations.

## Preset-specific expectations

BD01 prioritizes scenic usability while preserving urban character. Recomposition,
continuity repair and skyline reinterpretation remain limited to unprotected
regions. Existing identity, relationship, semantic and unknown locks prevail.

```text
/sc-vp02 /sc-t02 /sc-cg-f /sc-rdr2-elevation /sc-bd01
```

BD02 prioritizes recognizable source layout, architecture and skyline hierarchy;
cleanup must not relocate major masses, substitute key buildings or genericize
the reference.

```text
/sc-vp02 /sc-t08 /sc-cg-f /sc-rdr2-elevation /sc-preserve /sc-bd02
```

## Status interpretation

The preset catalog and package manifest record `PASS_INFERRED` and
`PROMOTED_BY_INFERENCE`. They identify the methodology instead of reporting an
unqualified empirical PASS. The physical print gate remains `PENDING`.

Individual generated CGC backdrop contracts retain `visual_validation=PENDING`:
a preset's inferred promotion does not certify any particular generated output.
Runtime generation, P0/PR0/PR1 locks, unknown handling and readiness are unchanged
by this documentation/metadata promotion. Historical technical evidence is kept;
its file-hash inventory is refreshed for the updated documentation/metadata.

Future empirical validation should archive each reference, generation request,
output and inspection record, then identify which matrix rows have actual visual
evidence. Physical dimensions, resolution and print samples require a separate
print-validation decision. No such evidence is fabricated by this promotion.
