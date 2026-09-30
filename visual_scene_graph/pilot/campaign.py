"""Versioned global closure; dry runs and partial coverage never establish PASS."""
import base64
import json
from pathlib import Path

import jsonschema

from .harness import ROOT, PilotBlocked, image_valid, prepare, sha, validate
from .evaluation import assess_review
from ..generation_compiler import digest

POLICY_PATH = ROOT / 'visual_scene_graph/pilot/campaign_policy.json'
REGISTRY_PATH = ROOT / 'visual_scene_graph/pilot/allowlist.json'


def read(path):
    return json.loads(Path(path).read_text())


def load_policy():
    policy = read(POLICY_PATH)
    validate(policy, 'campaign')
    selections = set(policy['global_selection']) | set(policy['partial_selection'])
    if not selections <= policy['fixtures'].keys():
        raise PilotBlocked('UNKNOWN_POLICY_SELECTION')
    for entry in policy['fixtures'].values():
        if entry['status'] == 'ADMITTED' and (not entry['manifest_sha256'] or
                any(not criteria for criteria in entry['phenomena'].values())):
            raise PilotBlocked('EMPTY_PHENOMENON_COVERAGE')
    return policy


def verify_pair(path, entry, registry):
    """Replay admission and inputs, actual receipts, images and the blind review."""
    manifest, report = read(path/'manifest.json'), read(path/'report.json')
    if entry['status'] != 'ADMITTED' or digest(manifest) != entry['manifest_sha256']:
        raise PilotBlocked('FIXTURE_NOT_ADMITTED_FOR_CAMPAIGN')
    prepared = prepare(manifest, registry, root=ROOT)
    for name, blob in prepared['blobs'].items():
        suffix = '.image' if name == 'source' else '.json'
        if (path/(name+suffix)).read_bytes() != blob:
            raise PilotBlocked('PERSISTED_ARTIFACT_CHANGED:' + name)
    for name, blob in prepared['sidecars'].items():
        if (path/'sidecars'/name).read_bytes() != blob:
            raise PilotBlocked('PERSISTED_SIDECAR_CHANGED:' + name)
    if read(path/'payloads.json') != prepared['payloads'] or read(path/'comparison.json') != prepared['comparison']:
        raise PilotBlocked('PERSISTED_PREPARATION_CHANGED')
    generation = manifest['generation']
    if any(str(generation[key]).startswith('DRY_RUN_ONLY') for key in ('provider', 'model')):
        raise PilotBlocked('PROVISIONAL_GENERATION_CONFIGURATION')
    if (report['run_id'] != path.name or report['fixture_id'] != manifest['fixture_id'] or
            report['reason'] != 'AWAITING_BLIND_REVIEW' or
            report['seed_controlled'] != (generation['seed'] is not None)):
        raise PilotBlocked('INVALID_PAIR_REPORT')
    if {r['branch'] for r in report['images']} != {'A', 'B'} or len(report['images']) != 2:
        raise PilotBlocked('NOT_A_VALID_PAIR')
    if {p.name for p in path.glob('*.attempt.json')} != {'A.attempt.json', 'B.attempt.json'}:
        raise PilotBlocked('INVALID_PAIR_ATTEMPTS')
    ids, dimensions, output_paths = set(), [], set()
    for record in report['images']:
        branch = record['branch']
        request = {'source_base64': base64.b64encode(prepared['source']).decode(),
                   'payload': prepared['payloads'][branch], **generation}
        if (read(path/(branch+'.input.json')) != request or
                read(path/(branch+'.attempt.json')) != {'input_sha256': digest(request), 'branch': branch}):
            raise PilotBlocked('ATTEMPT_INPUT_MISMATCH')
        receipt = read(path/(branch+'.output.json'))
        if receipt != {k: record[k] for k in ('sha256', 'input_sha256', 'metadata', 'path')}:
            raise PilotBlocked('RECEIPT_MISMATCH')
        metadata = record['metadata']
        if record['input_sha256'] != digest(request) or any(
                key not in metadata or metadata[key] != generation[key] for key in generation):
            raise PilotBlocked('PROVIDER_SETTINGS_MISMATCH')
        ident = metadata.get('generation_id')
        if not isinstance(ident, str) or not ident or ident in ids:
            raise PilotBlocked('INVALID_GENERATION_ID')
        ids.add(ident)
        output = record['path']
        if output not in {'blind-1.image', 'blind-2.image'} or output in output_paths:
            raise PilotBlocked('INVALID_OUTPUT_PATH')
        output_paths.add(output)
        raw = (path/output).read_bytes()
        size = image_valid(raw)
        if sha(raw) != record['sha256'] or any(record[k] != v for k, v in size.items()):
            raise PilotBlocked('OUTPUT_RECEIPT_MISMATCH')
        if size['format'].lower() != generation['parameters']['output_format']:
            raise PilotBlocked('OUTPUT_FORMAT_MISMATCH')
        dimensions.append(size)
    if dimensions[0] != dimensions[1]:
        raise PilotBlocked('PAIR_FORMAT_MISMATCH')
    review = read(path/'review.submitted.json')
    result = assess_review(path, review)
    if read(path/'evaluation.json') != result:
        raise PilotBlocked('EVALUATION_REPLAY_MISMATCH')
    rubric = {r['constraint_id'] for r in manifest['rubric']}
    exercised = set()
    b_path = next(r['path'] for r in report['images'] if r['branch'] == 'B')
    b_observations = {r['constraint_id']: r for item in review['images']
                      if item['path'] == b_path for r in item['observations']}
    for phenomenon, criteria in entry['phenomena'].items():
        if not criteria or not set(criteria) <= rubric:
            raise PilotBlocked('EMPTY_OR_UNBOUND_PHENOMENON:' + phenomenon)
        # Coverage requires actual observations of nonempty frozen rubric criteria.
        # UNKNOWN is handled by assess_review and can never establish global PASS.
        if all(b_observations[c]['preserved'] == 'YES' for c in criteria):
            exercised.add(phenomenon)
    return result, exercised


