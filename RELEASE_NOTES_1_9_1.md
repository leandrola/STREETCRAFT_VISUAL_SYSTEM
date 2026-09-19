# SVS 1.9.1 Release Notes

## Release focus
Critical R2b hardening on top of Scene Intelligence 1.9.0.

## Why
The 1.9.0 critical R2b audit exposed four S3 failures: semantic text mutation/invention, Fear City regional leakage, authored-world drift and atmosphere/material carryover.

## Added
- Semantic Token Freeze
- Low-Confidence Text Mask
- Fear City Geographic Null Lock
- Reference Bleed Preflight
- Atmosphere / Material Carryover Guard
- S3 pre-generation block

## Unchanged
- Camera Grammar
- VP00/VP01/VP02/VP03 definitions
- CIL syntax
- Canon authority
- Archive ownership boundaries

## Promotion gate
Candidate only until fresh R2b visual evidence reaches `S3=0` and global score `>=90`.
