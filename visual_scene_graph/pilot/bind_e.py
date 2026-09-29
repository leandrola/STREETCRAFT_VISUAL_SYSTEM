"""Prospective E creation/replay; no admission, Archive retrieval or generation."""
from copy import deepcopy
import argparse
import json

from integration.streetcraft_orchestrator import orchestrate
from ..generation_compiler import DIRECTIVES, POLICIES, compile_generation_contract, digest
from ..generation_comparator import compare_generation_contract
from ..vsg_observer import build_visual_scene_graph
from .harness import ROOT, image_valid, sha, validate
from .fixture_replay import verify_snapshots

FIXTURE = ROOT / 'visual_scene_graph/pilot/fixtures/r2b_e_new_01'
SOURCE_SHA256 = 'f0ba6e1f5bb5e3f40f39c0847f3d980e25c8c110b15b932cb1b3a10984a62860'
PRIORITIES = ['P0', 'PR0', 'LOCK']  # PR1 is explicitly unexercised.


def empty_retriever(request):
    raise ValueError('UNEXPECTED_ARCHIVE_QUERY: E permits no reference fill')


def check_occlusion(runtime, graph):
    """Check effective unknown action and edge ledger without assuming node type."""
    hidden = next(n for n in graph['nodes'] if n['id'] == 'hidden_01')
    action = next(a for a in runtime['sar2']['action_plan'] if a['entity_id'] == 'hidden_01')
    if (action['action'] != 'UNKNOWN_LOCKED' or not hidden['locks']['occlusion']
            or hidden['observed'] or hidden['epistemic_class'] != 'UNKNOWN'):
        raise ValueError('E_UNKNOWN_NOT_LOCKED')
    edge = next(e for e in graph['edges'] if e['id'] == 'rel_foreground_occludes_unknown')
    if (edge['from'], edge['to'], edge['type'], edge['protection']) != (
            'occluder_01', 'hidden_01', 'OCCLUDES', 'PR0'):
        raise ValueError('E_OCCLUSION_ENDPOINT_MISMATCH')
    lock = next((l for l in graph['graph_locks']['items'] if l['type'] == 'OCCLUSION_LOCK'
                 and l['target'] == {'kind': 'EDGE', 'id': edge['id']}), None)
    if (not lock or lock['strength'] != 'ABSOLUTE'
            or lock['expected']['edge'] != {k: edge[k] for k in ('id', 'type', 'from', 'to')}
            or lock['provenance']['evidence'] != edge['evidence']):
        raise ValueError('E_OCCLUSION_LEDGER_MISMATCH')
    cgc = runtime['cgc_final']
    if ('hidden_01' not in cgc['occlusion_locks'] or cgc['infer']
            or 'resolve_exact_unknown:hidden_01' not in cgc['forbid']):
        raise ValueError('E_UNAUTHORIZED_RECONSTRUCTION')


