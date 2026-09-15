# R2 Visual Baseline Calibration — SVS 1.8.1

## Decision

`BASELINE_CALIBRATED`

The first R2 milestone establishes the visual baseline without pretending that existing golden images are newly generated candidate outputs.

## Two distinct operations

### R2a · Baseline Calibration
Used once to define stable visual expectations from already validated evidence.

It records:
- fixture identity
- SHA-256
- perceptual dHash
- dimensions/aspect ratio
- visible identity anchors
- critical invariants

R2a is complete in SVS 1.8.1.

### R2b · Candidate Regression Run
Used for future releases that change generation/runtime behavior.

R2b requires:
1. generation by the candidate runtime;
2. output SHA-256;
3. side-by-side inspection against source/golden baseline;
4. independent scoring using the R2 rubric;
5. PASS / REVIEW / FAIL decision.

## Why the distinction matters

A benchmark framework release must establish its baseline before it can compare later candidates.

Calling the existing golden fixture a newly generated PASS would be circular self-certification. SVS explicitly forbids that.

## Baseline coverage

R2a includes:
- VP00 CG-A / CG-B pair
- VP01 CG-A / CG-B pair
- VP02 CG-A / CG-B pair
- Fear City Validation Set #001
- Economy Candy hardening fixture
- Fear City reference-isolation source baseline
- eight stable visual identity fixtures

Future behavior-changing releases must execute R2b.
