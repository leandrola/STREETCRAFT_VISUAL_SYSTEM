# STREETCRAFT ROADMAP · CURRENT

## Current release line

### CIL 1.1 · RDR2 Elevation Recovery
Status: RECOVERED / INTEGRATED

Recovered before continuing R2b:
- `/sc-rdr2-elevation` → `VP02 + T02 + CG-F`
- Identity Lock
- Occlusion Lock
- strict frontalization
- 16:9
- minimal street
- `/sc-front`
- aliases `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`

Because CG-F changes camera behavior, R2b now includes a sixth required CG-F elevation regression case.

### SVS 1.9.1 · Scene Intelligence Critical Patch
Status: CANDIDATE
Implementation: complete
Deterministic QA: complete
Remaining release gate: fresh R2b visual candidate regression

### R2b 1.9.1 · Fresh Critical Run
Status: NEXT / PREPARED

Required blocks:
1. VP02 CG-A
2. VP02 CG-B
3. Fear City / Reference Isolation
4. Semantic Text Lock
5. Occlusion Lock
6. VP02 CG-F / Elevation

Exit criteria:
- six valid fresh outputs;
- no labels/dashboards in generated candidates;
- S3 = 0;
- global weighted score >= 90;
- independent evaluation against source + 1.8.1 baseline.

### SVS 1.9.1 → Stable
Status: BLOCKED BY R2b

Promotion occurs only after R2b exit criteria are satisfied.

## Next intelligence milestone

### SVS 1.10 · Reference Reasoning 2.0
Status: NOT STARTED
Starts only after 1.9.1 Stable.

Scope:
- contextual Reference Need dependency graph;
- smarter RN_NONE / RN_SUPPORT / RN_REQUIRED / RN_BLOCKED decisions;
- domain-scoped query routing;
- evidence saturation / budget optimization;
- contradiction handling;
- cross-domain contamination firewall;
- explicit no-reference rationale;
- traceability from admitted Evidence Unit to generation decision;
- similarity never creates authority.

## Runtime milestone

### SVS 2.0 · Agent Runtime
Status: PLANNED

Sequence:
`Analyze → Route → Scene Intelligence → CGC → Reference Reasoning 2.0 → Archive → Generate → Critic → Correct → Benchmark`

Goals:
- deterministic orchestration;
- state-machine/checkpoint execution;
- safe halts on contradiction or unresolved required evidence;
- retry/replan rules;
- complete run manifest and audit trail.

## Production / image-output milestone

### Image Export Runtime
Status: DEFINED / NOT IMPLEMENTED

Purpose:
Convert an approved Streetcraft image into print-ready raster outputs without changing visual authorship.

Approved formats:
- A4 landscape: 297 × 210 mm, 150 or 300 dpi
- A3 landscape: 420 × 297 mm, 150 or 300 dpi
- 90 × 45 cm landscape: 150 dpi ONLY

Target pixels:
- A4 150: 1754 × 1240
- A4 300: 3508 × 2480
- A3 150: 2480 × 1754
- A3 300: 4961 × 3508
- 90 × 45 cm 150: 5315 × 2657

Explicit exclusion:
- 90 × 45 cm at 300 dpi

Planned controls:
- aspect-ratio policy;
- crop/pad policy;
- effective DPI calculation;
- resampling vs upscale declaration;
- post-upscale identity/text/geometry regression check;
- embedded print metadata.

## Current recommended order

1. Finish R2b 1.9.1
2. Promote 1.9.1 Stable
3. SVS 1.10 Reference Reasoning 2.0
4. SVS 2.0 Agent Runtime
5. Image Export Runtime

Image Export Runtime is already specification-frozen enough to prototype earlier if needed, but it does not block 1.9.1 Stable.
