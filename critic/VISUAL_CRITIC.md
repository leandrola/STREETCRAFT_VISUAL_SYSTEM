# SVS 1.4 Visual Critic

Flow:
SOURCE + SAR + TRANSFORMATION PLAN + OUTPUT → COMPARE → DIAGNOSE → COMPLIANCE → REVISION CONTRACT

## Difference classes
AUTHORIZED_CHANGE
EXPECTED_RECONSTRUCTION
UNAUTHORIZED_CHANGE
UNRESOLVED_DIFFERENCE

Compare independently: geometry, camera, architecture, materials, signage, light, atmosphere, temporal layers, regional character, objects, protected relationships and inferred regions.

## Preservation Delta
P0 unauthorized change = CRITICAL DELTA
P1 moderate alteration = MAJOR DELTA
P2 small variation = ACCEPTABLE DELTA
P3 intended transformation = AUTHORIZED DELTA
P4 removal = EXPECTED DELTA
P5 reconstruction = evaluate against evidence boundary

## Visual Failure Record
id / domain / location / observed_delta / expected_state / failure_class / severity / confidence / preservation_level / affected_anchor / affected_relationship / probable_cause / propagation / correction_scope / collateral_risk

Severity: S0 NOTICE / S1 MINOR / S2 MATERIAL / S3 MAJOR / S4 CRITICAL

## Failure families
Geometry: GEOMETRY_MUTATION, PROPORTION_DRIFT, OPENING_COUNT_DRIFT, FLOOR_COUNT_DRIFT, MASSING_DRIFT
Camera: VIEWPOINT_DRIFT, PERSPECTIVE_DRIFT, UNAUTHORIZED_FRONTALIZATION, UNAUTHORIZED_DEPTH_CHANGE
Architecture: ARCHITECTURAL_HALLUCINATION, ARCHITECTURAL_SIMPLIFICATION, STYLE_SUBSTITUTION, FACADE_BEAUTIFICATION
Materials: MATERIAL_SUBSTITUTION, PROCEDURAL_DECAY, UNIFORM_AGING, SURFACE_MEMORY_LOSS, CAUSALITY_FAILURE
Signage: SIGN_IDENTITY_LOSS, SIGN_POSITION_DRIFT, SIGNAGE_SANITIZATION, SIGNAGE_ACCUMULATION_LOSS, UNSUPPORTED_SIGNAGE
Period/Region: PERIOD_CONTAMINATION, PERIOD_COSPLAY, GENERIC_AMERICANA, REGIONAL_IDENTITY_LOSS, SINGLE_TIMESTAMP_WORLD
Atmosphere: CINEMATIC_INFLATION, LIGHTING_CAUSALITY_FAILURE, ATMOSPHERE_OVERRIDE, FALSE_WETNESS, EXCESSIVE_MOOD
Documentary: DOCUMENTARY_FRICTION_LOSS, UNAUTHORIZED_CLEANUP, PROP_SPAM, UNSUPPORTED_SPECIFICITY
Fear City: AUTHORSHIP_MUTATION, MODEL_WORLD_REDESIGN, MODEL_MATERIAL_CONFUSION, CAPTURE_ARTIFACT_RETENTION, UNSUPPORTED_WORLD_EXTENSION, GEOGRAPHIC_IDENTITY_IMPORT, MATERIAL_INTENSITY_DRIFT

## Failure graph
PRIMARY_FAILURE / DEPENDENT_FAILURE / INDEPENDENT_FAILURE
Scope: LOCAL / REGIONAL / DOMAIN-WIDE / SYSTEMIC
Collateral Risk: CR0–CR4

## Revision Contract
TARGET FAILURES
ROOT FAILURE
REQUIRED ACTION
EDIT REGION
FREEZE
PROTECTED RELATIONSHIPS
FORBIDDEN
SUCCESS CONDITION
REGRESSION TEST

## Reference Reasoning audit
When external references were used, inspect OUTPUT against RAM, RTC, SLM, ETO, RF and CL.
Additional failures:
REFERENCE_LEAKAGE — correlated unauthorized traits transferred from a selected reference.
REFERENCE_ECHO — Canon traits begin replacing source identity without a single decisive copied feature.
UNAUTHORIZED_REFERENCE_TRANSFER — a property marked INERT/FORBIDDEN appears to have influenced the output.
REFERENCE_SCOPE_VIOLATION — a reference influences a domain outside declared Canon Scope/RTC.
CANON_PROFILE_CONFLICT — output follows a Canon exception against an explicit Profile rule without human authorization.
REFERENCE_DEBT_EXCEEDED — breadth of external transfer exceeds transformation need/budget.

Do not infer leakage from one common urban feature. Require correlated evidence or a highly distinctive unauthorized feature.
