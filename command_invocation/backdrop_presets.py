"""Opt-in BD01/BD02 contracts; no rendering or visual-pass claims."""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

CATALOG = json.loads(Path(__file__).with_name('BACKDROP_PRESETS.json').read_text())


def contract_sha256(contract):
    content = {k: v for k, v in contract.items() if k != 'contract_sha256'}
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def resolve_backdrop_options(options=None, default_ratio='16:9'):
    options = {} if options is None else options
    if not isinstance(options, dict) or set(options)-{'aspect_ratio', 'target_scale'}:
        raise ValueError('INVALID_BACKDROP_OPTIONS')
    ratio = options.get('aspect_ratio', default_ratio)
    if not isinstance(ratio, str) or not re.fullmatch(r'[1-9][0-9]*:[1-9][0-9]*', ratio):
        raise ValueError('INVALID_BACKDROP_ASPECT_RATIO')
    width, height = map(int, ratio.split(':'))
    if width <= height:
        raise ValueError('BACKDROP_REQUIRES_HORIZONTAL_FORMAT')
    aspect = Fraction(width, height)
    scale = options.get('target_scale', '1:64')
    if not isinstance(scale, str) or not re.fullmatch(r'1:[1-9][0-9]*', scale):
        raise ValueError('INVALID_BACKDROP_TARGET_SCALE')
    return {'aspect_ratio': f'{aspect.numerator}:{aspect.denominator}', 'target_scale': scale}


def build_backdrop_contract(config, sar2, options=None):
    preset = config['backdrop_preset']
    policy = deepcopy(CATALOG['presets'][preset])
    options = resolve_backdrop_options(options, config['aspect_ratio'])
    if (config['profile'], config['mode'], config['camera']) != ('VP02', policy['mode'], 'CG-F'):
        raise ValueError('BACKDROP_CONFIG_CONFLICT')
    if sar2['mode'] != policy['mode'] or sar2['profile'] != 'VP02':
        raise ValueError('BACKDROP_SCENE_CONFIG_CONFLICT')
    preserve = preset == 'BD02' or config.get('preservation') == 'STRICT_OBSERVED_EVIDENCE'
    locked_nodes = sorted(e['entity_id'] for e in sar2['entities']
                          if e['preservation_level'] == 'P0' or 'IDENTITY_ANCHOR' in e.get('roles', [])
                          or (preserve and e.get('observed', e.get('epistemic_class') == 'OBSERVED')))
    contract = {'schema_version': '1.0.0', 'preset': preset,
        'base_profile': 'VP02', 'mode': policy.pop('mode'), 'scene_id': sar2['scene_id'],
        'source_identity': sar2['source_identity'], 'visual_validation': 'PENDING',
        **deepcopy(CATALOG['shared']), **{k:v for k,v in policy.items() if k not in {'additional_locks', 'forbidden_operations'}}}
    contract['framing']['aspect_ratio'] = options['aspect_ratio']
    contract['internal_locks'] += policy['additional_locks']
    contract['forbidden_operations'] += policy['forbidden_operations']
    contract['scope'] = {'recomposition': 'UNPROTECTED_REGIONS_ONLY' if preset=='BD01' and not preserve else 'NO_MAJOR_RECOMPOSITION',
        'protected_node_ids': locked_nodes,
        'protected_relationship_ids': sorted(r['relationship_id'] for r in sar2['relationships'] if r['protection'] in {'PR0','PR1'}),
        'locked_unknown_ids': sorted(sar2['unknown_locks']),
        'source_locks_override_preset_allowances': True,
        'unknown_resolution': 'FORBIDDEN_WITHOUT_INDEPENDENT_EVIDENCE',
        'detail_removal': 'EXISTING_AUTHORIZATION_REQUIRED'}
    if preserve:
        contract['allowed_operations'] = deepcopy(CATALOG['presets']['BD02']['allowed_operations'])
        contract['forbidden_operations'] = sorted(set(contract['forbidden_operations'] + CATALOG['presets']['BD02']['forbidden_operations']))
    contract['print_target'] = {'nominal_scale': options['target_scale'], 'physical_dimensions_and_resolution': 'NOT_SPECIFIED',
                              'print_readiness': 'REQUIRES_OUTPUT_REVIEW'}
    contract['contract_sha256'] = contract_sha256(contract)
    return contract


def validate_backdrop_contract(contract, config, sar2, options=None):
    errors=[]
    try:
        if contract_sha256(contract) != contract.get('contract_sha256'):errors.append('BACKDROP_HASH_MISMATCH')
        if contract != build_backdrop_contract(config, sar2, options):errors.append('BACKDROP_CONTRACT_MISMATCH')
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return {'status':'FAIL' if errors else 'PASS','errors':errors}
