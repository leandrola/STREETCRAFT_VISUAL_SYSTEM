# Streetcraft SVS 1.10.0 / CIL 1.1 · Cheat Sheet

## Everyday commands
- `/sc-core` — VP00 + T01 + Camera Auto
- `/sc-classic` — VP01 + T01 + Camera Auto
- `/sc-2` — VP02 + T01 + Camera Auto
- `/sc-2a` — VP02 + CG-A
- `/sc-2b` — VP02 + CG-B
- `/sc-rdr2-elevation` — VP02 + T02 + CG-F + Identity Lock + Occlusion Lock + strict frontalization + 16:9 + minimal street
- `/sc-fear` — T06 + VP03 + CG-FC
- `/sc-fear2` — explicit Fear City → VP02 override

## Elevation aliases
- `/sc-2f`
- `/sc-rdr2-front`
- `/sc-elevation`

All three expand to `/sc-rdr2-elevation`.

## Modifiers
- `/sc-clean` — T03 Clean Plate
- `/sc-lock` — CG-S
- `/sc-auto` — automatic camera resolution
- `/sc-front` — CG-F + strict frontalization, without changing current profile/mode
- `/sc-preserve` — strict source preservation
- `/sc-noinvent` — strict unknown preservation
- `/sc-status` — show resolved configuration

## 1.9.1 automatic protections
No extra command is needed for Semantic Token Freeze, Low-Confidence Text Mask, Fear City Geographic Null Lock, Reference Bleed Preflight or material/atmosphere carryover protection.

## Safe defaults
- normal RDR 2.0: `/sc-2`
- facade dominant / frontal-oblique: `/sc-2a`
- corner / side depth: `/sc-2b`
- strict RDR 2.0 elevation: `/sc-rdr2-elevation`
- documentary maximum fidelity: `/sc-core /sc-lock /sc-preserve /sc-noinvent`
- Fear City: `/sc-fear`

## Backdrop presets · visual validation PENDING

- `/sc-bd01` — photo-based urban backdrop; recomposition within unprotected regions, preserving urban character.
- `/sc-bd02` — recognizable source layout translated into a panoramic backdrop; no major recomposition.
- Full BD01: `/sc-vp02 /sc-t02 /sc-cg-f /sc-rdr2-elevation /sc-bd01`
- Full BD02: `/sc-vp02 /sc-t08 /sc-cg-f /sc-rdr2-elevation /sc-preserve /sc-bd02`

Default 16:9, nominal 1:64; request `backdrop.aspect_ratio` can select 2:1 or
another horizontal format. P0, protected relationships and locked unknowns remain
protected. See [scope, options and print limitations](command_invocation/BACKDROP_PRESETS.md).

All ten visual benchmark cases are PENDING. Only inspection of a specific output
against BD01/BD02 criteria can grant that output visual PASS. Technical checks
cannot substitute for inspection. Physical print validation remains pending.
[Visual benchmark](validation/BD_VISUAL_VALIDATION_BENCHMARK.md).
