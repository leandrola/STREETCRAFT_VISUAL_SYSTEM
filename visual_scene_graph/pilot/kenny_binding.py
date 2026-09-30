"""K1 authority boundary. Versioned pins are admission authority, not observations.

No provider or Archive access. The same frozen-byte verifier runs on replay,
prepare, execution and persisted review; design never enters the source graph.
"""
from copy import deepcopy
from io import BytesIO
import hashlib
import json
from pathlib import Path

from PIL import Image
from ..generation_compiler import ROOT, DIRECTIVES, POLICIES, canonical_bytes

FIXTURE = ROOT / 'visual_scene_graph/pilot/fixtures/kennys_new_01'
IDENT = 'KENNYS-ROOFTOP'
SOURCE_PATH = 'visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg'
SOURCE_SHA = '45b8bff5c33ea411ffef3c88db99d757ce462a7f13b56df3f2fbc62b994357b2'
SOURCE_ID = 'KENNYS_SOURCE_SHA256_' + SOURCE_SHA
VERSION = 'KENNYS_ROOFTOP_DESIGN_V1'
# Changes require a new reviewed binding version, not merely rehashed input.
RECORDS = {
    'k0.md': ('visual_scene_graph/pilot/fixtures/kennys/K0_OBSERVED_INFERRED_DESIGN.md', 'ed8f17f1204d041d47f0618378e7056b9d0d95fc4b67aa9d4203003b75194f90'),
    'reception.json': ('visual_scene_graph/pilot/fixtures/kennys/reception.json', '9ef38ea1a63d5d31f6542c888b336b4356dcdbf43822cfb5055b73d0604fb456'),
    'observations.json': ('visual_scene_graph/pilot/fixtures/kennys_new_01/observations.json', 'd9fd45e27f5ae76c4ce0de39ae732031077d1e776e3c2c0fad1d45d5763779b2'),
    'design.json': ('visual_scene_graph/pilot/fixtures/kennys_new_01/design.json', 'c09e93d07aebd51203e08d385a82c49918f318e47f60f51f3b672077cd98ee4e'),
    'source_provenance.json': ('visual_scene_graph/pilot/fixtures/kennys_new_01/source_provenance.json', 'ed153e4ea87eaa031a483e8ae12d670b6e5c2d142924e4d944dc511425a92adc'),
    'preservation_baseline.json': ('visual_scene_graph/pilot/fixtures/kennys_new_01/preservation_baseline.json', 'c2ea9832a4705caafb6b07564235996a7da90c8e97c498b6c2fd797ccc9e83d7'),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, code):
    if not condition:
        raise ValueError('K1_' + code)


def binding_records():
    return {name: {'path': path, 'sha256': checksum} for name, (path, checksum) in RECORDS.items()}


def applies(manifest, blobs):
    request = json.loads(blobs['request'])
    return (manifest['fixture_id'] == IDENT or sha(blobs['source']) == SOURCE_SHA
            or 'k1_binding' in request or request.get('scene', {}).get('source_identity') == SOURCE_ID)


def load_sidecars(request, root=ROOT, persisted=None):
    require(request.get('k1_binding') == binding_records(), 'BINDING_RECORDS_CHANGED')
    result = {}
    for name, (path, checksum) in RECORDS.items():
        p = Path(persisted) / 'sidecars' / name if persisted is not None else Path(root) / path
        require(p.resolve().is_relative_to(Path(persisted if persisted is not None else root).resolve()), 'SIDECAR_OUTSIDE_ROOT')
        try:
            result[name] = p.read_bytes()
        except OSError as exc:
            raise ValueError('K1_MISSING_SIDECAR:' + name) from exc
        require(sha(result[name]) == checksum, 'SIDECAR_HASH:' + name)
    return result


def verify_design(d):
    require(d['design_version'] == VERSION and d['authority'] == 'AUTHORIZED_INFERENCE', 'DESIGN_AUTHORITY')
    require(d['source_binding']['sha256'] == SOURCE_SHA and d['source_binding']['path'] == SOURCE_PATH, 'DESIGN_SOURCE')
    require(d['external_anchors'] == ['ks_facade'], 'EXTERNAL_ANCHORS')
    nodes = d['nodes']
    require(len(nodes) == 3 and {n['id'] for n in nodes} == {'kd_roof', 'kd_parapet', 'kd_hvac'}, 'DESIGN_COMPONENTS')
    require(all(n['observed'] is False and n['epistemic_class'] == 'AUTHORIZED_INFERENCE'
                and n['requirement'] == 'REQUIRED' and 'preservation_level' not in n for n in nodes), 'DESIGN_OBSERVED_OR_PRIORITY')
    expected = [('KDR-01', 'kd_roof', 'ABOVE', 'ks_facade'),
                ('KDR-02', 'kd_parapet', 'PART_OF', 'kd_roof'),
                ('KDR-03', 'kd_hvac', 'PART_OF', 'kd_roof'),
                ('KDR-04', 'kd_hvac', 'BEHIND', 'kd_parapet')]
    rels = d['relationships']
    require(sorted((r['id'], r['subject'], r['predicate'], r['object']) for r in rels) == expected, 'DESIGN_RELATIONSHIPS')
    require(all(r['authority'] == 'AUTHORIZED_INFERENCE' and r['requirement'] == 'REQUIRED'
                and 'protection' not in r for r in rels), 'DESIGN_RELATION_AUTHORITY')
    require(d['excluded_components'] == ['kd_skylight', 'chimney', 'water_tank', 'access_bulkhead'], 'EXCLUSIONS')
    require(d['authority_records'] == {k: binding_records()[name] for k, name in [('k0', 'k0.md'), ('reception', 'reception.json')]}, 'DESIGN_AUTHORITY_RECORDS')


