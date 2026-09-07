# SVS 1.3 Reference Reasoning

Purpose: decide whether external visual evidence is needed, retrieve the smallest eligible reference set, assign property-level authority, prevent leakage, resolve conflicts, and preserve uncertainty.

## Pipeline
INPUT → SAR / FC-SAR → SOURCE EVIDENCE MAP → INTERNAL INFERENCE → REFERENCE NEED MAP → NRN? → RETRIEVAL MODE → ELIGIBILITY GATES → REFERENCE RESOLVER → MINIMUM SUFFICIENT SET → RAM → RTC × SLM → CONFLICT RESOLVER → TRANSFORMATION PLAN → GENERATION → VISUAL CRITIC → REFERENCE LEAKAGE CHECK → SELF-CORRECTION.

## Reference Need Map (RNM)
RS0 SOURCE_SUFFICIENT
RS1 REFERENCE_OPTIONAL
RS2 REFERENCE_BENEFICIAL
RS3 REFERENCE_REQUIRED
RS4 REFERENCE_CANNOT_RESOLVE

Evaluate independently where relevant: geometry, architecture, material, signage, period, region, camera, light, atmosphere, temporal_layers, urban_use, fear_city_scale.

NRN / NO_REFERENCE_NEEDED is preferred when source/task/profile evidence is sufficient.

## Retrieval Modes
RM0 NONE
RM1 CANON_ONLY — how Streetcraft has validated a transformation problem.
RM2 DOCUMENTARY_EVIDENCE — how the represented world plausibly behaves.
RM3 HYBRID — requires both transformation and real-world evidence, with non-overlapping responsibilities.

## Eligibility before ranking
Reject a candidate before ranking when domain authority is absent, Canon Scope does not cover the request, provenance is insufficient for the claim, transfer collides with protected source evidence, or Boundary Canon was not explicitly activated.

## Reference Resolution
Evaluate eligible candidates by Domain Match, Canon Scope Match, Authority Quality, Profile Compatibility, Evidence Compatibility, Transfer Risk and Reference Debt. Similarity is secondary to relevance. Weights are implementation policy, not artistic law.

RRC / Reference Resolution Confidence:
0.90–1.00 STRONG
0.75–0.89 GOOD
0.60–0.74 WEAK
<0.60 UNRESOLVED

Retrieval may validly return REFERENCE_UNRESOLVED. Never choose the least-bad reference merely to fill a slot.

## Minimum Sufficient Reference Set
Use the smallest reference set that resolves the declared deficit. Multiple references require explicit, non-ambiguous responsibilities.

## RAM / Reference Authority Map
Records which authority controls each relevant domain/property. Example:
geometry=SOURCE; signage_text=SOURCE; brick_physics=DOCUMENTARY; material_translation=DOMAIN_CANON; profile_behavior=PROFILE.

## RTC / Reference Transfer Contract
Every selected reference is partitioned at property level:
ACTIVE — permitted to transfer for the declared need.
INERT — visible but irrelevant; do not transfer.
FORBIDDEN — must not transfer.
CONDITIONAL — may resolve/physicalize content only when other evidence confirms its existence.

Reference visibility never grants transfer authority.

## SLM / Source Lock Map
Protect source properties as HARD / SOFT / OPEN. Locks can cover objects, properties and relationships. A reference cannot override a stronger lock unless a narrow Explicit Transformation Override authorizes the change.

## ETO / Explicit Transformation Override
Task/profile intent may override source authority only for the properties required to fulfill the requested transformation. Example: RDR 2.0 may authorize camera/perspective frontalization without authorizing arbitrary facade, signage, color or decay changes.

## RF / Reference Fingerprint and leakage
A Reference Fingerprint records distinctive non-transferable clusters. A common feature alone is not leakage. Correlated unauthorized similarities or a highly distinctive transferred feature can trigger REFERENCE_LEAKAGE. Softer canonical over-assimilation is REFERENCE_ECHO.

## RD / Reference Debt
RD0 none; RD1 low; RD2 moderate; RD3 high; RD4 critical. More external domains increase contamination risk. Conservative transformations should minimize RD. Reference freedom must scale with Transformation Budget.

## Conflict Resolution
Resolve per property and task, using authority × confidence × domain specificity.
Base authority classes, interpreted per property:
1 explicit user / Transformation Contract
2 authored source evidence
3 direct source evidence
4 corroborated / multi-view source evidence
5 profile constraint when explicitly invoked by task
6 documentary evidence for real-world truth/physics
7 scoped Canon for validated Streetcraft translation behavior
8 general visual knowledge
9 generator prior

Truth authority and transformation authority are distinct. Documentary evidence governs plausible real-world behavior; Canon governs validated Streetcraft transformation behavior within declared scope. Canon cannot silently rewrite a Profile.

Conflict classes:
C1 EVIDENCE_CONFLICT
C2 AUTHORITY_CONFLICT
C3 INTENT_CONFLICT

Resolution states:
CR0 AUTO_RESOLVED
CR1 RESOLVED_WITH_CONFIDENCE_LOSS
CR2 CONSERVATIVE_FALLBACK
CR3 HUMAN_DECISION_REQUIRED

## Internal inference
Before external retrieval, attempt conservative reconstruction from source repetition, symmetry, continuation and corroborating views. Provenance levels: DOCUMENTED, CORROBORATED, INFERRED_HIGH, INFERRED_LOW, UNKNOWN. Inference never becomes documented fact.

## Conflict Ledger (CL)
For material conflicts record: property, competing authorities/evidence, confidence, resolution, transfer permission and remaining uncertainty. This prevents repeated re-litigation during revision.

## Reference Reasoning Rules
SC-67 Reference Cannot Override Stronger Source Evidence
SC-68 Reference Use Must Solve a Deficit
SC-69 Minimum Sufficient Reference Set
SC-70 Reference Visibility Does Not Grant Transfer Authority
SC-71 Eligibility Precedes Similarity
SC-72 Specific Authority Beats Unrelated Prestige
SC-73 References Must Have Non-Ambiguous Responsibilities
SC-74 Retrieval May Resolve to Nothing
SC-75 Boundary Canon Is Opt-In
SC-76 Reference May Resolve, Not Manufacture
SC-77 Transfer Authority Is Property-Level
SC-78 Preservation Includes Relationships
SC-79 Reference Leakage Requires Correlated Evidence
SC-80 Canon Must Not Become the Subject
SC-81 Reference Freedom Scales With Transformation Budget
SC-82 Authority Is Property- and Task-Specific
SC-83 Override Must Be Narrow
SC-84 Unknown Is Not Creative License
SC-85 Truth Authority and Transformation Authority Are Distinct
SC-86 Canon Cannot Silently Rewrite Specification
SC-87 Internal Evidence Precedes External Reference
SC-88 Inference Must Preserve Uncertainty
SC-89 Intelligence Must Reduce Unjustified Freedom
