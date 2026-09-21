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
