# Scene Entity Model (SEM) 1.0

Every meaningful scene component may be represented as an entity.

## Entity kinds

- `ARCHITECTURE`
- `INFRASTRUCTURE`
- `STOREFRONT`
- `SIGNAGE`
- `GRAPHIC`
- `SURFACE`
- `VEHICLE`
- `PERSON`
- `STREET_FURNITURE`
- `VEGETATION`
- `LIGHT_SOURCE`
- `ATMOSPHERIC_REGION`
- `OCCLUDED_REGION`
- `FRAME_BOUNDARY`
- `UNKNOWN`

## Scene roles

An entity may carry multiple roles.

### `STRUCTURAL_CORE`
Defines spatial/architectural organization.

### `IDENTITY_ANCHOR`
Strongly contributes to recognizing this specific source/world.

### `RELATIONSHIP_ANCHOR`
Its importance comes substantially from a protected relationship.

### `CONTEXTUAL_SUPPORT`
Individually secondary but contributes to scene character.

### `TEMPORAL_EVIDENCE`
Carries evidence about time, use, maintenance or historical layering.

### `TRANSIENT_OBJECT`
Potentially temporary in the world, such as a person or vehicle.

`TRANSIENT_OBJECT` does not mean removable.

### `OCCLUDER`
Blocks evidence behind it.

### `REMOVAL_CANDIDATE`
May be removable only when Mode/task authority allows.

### `UNKNOWN_REGION`
The evidence state is unresolved.

## Important distinction

`role ≠ preservation level`

A transient car can still be P2 observed evidence under T01.
A small sign can be P0/P1 because it is an identity anchor.
