# Archive Retrieval Contract

SVS 1.3 Reference Reasoning queries the Archive only after RNM declares a deficit.

## Request
- requested_domain
- specific_problem
- source_context
- period_constraint
- regional_constraint
- minimum_provenance
- minimum_confidence
- forbidden_transfer
- max_results

## Retrieval stages
1. eligibility filter
2. domain match
3. provenance filter
4. period/regional compatibility
5. evidence confidence
6. redundancy reduction
7. transfer-risk penalty
8. diversity only when it resolves distinct subproblems

## Output
Return a small candidate set, normally 1–5 items, each with:
- archive_id
- selected_evidence_units
- confidence
- provenance
- why_selected
- permitted_learning
- forbidden_transfer

## Critical rule
Do not retrieve because an image is globally similar. Retrieve because a declared evidence deficit matches a scoped Evidence Unit.

## No-result behavior
REFERENCE_UNRESOLVED is valid and preferred over contaminating retrieval.