def close(run_dirs, selected_fixtures, regression_passed):
    results, reasons, covered = [], [], set()
    summary = {'status': 'INCONCLUSIVE', 'scope': 'GLOBAL', 'results': results,
               'production_authorized': False, 'reasons': reasons}
    try:
        policy, registry = load_policy(), read(REGISTRY_PATH)
        summary.update(policy_version=policy['version'], policy_sha256=digest(policy))
        selected = list(selected_fixtures)
        paths = [Path(p).resolve() for p in run_dirs]
        if len(set(selected)) != len(selected) or len(set(paths)) != len(paths):
            raise PilotBlocked('DUPLICATE_FIXTURE_OR_RUN')
        if set(selected) == set(policy['partial_selection']):
            summary['scope'] = 'PARTIAL_D_E_KENNY'
        elif set(selected) != set(policy['global_selection']):
            reasons.append('SELECTION_OUTSIDE_CAMPAIGN_SCOPE')
        for ident in selected:
            entry = policy['fixtures'].get(ident)
            if not entry or entry['status'] != 'ADMITTED':
                reasons.append('FIXTURE_NOT_ADMITTED_FOR_CAMPAIGN:' + ident)
        if paths:
            roots = {p.parent for p in paths}
            if len(roots) != 1:
                raise PilotBlocked('MULTIPLE_CAMPAIGN_DIRECTORIES')
            root = roots.pop()
            if (root/'STOP').exists():
                reasons.append('CAMPAIGN_STOPPED')
            attempts = list(root.glob('*/*.attempt.json'))
            summary['generation_attempts'] = len(attempts)
            if len(attempts) > policy['maximum_generation_attempts']:
                reasons.append('GENERATION_BUDGET_EXHAUSTED')
            if {p.parent for p in attempts} != set(paths):
                reasons.append('OMITTED_OR_UNATTEMPTED_PAIR')
        else:
            summary['generation_attempts'] = 0
        for path in paths:
            ident = read(path/'manifest.json')['fixture_id']
            if ident not in selected or ident not in policy['fixtures']:
                raise PilotBlocked('UNSELECTED_FIXTURE:' + ident)
            result, exercised = verify_pair(path, policy['fixtures'][ident], registry)
            results.append(result)
            covered.update(exercised)
        if sorted(r['fixture_id'] for r in results) != sorted(selected):
            reasons.append('INCOMPLETE_OR_REPEATED_FIXTURES')
        if len(results) < policy['minimum_pairs']:
            reasons.append('MINIMUM_PAIRS_NOT_MET')
        missing = sorted(set(policy['required_phenomena']) - covered)
        summary.update(covered_phenomena=sorted(covered), missing_phenomena=missing)
        if missing:
            reasons.append('MISSING_REQUIRED_PHENOMENA')
        if regression_passed is not True:
            reasons.append('REGRESSION_NOT_PASS')
        if not any(r['status'] == 'PASS' for r in results):
            reasons.append('NO_VERIFIED_IMPROVEMENT')
        if any(r['verdict'] not in {'BETTER', 'TIE'} or r['limitation'] for r in results):
            reasons.append('UNRESOLVED_VISUAL_RESULT_OR_SEED')
        if any(r['status'] == 'FAIL' for r in results):
            summary['status'] = 'FAIL'
        elif not reasons and summary['scope'] == 'GLOBAL':
            summary['status'] = 'PASS'
    except (ValueError, OSError, KeyError, TypeError, jsonschema.ValidationError) as exc:
        reasons.append('INVALID_CAMPAIGN_EVIDENCE:' + str(exc))
    return summary
