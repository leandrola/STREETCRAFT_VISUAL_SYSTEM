# SVS 1.2 Visual Intelligence

Flow:
SOURCE → Visual Decomposition → Visual Evidence Graph → Preservation Intelligence → Uncertainty/Occlusion Intelligence → Scene Understanding → SAR → Transformation Readiness

## Visual Decomposition
VD01 Scene Structure
VD02 Camera
VD03 Architecture
VD04 Materials & Surfaces
VD05 Signage & Graphics
VD06 Light & Atmosphere
VD07 Objects & Urban Residue
VD08 Relationships

Architectural Identity Anchors (AIA) capture high-identity features without automatically making all of them P0.

## Visual Evidence Unit
subject / observation / location / epistemic_class / confidence

## Visual Evidence Graph (VEG)
Relations include SPATIAL, OCCLUSION, STRUCTURAL, MATERIAL and TEMPORAL.

## Preservation Intelligence
Source Authority signals: geometry, identity, relationship, documentary, authorship, atmospheric.
Task Authority comes from requested transformation.

## Uncertainty & Occlusion
O1 TRANSIENT
O2 ENVIRONMENTAL
O3 ARCHITECTURAL
O4 FRAME
O5 CAPTURE

Reconstruction Confidence: RC3 HIGH / RC2 MEDIUM / RC1 LOW / RC0 NONE
Uncertainty Budget: UB0 STRICT / UB1 CONSERVATIVE / UB2 INTERPRETIVE / UB3 SPECULATIVE
Hallucination Pressure: LOW / MEDIUM / HIGH / CRITICAL
Evidence Sufficiency: SUFFICIENT / LIMITED / INSUFFICIENT

If Hallucination Pressure is HIGH/CRITICAL and evidence is LIMITED/INSUFFICIENT, recommend references instead of silently inventing.

## Scene Understanding
Temporal Layer Graph relations: PRECEDES, POSTDATES, OVERLAPS, REPLACES, COVERS, UNKNOWN_RELATION.
Use State: ACTIVE, USED, UNDERUSED, VACANT, ABANDONED, UNKNOWN.
Maintenance Signature: uniform, patch, reactive, layered, minimal.
Regional signals: STRONG, SUPPORTING, WEAK, GENERIC.
Modern Contamination: PERIOD-COMPATIBLE, POSSIBLY COMPATIBLE, TEMPORALLY AMBIGUOUS, TARGET-CONFLICTING, UNKNOWN.

## Transformation Readiness Engine
READY / READY_WITH_INFERENCE / REFERENCE_ADVISED / INSUFFICIENT_EVIDENCE / MODE_CONFLICT / USER_DECISION_REQUIRED
