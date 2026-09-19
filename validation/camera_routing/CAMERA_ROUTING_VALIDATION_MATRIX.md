# Camera Routing Validation Matrix — CRVM 1.0

## Objective
Validate the formal Camera Grammar and routing patch before any further Canon modification.

This matrix tests four distinct questions:

1. **Camera-family selection:** CG-A vs CG-B.
2. **Source-preservation precedence:** CG-S vs profile preference.
3. **Fear City identity routing:** VP03 / CG-FC vs VP00/VP01/VP02.
4. **Preservation side-effects:** camera/profile defaults must not silently remove source evidence.

## Validation levels

### L0 — Structural routing
Deterministic specification-consistency test. No image generation is involved.

### L1 — Camera-family visual recognition
Use existing Streetcraft packaged references to verify that CG-A and CG-B are visually distinguishable and that strict frontal views remain legal.

### L2 — Transformation validation
Run controlled source→output tests under VP00 / VP01 / VP02 and score camera behavior against the selected family.

### L3 — Fear City routing validation
Use confirmed Fear City multi-view source material and verify automatic T06 + VP03 + CG-FC routing, plus explicit-override behavior.

## Acceptance thresholds

- L0: **100%** required.
- L1: ≥90% unambiguous family agreement; ambiguous cases become boundary fixtures rather than failures.
- L2: ≥85% camera-family compliance and **100% Source Identity Preservation on critical relationships**.
- L3: **100% correct Fear City routing** on confirmed inputs; **0 false-positive Fear City routes** on resemblance-only inputs.

## Structural cases

