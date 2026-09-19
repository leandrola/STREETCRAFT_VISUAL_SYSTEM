# Atmosphere / Material Carryover Guard (AMCG)

AMCG tightens MID for properties that are easy to smuggle in through references.

Source states may be explicitly declared, for example:
- `surface_wetness = DRY`
- `haze = ABSENT`
- `smoke = ABSENT`
- `night = FALSE`

A reference cannot flip these states unless the active transformation explicitly authorizes it.

For Fear City T06, material translation is allowed; atmosphere import is not automatically allowed.

Example: translating miniature brick roughness into plausible full-scale brick is allowed. Turning a dry authored street into cinematic wet asphalt is not.
