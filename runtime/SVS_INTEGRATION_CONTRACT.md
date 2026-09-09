# SVS ↔ Archive Runtime Contract

## Boundary
SVS owns the transformation decision.
Archive owns evidence discovery and scoped documentary support.
Archive never decides what the output should become.

## SVS → Archive
SVS sends a Retrieval Request only after Reference Need is established.

Required request fields:
- request_id
- requested_domain
- specific_problem
- source_context
- minimum_confidence
- max_results

Recommended:
- period_constraint
- regional_constraint
- forbidden_transfer
- required_tags
- minimum_provenance

## Archive → SVS
Archive returns:
- retrieval_status: RESOLVED | PARTIAL | UNRESOLVED
- candidates[]
- unresolved_questions[]

Each candidate contains:
- archive_id
- evidence_unit_ids
- authority_score
- confidence
- provenance
- why_selected
- permitted_learning
- forbidden_transfer

## Critical boundary
The Archive response is advisory evidence.
SVS still applies:
SOURCE AUTHORITY
→ MODE / PROFILE
→ ETO
→ REFERENCE AUTHORITY MAP
→ COMPACT GENERATION CONTRACT

Archive content must not be copied into the generated world outside the returned permitted-learning scope.

## Runtime failure behavior
Archive unavailable:
- continue with source-only reasoning where possible
- mark reference deficit unresolved
- never substitute arbitrary world knowledge as if it came from Archive evidence

Zero candidates:
- preserve ambiguity
- reduce transformation freedom
- or stop the unsupported branch