| ID | Group | Scenario | Expected |
|---|---|---|---|
| CR-01 | SOURCE_LOCK | Historical photo, no explicit profile, ordinary source camera. | mode=T01, profile=VP00, camera=CG-S, fear_city_identity=NOT_APPLICABLE |
| CR-02 | SOURCE_LOCK | Historical photo already naturally conforms to CG-A, VP02 requested under T01. | mode=T01, profile=VP02, camera=CG-A/CG-S, fear_city_identity=NOT_APPLICABLE |
| CR-03 | SOURCE_LOCK | Historical photo already naturally conforms to CG-B, VP02 requested under T01. | mode=T01, profile=VP02, camera=CG-B/CG-S, fear_city_identity=NOT_APPLICABLE |
| CR-04 | SOURCE_LOCK | Elevated historical source, VP02, T01. | mode=T01, profile=VP02, camera=CG-S, fear_city_identity=NOT_APPLICABLE |
| CR-05 | SOURCE_LOCK | Historical source with camera transformation explicitly authorized toward a facade-oriented result. | mode=T08, profile=VP02, camera=CG-A, fear_city_identity=NOT_APPLICABLE |
| CR-06 | SOURCE_LOCK | Corner historical source with camera transformation explicitly authorized. | mode=T08, profile=VP01, camera=CG-B, fear_city_identity=NOT_APPLICABLE |
| CR-07 | PROFILE_CAMERA | VP00 generative/reconstructive frontal-oblique architecture. | mode=T07, profile=VP00, camera=CG-A, fear_city_identity=NOT_APPLICABLE |
| CR-08 | PROFILE_CAMERA | VP00 generative/reconstructive corner architecture. | mode=T07, profile=VP00, camera=CG-B, fear_city_identity=NOT_APPLICABLE |
| CR-09 | PROFILE_CAMERA | VP01 frontal-oblique mid-century facade. | mode=T07, profile=VP01, camera=CG-A, fear_city_identity=NOT_APPLICABLE |
| CR-10 | PROFILE_CAMERA | VP01 corner / industrial block. | mode=T07, profile=VP01, camera=CG-B, fear_city_identity=NOT_APPLICABLE |
| CR-11 | PROFILE_CAMERA | VP02 strict frontal facade. | mode=T07, profile=VP02, camera=CG-A, fear_city_identity=NOT_APPLICABLE |
| CR-12 | PROFILE_CAMERA | VP02 street-level corner with meaningful side depth. | mode=T07, profile=VP02, camera=CG-B, fear_city_identity=NOT_APPLICABLE |
| CR-13 | FEAR_CITY_ROUTING | Fear City explicitly identified, no mode/profile specified. | mode=T06, profile=VP03, camera=CG-FC, fear_city_identity=CONFIRMED |
| CR-14 | FEAR_CITY_ROUTING | Confirmed Fear City source; user merely names VP02/RDR 2.0, with no explicit routing override. | mode=T06, profile=VP03, camera=CG-FC, fear_city_identity=CONFIRMED |
| CR-15 | FEAR_CITY_ROUTING | Confirmed Fear City source; VP01 named without explicit routing override. | mode=T06, profile=VP03, camera=CG-FC, fear_city_identity=CONFIRMED |
| CR-16 | FEAR_CITY_ROUTING | Confirmed Fear City source with explicit profile-routing override to VP02, Mode not overridden. | mode=T06, profile=VP02, camera=CG-FC/CG-S, fear_city_identity=CONFIRMED |
| CR-17 | FEAR_CITY_ROUTING | Miniature/diorama source; Fear City identity uncertain, no profile specified. | mode=T01, profile=VP00, camera=CG-S, fear_city_identity=UNRESOLVED |
| CR-18 | FEAR_CITY_ROUTING | Miniature/diorama source; Fear City identity uncertain, VP01 explicitly selected. | mode=T01, profile=VP01, camera=CG-S, fear_city_identity=UNRESOLVED |
| CR-19 | PRESERVATION | T01 + VP02 source contains people and vehicles. | mode=T01, profile=VP02, camera=CG-A/CG-S, fear_city_identity=NOT_APPLICABLE |
| CR-20 | PRESERVATION | Generative VP02 task with no source people/vehicles. | mode=T07, profile=VP02, camera=CG-A, fear_city_identity=NOT_APPLICABLE |
| CR-21 | PRESERVATION | T03 Clean Plate on historical source; camera not authorized to change. | mode=T03, profile=VP00, camera=CG-S/CG-B, fear_city_identity=NOT_APPLICABLE |
| CR-22 | PRESERVATION | T05 Atmosphere Transfer on historical source; spatial identity must remain. | mode=T05, profile=VP01, camera=CG-S/CG-A, fear_city_identity=NOT_APPLICABLE |
| CR-23 | BOUNDARY | Real-world photo visually resembles Fear City but has no Fear City authorship. | mode=T01, profile=VP00, camera=CG-S, fear_city_identity=NOT_APPLICABLE |
| CR-24 | BOUNDARY | Unknown miniature strongly resembles New York / Fear City. | mode=T01, profile=VP00, camera=CG-S, fear_city_identity=UNRESOLVED |
| CR-25 | BOUNDARY | VP02 corner geometry with deep side plane but no wide-angle spectacle requirement. | mode=T07, profile=VP02, camera=CG-B, fear_city_identity=NOT_APPLICABLE |
| CR-26 | BOUNDARY | VP02 source with naturally strict frontal one-point camera. | mode=T01, profile=VP02, camera=CG-A/CG-S, fear_city_identity=NOT_APPLICABLE |

## Core boundary tests

### CG-A ↔ CG-B
The deciding factor is not whether the image is aesthetically dramatic. The decision is architectural geometry:
- CG-A: frontal-oblique, near-elevation, dominant facade plane.
- CG-B: street-level oblique, meaningful side depth/corner geometry, principally two-point.

### CG-S ↔ profile preference
Source preservation wins whenever camera transformation is not authorized. A profile may describe a preferred camera without gaining permission to redesign the source camera.

### Real photo ↔ Fear City
Fear City routing requires authored-world identity. New York resemblance, grime, elevated rail, graffiti, period atmosphere or model-like appearance are insufficient by themselves.

## Visual fixture plan

The packaged reference assets are reused only as validation fixtures within their existing authority. The matrix does **not** promote or reclassify any Canon item.

Fear City Validation Set #001 is documented by `fear_city/VALIDATION_001.md` but its three source images are not embedded in this package. Therefore L3 visual execution remains pending until those confirmed views are explicitly available in the active validation environment.

## Decision gate
No additional Canon changes should be made until:
1. L0 passes completely.
2. L1 boundary fixtures are reviewed.
3. At least one controlled L2 test exists for each VP00/VP01/VP02 × CG-A/CG-B combination.
4. L3 validates confirmed Fear City routing and resemblance-only negative controls.
