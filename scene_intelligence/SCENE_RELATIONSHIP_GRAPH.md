# Scene Relationship Graph (SRG) 1.0

Streetcraft models protected relationships explicitly because identity often lives between objects rather than inside one object.

## Relationship vocabulary

- `ATTACHED_TO`
- `SUPPORTED_BY`
- `ABOVE`
- `BELOW`
- `ADJACENT_TO`
- `ALIGNED_WITH`
- `CONTINUES_INTO`
- `BOUNDS`
- `APPLIED_TO`
- `OCCLUDES`
- `COVERS`
- `REPLACES`
- `PART_OF`
- `CONNECTED_TO`
- `FOLLOWS`
- `INTERSECTS`

## Relationship protection

- `PR0` absolute
- `PR1` strong
- `PR2` contextual
- `PRX` unprotected/diagnostic

A low-salience entity participating in a PR0 relationship cannot be casually removed if that would break the relationship.

## Examples

- fire escape `ATTACHED_TO` specific facade bays
- track `CONTINUES_INTO` Fear City underpass
- graffiti `APPLIED_TO` a specific brick wall
- Tanner Street sign `ATTACHED_TO` its pole
- sidewalk `FOLLOWS` building edge
- parked car `OCCLUDES` storefront base