def design_directives(d):
    """Explicit original instructions, not SAR2 INFER_MINIMAL or source evidence."""
    prefix = VERSION + ':AUTHORIZED_INFERENCE:'
    infer = [prefix + 'node:' + canonical_bytes(n).decode() for n in d['nodes']]
    infer += [prefix + 'relation:' + canonical_bytes(r).decode() for r in d['relationships']]
    infer += [prefix + key + ':' + value for key, value in sorted(d['visual_rules'].items())]
    infer += [prefix + 'presentation:' + canonical_bytes(d['presentation']).decode()]
    forbid = [prefix + 'forbid:' + value for value in d['prohibitions']]
    forbid += [prefix + 'excluded:' + canonical_bytes(d['excluded_components']).decode()]
    return infer, forbid


def make_request(obs, design):
    verify_design(design)
    kinds = ['FACADE', 'WINDOW', 'SIGNAGE', 'SIGNAGE', 'STOREFRONT', 'DOOR',
             'STOREFRONT', 'SURFACE', 'FACADE', 'SURFACE', 'SURFACE']
    levels = ['P0'] * 7 + ['P1', 'P1', 'P2', 'P2']
    entities = []
    for claim, kind, level in zip(obs['claims'][:11], kinds, levels):
        ident = claim['entity_id']
        entity = dict(entity_id=ident, label=claim['visible_fact'], kind=kind,
            roles=['IDENTITY_ANCHOR'] if ident in {'ks_facade', 'ks_main_sign', 'ks_banner'} else ['CONTEXTUAL_SUPPORT'],
            preservation_level=level, epistemic_class='OBSERVED', observed=True,
            confidence='HIGH', salience={}, region=claim['regions'][0],
            reference_id=SOURCE_ID, evidence_id=claim['claim_id'], authority='OBSERVED_SOURCE')
        if len(claim['regions']) > 1:
            entity['vsg_properties'] = {'visible_regions': claim['regions']}
        if ident in {'ks_main_sign', 'ks_banner'}:
            entity.update(text=claim['literal_record'], semantic_lock=True)
        entities.append(entity)
    by_id = {e['entity_id']: e for e in entities}
    relationships = deepcopy(obs['relationships'])
    for r in relationships:
        boxes = [by_id[r[k]]['region'] for k in ('subject', 'object')]
        r.update(region=[min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)],
                 reference_id=SOURCE_ID, evidence_id=r['relationship_id'], authority='OBSERVED_SOURCE')
    infer, forbid = design_directives(design)
    # Freeze CIL's source/unknown prohibitions as original directives too; the
    # shadow compiler does not independently expand CIL into directives.
    forbid += ['replace_observed_evidence', 'resolve_locked_unknown_without_evidence']
    tokens = [dict(token_id=e['entity_id'], literal=e['text'], confidence=.99,
                   preservation_level='P0', identity_bearing=True) for e in entities if 'text' in e]
    tokens.append(dict(token_id='ks_sale_strip_partial', literal='EVERYTHING MUST GO', confidence=.7,
                       preservation_level='P1', identity_bearing=False))
    return dict(command_text='/sc-preserve /sc-noinvent', mode='T04', profile='VP00', camera='CG-B',
        scene=dict(scene_id='VSG2B-KENNYS-NEW-01', source_identity=SOURCE_ID, mode='T04', profile='VP00',
                   entities=entities, relationships=relationships),
        k1_binding=binding_records(), vsg={'mode': 'OBSERVER'}, semantic_text_lock='STRICT',
        reference_needs=[], query_budget=0, allow_support=False, material_intensity_delta=0,
        preserve=['Preserve observed facade proportions, opening rhythm, signs and all KSR relationships; source scope only.',
                  'ks_sale_strip: preserve known words EVERYTHING MUST GO; punctuation unresolved, graphic appearance retained.'],
        transform=[design['presentation']['scope']], remove=[], infer=infer, unknown=deepcopy(obs['uncertainties']),
        forbid=forbid, text_tokens=tokens)


def reject_archive(request):
    raise ValueError('K1_UNEXPECTED_ARCHIVE_QUERY')


