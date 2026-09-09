# Retrieval Ranking Policy

## Goal
Rank evidence by usefulness under Streetcraft authority constraints, not by visual seduction.

## Hard gates
A candidate is ineligible when any applies:
- evidence_state = UNKNOWN
- transfer_risk = PROHIBITED
- archive_class = REJECTED
- source_status = QUARANTINED
- below user/SVS minimum confidence
- violates hard region/period constraint
- contradicts a source-locked fact

## Suggested weights
Weights are implementation defaults, not new SVS rules.

### Evidence confidence
Use raw 0–1 confidence.

### Provenance
- P4: 1.00
- P3: 0.95
- P2: 0.85
- P1: 0.70
- P0: 0.50

### Domain specificity
- exact Evidence Unit domain: 1.00
- adjacent domain: 0.75
- broad whole-image relevance: 0.40

### Period compatibility
- within supported interval: 1.00
- adjacent/uncertain but plausible: 0.80
- unknown: 0.65
- conflicting: hard reject when period is a hard constraint

### Region compatibility
- exact/supported: 1.00
- broader compatible region: 0.85
- unknown: 0.70
- conflicting: hard reject when region is a hard constraint

### Transfer safety
- LOW: 1.00
- MEDIUM: 0.85
- HIGH: 0.55
- PROHIBITED: reject

### Archive class
- CANONICAL: governed by Canon rules, not automatically preferred
- CANON_CANDIDATE: 0.95
- DOCUMENTARY_EVIDENCE: 1.00
- INFLUENCE_REFERENCE: 0.65 for documentary deficits
- REJECTED: reject

Canon status does not override source authority and does not make an item universally relevant.

## Similarity cap
Semantic + visual similarity bonus should contribute no more than 20% of final reranking influence after authority gates.

This prevents a highly similar but semantically unsafe image from beating a stronger documentary reference.

## Corroboration
Independent corroboration may increase confidence.
Do not count:
- crops
- reposts
- alternate scans
- same-scene variants
as independent corroboration.
