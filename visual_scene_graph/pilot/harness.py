"""Fail-closed preparation and append-only execution of controlled A/B pairs."""
from copy import deepcopy
import base64
import fcntl
import hashlib
from io import BytesIO
import json
from pathlib import Path
import secrets
import subprocess
import uuid

import jsonschema
from PIL import Image

from ..generation_compiler import ROOT, canonical_bytes, digest, normalize
from ..generation_comparator import compare_generation_contract, stable_constraints
from ..vsg_observer import build_visual_scene_graph

ARTIFACTS = ('request', 'runtime', 'sar2', 'rr2', 'cgc_final', 'expected_graph',
             'candidate_graph', 'generation_context', 'contract', 'source')


class PilotBlocked(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate(value, name):
    jsonschema.validate(value, json.loads((ROOT / 'schemas' / ('vsg-pilot-' + name + '.schema.json')).read_text()))


def save(path, data):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')


def image_valid(data):
    with Image.open(BytesIO(data)) as im:
        im.verify()
    with Image.open(BytesIO(data)) as im:
        im.load()
        return {'format': im.format, 'width': im.width, 'height': im.height}


def control_file_hashes():
    paths = []
    for directory in ('visual_scene_graph', 'integration', 'scene_intelligence', 'reference_runtime',
                      'command_invocation', 'hardening', 'schemas', 'benchmark'):
        paths.extend(p for p in (ROOT/directory).rglob('*') if p.suffix in {'.py', '.json'} and '__pycache__' not in p.parts)
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted(paths)}


def check_preconditions():
    """Freeze regression evidence against current code, schemas and fixture registry."""
    from ..run_generation_benchmark import verify_report
    path = ROOT/'validation/vsg_2b/preconditions.json'
    if not path.exists():
        raise PilotBlocked('MISSING_PRECONDITIONS')
    evidence = json.loads(path.read_text())
    if evidence['control_file_sha256'] != control_file_hashes():
        raise PilotBlocked('STALE_PRECONDITIONS')
    reports = {}
    for key in ('vsg2a', 'regression', 'pilot_controls'):
        record = evidence[key]
        raw = (ROOT/record['path']).read_bytes()
        if sha(raw) != record['sha256']:
            raise PilotBlocked('PRECONDITION_HASH_MISMATCH:' + key)
        reports[key] = json.loads(raw)
    if verify_report(reports['vsg2a'])['status'] != 'PASS':
        raise PilotBlocked('VSG2A_PRECONDITION_FAILED')
    if reports['regression']['R0'] != 'PASS' or reports['pilot_controls']['status'] != 'PASS':
        raise PilotBlocked('REGRESSION_PRECONDITION_FAILED')


