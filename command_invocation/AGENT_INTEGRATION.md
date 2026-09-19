# CIL 1.1 Agent Integration
1. Scan `/sc-*` commands.
2. Expand aliases and macros via `COMMANDS.json`.
3. Reject unknown commands and profile-macro conflicts.
4. Apply normal Streetcraft authority hierarchy.
5. When `CG-F` is selected, load `CG_F_FRONTAL_ELEVATION.md`.
6. For `/sc-rdr2-elevation`, carry Identity Lock, Occlusion Lock, strict frontalization, 16:9 and minimal-street constraints into SAR2/CGC.
7. Identity Lock projects source-defining P0 geometry/relationships into preserve/forbid constraints.
8. `LOCKED_UNKNOWN` occlusion remains unknown unless independent evidence authorizes reconstruction.
9. Build SAR2 and CGC.
10. Reference retrieval remains automatic and scoped. References cannot fill locked occlusions or redesign identity during frontalization.
11. 1.9.1 preflight gates run before generation.
