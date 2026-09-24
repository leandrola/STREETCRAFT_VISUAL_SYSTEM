"""Controlled VSG-2A faults over the actual stable Kenny's CGC."""
from copy import deepcopy
import json
import sys

from .generation_compiler import ROOT, DIRECTIVES, POLICIES, compile_generation_contract, digest, seal
from .generation_comparator import compare_generation_contract
from .causal_trace import build_causal_trace
from .causal_cases import complete_artifacts
from .diagnostic_benchmark.run_benchmark import _contract_from_vsg

sys.path.insert(0, str(ROOT/'integration'))
from streetcraft_orchestrator import orchestrate


def retriever(request):
    return {'evidence_bundle_id': 'EB-ROOF', 'items': [{
        'evidence_unit_id': 'EU-ROOF', 'archive_id': 'VSG2A-CONTROLLED',
        'status': 'CLASSIFIED', 'domain': 'MATERIALS', 'provenance_level': 'P3',
        'transfer_risk': 'LOW', 'visible_fact': 'restrained rooftop material',
        'permitted_learning': ['material family'],
        'forbidden_transfer': ['exact geometry', 'source signage']}],
        'conflicts': [], 'negative_evidence': []}


def base_inputs():
    scene = json.loads((ROOT/'visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json').read_text())
    scene['scene_id'] = 'VSG2A-KENNYS-SHADOW'
    scene['entities'].append({'entity_id': 'hidden_01', 'label': 'unseen rear region',
        'kind': 'OCCLUDED_REGION', 'roles': ['UNKNOWN_REGION'], 'preservation_level': 'P5-D',
        'epistemic_class': 'UNKNOWN', 'confidence': 'LOW', 'observed': False, 'salience': {}})
    request = {'command_text': '/sc-2a', 'scene': scene, 'vsg': {'mode': 'OBSERVER'},
        'reference_needs': [{'need_id': 'N-ROOF', 'state': 'RN_REQUIRED',
            'target_domains': ['MATERIALS'], 'specific_problem': 'roof material behavior',
            'task_context': 'controlled shadow benchmark', 'source_context': 'Kenny rooftop',
            'target_entity_id': 'roof_01', 'min_provenance': 'P2', 'max_transfer_risk': 'LOW',
            'source_invariants': ['geometry preserved'], 'forbidden_transfers': ['exact geometry']}]}
    runtime = orchestrate(request, archive_retriever=retriever)
    if runtime['status'] != 'GENERATION_READY':
        raise ValueError('Fixture not ready: ' + runtime['status'])
    cgc = runtime['cgc_final']
    # Non-scene policies are captured explicitly, including actual RR2/preflight
    # data. Scene directives are independently supplied request directives.
    context = {'policies': {k: deepcopy(v) for k, v in cgc.items() if k in POLICIES},
               'directives': {k: deepcopy(request.get(k, [])) for k in DIRECTIVES}}
    return {'request': request, 'runtime': runtime, 'stable_cgc': cgc, 'sar2': runtime['sar2'],
            'expected_graph': runtime['visual_scene_graph'], 'generation_context': context}


def trace_inputs(base):
    graph = base['expected_graph']
    shadow = _contract_from_vsg(graph)
    shadow['required_locks'] = [l['id'] for l in graph['graph_locks']['items']]
    return complete_artifacts({'expected_graph': graph, 'sar2': base['sar2'],
        'reference_reasoning': base['runtime']['reference_reasoning'], 'vsg': graph,
        'shadow_contract': shadow, 'observed_output_graph': deepcopy(graph)})


