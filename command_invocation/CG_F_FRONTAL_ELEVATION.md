# CG-F · Frontal Elevation Camera

Status: CIL 1.1 camera contract.

CG-F is the strict frontal-elevation camera selected by `/sc-rdr2-elevation` and available as a camera override through `/sc-front`.

## Contract
- frontalization: `STRICT`
- architectural identity remains locked; frontalization may not redesign facade proportions, bays, openings, roofline or signage relationships
- camera target is a frontal visual elevation rather than CG-A frontal-oblique immersion or CG-B street-level obliquity
- verticals remain controlled and the facade plane is dominant
- default output aspect ratio for the full elevation macro is `16:9`
- street presence for the full elevation macro is `MINIMAL`
- no aerial or elevated overview
- no geographic, architectural or semantic invention is authorized by frontalization

## Locks
The full `/sc-rdr2-elevation` macro activates:
- `identity_lock = STRICT`
- `occlusion_lock = LOCKED_UNKNOWN`

Identity Lock protects source-defining architectural geometry and relationships during frontalization.
Occlusion Lock means hidden content stays unresolved unless independent evidence authorizes constrained reconstruction.

## Scope of `/sc-front`
`/sc-front` is a camera modifier. It sets `CG-F + STRICT frontalization` but does not by itself change profile, Transformation Mode, aspect ratio, street presence or safety locks.

## Authority
CG-F does not weaken source authority. If exact frontalization cannot be achieved without inventing hidden geometry, Streetcraft must preserve uncertainty rather than fabricate a complete elevation.
