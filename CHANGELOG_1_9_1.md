# CIL 1.1 · RDR2 Elevation Recovery

- Recovered `/sc-rdr2-elevation` → `VP02 + T02 + CG-F`.
- Added strict Identity Lock and LOCKED_UNKNOWN Occlusion Lock to the full elevation macro.
- Added strict frontalization, 16:9 and minimal-street output constraints.
- Added `/sc-front` camera modifier.
- Added aliases `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`.
- Added CG-F R2b regression requirement.
- Historical commit `696afe5` remains unavailable for byte-level diff verification.

# SVS 1.9.1 Patch Changelog

- Added Semantic Token Freeze for exact P0/P1 text and numerals.
- Added Low-Confidence Text Mask.
- Added Fear City Geographic Null Lock.
- Added Reference Bleed Preflight before generation.
- Added Atmosphere/Material Carryover Guard.
- Added pre-generation hard block on S3-class transfer.
- Added 24 deterministic patch tests derived from R2b failures.
- No Camera Grammar, profile, Canon, CIL or Archive ownership changes.