def build_snapshots(request):
    from integration.streetcraft_orchestrator import orchestrate
    from ..generation_compiler import compile_generation_contract
    from ..generation_comparator import compare_generation_contract
    from ..vsg_observer import build_visual_scene_graph
    runtime = orchestrate(request, archive_retriever=reject_archive)
    require(runtime['status'] == 'GENERATION_READY' and runtime['pre_generation_gate']['status'] == 'PASS', 'RUNTIME_NOT_READY')
    rr, sar2, cgc = runtime['reference_reasoning'], runtime['sar2'], runtime['cgc_final']
    require(rr['status'] == 'READY' and rr['queries'] == 0 and not rr['admissions']
            and not rr['generation_projection'] and not runtime['reference_needs'], 'REFERENCE_ACTIVITY')
    graph = build_visual_scene_graph(sar2, reference_reasoning=rr, reference_needs=[])
    context = {'policies': {k: deepcopy(v) for k,v in cgc.items() if k in POLICIES},
               'directives': {k: deepcopy(request[k]) for k in DIRECTIVES}}
    candidate = deepcopy(graph)  # Equivalent input; no output image observation.
    contract = compile_generation_contract(candidate, sar2=sar2, generation_context=context)
    comparison = compare_generation_contract(cgc, contract, sar2=sar2, expected_graph=graph,
                                            candidate_graph=candidate, generation_context=context)
    require(comparison['status'] == 'PASS' and not comparison['unresolved_required_mappings'], 'COMPARISON_FAILED')
    require(all(c['required'] and c['required'] == c['preserved'] for c in comparison['coverage'].values()), 'EMPTY_COVERAGE')
    return dict(runtime=runtime, sar2=sar2, rr2=rr, cgc_final=cgc, expected_graph=graph,
                candidate_graph=candidate, generation_context=context, contract=contract), comparison


def verify_bundle(manifest, blobs, sidecars):
    """Validate exactly the supplied bytes, including persisted copies, never fallback."""
    require(manifest['fixture_id'] == IDENT, 'IDENTITY_BYPASS')
    require(set(sidecars) == set(RECORDS), 'SIDECAR_SET')
    for name, (_, checksum) in RECORDS.items():
        require(sha(sidecars[name]) == checksum, 'SIDECAR_HASH:' + name)
    for name, record in manifest['artifacts'].items():
        require(name in blobs and sha(blobs[name]) == record['sha256'], 'ARTIFACT_HASH:' + name)
    require(sha(blobs['source']) == SOURCE_SHA, 'SOURCE_HASH')
    with Image.open(BytesIO(blobs['source'])) as im:
        require(im.format == 'JPEG' and im.size == (736, 414), 'SOURCE_DIMENSIONS')
        im.verify()
    require(manifest['source_binding']['source_identity'] == SOURCE_ID, 'SOURCE_IDENTITY')
    require(set(manifest['required_priorities']) == {'P0','PR0','PR1','LOCK'}, 'REQUIRED_PRIORITIES')
    data = {k: json.loads(v) for k,v in blobs.items() if k != 'source'}
    design, obs = (json.loads(sidecars[k]) for k in ('design.json','observations.json'))
    verify_design(design)
    request = make_request(obs, design)
    require(data['request'] == request, 'REQUEST_AUTHORITY_OR_DIRECTIVES')
    source_ids = {e['entity_id'] for e in request['scene']['entities']}
    require(source_ids.isdisjoint(n['id'] for n in design['nodes']), 'SOURCE_DESIGN_ID_COLLISION')
    require({e['entity_id'] for e in data['sar2']['entities']} == source_ids, 'DESIGN_IN_SOURCE')
    snapshots, comparison = build_snapshots(request)
    for name, value in snapshots.items():
        require(data[name] == value, 'SNAPSHOT_REPLAY:' + name)
    infer, forbid = design_directives(design)
    require(data['cgc_final']['infer'] == infer and set(forbid) <= set(data['cgc_final']['forbid']), 'DESIGN_DIRECTIVE_LOSS')
    return {'status':'PASS', 'source_vsg2a':comparison['status'], 'design_authority':'PASS',
            'design_nodes_required':3, 'design_relations_required':4, 'source_entities':len(source_ids),
            'source_relations':10, 'rooftop_graph_locks':{'required':0,'preserved':0,'exercised':False},
            'visual_rubric':'PENDING', 'archive_calls':0,
            'sidecar_sha256':{k:sha(v) for k,v in sidecars.items()}}


def verify_preserved():
    path, checksum = RECORDS['preservation_baseline.json']
    raw = (ROOT/path).read_bytes()
    require(sha(raw) == checksum, 'BASELINE_HASH')
    baseline = json.loads(raw)
    for path, expected in baseline['files'].items():
        require(sha((ROOT/path).read_bytes()) == expected, 'PRESERVED_FILE_CHANGED:' + path)
    registry = json.loads((ROOT/'visual_scene_graph/pilot/allowlist.json').read_text())
    for ident, entry in baseline['registry']['fixtures'].items():
        if ident != IDENT:
            require(registry['fixtures'][ident] == entry, 'OTHER_ADMISSION_CHANGED:' + ident)
    return baseline
