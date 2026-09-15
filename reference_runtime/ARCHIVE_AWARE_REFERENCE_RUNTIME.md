# SVS 1.7 · Archive-Aware Reference Runtime

## Purpose

SVS 1.7 closes the loop between Streetcraft Visual System and Streetcraft Archive V1.

The runtime sequence is:

`CIL → Source Analysis → CGC → Reference Need → Archive Retrieval → Evidence Admission → CGC Enrichment → Generation → Visual Critic → Micro-Drift Critic`

The Archive supplies scoped documentary evidence.  
SVS remains the only authority that decides what may change in the output.

## Boundary

### SVS owns
- source identity
- preservation invariants
- transformation mode
- visual profile
- camera grammar
- semantic-text locks
- material-intensity limits
- occlusion locks
- generation contract
- final evidence admission

### Archive owns
- evidence discovery
- provenance
- eligibility
- authority-first ranking
- transfer-risk metadata
- conflict retention
- negative evidence
- Evidence Bundle assembly

Archive evidence is advisory. It never becomes Canon automatically and never overrides P0 source invariants.

## Runtime principle

Retrieval is not:

> find images that look similar.

Retrieval is:

> find eligible Evidence Units for a declared and scoped Reference Need.

Global visual resemblance is never sufficient authority.

## Evidence budget

For each Reference Need:
- normal target: 1–3 admitted Evidence Units
- hard maximum: 5
- total generation target: ≤8 admitted units

More evidence is not automatically better. Reference soup increases transfer risk.

## No-result behavior

`REFERENCE_UNRESOLVED` is a valid result.

When Archive cannot resolve a need:
1. preserve source evidence,
2. preserve uncertainty,
3. reduce transformation freedom,
4. never substitute arbitrary model knowledge as if it were Archive evidence.

## Archive-unavailable behavior

SVS may continue source-only when the requested transformation is still valid without external evidence.

If evidence is required for the requested transformation, the unsupported branch is blocked rather than hallucinated.
