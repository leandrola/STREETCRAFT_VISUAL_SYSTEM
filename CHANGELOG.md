# VSG-0.1.0 — Observer · 2026-09-22

- Added an optional, non-governing Visual Scene Graph projection over SAR2.
- Retained RR2 outcomes as passive, node-targeted reference observations.
- Added typed nodes, explicit spatial/semantic edges, confidence, locks and provenance.
- Added semantic text, rooftop, geometry and occlusion functional subgraphs.
- Added the Kenny's Shop volumetric rooftop fixture and VSG JSON Schema.
- Proved observer equivalence: stable orchestration output is unchanged except for the diagnostic graph.
- Validation: VSG 24/24, orchestrator 12/12, unified regression PASS, R2b 91.0 and S3=0.

# SVS 1.10.0 — STABLE · 2026-09-21

- Promoted after Gate 4 final PASS by explicit user decision.
- Unified regression PASS.
- R2b visual 6/6, S3=0, global score 91.0.
- RR2 real Archive 8/8 PASS; bundles, traces and provenance SHA preserved.
- CGC end-to-end real Archive 8/8 PASS.
- Archive runtime identity 20/20 SHA-256 match.
- Single Streetcraft client remains authoritative.

# SVS 1.10.0 — Single-client integration in progress

- Established one Streetcraft client and one release line.
- Integrated Reference Reasoning 2.0 as the primary reference interface.
- Retained Archive-aware admission as an internal component, not an alternative client runtime.
- Removed pre-release, opt-in and unpushed-state labels from current release documentation.
- Preserved the release gate: R2b must finish with S3=0 and global score >=90.

# CIL 1.1 · RDR2 Elevation Recovery

- Recovered `/sc-rdr2-elevation` → `VP02 + T02 + CG-F`.
- Added strict Identity Lock and LOCKED_UNKNOWN Occlusion Lock to the full elevation macro.
- Added strict frontalization, 16:9 and minimal-street output constraints.
- Added `/sc-front` camera modifier.
- Added aliases `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`.
- Added CG-F R2b regression requirement.
- Historical commit `696afe5` remains unavailable for byte-level diff verification.

# SVS 1.9.1 — Critical R2b Hardening

- Integrated Semantic Token Freeze.
- Integrated Low-Confidence Text Mask.
- Integrated Fear City Geographic Null Lock.
- Integrated Reference Bleed Preflight.
- Integrated Atmosphere/Material Carryover Guard.
- Added pre-generation block on S3 violations.
- Added 24 deterministic patch regressions.
- Full package reconstructed from GitHub 1.9.0 candidate base.
- Stable promotion remains gated on fresh R2b visual rerun.

# Changelog

## 1.6 - 2026-09-06
- Consolidated SVS 1.4 Visual Critic, 1.5 Self-Correction and 1.6 Fear City Vision into the portable package.
- Added SC-27 through SC-48.
- Added comparative vision, Visual Failure Records, gate-based Compliance 2.0 and Revision Contracts.
- Added BKO, Protected Success Set, regression protection, correction budgets, escalation and stop engine.
- Added Fear City world/model/capture evidence separation, Authored World Authority, Authorial Persistence, Multi-View Consistency Evidence, scale translation and material-world translation.
- Added UNSUPPORTED_WORLD_EXTENSION, GEOGRAPHIC_IDENTITY_IMPORT and MATERIAL_INTENSITY_DRIFT as Fear City failure families.
- Added domain-specific T06 budgets and explicit depth/decay/geographic constraints.
- Validated Fear City Vision against a three-view real Fear City set and one generated T06 transformation. Validation PASS; generated output rated STREETCRAFT PASS, not Canon Candidate.

## 1.2 - 2026-09-05
- Added Visual Intelligence pre-generation analysis stack, SAR 1.2, uncertainty and Transformation Readiness.
- Added SC-18 through SC-26.

## 1.0 - 2026-09-05
- Reframed Streetcraft into an AI-agnostic visual system.
- Preserved RDR and RDR 2.0 as visual profiles.
- Defined Fear City as authored physical source domain/profile.

## 1.6.1 — 2026-09-06
- Integrated SVS 1.1 Visual Canon into the portable build.
- Added scoped Canon architecture, candidate registry, Documentary Evidence and Boundary Canon.
- Added reference assets selected from user-supplied RDR/Streetcraft outputs.
- Added SC-49 through SC-62 for canon governance, documentary evidence, lineage, decay ceiling and signage semantics.
- Closed Fear City Vision depth/geography/atmosphere gaps with WDB0–WDB3 and SC-63 through SC-66.
- Added validation-derived Fear City failures: UNSUPPORTED_WORLD_EXTENSION, GEOGRAPHIC_IDENTITY_IMPORT, ATMOSPHERIC_INFLATION, MATERIAL_INTENSITY_DRIFT.
- Added T06 lexical guardrails to reduce semantic leakage from generic cinematic language.
