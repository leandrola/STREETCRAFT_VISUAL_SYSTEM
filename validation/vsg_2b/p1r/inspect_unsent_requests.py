"""Offline P1R feasibility only: no transport, credentials, image writes or admission.

Run from repository root. Full request bodies exist only in memory. Stdout contains
hashes and checks, never the source's data URI. Prompt text is the frozen D payload,
not a generated or rewritten prompt. This is not a provider bridge.
"""
import base64
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from visual_scene_graph.pilot.harness import check_preconditions
from visual_scene_graph.pilot.review_dry_run import review
from visual_scene_graph.pilot.fixture_replay import verify_snapshots
from visual_scene_graph.pilot import bind_d

VERSION = '569705b35f79b1160d51de1d0e3955626af86c77a034a16e89010dbdde5ad312'
MODEL = 'black-forest-labs/flux-kontext-pro'
SOURCE_HASH = '282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc'


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load(path):
    return json.loads(path.read_text())


def main():
    check_preconditions()
    manifest, comparison = verify_snapshots(bind_d.FIXTURE, bind_d.reconstruct)
    qa = load(ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json')
    old = qa['dry_run']['fixtures']['R2B-191-D']
    package = ROOT/Path(old['report']['path']).parent
    reviewed = review(package)
    payloads = load(package/'payloads.json')
    source = (ROOT/manifest['artifacts']['source']['path']).read_bytes()
    checks = {}
    def require(name, passed):
        checks[name] = bool(passed)
        if not passed:
            raise ValueError(name)
    require('current_preconditions_and_D_replay', comparison['status'] == 'PASS')
    require('D_source_hash', sha(source) == SOURCE_HASH)
    require('source_identical_to_persisted_package', source == (package/'source.image').read_bytes())
    require('historical_delta_unchanged', reviewed['delta_sha256'] == old['delta_sha256'])
    require('historical_manifest_unchanged', sha(encoded(manifest)) == old['manifest_sha256'])
    require('AB_common_identical', payloads['A']['common'] == payloads['B']['common'])
    require('A_is_string_B_is_array', isinstance(payloads['A']['relations_and_locks'], str)
            and isinstance(payloads['B']['relations_and_locks'], list))
    records = [json.loads(line) for line in payloads['A']['relations_and_locks'].splitlines()]
    require('relation_values_order_ids_priorities_locks_equal', records == payloads['B']['relations_and_locks'])
    # Source URI is assembled in memory and never printed, persisted or submitted.
    source_uri = 'data:image/jpeg;base64,' + base64.b64encode(source).decode('ascii')
    source_descriptor = {'redacted': True, 'transport': 'data URI, JPEG',
                         'local_path': manifest['artifacts']['source']['path'],
                         'source_sha256': SOURCE_HASH, 'data_uri_sha256': sha(source_uri.encode())}
    settings = {'seed': 20260930, 'aspect_ratio': 'match_input_image',
                'output_format': 'png', 'prompt_upsampling': False, 'safety_tolerance': 2}
    bodies, branches = {}, {}
    for branch in ('A', 'B'):
        prompt = encoded(payloads[branch]).decode('utf-8')
        body = {'version': VERSION, 'input': {'input_image': source_uri, 'prompt': prompt, **settings}}
        bodies[branch] = body
        require(branch+'_prompt_lossless_roundtrip', json.loads(prompt) == payloads[branch])
        require(branch+'_source_roundtrip', base64.b64decode(body['input']['input_image'].split(',', 1)[1]) == source)
        require(branch+'_forbid_preserve_unknown_unchanged', all(
            json.loads(prompt)['common']['stable_cgc'][k] == payloads['A']['common']['stable_cgc'][k]
            for k in ('forbid', 'preserve', 'unknown', 'infer', 'semantic_text_lock', 'source_identity')))
        redacted = deepcopy(body)
        redacted['input']['input_image'] = source_descriptor
        branches[branch] = {'provider_prompt_type': type(prompt).__name__,
                            'prompt_sha256': sha(prompt.encode()), 'prompt_utf8_bytes': len(prompt.encode()),
                            'prompt_characters': len(prompt), 'quotes': prompt.count('"'),
                            'backslashes': prompt.count('\\'),
                            'json_lexical_token_count': len(re.findall(
                                r'"(?:\\.|[^"\\])*"|true|false|null|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|[{}\[\],:]', prompt)),
                            'model_token_count': 'UNKNOWN',
                            'full_unsent_body_sha256': sha(encoded(body)),
                            'full_unsent_body_utf8_bytes': len(encoded(body)),
                            'redacted_body': redacted}
    require('same_version_seed_source_settings',
            {k:v for k,v in bodies['A']['input'].items() if k != 'prompt'} ==
            {k:v for k,v in bodies['B']['input'].items() if k != 'prompt'} and
            bodies['A']['version'] == bodies['B']['version'])
    require('both_provider_prompts_are_text', all(isinstance(b['input']['prompt'], str) for b in bodies.values()))
    require('AB_serializations_distinct', bodies['A']['input']['prompt'] != bodies['B']['input']['prompt'])
    require('source_below_stricter_256KB_doc_recommendation', len(source) < 256000)
    print(json.dumps({'status': 'OFFLINE_FEASIBILITY_CHECKS_PASS', 'representation': 'TEXT_SERIALIZED_AB',
        'not_sent': True, 'not_an_operational_manifest_or_delta': True,
        'candidate_version_documentation_only': VERSION, 'model': MODEL,
        'settings': settings, 'settings_authority': 'Feasibility proposal only; seed chosen locally for unsent bodies.',
        'serialization': "json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)",
        'historical_D_package': str(package.relative_to(ROOT)),
        'historical_D_manifest_sha256': old['manifest_sha256'],
        'historical_D_delta_sha256': old['delta_sha256'],
        'payloads_file_sha256': sha((package/'payloads.json').read_bytes()),
        'source': {**source_descriptor, 'source_bytes': len(source)},
        'common_sha256': sha(encoded(payloads['A']['common'])),
        'relation_record_count': len(records), 'relation_ids_in_order': [r['id'] for r in records],
        'priorities': dict(Counter(r['priority'] for r in records)),
        'locks': sorted({lock for r in records for lock in r['lock_ids']}),
        'checks': checks, 'branches': branches,
        'token_limitations': 'JSON lexical tokens are not model tokens. Provider tokenizer, prompt limit and truncation behavior are unverified; no tiktoken estimate is substituted.',
        'real_activity_counts': {'archive_calls':0,'predictions':0,'generated_images':0,'visual_pairs':0}}, indent=2)+'\n')


if __name__ == '__main__':
    main()
