"""Semantic preservation gate against the stable CGC and its source snapshots."""
from copy import deepcopy
import json
import jsonschema

from .generation_compiler import (
    ROOT, DIRECTIVES, POLICIES, normalize, digest, index, graph_constraints, graph_content,
    validate_generation_contract, _constraint,
)


def stable_constraints(cgc, *, sar2, expected_graph):
    """Read stable CGC actions/directives independently of the shadow compiler.

CGC has no node attributes or Graph Lock ledger. Its immutable source VSG is
therefore required evidence for those restrictions, not a candidate-derived
baseline. Unrecognized CGC extensions fail closed.
"""
    import jsonschema
    jsonschema.validate(cgc, json.loads((ROOT/'schemas/compact-generation-contract.schema.json').read_text()))
    unknown = set(cgc) - POLICIES - set(DIRECTIVES) - {'source_identity', 'scene_intelligence'}
    issues = ['UNSUPPORTED_CGC_FIELD:' + key for key in sorted(unknown)]
    constraints, graph_issues = graph_constraints(expected_graph, sar2)
    issues += ['INVALID_BASELINE:' + e for e in graph_issues]
    si = cgc.get('scene_intelligence')
    if not isinstance(si, dict):
        raise ValueError('MISSING_CGC_SCENE_INTELLIGENCE')
    if si['scene_id'] != sar2['scene_id'] or expected_graph['scene_id'] != sar2['scene_id']:
        raise ValueError('CGC_SCENE_MISMATCH')
    si_fields = {'scene_id', 'identity_anchors', 'protected_relationships', 'entity_actions', 'unknown_locks', 'reference_need_hints'}
    issues += ['UNSUPPORTED_CGC_SCENE_FIELD:' + k for k in sorted(set(si) - si_fields)]
    entities = index(sar2['entities'], 'entity_id')
    actions = index(si['entity_actions'], 'entity_id')
    source_actions = index(sar2['action_plan'], 'entity_id')
    if set(actions) != set(entities) or set(source_actions) != set(entities):
        issues.append('AMBIGUOUS_REQUIRED_ACTION_MAPPING')
    if set(index(expected_graph['nodes'])) != set(entities):
        issues.append('INCOMPLETE_SOURCE_GRAPH')
    baseline_edges = index(expected_graph['edges'])
    relationships = index(si['protected_relationships'], 'relationship_id')
    required = {r['relationship_id']: r for r in sar2['relationships'] if r['protection'] in {'PR0', 'PR1'}}
    if normalize(list(relationships.values()), 'relationships') != normalize(list(required.values()), 'relationships'):
        issues.append('CGC_SOURCE_RELATIONSHIP_MISMATCH')
    for rid, relation in required.items():
        edge = baseline_edges.get(rid)
        if not edge or any(edge[k] != relation[v] for k, v in (('from', 'subject'), ('to', 'object'), ('type', 'predicate'), ('protection', 'protection'))):
            issues.append('UNRESOLVED_REQUIRED_RELATIONSHIP:' + rid)
    for nid, entity in entities.items():
        a = actions.get(nid)
        if not a:
            continue
        if normalize(a) != normalize(source_actions[nid]):
            issues.append('CGC_SOURCE_ACTION_MISMATCH:' + nid)
        if entity['preservation_level'] == 'P0' and a['action'] != 'PRESERVE_EXACT':
            issues.append('P0_NOT_EXACT:' + nid)
        label = entity.get('label', nid)
        act = a['action']
        encoded = None
        if act.startswith('PRESERVE_'):
            encoded = ('preserve', f'{nid}:{label}:{act}')
        elif act == 'UNKNOWN_LOCKED':
            encoded = ('unknown', f'{nid}:{label}')
            if nid not in si['unknown_locks'] or nid not in cgc['occlusion_locks'] or f'resolve_exact_unknown:{nid}' not in cgc['forbid']:
                issues.append('CGC_UNKNOWN_PERMISSIVE:' + nid)
        elif act == 'REMOVE_AUTHORIZED':
            encoded = ('remove', f'{nid}:{label}')
        elif act == 'INFER_MINIMAL':
            encoded = ('infer', f'{nid}:{label}:MINIMAL')
        elif act == 'FORBID_CHANGE':
            encoded = ('forbid', f'change:{nid}')
        elif act != 'TRANSFORM_SCOPED':
            issues.append('UNSUPPORTED_ACTION:' + nid)
        if encoded and encoded[1] not in cgc[encoded[0]]:
            issues.append('CGC_DIRECTIVE_MISSING:' + nid)
        if a['relationship_lock'] and f'break_protected_relationships:{nid}' not in cgc['forbid']:
            issues.append('CGC_RELATIONSHIP_LOCK_MISSING:' + nid)
    if sorted(si['identity_anchors']) != sorted(sar2['identity_anchors']):
        issues.append('CGC_IDENTITY_MAPPING_MISMATCH')
    if sorted(si['unknown_locks']) != sorted(sar2['unknown_locks']):
        issues.append('CGC_UNKNOWN_MAPPING_MISMATCH')
    for c in constraints:
        if c['id'].startswith('action:'):
            c['value'] = actions.get(c['id'][7:], {}).get('action', 'UNRESOLVED')
        elif c['id'] == 'identity_anchors':
            c['value'] = sorted(si['identity_anchors'])
        elif c['id'] == 'source_identity':
            c['value'] = cgc['source_identity']
        c['cgc_ref'] = 'stable_cgc#/scene_intelligence'
        if c['id'].startswith(('node:', 'lock:', 'topology:', 'reference:')):
            c['cgc_ref'] = 'source_vsg (CGC source restriction)'
    for key in sorted(set(cgc) & POLICIES):
        c = _constraint('policy:' + key, 'POLICY', cgc[key], [])
        c['cgc_ref'] = 'stable_cgc#/' + key
        constraints.append(c)
    for key in DIRECTIVES:
        c = _constraint('directive:' + key, 'REQUIRED', sorted(set(cgc[key])), [])
        c['cgc_ref'] = 'stable_cgc#/' + key
        constraints.append(c)
    return constraints, sorted(set(issues))