def prepare(manifest, allowlist, root=ROOT):
    """Read frozen bytes once; no generator, evaluator or external Archive calls."""
    validate(manifest, 'manifest')
    if manifest['pilot_enabled'] is not True:
        raise PilotBlocked('PILOT_DISABLED')
    if allowlist.get('version') != '1.0.0':
        raise PilotBlocked('ALLOWLIST_VERSION')
    entry = allowlist.get('fixtures', {}).get(manifest['fixture_id'])
    if not entry or entry.get('status') != 'ADMITTED' or entry.get('manifest_sha256') != digest(manifest):
        raise PilotBlocked('FIXTURE_NOT_AUTHORIZED_OR_CHANGED')
    check_preconditions()
    blobs = {}
    for name, record in manifest['artifacts'].items():
        path = (Path(root) / record['path']).resolve()
        if not path.is_relative_to(Path(root).resolve()):
            raise PilotBlocked('ARTIFACT_OUTSIDE_ROOT:' + name)
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise PilotBlocked('MISSING_ARTIFACT:' + name) from exc
        if sha(data) != record['sha256']:
            raise PilotBlocked('ARTIFACT_HASH_MISMATCH:' + name)
        blobs[name] = data
    image_valid(blobs['source'])
    a = {k: json.loads(v) for k, v in blobs.items() if k != 'source'}
    runtime = a['runtime']
    if runtime.get('status') != 'GENERATION_READY' or runtime.get('generation_ready') is not True:
        raise PilotBlocked('NOT_GENERATION_READY')
    for name, key in [('sar2', 'sar2'), ('rr2', 'reference_reasoning'), ('cgc_final', 'cgc_final')]:
        if a[name] != runtime.get(key):
            raise PilotBlocked('RUNTIME_SNAPSHOT_MISMATCH:' + name)
    if a['cgc_final'].get('pre_generation_gate', {}).get('status') != 'PASS' or runtime.get('pre_generation_gate', {}).get('status') != 'PASS':
        raise PilotBlocked('BLOCKED_PREFLIGHT')
    if a['request'].get('scene', {}).get('source_identity') != a['sar2']['source_identity']:
        raise PilotBlocked('REQUEST_SOURCE_MISMATCH')
    if manifest['source_binding']['source_identity'] != a['sar2']['source_identity']:
        raise PilotBlocked('SOURCE_BINDING_MISMATCH')
    if manifest['artifacts']['expected_graph']['path'] == manifest['artifacts']['candidate_graph']['path']:
        raise PilotBlocked('CANDIDATE_USED_AS_BASELINE')
    jsonschema.validate(a['sar2'], json.loads((ROOT/'schemas/scene-analysis-record-v2.schema.json').read_text()))
    from integration.streetcraft_orchestrator import _resolved_config, _scene_with_runtime_config
    from scene_intelligence import build_scene_analysis_record
    command, config = _resolved_config(a['request'])
    if command.get('status') == 'ERROR' or build_scene_analysis_record(**_scene_with_runtime_config(a['request']['scene'], config)) != a['sar2']:
        raise PilotBlocked('REQUEST_SAR2_REPLAY_MISMATCH')
    expected = build_visual_scene_graph(a['sar2'], reference_reasoning=a['rr2'],
                                       reference_needs=runtime['reference_needs'])
    if expected != a['expected_graph']:
        raise PilotBlocked('EXPECTED_GRAPH_REPLAY_MISMATCH')
    comparison = compare_generation_contract(a['cgc_final'], a['contract'], sar2=a['sar2'],
        expected_graph=a['expected_graph'], candidate_graph=a['candidate_graph'],
        generation_context=a['generation_context'])
    if comparison['status'] != 'PASS' or comparison['unresolved_required_mappings']:
        raise PilotBlocked('COMPARISON_FAILED:' + ','.join(comparison['issues']))
    for priority in manifest['required_priorities']:
        coverage = comparison['coverage'][priority]
        if not coverage['required'] or coverage['preserved'] != coverage['required']:
            raise PilotBlocked('EMPTY_OR_INCOMPLETE_COVERAGE:' + priority)
    baseline, issues = stable_constraints(a['cgc_final'], sar2=a['sar2'], expected_graph=a['expected_graph'])
    if issues:
        raise PilotBlocked('BASELINE_INVALID')
    def semantic(rows):
        return sorted(({k: deepcopy(c[k]) for k in ('id', 'priority', 'value', 'lock_ids')} for c in rows), key=lambda c: c['id'])
    left, right = semantic(baseline), semantic(a['contract']['constraints'])
    if left != right:
        raise PilotBlocked('RENDERER_CONSTRAINT_LOSS')
    relation = lambda c: c['id'].startswith(('edge:', 'topology:', 'lock:'))
    common = {'stable_cgc': normalize(a['cgc_final']),
              'approved_source_restrictions': [c for c in left if not relation(c)]}
    # Both adapters convey precisely the same approved facts. Only relationship /
    # lock expression changes: individually serialized records vs structured array.
    records = [c for c in left if relation(c)]
    payloads = {
        'A': {'common': deepcopy(common), 'relations_and_locks': '\n'.join(canonical_bytes(c).decode() for c in records)},
        'B': {'common': deepcopy(common), 'relations_and_locks': [c for c in right if relation(c)]},
    }
    if [json.loads(line) for line in payloads['A']['relations_and_locks'].splitlines()] != payloads['B']['relations_and_locks']:
        raise PilotBlocked('UNAUTHORIZED_RENDERER_DELTA')
    constraint_ids = {c['id'] for c in left if c['priority'] in {'P0', 'PR0', 'PR1', 'LOCK'} or c['id'].startswith('edge:')}
    rubric_ids = {c['constraint_id'] for c in manifest['rubric']}
    if len(rubric_ids) != len(manifest['rubric']):
        raise PilotBlocked('DUPLICATE_RUBRIC_CRITERION')
    priorities = {c['id']: c['priority'] for c in left}
    if any(r['constraint_id'] in priorities and r['priority'] != priorities[r['constraint_id']] for r in manifest['rubric']):
        raise PilotBlocked('RUBRIC_PRIORITY_MISMATCH')
    if not constraint_ids <= rubric_ids or not {'identity', 'unauthorized_change'} <= {c['category'] for c in manifest['rubric']}:
        raise PilotBlocked('INCOMPLETE_VISUAL_RUBRIC')
    return {'manifest': deepcopy(manifest), 'comparison': comparison, 'payloads': payloads,
            'blobs': blobs, 'source': blobs['source']}


