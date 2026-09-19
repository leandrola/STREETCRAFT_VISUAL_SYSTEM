"""Opt-in reference orchestration; does not change the legacy runtime."""
from __future__ import annotations
from copy import deepcopy
import json
from archive_aware_runtime import resolve_runtime, ARCHIVE_DOMAINS

STATES = {'RN_NONE', 'RN_BLOCKED', 'RN_REQUIRED', 'RN_SUPPORT'}


def _ordered(needs):
    nodes = {}
    for n in needs:
        key = n['need_id']
        if not key or key in nodes:
            raise ValueError('Missing or duplicate need_id')
        if n['state'] not in STATES or not set(n['target_domains']) <= ARCHIVE_DOMAINS:
            raise ValueError('Invalid need state/domain')
        if not n['target_domains'] and n['state'] in {'RN_REQUIRED', 'RN_SUPPORT'}:
            raise ValueError('Queryable need requires a domain')
        if type(n.get('max_results', 3)) is not int or not 1 <= n.get('max_results', 3) <= 5:
            raise ValueError('max_results must be 1..5')
        nodes[key] = deepcopy(n)
        nodes[key].setdefault("task_context", "")
    visiting, done, order = set(), set(), []
    def visit(key):
        if key not in nodes:
            raise ValueError('Unknown dependency: ' + key)
        if key in visiting:
            raise ValueError('Cyclic reference dependency')
        if key in done:
            return
        visiting.add(key)
        for dep in nodes[key].get('depends_on', []):
            visit(dep)
        visiting.remove(key)
        done.add(key)
        order.append(nodes[key])
    for key in sorted(nodes, key=lambda k: (nodes[k]['state'] != 'RN_REQUIRED', k)):
        visit(key)
    return order


