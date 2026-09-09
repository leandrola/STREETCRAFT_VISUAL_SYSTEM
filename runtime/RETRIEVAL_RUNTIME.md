# Streetcraft Archive Retrieval Runtime

## Objective
Translate a Reference Need Map deficit into a small, authority-safe set of documentary evidence candidates.

The runtime is not a generic image recommender. It is a scoped evidence resolver.

## Inputs
Required:
- requested_domain
- specific_problem
- source_context
- max_results

Optional:
- period_constraint
- regional_constraint
- minimum_provenance
- minimum_confidence
- allowed_archive_classes
- required_tags
- forbidden_tags
- forbidden_transfer
- source_visual_fingerprint

## Query plan

### Stage 0 — RNM gate
Do not query the archive unless SVS Reference Reasoning has declared a real deficit.

If the source already provides sufficient evidence:
`RM0 NONE`

### Stage 1 — hard eligibility
Exclude:
- REJECTED
- QUARANTINED
- prohibited transfer risk
- items below explicit provenance threshold
- evidence units below minimum confidence
- items incompatible with hard period/region constraints

### Stage 2 — evidence-domain match
Select Evidence Units whose domain directly matches `requested_domain`.

Examples:
- storefront composition → storefront Evidence Units
- fire escape construction → architectural-detail Evidence Units
- painted wall sign typography → signage Evidence Units
- brick weathering → material/weathering Evidence Units

Do not treat whole-image similarity as domain authority.

### Stage 3 — semantic retrieval
Search the normalized `semantic_document` built from Evidence Unit observations, tags and scoped context.

Semantic retrieval produces candidates, not final authority.

### Stage 4 — deterministic compatibility score
Calculate source-relative compatibility from:
- evidence confidence
- provenance
- period compatibility
- regional compatibility
- domain specificity
- archive class
- transfer risk

### Stage 5 — optional visual support
Visual similarity may rerank candidates only when visual form is relevant to the declared deficit.

Its influence must remain capped. A visually similar image with weak documentary authority must not outrank stronger evidence merely because it looks closer.

### Stage 6 — duplicate collapse
Collapse SAME_SCENE, CROP_OF, ALTERNATE_SCAN and REPOST_OF families so one historical image does not masquerade as independent corroboration.

### Stage 7 — evidence diversity
When the deficit contains distinct subproblems, prefer candidates that resolve different subproblems.

Do not diversify for aesthetics.

### Stage 8 — final authority envelope
For each returned candidate emit:
- archive_id
- evidence_unit_id(s)
- confidence
- provenance
- why_selected
- permitted_learning
- forbidden_transfer
- unresolved_uncertainty

## Default result budget
- 0 is valid.
- 1–3 is preferred.
- 5 is the normal maximum.
- >5 requires explicit diagnostic/research mode.

## Ranking model
Recommended conceptual score:

`authority_score = domain_match × evidence_confidence × provenance_weight × compatibility × transfer_safety`

Semantic/visual similarity only influence candidate discovery and bounded reranking.

They do not create authority.

## No-result behavior
If nothing passes hard eligibility:

`REFERENCE_UNRESOLVED`

SVS must then preserve ambiguity, reduce transformation, or terminate the unsupported transformation branch.

Never lower authority thresholds automatically merely to return a result.
