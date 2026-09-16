# Fear City Scene Intelligence Policy

Confirmed Fear City uses Scene Intelligence with authored-world authority.

## Typical high-authority classes

- elevated structure: STRUCTURAL_CORE
- underpass: STRUCTURAL_CORE / IDENTITY_ANCHOR
- embedded track path: STRUCTURAL_CORE / RELATIONSHIP_ANCHOR
- principal brick walls: STRUCTURAL_CORE
- recurring graffiti wall: IDENTITY_ANCHOR / TEMPORAL_EVIDENCE
- Tanner/Jericho signage: IDENTITY_ANCHOR
- curb/street topology: RELATIONSHIP_ANCHOR

## Required relationship examples

- elevated `ABOVE` street
- tracks `CONTINUES_INTO` underpass
- walls `BOUNDS` underpass
- graffiti `APPLIED_TO` authored wall
- street sign `ATTACHED_TO` authored pole
- sidewalk `FOLLOWS` authored building/street edge

## Transient content

Vehicles and figures may be transient, but their removability still depends on task/mode authority.

## Forbidden interpretation

Scene Intelligence cannot infer “New York” from brick, graffiti, elevated infrastructure or 1970s visual resemblance.