def reconstruct():
    request = json.loads((FIXTURE / 'request.json').read_text())
    source = json.loads((FIXTURE / 'source_provenance.json').read_text())['source']
    raw = (ROOT / source['path']).read_bytes()
    if sha(raw) != SOURCE_SHA256 or source['sha256'] != SOURCE_SHA256:
        raise ValueError('SOURCE_HASH_MISMATCH')
    if image_valid(raw) != {'format': 'JPEG', 'width': 500, 'height': 454}:
        raise ValueError('SOURCE_DIMENSIONS_MISMATCH')
    runtime = orchestrate(request, archive_retriever=empty_retriever)
    if runtime['status'] != 'GENERATION_READY' or runtime['pre_generation_gate']['status'] != 'PASS':
        raise ValueError('ORCHESTRATION_NOT_READY')
    rr = runtime['reference_reasoning']
    needs = runtime['reference_needs']
    if (len(needs) != 1 or needs[0]['state'] != 'RN_BLOCKED'
            or needs[0]['target_entity_id'] != 'hidden_01' or rr['queries'] != 0
            or rr['admissions'] or rr['generation_projection']
            or rr['need_results'] != {'SAR2-hidden_01': 'LOCKED_UNKNOWN'}):
        raise ValueError('UNEXPECTED_REFERENCE_ACTIVITY')
    cgc, sar2 = runtime['cgc_final'], runtime['sar2']
    graph = build_visual_scene_graph(sar2, reference_reasoning=rr, reference_needs=needs)
    check_occlusion(runtime, graph)
    context = {'policies': {k: deepcopy(v) for k, v in cgc.items() if k in POLICIES},
               'directives': {k: deepcopy(request.get(k, [])) for k in DIRECTIVES}}
    candidate = deepcopy(graph)  # Equivalent input, not an observed generated result.
    contract = compile_generation_contract(candidate, sar2=sar2, generation_context=context)
    comparison = compare_generation_contract(cgc, contract, sar2=sar2,
        expected_graph=graph, candidate_graph=candidate, generation_context=context)
    if comparison['status'] != 'PASS' or comparison['unresolved_required_mappings']:
        raise ValueError('COMPARISON_FAILED:' + repr(comparison['issues']))
    for priority in PRIORITIES:
        coverage = comparison['coverage'][priority]
        if not coverage['required'] or coverage['preserved'] != coverage['required']:
            raise ValueError('EMPTY_OR_INCOMPLETE_COVERAGE:' + priority)
    return {'runtime': runtime, 'sar2': sar2, 'rr2': rr, 'cgc_final': cgc,
            'expected_graph': graph, 'candidate_graph': candidate,
            'generation_context': context, 'contract': contract}, comparison


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def make_manifest(snapshots):
    provenance_path = FIXTURE / 'source_provenance.json'
    provenance = json.loads(provenance_path.read_text())
    source = provenance['source']
    request = json.loads((FIXTURE / 'request.json').read_text())
    entities = {e['entity_id']: e for e in request['scene']['entities']}
    criteria = {
        'left_facades_01': 'Preserve visible left facade outlines, openings and camera placement; do not extrapolate beyond the crop.',
        'right_facades_01': 'Preserve visible right facade outlines, openings and camera placement; do not extrapolate beyond the crop.',
        'occluder_01': 'Preserve the observed dark textured foreground surface, silhouette and position. No removal, displacement, shrinking or transparency that reveals behind it; physical identity unassigned.',
        'hidden_01': 'Keep behind-silhouette content UNKNOWN_LOCKED. No exact object, text, facade, vehicle or geometry may be revealed. Region is a screen-space review mask, not hidden geometry.',
    }
    rubric = []
    # Include unknown/action/topology and policy constraints even when not P0/LOCK.
    for c in snapshots['contract']['constraints']:
        cid = c['id']
        if cid.startswith(('node:', 'action:', 'topology:', 'unknown:')):
            target = cid.split(':', 1)[1]
            criterion = criteria[target] + ' Source region ' + repr(entities[target]['region']) + '.'
            category = 'lock' if target == 'hidden_01' else 'identity'
        elif cid.startswith(('edge:', 'lock:')):
            target = cid
            criterion = ('Preserve occluder_01 OCCLUDES hidden_01 within [0.496,0.819,0.790,0.969]; '
                         'retain facade geometry where targeted. Preserve every protected endpoint; no specific hidden content or reference fill.')
            category = 'lock' if cid.startswith('lock:') else 'relation'
        elif cid in {'directive:forbid', 'directive:infer', 'policy:occlusion_locks',
                     'policy:reference_reasoning', 'policy:semantic_text_lock'}:
            target, category = 'whole source / hidden_01', 'unauthorized_change'
            criterion = ('No exact hidden reconstruction, minimum-continuity synthesis or reference-derived fill is authorized. '
                         'Keep ambiguous text unresolved; do not treat darkness, clipping or low resolution as observed hidden objects.')
        else:
            continue
        rubric.append(dict(constraint_id=cid, category=category, priority=c['priority'], target=target, criterion=criterion))
    rubric.extend([
        dict(constraint_id='identity', category='identity', priority='REQUIRED', target='whole source',
             criterion='Retain this street corridor, visible facade composition, lighting, vehicle and traffic lights; hold the source camera.'),
        dict(constraint_id='unauthorized_change', category='unauthorized_change', priority='REQUIRED', target='whole source / hidden_01',
             criterion='No new hidden content or reference fill (S3), invented readable microtext, camera change, occluder removal or unsupported extension beyond the crop.')])
    artifacts = {}
    for name in ('request', *snapshots, 'source'):
        path = ROOT / source['path'] if name == 'source' else FIXTURE / (name + '.json')
        raw = encoded(snapshots[name]) if name in snapshots else path.read_bytes()
        artifacts[name] = dict(path=str(path.relative_to(ROOT)), sha256=sha(raw),
            provenance=('Original repository JPEG, unchanged; photographer/capture date UNKNOWN.' if name == 'source' else
                        'Prospective E annotation/orchestration of 2026-09-29; same new request, not recovered historical snapshots. '
                        'RR2: one RN_BLOCKED hint, zero queryable needs, queries, admissions or projections. Candidate is equivalent input, not output-image evidence.'))
    manifest = dict(schema_version='1.0.0', fixture_id='R2B-191-E', pilot_enabled=True,
        source_binding=dict(source_identity=request['scene']['source_identity'],
            attested_by='Codex — current native-resolution inspection and prospective annotation, 2026-09-29',
            evidence=f"New VSG2B-R2B-E-NEW-01; no historical recovery. Source {source['path']} SHA-256 {source['sha256']} (JPEG 500x454). Region-specific facts, uncertainties and checklist: {provenance_path.relative_to(ROOT)} SHA-256 {sha(provenance_path.read_bytes())}. Observed dark foreground silhouette blocks behind-content visibility; physical identity unassigned, hidden content UNKNOWN. Photographer/capture date UNKNOWN."),
        artifacts=artifacts, required_priorities=PRIORITIES,
        generation=dict(provider='DRY_RUN_ONLY_UNSELECTED_PROVIDER', model='DRY_RUN_ONLY_UNSELECTED_MODEL', seed=None,
                        parameters=dict(size='500x454', quality='DRY_RUN_ONLY_UNSELECTED', output_format='png')),
        rubric=rubric)
    validate(manifest, 'manifest')
    return manifest