class CommandGenerator:
    """Explicit local provider bridge, argv without shell; JSON stdin/stdout.

    The bridge receives only source bytes, payload, model and parameters.
    It must perform fresh generation and return image_base64 and metadata.
    No command is taken from a fixture. Configure only a trusted local adapter.
    """
    def __init__(self, argv, provider, model):
        self.argv, self.provider, self.model = list(argv), provider, model

    def generate(self, request):
        result = subprocess.run(self.argv, input=json.dumps(request), capture_output=True,
                                text=True, timeout=600, check=True)
        response = json.loads(result.stdout)
        if set(response) != {'image_base64', 'metadata'} or not isinstance(response['metadata'], dict):
            raise ValueError('INVALID_PROVIDER_RESPONSE')
        metadata = response['metadata']
        if metadata.get('provider') != self.provider or metadata.get('model') != self.model or not metadata.get('generation_id'):
            raise ValueError('UNVERIFIED_PROVIDER_METADATA')
        return base64.b64decode(response['image_base64'], validate=True), metadata


def _execute(prepared, output_root, *, generator=None, dry_run=True, reviewed_delta=None):
    """Persist effective inputs before calls; any technical failure stops the pair."""
    m = prepared['manifest']
    run_id = str(uuid.uuid4())
    out = Path(output_root) / run_id
    out.mkdir(parents=True, exist_ok=False)
    for name, data in prepared['blobs'].items():
        (out / (name + ('.image' if name == 'source' else '.json'))).write_bytes(data)
    save(out / 'manifest.json', m)
    save(out / 'comparison.json', prepared['comparison'])
    save(out / 'payloads.json', prepared['payloads'])
    delta_hash = digest({'manifest': m, 'payloads': prepared['payloads']})
    report = {'schema_version': '1.0.0', 'run_id': run_id, 'fixture_id': m['fixture_id'],
              'status': 'INCONCLUSIVE', 'reason': 'DRY_RUN_NO_IMAGES', 'delta_sha256': delta_hash,
              'images': [], 'technical_failures': [], 'visual_verdict': 'INDETERMINATE',
              'seed_controlled': m['generation']['seed'] is not None}
    if not dry_run:
        if any(m['generation'][key].startswith('DRY_RUN_ONLY') for key in ('provider', 'model')):
            report.update(status='BLOCKED', reason='PROVISIONAL_GENERATION_CONFIGURATION')
        elif reviewed_delta != delta_hash:
            report.update(status='BLOCKED', reason='DELTA_REVIEW_REQUIRED')
        elif generator is None:
            report.update(status='BLOCKED', reason='NO_GENERATOR')
        elif (generator.provider, generator.model) != (m['generation']['provider'], m['generation']['model']):
            report.update(status='BLOCKED', reason='PROVIDER_MODEL_MISMATCH')
        else:
            report['reason'] = 'AWAITING_BLIND_REVIEW'
            blind_map = {}
            branches = ['A', 'B']
            secrets.SystemRandom().shuffle(branches)
            for index, branch in enumerate(branches):
                request = {'source_base64': base64.b64encode(prepared['source']).decode(),
                           'payload': prepared['payloads'][branch], **m['generation']}
                save(out / (branch + '.input.json'), request)
                save(out / (branch + '.attempt.json'), {'input_sha256': digest(request), 'branch': branch})
                try:
                    data, metadata = generator.generate(deepcopy(request))
                    # Persist even invalid images as failure evidence.
                    filename = f'blind-{index + 1}.image'
                    (out / filename).write_bytes(data)
                    save(out / (branch + '.output.json'), {'sha256': sha(data), 'input_sha256': digest(request), 'metadata': metadata, 'path': filename})
                    for key in ('provider', 'model', 'seed', 'parameters'):
                        if metadata.get(key) != request[key]:
                            raise ValueError('PROVIDER_SETTINGS_MISMATCH:' + key)
                    if not metadata.get('generation_id'):
                        raise ValueError('MISSING_GENERATION_ID')
                    dimensions = image_valid(data)
                    if dimensions['format'].lower() != m['generation']['parameters']['output_format']:
                        raise ValueError('OUTPUT_FORMAT_MISMATCH')
                    if report['images'] and any(dimensions[k] != report['images'][0][k] for k in ('width', 'height', 'format')):
                        raise ValueError('PAIR_FORMAT_MISMATCH')
                    if any(r['metadata'].get('generation_id') == metadata.get('generation_id') for r in report['images']):
                        raise ValueError('DUPLICATE_GENERATION_ID')
                    record = {'branch': branch, 'path': filename, 'sha256': sha(data),
                              'input_sha256': digest(request), 'metadata': metadata, **dimensions}
                    report['images'].append(record)
                    blind_map[filename] = branch
                except Exception as exc:
                    report['technical_failures'].append({'branch': branch, 'error': type(exc).__name__, 'detail': str(exc)})
                    report['reason'] = 'TECHNICAL_FAILURE'
                    break
            save(out / 'private_branch_map.json', blind_map)
            # Export only this packet, source and blind images to a separate reviewer.
            review_dir = out / 'review_packet'
            review_dir.mkdir()
            (review_dir / 'source.image').write_bytes(prepared['source'])
            for record in report['images']:
                (review_dir / record['path']).write_bytes((out / record['path']).read_bytes())
            save(review_dir / 'blind_review.json', {'run_id': run_id, 'source_sha256': sha(prepared['source']),
                'source': 'source.image', 'images': [{'path': r['path'], 'sha256': r['sha256']} for r in report['images']],
                'rubric': m['rubric'], 'instructions': 'Review each image against source; do not consult private run files.'})
    validate(report, 'report')
    save(out / 'report.json', report)
    return out, report


