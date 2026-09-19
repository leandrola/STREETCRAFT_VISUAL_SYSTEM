# Streetcraft Visual System (SVS) 1.9.1 / CIL 1.1

**Package type:** full reconstructed candidate release  
**Authoritative base:** `https://github.com/leandrola/STREETCRAFT_VISUAL_SYSTEM` @ `04c070d2043295bb802ce3381b7c78faa26ee991`  
**Base release:** SVS 1.9.0 Candidate  
**Integrated patch:** SVS 1.9.1 Critical R2b Hardening
**Command layer:** CIL 1.1 recovered elevation command set

SVS 1.9.1 integrates Scene Intelligence with the critical hardening patch derived from the failed 1.9.0 R2b audit.

## Runtime

`CIL 1.1 → Source Analysis → SAR2 Scene Intelligence → CGC → Archive-Aware Runtime → 1.9.1 Preflight → Generation → Visual Critic → Micro-Drift Critic`

## 1.9.1 controls

- Semantic Token Freeze
- Low-Confidence Text Mask
- Fear City Geographic Null Lock
- Reference Bleed Preflight
- Atmosphere / Material Carryover Guard
- hard block on S3 pre-generation violations

## Stability status

This is a **candidate release**, not Stable.

Deterministic regression is expected to pass, but the benchmark policy still requires a fresh R2b visual candidate rerun with:

- `S3 = 0`
- global visual score `>= 90`

before Stable promotion.

## Reconstruction note

The operational package was rebuilt from the public GitHub 1.9.0 base plus the local 1.9.1 patch. Exact reference and Fear City source assets were recovered and verified against Git blob IDs. Seven historical L2 camera-validation binaries could not be materialized through the connected repository interface in this runtime; they remain explicitly indexed as remote verified fixtures in `benchmark/fixtures/REMOTE_BINARY_FIXTURES.json`.

See `RECONSTRUCTION_PROVENANCE.md` for the audit trail.


## CIL 1.1 recovery
The recovered elevation command is `/sc-rdr2-elevation` → `VP02 + T02 + CG-F`, with strict Identity Lock, `LOCKED_UNKNOWN` Occlusion Lock, strict frontalization, 16:9 and minimal street. `/sc-front` is available as a camera modifier. Aliases: `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`.

The historical commit id supplied for this work (`696afe5`) was not resolvable in the connected GitHub repository, so this build records a semantic reconstruction from the explicit project definition rather than claiming byte-identical recovery of that commit.
