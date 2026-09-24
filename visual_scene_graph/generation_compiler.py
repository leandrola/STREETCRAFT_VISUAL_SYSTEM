"""VSG-2A: explicit-input, non-governing compilation. No runtime imports/calls.

VSG-1 omits SAR2 priorities/actions and request policies. Those are mandatory
sidecars, never inferred from node type or copied from the comparator's CGC.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from .graph_locks import build_graph_locks, validate_graph_locks
from .causal_trace import validate_causal_trace
from .diagnostic_benchmark.run_benchmark import build_scene_analysis_record
from scene_intelligence import project_scene_to_cgc

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.0.0'
# Only these named collections are sets. Property arrays (coordinates, matrices,
# polygon vertices, text fragments, etc.) retain their meaningful order.
SETS = {'nodes', 'edges', 'entities', 'relationships', 'action_plan', 'roles',
        'identity_anchors', 'unknown_locks', 'protected_relationships', 'entity_actions',
        'reference_need_hints', 'reference_observations', 'functional_subgraphs',
        'permitted_learning', 'forbidden_transfer', 'forbidden_transfers',
        'evidence_unit_ids', 'evidence_bundle_ids', 'applied_transfers',
        'source_invariants', 'preserve', 'transform', 'remove', 'infer', 'unknown',
        'forbid', 'occlusion_locks', 'protected_topology', 'warnings', 'items',
        'unclassified_nodes', 'unsupported_relations', 'dangling_relations',
        'constraints', 'source_refs', 'lock_ids', 'trace_event_ids', 'issues'}
DIRECTIVES = ('preserve', 'transform', 'remove', 'infer', 'unknown', 'forbid')
# Explicit policy sidecar is an acknowledged passthrough, never VSG evidence.
POLICIES = {'mode', 'profile', 'camera', 'semantic_text_lock', 'material_intensity_delta',
            'occlusion_locks', 'cil', 'aspect_ratio', 'street_presence',
            'reference_reasoning', 'reference_features', 'text_render_plan',
            'pre_generation_gate'}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def normalize(value, key=''):
    if isinstance(value, dict):
        return {k: normalize(v, k) for k, v in sorted(value.items())}
    if isinstance(value, list):
        out = [normalize(v) for v in value]
        return sorted(out, key=canonical_bytes) if key in SETS else out
    return value


def graph_content(graph):
    out = deepcopy(graph)
    # Observer's input hash and lock checksum are order-sensitive caches, not
    # scene semantics. Their underlying complete content is hashed below.
    out.get('provenance', {}).pop('input_sha256', None)
    out.get('graph_locks', {}).pop('ledger_sha256', None)
    return normalize(out)


def index(items, key='id'):
    out = {}
    for item in items:
        ident = item.get(key)
        if not isinstance(ident, str) or not ident or ident in out:
            raise ValueError('AMBIGUOUS_ID:' + str(ident))
        out[ident] = item
    return out


def ref(artifact, collection, ident):
    return {'artifact': artifact, 'collection': collection, 'id': ident}


def resolve_ref(reference, *, vsg, sar2, generation_context):
    name, collection, ident = (reference[k] for k in ('artifact', 'collection', 'id'))
    artifact = {'vsg': vsg, 'sar2': sar2, 'generation_context': generation_context}[name]
    if collection == '$':
        return artifact[ident]
    if collection == 'graph_locks':
        return index(artifact['graph_locks']['items'])[ident]
    key = {'entities': 'entity_id', 'relationships': 'relationship_id',
           'action_plan': 'entity_id', 'reference_observations': 'need_id'}.get(collection, 'id')
    return index(artifact[collection], key)[ident]


def _constraint(ident, priority, value, refs, locks=()):
    return {'id': ident, 'priority': priority, 'value': normalize(value),
            'source_refs': normalize(refs, 'source_refs'),
            'lock_ids': sorted(locks), 'trace_event_ids': []}


def validate_inputs(vsg, sar2, generation_context):
    import jsonschema
    schema = json.loads((ROOT/'schemas/visual-scene-graph-vsg1.schema.json').read_text())
    jsonschema.validate(vsg, schema)
    detail = json.loads((ROOT/'schemas/visual-scene-graph-vsg0.schema.json').read_text())
    for key in ('nodes', 'edges'):
        jsonschema.validate(vsg[key], detail['properties'][key])
    for key, ident in (('entities', 'entity_id'), ('relationships', 'relationship_id'), ('action_plan', 'entity_id')):
        index(sar2[key], ident)
    for key in ('nodes', 'edges'):
        index(vsg[key])
    index(vsg['graph_locks']['items'])
    index(vsg['reference_observations'], 'need_id')
    if sar2['scene_id'] != vsg['scene_id'] or sar2['source_identity'] != vsg['source_identity']:
        raise ValueError('SOURCE_IDENTITY_MISMATCH')
    if set(generation_context) != {'policies', 'directives'}:
        raise ValueError('EXPLICIT_CONTEXT_REQUIRED')
    policies = generation_context['policies']
    if set(policies) - POLICIES:
        raise ValueError('UNSUPPORTED_POLICY:' + ','.join(sorted(set(policies)-POLICIES)))
    if not {'mode', 'profile', 'camera', 'semantic_text_lock', 'material_intensity_delta', 'occlusion_locks'} <= set(policies):
        raise ValueError('MISSING_REQUIRED_POLICY')
    if set(generation_context['directives']) != set(DIRECTIVES):
        raise ValueError('EXPLICIT_DIRECTIVES_REQUIRED')
    for values in generation_context['directives'].values():
        if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
            raise ValueError('INVALID_DIRECTIVE')
    if policies['mode'] != sar2['mode'] or policies['profile'] != sar2['profile']:
        raise ValueError('SCENE_POLICY_MISMATCH')


def graph_constraints(vsg, sar2):
    entities = index(sar2['entities'], 'entity_id')
    actions = index(sar2['action_plan'], 'entity_id')
    nodes = index(vsg['nodes']); edges = index(vsg['edges'])
    locks = vsg['graph_locks']['items']
    constraints, issues = [], []
    for nid, node in sorted(nodes.items()):
        entity, action = entities.get(nid), actions.get(nid)
        priority = entity['preservation_level'] if entity else 'REQUIRED'
        refs = [ref('vsg', 'nodes', nid)]
        if not entity or not action:
            issues.append('UNRESOLVED_NODE_MAPPING:' + nid)
        else:
            refs += [ref('sar2', 'entities', nid), ref('sar2', 'action_plan', nid)]
        lock_ids = [l['id'] for l in locks if l['target'] == {'kind': 'NODE', 'id': nid}]
        constraints.append(_constraint('node:' + nid, priority,
            {**{k: deepcopy(v) for k, v in node.items() if k != 'id'},
             'cardinality': {'min': 1, 'max': 1},
             'source_attributes': {k: deepcopy(v) for k, v in (entity or {}).items()
                 if k not in {'entity_id', 'label', 'confidence', 'salience', 'text', 'vsg_properties'}}}, refs, lock_ids))
        constraints.append(_constraint('action:' + nid, priority,
            action['action'] if action else 'UNRESOLVED', refs, lock_ids))
        topology = [e for e in edges.values() if nid in {e['from'], e['to']} and e['protection'] in {'PR0', 'PR1'}]
        constraints.append(_constraint('topology:' + nid, priority, sorted(e['id'] for e in topology),
            refs + [ref('vsg', 'edges', e['id']) for e in topology], lock_ids))
        if node['epistemic_class'] == 'UNKNOWN' or node['type'] == 'unknown_region' or (action and action['action'] == 'UNKNOWN_LOCKED'):
            locked = bool(node['locks']['occlusion'] and action and action['action'] == 'UNKNOWN_LOCKED')
            constraints.append(_constraint('unknown:' + nid, 'REQUIRED',
                {'epistemic_class': node['epistemic_class'], 'locked': locked,
                 'action': action['action'] if action else 'UNRESOLVED'}, refs, lock_ids))
            if not locked:
                issues.append('UNKNOWN_NOT_LOCKED:' + nid)
    for eid, edge in sorted(edges.items()):
        refs = [ref('vsg', 'edges', eid)]
        for nid in (edge['from'], edge['to']):
            if nid in nodes:
                refs.append(ref('vsg', 'nodes', nid))
            else:
                issues.append('DANGLING_EDGE:' + eid + ':' + nid)
        lock_ids = [l['id'] for l in locks if l['target'] == {'kind': 'EDGE', 'id': eid}
                    or any(e['id'] == eid for e in l['expected'].get('protected_topology', []))]
        constraints.append(_constraint('edge:' + eid, edge['protection'],
            {k: deepcopy(v) for k, v in edge.items() if k != 'id'}, refs, lock_ids))
    for lock in locks:
        target = lock['target']; collection = 'nodes' if target['kind'] == 'NODE' else 'edges'
        refs = [ref('vsg', 'graph_locks', lock['id'])]
        if target['id'] in (nodes if collection == 'nodes' else edges):
            refs.append(ref('vsg', collection, target['id']))
        constraints.append(_constraint('lock:' + lock['id'], 'LOCK',
            {k: deepcopy(v) for k, v in lock.items() if k != 'id'}, refs, [lock['id']]))
    for obs in vsg['reference_observations']:
        constraints.append(_constraint('reference:' + obs['need_id'], 'REQUIRED', obs,
                                       [ref('vsg', 'reference_observations', obs['need_id'])]))
    constraints.append(_constraint('identity_anchors', 'REQUIRED',
        sorted(n['id'] for n in nodes.values() if n['locks']['identity']),
        [ref('vsg', 'nodes', n['id']) for n in nodes.values() if n['locks']['identity']]))
    constraints.append(_constraint('source_identity', 'REQUIRED', vsg['source_identity'],
                                   [ref('vsg', '$', 'source_identity')]))
    # Reuse VSG-1; additionally compare effective restrictions, not ledger caches.
    rebuilt = build_graph_locks(vsg)
    if normalize(rebuilt['items'], 'items') != normalize(locks, 'items'):
        issues.append('GRAPH_LOCK_LEDGER_INCONSISTENT')
    issues += [f['code'] + ':' + str(f['lock_id']) for f in validate_graph_locks(vsg)['findings']]
    issues += [w['code'] + ':' + w['target'] for w in rebuilt['summary']['warnings']]
    for field, values in vsg['diagnostics'].items():
        if values and field in {'unsupported_relations', 'dangling_relations'}:
            issues.append('UNRESOLVED_GRAPH_DIAGNOSTIC:' + field)
    return constraints, sorted(set(issues))


def projected_directives(vsg, sar2, context):
    nodes = index(vsg['nodes'])
    selected = deepcopy(sar2)
    selected['entities'] = [dict(e, label=nodes[e['entity_id']]['label']) for e in sar2['entities'] if e['entity_id'] in nodes]
    selected['action_plan'] = [a for a in sar2['action_plan'] if a['entity_id'] in nodes]
    selected['relationships'] = []  # directives depend on the explicit action plan
    base = deepcopy(context['directives'])
    result = project_scene_to_cgc(base, selected)
    return {k: sorted(set(result[k])) for k in DIRECTIVES}


def seal(contract):
    result = normalize({k: v for k, v in contract.items() if k != 'contract_sha256'})
    result['contract_sha256'] = digest(result)
    return result


def compile_generation_contract(vsg, *, sar2, generation_context, causal_trace=None, trace_artifacts=None):
    """Compile supplied snapshots; no CGC, adapter, preflight or readiness mutation."""
    validate_inputs(vsg, sar2, generation_context)
    constraints, issues = graph_constraints(vsg, sar2)
    directives = projected_directives(vsg, sar2, generation_context)
    for key, value in generation_context['policies'].items():
        constraints.append(_constraint('policy:' + key, 'POLICY', value,
                                       [ref('generation_context', '$', 'policies')]))
    for key, value in directives.items():
        refs = [ref('generation_context', '$', 'directives')]
        refs += [ref('sar2', 'action_plan', a['entity_id']) for a in sar2['action_plan'] if a['entity_id'] in index(vsg['nodes'])]
        constraints.append(_constraint('directive:' + key, 'REQUIRED', value, refs))
    trace_provenance = None
    if causal_trace is not None:
        if trace_artifacts is None or validate_causal_trace(causal_trace, trace_artifacts)['status'] != 'PASS':
            raise ValueError('INVALID_CAUSAL_TRACE')
        if causal_trace['status'] == 'INCOMPLETE' or (graph_content(trace_artifacts['vsg']) != graph_content(vsg)
                or normalize(trace_artifacts['sar2']) != normalize(sar2)):
            raise ValueError('CAUSAL_TRACE_SOURCE_MISMATCH')
        trace_provenance = {'trace_id': causal_trace['trace_id'], 'trace_sha256': causal_trace['trace_sha256']}
        for c in constraints:
            ids = {r['id'] for r in c['source_refs'] if r['artifact'] == 'vsg'}
            c['trace_event_ids'] = sorted(e['event_id'] for e in causal_trace['events']
                                          if e['stage'] in {'VSG', 'GRAPH_LOCKS'} and e['artifact_id'] in ids)
    return seal({'schema_version': VERSION, 'artifact_kind': 'VSG_GENERATION_CONTRACT',
        'mode': 'SHADOW', 'governs_generation': False, 'scene_id': vsg['scene_id'],
        'status': 'INCOMPLETE' if issues else 'COMPILED', 'constraints': constraints, 'issues': issues,
        'provenance': {'vsg_semantic_sha256': digest(graph_content(vsg)),
                       'sar2_semantic_sha256': digest(normalize(sar2)),
                       'context_sha256': digest(normalize(generation_context)), 'causal_trace': trace_provenance}})


def validate_generation_contract(contract, *, vsg, sar2, generation_context, causal_trace=None, trace_artifacts=None):
    errors = []
    try:
        import jsonschema
        jsonschema.validate(contract, json.loads((ROOT/'schemas/vsg-generation-contract.schema.json').read_text()))
        index(contract['constraints'])
        if seal(contract) != contract:
            errors.append('CONTRACT_HASH_OR_CANONICAL_ORDER')
        for c in contract['constraints']:
            for r in c['source_refs']:
                resolve_ref(r, vsg=vsg, sar2=sar2, generation_context=generation_context)
        replay = compile_generation_contract(vsg, sar2=sar2, generation_context=generation_context,
                                            causal_trace=causal_trace, trace_artifacts=trace_artifacts)
        if replay != contract:
            errors.append('CONTRACT_REPLAY_MISMATCH')
    except (ValueError, KeyError, TypeError, jsonschema.ValidationError) as exc:
        errors.append('INVALID_CONTRACT:' + str(exc).splitlines()[0])
    return {'status': 'FAIL' if errors else 'PASS', 'errors': errors}
