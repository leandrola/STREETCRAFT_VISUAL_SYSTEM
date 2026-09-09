# Reference Runtime Pseudocode

```text
function retrieve_evidence(request):
    assert request.max_results <= 5

    if not request.reference_need_confirmed:
        return RM0_NONE

    candidates = sql_filter(
        domain=request.requested_domain,
        min_confidence=request.minimum_confidence,
        min_provenance=request.minimum_provenance,
        allowed_classes=request.allowed_archive_classes,
        source_status="AVAILABLE"
    )

    candidates = reject_forbidden_transfer(candidates, request.forbidden_transfer)
    candidates = apply_period_region_constraints(candidates, request)

    semantic_ranked = semantic_search(request.specific_problem, candidates)
    scored = authority_score(semantic_ranked, request)

    if request.source_visual_fingerprint and visual_form_is_relevant(request):
        scored = bounded_visual_rerank(scored, bonus_cap=0.20)

    scored = collapse_duplicate_families(scored)
    scored = evidence_diversity(scored, only_for_distinct_subproblems=True)
    selected = take(scored, request.max_results)

    if selected is empty:
        return REFERENCE_UNRESOLVED

    return authority_envelope(selected)
```

## Non-negotiable behavior
The runtime must never relax hard gates solely because search returned no candidates.