def _weakened(source, target):
    if source is True and target is False:
        return True
    ranks = {'ABSOLUTE': 3, 'STRONG': 2, 'PR0': 3, 'PR1': 2, 'PR2': 1, 'PRX': 0,
             'PRESERVE_EXACT': 4, 'PRESERVE_CHARACTER': 3, 'PRESERVE_CONTEXT': 2,
             'PRESERVE_RELATIONSHIP': 2, 'TRANSFORM_SCOPED': 1,
             'STRICT': 3, 'NORMAL': 2, 'EXPLICIT_OVERRIDE': 1,
             'P0': 6, 'P1': 5, 'P2': 4, 'P3': 3, 'P4': 2}
    if isinstance(source, str) and isinstance(target, str):
        return (source in ranks and target in ranks and ranks[target] < ranks[source]) or (
            target in {'UNRESOLVED', 'UNKNOWN', 'PERMISSIVE', 'INFER_MINIMAL'} and source != target)
    if isinstance(source, dict) and isinstance(target, dict):
        return any(k not in target or
                   (k in {'min', 'minimum'} and isinstance(v, (int, float)) and isinstance(target[k], (int, float)) and target[k] < v) or
                   (k in {'max', 'maximum'} and isinstance(v, (int, float)) and isinstance(target[k], (int, float)) and target[k] > v) or
                   _weakened(v, target[k]) for k, v in source.items())
    if isinstance(source, list) and isinstance(target, list):
        return len(target) < len(source) or any(v not in target for v in source)
    return False


