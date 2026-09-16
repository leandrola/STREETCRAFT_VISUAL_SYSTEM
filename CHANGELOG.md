# SVS 1.9.0 — Scene Intelligence

- Added Scene Entity Model.
- Added Scene Relationship Graph.
- Added Scene Salience Model.
- Added Scene Action Resolver.
- Added Scene Analysis Record v2.
- Added Scene-to-CGC projection.
- Added Fear City Scene Intelligence policy.
- Added scene-derived Reference Need hints.
- Added B9 deterministic regression cases.
- CIL syntax unchanged.
- Visual Profiles, Camera Grammar and Canon authority unchanged.
- Fresh R2b visual candidate regression required before stable promotion.

# SVS 1.8.1 — R2 Baseline Calibration

- Calibrated the first R2 visual baseline.
- Added semantic identity anchors plus SHA-256/dHash fixture signatures.
- Split R2 into R2a baseline calibration and R2b future candidate regression.
- Added baseline-integrity checker.
- Framework release gate can now close without circular self-certification.
- No Streetcraft runtime behavior changes.

# SVS 1.8.0 — Regression & Benchmark Suite

- Added formal regression/release gate.
- Added R0 automated regression suite.
- Added R1 SHA-256 golden fixture integrity layer.
- Added R2 visual benchmark cases and scoring rubric.
- Added governing-file baseline drift detection.
- Added Archive V1 integration regression.
- Added visual result scorer and runbook.
- No Visual Canon or runtime behavior changes.

# SVS 1.7.0 — Archive-Aware Reference Runtime

- Added Reference Need Model 1.0.
- Added Reference Authority Map 1.0.
- Added Archive Domain Policy.
- Added Evidence Admission Policy 1.0.
- Added Archive failure/no-result policy.
- Added CGC reference-runtime enrichment.
- Added executable Archive V1 adapter.
- Added evidence-bundle admission and generation projection.
- Added reference-bleed inspection/correction.
- CIL syntax unchanged.
- Archive remains separate from Canon.
- No Canon-by-similarity behavior permitted.

# SVS 1.6.4 — Operational Hardening

- Added Semantic Text Lock.
- Added Material Intensity Delta.
- Added Occlusion Locks.
- Added Compact Generation Contract and schema.
- Added Micro-Drift Critic.
- Added Profile Delta Matrix.
- Integrated hardening gates with Visual Intelligence, Visual Critic, Self-Correction, Agent Protocol and CIL.
- No Visual Canon authority changes.

# SVS 1.6.3 — 2026-09-12

- Consolidated full release package from SVS 1.6.2 + CIL 1.0 patch.
- Added Streetcraft Command Invocation Layer (CIL) 1.0 to the mainline release.
- Added short `/sc-*` command vocabulary and resolver.
- No Visual Canon, Transformation Mode, Preservation Model or SC rule changes.

# SVS 1.6.3 CIL Patch

- Added CIL 1.0.
- Added `/sc-core`, `/sc-classic`, `/sc-2`, `/sc-2a`, `/sc-2b`.
- Added `/sc-fear`, `/sc-fear2`.
- Added `/sc-clean`, `/sc-lock`, `/sc-auto`, `/sc-preserve`, `/sc-noinvent`.
- Added `/sc-status`, `/sc-help`.
- Commands are turn-scoped. No hidden persistent state.
- Added deterministic resolver and tests.
- No Canon or governing visual-rule changes.

# SVS 1.6.2 — 2026-09-11

- Promoted the validated Camera/Routing patch to formal release.
- Camera Grammar validated across CG-A, CG-B, CG-S and CG-FC.
- VP00 / VP01 / VP02 camera behavior validated.
- VP02 no longer requires mandatory strict frontality or yaw≈0°.
- Fear City Auto-Routing validated structurally and with confirmed multi-view authored-world evidence.
- Added Fear City Identity Threshold: CONFIRMED / PROBABLE / UNRESOLVED / NOT_APPLICABLE.
- CRVM validation complete: L0 PASS 26/26, L1 PASS, L2 PASS, L3 PASS.
- No Visual Canon authority, Transformation Mode, Preservation Model or SC rule changes.

# SVS 1.6.2 Camera/Routing Patch

- Formalized CG-A frontal-oblique architectural immersion.
- Formalized CG-B street-level oblique monumentality.
- Added CG-S source-locked camera.
- Added CG-FC Fear City authored-view camera.
- Revised VP00, VP01 and VP02 camera behavior.
- Retired mandatory yaw≈0° and mandatory one-point frontality from VP02.
- Added conservative Fear City Auto-Routing.
- No Visual Canon or SC rule changes.

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