def verify_d_preserved():
    provenance = json.loads((FIXTURE / 'source_provenance.json').read_text())
    record = provenance['d_preservation_baseline']
    raw = (ROOT / record['path']).read_bytes()
    if sha(raw) != record['sha256']:
        raise ValueError('D_BASELINE_HASH_MISMATCH')
    baseline = json.loads(raw)
    for name, expected in baseline['files'].items():
        if sha((ROOT / name).read_bytes()) != expected:
            raise ValueError('D_FROZEN_ARTIFACT_CHANGED:' + name)
    return baseline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true', help='Exclusive initial creation; never overwrite')
    args = parser.parse_args()
    verify_d_preserved()
    if args.freeze:
        snapshots, comparison = reconstruct()
        manifest = make_manifest(snapshots)
        files = {name + '.json': encoded(value) for name, value in snapshots.items()}
        files['manifest.json'] = encoded(manifest)
        if any((FIXTURE / name).exists() for name in files):
            raise FileExistsError('E_ALREADY_FROZEN: use replay or a new fixture version')
        for name, raw in files.items():
            with (FIXTURE / name).open('xb') as handle:
                handle.write(raw)
    else:
        manifest, comparison = verify_snapshots(FIXTURE, reconstruct)
        snapshots = {k: json.loads((ROOT / r['path']).read_text()) for k, r in manifest['artifacts'].items()
                     if k not in {'request', 'source'}}
        if manifest != make_manifest(snapshots):
            raise ValueError('E_MANIFEST_REPLAY_MISMATCH')
    print(json.dumps({'status': 'FROZEN' if args.freeze else 'PASS', 'manifest_sha256': digest(manifest),
                      'coverage': comparison['coverage'], 'reference_needs': 1, 'queryable_needs': 0,
                      'archive_calls': 0, 'd_preserved': True}))


if __name__ == '__main__':
    main()