def classify(source, target):
    if source is None:
        return 'unauthorized_addition'
    if target is None:
        return 'omission'
    if source['priority'] != target['priority']:
        return 'weakening' if _weakened(source['priority'], target['priority']) else 'contradiction'
    if not set(source['lock_ids']) <= set(target['lock_ids']):
        return 'weakening'
    if set(target['lock_ids']) - set(source['lock_ids']):
        return 'unauthorized_addition'
    a, b = source['value'], target['value']
    if a == b:
        return 'equivalent'
    if source['id'].startswith('directive:') or source['id'] in {'identity_anchors', 'policy:occlusion_locks'}:
        return 'weakening' if any(x not in b for x in a) else 'unauthorized_addition'
    if _weakened(a, b):
        return 'weakening'
    if isinstance(a, dict) and isinstance(b, dict) and set(b) > set(a):
        return 'unauthorized_addition'
    return 'contradiction'


def compare_generation_contract(stable_cgc, contract, *, sar2, expected_graph,
                                candidate_graph, generation_context,
                                causal_trace=None, trace_artifacts=None):
    """PASS is evidence of preservation only; it never authorizes generation."""
    validation = validate_generation_contract(contract, vsg=candidate_graph, sar2=sar2,
        generation_context=generation_context, causal_trace=causal_trace, trace_artifacts=trace_artifacts)
    issues = list(validation['errors'])
    try:
        expected, baseline_issues = stable_constraints(stable_cgc, sar2=sar2, expected_graph=expected_graph)
        issues += baseline_issues
        source = index(expected); target = index(contract['constraints'])
    except (ValueError, KeyError, TypeError, jsonschema.ValidationError) as exc:
        issues.append('UNRESOLVED_REQUIRED_MAPPING:' + str(exc).splitlines()[0])
        source, target = {}, {}
    issues += contract.get('issues', [])
    rows = []
    for ident in sorted(set(source) | set(target)):
        a, b = source.get(ident), target.get(ident)
        rows.append({'constraint_id': ident, 'classification': classify(a, b),
            'priority': (a or b)['priority'], 'cgc_ref': a.get('cgc_ref') if a else None,
            'source_value': a['value'] if a else None, 'target_value': b['value'] if b else None,
            'expected_lock_ids': a['lock_ids'] if a else [], 'actual_lock_ids': b['lock_ids'] if b else [],
            'source_refs': deepcopy(a['source_refs']) if a else [],
            'target_refs': deepcopy(b['source_refs']) if b else [],
            'trace_event_ids': deepcopy(b['trace_event_ids']) if b else []})
    coverage = {}
    for priority in ('P0', 'PR0', 'PR1', 'LOCK'):
        required = [r for r in rows if r['constraint_id'] in source and r['priority'] == priority]
        preserved = sum(r['classification'] == 'equivalent' for r in required)
        coverage[priority] = {'required': len(required), 'preserved': preserved,
                              'ratio': preserved / len(required) if required else 1.0}
    counts = {k: sum(r['classification'] == k for r in rows) for k in
              ('equivalent', 'omission', 'weakening', 'contradiction', 'unauthorized_addition')}
    passed = not issues and bool(source) and all(r['classification'] == 'equivalent' for r in rows)
    report = {'schema_version': '2.0.0', 'mode': 'SHADOW', 'governs_generation': False,
        'status': 'PASS' if passed else 'FAIL', 'coverage': coverage, 'counts': counts,
        'unresolved_required_mappings': len(set(issues)), 'issues': sorted(set(issues)), 'results': rows,
        'stable_cgc_sha256': digest(normalize(stable_cgc)),
        'source_vsg_semantic_sha256': digest(graph_content(expected_graph)),
        'sar2_semantic_sha256': digest(normalize(sar2)), 'contract_sha256': contract.get('contract_sha256')}
    report['report_sha256'] = digest(report)
    return report


def render_comparison(report):
    text = [f"VSG-2A shadow preservation: {report['status']} (governs_generation=false)"]
    text += [f"{p}: {v['preserved']}/{v['required']}" for p, v in report['coverage'].items()]
    text += [f"{r['classification']}: {r['constraint_id']} ({r['cgc_ref']})"
             for r in report['results'] if r['classification'] != 'equivalent']
    text += report['issues']
    return '\n'.join(text)