def run_case(case, base):
    graph = deepcopy(base['expected_graph']); context = deepcopy(base['generation_context'])
    sar2 = deepcopy(base['sar2']); cgc = deepcopy(base['stable_cgc'])
    original = digest(base)
    node = lambda nid: next(n for n in graph['nodes'] if n['id'] == nid)
    edge = lambda eid: next(e for e in graph['edges'] if e['id'] == eid)
    op = case['mutation']
    trace, artifacts = None, None
    if op == 'missing_p0':
        graph['nodes'] = [n for n in graph['nodes'] if n['id'] != 'sign_01']
    elif op == 'weak_p0':
        node('sign_01')['locks']['semantic'] = False
    elif op == 'missing_pr0':
        graph['edges'] = [e for e in graph['edges'] if e['id'] != 'rel_sign_attached']
    elif op == 'weak_pr1':
        edge('rel_hvac_behind')['protection'] = 'PR2'
    elif op == 'contradiction':
        node('sign_01')['properties']['text'] = 'OTHER SHOP'
    elif op == 'addition':
        n = deepcopy(node('hvac_01')); n['id'] = 'hvac_extra'; graph['nodes'].append(n)
    elif op == 'removed_lock':
        graph['graph_locks']['items'] = [l for l in graph['graph_locks']['items'] if l['id'] != 'GL-SEM-SIGN_01']
    elif op == 'weak_lock':
        next(l for l in graph['graph_locks']['items'] if l['id'] == 'GL-SEM-SIGN_01')['strength'] = 'STRONG'
    elif op == 'permissive_unknown':
        node('hidden_01')['locks']['occlusion'] = False
    elif op == 'resolved_unknown':
        node('hidden_01')['epistemic_class'] = 'OBSERVED'
    elif op == 'reorder':
        for key in ('nodes', 'edges', 'functional_subgraphs', 'reference_observations'):
            graph[key].reverse()
        graph['graph_locks']['items'].reverse()
        for l in graph['graph_locks']['items']:
            if 'protected_topology' in l['expected']: l['expected']['protected_topology'].reverse()
        for key in ('entities', 'relationships', 'action_plan', 'identity_anchors', 'unknown_locks'):
            sar2[key].reverse()
        for a in sar2['action_plan']: a['protected_relationships'].reverse()
        # The observer's original-order cache may legitimately change.
        graph['provenance']['input_sha256'] = '0'*64
    elif op == 'trace':
        artifacts = trace_inputs(base); trace = build_causal_trace(**artifacts)
    elif op == 'policy':
        context['policies']['semantic_text_lock'] = 'NORMAL'
    elif op == 'topology':
        edge('rel_hvac_behind')['to'] = 'building_01'
    elif op == 'reference_leak':
        next(o for o in graph['reference_observations'] if o['need_id'] == 'N-ROOF')['applied_transfers'] = ['exact geometry']
    elif op == 'ambiguous':
        cgc['scene_intelligence']['entity_actions'].append(deepcopy(cgc['scene_intelligence']['entity_actions'][0]))
    contract = compile_generation_contract(graph, sar2=sar2, generation_context=context,
                                          causal_trace=trace, trace_artifacts=artifacts)
    if op in {'weak_action', 'detach_lock', 'cardinality', 'tamper_lineage'}:
        by_id = {c['id']: c for c in contract['constraints']}
        if op == 'weak_action': by_id['action:sign_01']['value'] = 'PRESERVE_CHARACTER'
        elif op == 'detach_lock': by_id['node:sign_01']['lock_ids'] = []
        elif op == 'cardinality': by_id['topology:building_01']['value'] = []
        elif op == 'tamper_lineage': by_id['node:sign_01']['source_refs'][0]['id'] = 'not-present'
        contract = seal(contract)
    report = compare_generation_contract(cgc, contract, sar2=sar2,
        expected_graph=base['expected_graph'], candidate_graph=graph, generation_context=context,
        causal_trace=trace, trace_artifacts=artifacts)
    checks = {'gate': report['status'] == case['expected_status'], 'inputs_unchanged': original == digest(base)}
    if 'constraint_id' in case:
        checks['precise_diagnostic'] = any(r['constraint_id'] == case['constraint_id'] and
            r['classification'] == case['classification'] for r in report['results'])
    if 'issue' in case:
        checks['precise_issue'] = any(case['issue'] in i for i in report['issues'])
    if op == 'reorder':
        checks['reorder_byte_stable'] = contract == compile_generation_contract(base['expected_graph'],
            sar2=base['sar2'], generation_context=base['generation_context'])
    if op == 'many_to_one':
        c = next(c for c in contract['constraints'] if c['id'] == 'topology:building_01')
        checks['multiple_sources'] = len([r for r in c['source_refs'] if r['collection'] == 'edges']) >= 2
    if op == 'one_to_many':
        checks['multiple_constraints'] = sum(any(r['id'] == 'sign_01' and r['artifact'] == 'vsg' for r in c['source_refs'])
                                                for c in contract['constraints']) >= 3
    if op == 'trace':
        checks['verified_trace_links'] = trace['status'] == 'HEALTHY' and all(
            c['trace_event_ids'] for c in contract['constraints'] if c['id'].startswith(('node:', 'edge:', 'lock:')))
    if op == 'generator':
        checks['generator_unchanged'] = orchestrate(base['request'], archive_retriever=retriever) == base['runtime']
    return {'case_id': case['case_id'], 'status': 'PASS' if all(checks.values()) else 'FAIL',
            'checks': checks, 'expected_status': case['expected_status'], 'comparison': report,
            'contract': contract}


def run_generation_cases():
    cases = json.loads((ROOT/'visual_scene_graph/fixtures/generation_compiler_cases.json').read_text())['cases']
    base = base_inputs()
    results = [run_case(case, base) for case in cases]
    return {'suite': 'VSG-2A Generation Compiler Shadow', 'mode': 'SHADOW', 'governs_generation': False,
        'status': 'PASS' if all(r['status'] == 'PASS' for r in results) else 'FAIL',
        'cases': len(results), 'passed': sum(r['status'] == 'PASS' for r in results),
        'healthy_control_false_positives': sum(r['comparison']['status'] != 'PASS' for r in results if r['expected_status'] == 'PASS'),
        'healthy_coverage': results[0]['comparison']['coverage'], 'results': results}


def stored_cgc_snapshots():
    """Replay five persisted final CGCs without querying the external Archive.

    Global policies/request directives are captured passthroughs. The VSG scene
    projection is independently built from each persisted SAR2/RR2 snapshot.
    Blocked-reference records have no final CGC and are explicitly unavailable.
    """
    from .vsg_observer import build_visual_scene_graph
    from .generation_compiler import project_scene_to_cgc
    rows = []
    for path in sorted((ROOT/'validation/cgc_e2e/results').glob('*.json')):
        runtime = json.loads(path.read_text())
        if 'cgc_final' not in runtime:
            rows.append({'case_id': path.stem, 'status': 'UNAVAILABLE',
                         'reason': 'No stable final CGC: ' + runtime['status']})
            continue
        sar2, cgc = runtime['sar2'], runtime['cgc_final']
        graph = build_visual_scene_graph(sar2, reference_reasoning=runtime['reference_reasoning'],
                                        reference_needs=runtime['reference_needs'])
        scene_directives = project_scene_to_cgc({k: [] for k in DIRECTIVES}, sar2)
        context = {'policies': {k: deepcopy(v) for k, v in cgc.items() if k in POLICIES},
                   'directives': {k: [v for v in cgc[k] if v not in scene_directives[k]] for k in DIRECTIVES}}
        contract = compile_generation_contract(graph, sar2=sar2, generation_context=context)
        report = compare_generation_contract(cgc, contract, sar2=sar2,
            expected_graph=graph, candidate_graph=graph, generation_context=context)
        rows.append({'case_id': path.stem, 'status': report['status'], 'comparison': report})
    return rows