def execute(prepared, output_root, *, generator=None, dry_run=True, reviewed_delta=None):
    """One campaign directory; eight-call hard budget, no implicit retries.

    Lock spans provider calls so parallel CLI invocations cannot overspend.
    An interrupted/failed/unreviewed pair prevents the next pair from starting.
    """
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return _execute(prepared, root, dry_run=True)
    with (root / '.campaign.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if (root / 'STOP').exists():
            raise PilotBlocked('CAMPAIGN_STOPPED')
        attempts = list(root.glob('*/*.attempt.json'))
        if len(attempts) + 2 > 8:
            raise PilotBlocked('GENERATION_BUDGET_EXHAUSTED')
        for previous in {p.parent for p in attempts}:
            result_path = previous / 'evaluation.json'
            if not result_path.exists():
                raise PilotBlocked('PREVIOUS_PAIR_REQUIRES_REVIEW_OR_FAILURE_TRIAGE')
            result = json.loads(result_path.read_text())
            if result['status'] == 'FAIL':
                raise PilotBlocked('CAMPAIGN_STOPPED')
            if result['fixture_id'] == prepared['manifest']['fixture_id']:
                raise PilotBlocked('REPEAT_NOT_AUTHORIZED')
        return _execute(prepared, root, generator=generator, dry_run=False, reviewed_delta=reviewed_delta)