def resolve_reference_v2(*, needs, profile, mode, camera, archive_retriever,
                         query_budget=4, allow_support=True,
                         semantic_text_lock='STRICT', occlusion_locked=False,
                         fear_city_confirmed=False):
    """Single-bundle saturation; required unresolved needs block CGC projection.

    Dependencies must be satisfied, not merely visited. RN_BLOCKED retains
    unknowns without requesting evidence. This is not a scene analysis engine.
    """
    if type(query_budget) is not int or query_budget < 0:
        raise ValueError('query_budget must be a nonnegative integer')
    ordered = _ordered(needs)  # Validate entire graph before external calls.
    results, trace, cache, admissions = {}, [], {}, []
    query_count = 0
    for need in ordered:
        key, state = need['need_id'], need['state']
        if state == 'RN_BLOCKED':
            results[key] = 'LOCKED_UNKNOWN'
            trace.append({'need_id': key, 'reason': 'NO_QUERY_LOCKED_UNKNOWN'})
            continue
        if state == 'RN_NONE':
            results[key] = 'SATISFIED_SOURCE'
            trace.append({'need_id': key, 'reason': 'NO_QUERY_SOURCE_SUFFICIENT'})
            continue
        deps = need.get('depends_on', [])
        if any(results[d] not in {'SATISFIED_SOURCE', 'SATISFIED_EVIDENCE'} for d in deps):
            results[key] = 'DEPENDENCY_UNRESOLVED'
            trace.append({'need_id': key, 'reason': 'DEPENDENCY_UNRESOLVED', 'dependencies': deps})
            continue
        if state == 'RN_SUPPORT' and not allow_support:
            results[key] = 'SUPPORT_SKIPPED'
            trace.append({'need_id': key, 'reason': 'OPTIONAL_SUPPORT_DISABLED'})
            continue
        reason = []
        def retrieve(request):
            nonlocal query_count
            # Preserve all constraints and problem identity in the cache key.
            request = deepcopy(request)
            request.update(specific_problem=need['specific_problem'])
            cache_request = {k: v for k, v in request.items() if k != 'need_id'}
            sig = json.dumps(cache_request, sort_keys=True)
            if sig in cache:
                reason.append('CACHE_REUSE')
                return deepcopy(cache[sig])
            if query_count >= query_budget:
                reason.append('BUDGET_EXHAUSTED')
                raise RuntimeError('Budget exhausted')
            if archive_retriever is None:
                reason.append('ARCHIVE_UNAVAILABLE')
                raise RuntimeError('Archive unavailable')
            query_count += 1
            try:
                bundle = archive_retriever(deepcopy(request))
                if not isinstance(bundle, dict) or not isinstance(bundle.get('items', []), list):
                    raise ValueError('Invalid Archive response')
            except Exception:
                reason.append('ARCHIVE_ERROR')
                raise
            cache[sig] = deepcopy(bundle)
            reason.append('ARCHIVE_QUERY')
            return deepcopy(bundle)
        # Pre-screen provenance, identity and duplicates before legacy admission.
        rejected = []
        def screened(request):
            bundle = retrieve(request)
            unique = {}
            conflicted = set()
            for raw in bundle.get('items', []):
                item = deepcopy(raw)
                eid = item.get('evidence_unit_id')
                provenance = item.get('provenance_level')
                minimum = need.get('min_provenance', 'P1')
                levels = {f'P{i}': i for i in range(5)}
                if not eid or minimum not in levels or provenance not in levels or levels[provenance] < levels[minimum]:
                    rejected.append({'evidence_unit_id': eid, 'reason': 'MISSING_ID_OR_INSUFFICIENT_PROVENANCE'})
                    continue
                if eid in unique and unique[eid] != item:
                    conflicted.add(eid)
                unique[eid] = item
            for eid in conflicted:
                unique[eid]['bundle_conflict'] = True
            # Structured contradictions from the adapter are also honored by v1.
            bundle['items'] = list(unique.values())
            return bundle
        record = resolve_runtime(needs=[need], profile=profile, mode=mode, camera=camera,
                                 archive_retriever=screened, semantic_text_lock=semantic_text_lock,
                                 occlusion_locked=occlusion_locked, fear_city_confirmed=fear_city_confirmed)
        local = record['admissions']
        for item in local:
            item['need_id'] = key
        admissions.extend(local)
        review = any(a['decision'] == 'REVIEW_REQUIRED' for a in local)
        positive = any(a['decision'] == 'ADMITTED_SCOPED' for a in local)
        results[key] = 'REVIEW_REQUIRED' if review else ('SATISFIED_EVIDENCE' if positive else 'UNRESOLVED')
        trace.append({'need_id': key, 'reason': reason, 'screen_rejections': rejected,
                      'result': results[key], 'evidence_ids': [a['evidence_unit_id'] for a in local],
                      'evidence_bundle_ids': record['evidence_bundle_ids'],
                      'negative_evidence': record['negative_evidence']})
    missing = [n['need_id'] for n in ordered if n['state'] == 'RN_REQUIRED'
               and results[n['need_id']] != 'SATISFIED_EVIDENCE']
    reviews = [k for k, v in results.items() if v == 'REVIEW_REQUIRED']
    status = 'BLOCKED_REQUIRED' if missing else ('REVIEW_REQUIRED' if reviews else 'READY')
    projection = []
    if status == 'READY':
        for a in admissions:
            if a['decision'] == 'ADMITTED_SCOPED' and results[a['need_id']] == 'SATISFIED_EVIDENCE':
                projection.append({k: deepcopy(a.get(k)) for k in
                                   ['need_id', 'evidence_unit_id', 'domain', 'visible_fact', 'permitted_learning', 'forbidden_transfer']})
    return {'version': 'RR-2.0-experimental', 'status': status, 'queries': query_count,
            'query_budget': query_budget, 'need_results': results, 'unresolved_required': missing,
            'trace': trace, 'admissions': admissions, 'generation_projection': projection,
            'locked_unknowns': [k for k, v in results.items() if v == 'LOCKED_UNKNOWN']}


def enrich_cgc_v2(cgc, record):
    if record['status'] != 'READY':
        raise ValueError('Reference reasoning has unresolved requirements or review')
    out = deepcopy(cgc)
    out['reference_reasoning_v2'] = deepcopy(record)
    return out
