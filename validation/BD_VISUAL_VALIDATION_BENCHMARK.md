# BD Visual Validation Benchmark · BD01 / BD02

**Visual validation: PENDING. Promotion decision: PENDING.**
**Benchmark cases defined: 10. Visual PASS: 0. Pending: 10.**
**Physical print validation: PENDING.**

## Mandatory visual acceptance rule

> No visual PASS may be inferred from technical, contract, matrix, regression, or hash validation. A generated output receives visual PASS only after that specific output has been inspected against the applicable BD01/BD02 visual acceptance criteria.

The previous inferred promotion is withdrawn. Technical implementation remains
validated, but that result does not close the visual gate. No independent
image-generation runs or inspected outputs are recorded for this matrix.

## Defined benchmark matrix

| Case | Reference class | Preset | Expected behavior | Visual status |
| --- | --- | --- | --- | --- |
| BDV-01 | Low-rise continuous street wall | BD01 | Controlled backdrop recomposition | PENDING |
| BDV-02 | Low-rise continuous street wall | BD02 | Layout and recognition preservation | PENDING |
| BDV-03 | Mixed urban skyline | BD01 | Skyline reinterpretation with continuity | PENDING |
| BDV-04 | Mixed urban skyline | BD02 | Skyline hierarchy preservation | PENDING |
| BDV-05 | Vacant lot + deep skyline | BD01 | Foreground suppression and recomposition | PENDING |
| BDV-06 | Vacant lot + deep skyline | BD02 | Foreground and layout preservation | PENDING |
| BDV-07 | Exposed construction / tower structures | BD01 | Controlled structural reinterpretation | PENDING |
| BDV-08 | Exposed construction / tower structures | BD02 | Structural recognition preservation | PENDING |
| BDV-09 | Institutional architecture + skyline | BD01 | Backdrop-oriented recomposition | PENDING |
| BDV-10 | Institutional architecture + skyline | BD02 | Landmark and layout preservation | PENDING |

Each row is a defined benchmark case, not an executed or passed visual test.
[Machine-readable matrix](BD_VISUAL_VALIDATION_BENCHMARK.json).

## Technical evidence, separate from visual evidence

The [technical baseline](BACKDROP_PRESETS_QA.json) records 15/15 preset tests,
20 regression checks, 40 unchanged legacy outputs, R2b 91 and S3=0.
These establish implementation/contract properties only. They do not establish
visual framing, architectural fidelity, narrative suppression or print quality.

## Required inspection

For each case, retain the reference, generation request, specific generated
output and an inspection record identifying that output and recording the
applicable acceptance criteria and findings. An output can receive visual PASS
only after that inspection. A different output does not inherit the result.

Shared criteria: panoramic framing, frontal/elevational stability, architectural
priority, subordinate foreground, reduced narrative clutter and backdrop continuity.
BD01 additionally requires recognizable source urban character and controlled
recomposition within unprotected regions. BD02 requires recognizable source
layout, preserved skyline/landmark hierarchy and no major redesign.
See [BD01/BD02 acceptance criteria](../command_invocation/BACKDROP_PRESETS.md).
Missing inspection evidence leaves the case PENDING. Inspection failures must
be recorded as failures, never replaced by a technical or inferred PASS.
Physical print validation remains a separate pending gate.

The preset catalog, package manifest and per-output CGC contracts retain visual
status PENDING. Generation behavior, readiness and source locks are unchanged.
