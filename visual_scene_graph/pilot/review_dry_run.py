"""Review persisted payload bytes independently of the harness renderer (no calls)."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from ..generation_compiler import normalize

ROOT = Path(__file__).resolve().parents[2]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def review(path):
    path = Path(path)
    read = lambda name: json.loads((path / (name + '.json')).read_text())
    manifest, payloads, report = read('manifest'), read('payloads'), read('report')
    comparison, contract = read('comparison'), read('contract')
    a, b = payloads['A'], payloads['B']
    records = [json.loads(line) for line in a['relations_and_locks'].splitlines()]
    expected = sorted([{k: c[k] for k in ('id', 'priority', 'value', 'lock_ids')}
                       for c in contract['constraints']], key=lambda c: c['id'])
    is_relation = lambda c: c['id'].split(':', 1)[0] in {'edge', 'topology', 'lock'}
    checks = {
        'common_equal': a['common'] == b['common'],
        'shared_cgc_matches_frozen_snapshot': a['common']['stable_cgc'] == normalize(read('cgc_final')),
        'parsed_A_equals_B': records == b['relations_and_locks'],
        'relations_locks_match_frozen_contract': records == [c for c in expected if is_relation(c)],
        'shared_restrictions_match_frozen_contract': a['common']['approved_source_restrictions'] == [c for c in expected if not is_relation(c)],
        'delta_digest': report['delta_sha256'] == digest({'manifest': manifest, 'payloads': payloads}),
        'comparison_pass': comparison['status'] == 'PASS' and not comparison['unresolved_required_mappings'],
        'nonempty_required_coverage': all(comparison['coverage'][p]['required'] > 0 and
            comparison['coverage'][p]['preserved'] == comparison['coverage'][p]['required']
            for p in manifest['required_priorities']),
        'no_images_or_calls': report['images'] == [] and not list(path.glob('*.attempt.json')),
        'dry_run_only': (report['status'], report['reason']) == ('INCONCLUSIVE', 'DRY_RUN_NO_IMAGES'),
        'no_technical_failures': report['technical_failures'] == [],
        'snapshot_bytes': all(hashlib.sha256((path / (name + ('.image' if name == 'source' else '.json'))).read_bytes()).hexdigest() == rec['sha256'] for name, rec in manifest['artifacts'].items()),
    }
    if not all(checks.values()):
        raise ValueError('DRY_RUN_REVIEW_FAILED:' + repr(checks))
    return {'status': 'PASS', 'reviewer': 'Codex / independent persisted-byte review',
            'review_method': 'Separate review implementation; does not invoke or import the harness renderer. Automated technical review, not human or blind visual review.',
            'reviewed_at': datetime.now(timezone.utc).isoformat(),
            'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'run_path': str(path.resolve().relative_to(ROOT)) if path.resolve().is_relative_to(ROOT) else str(path.resolve()),
            'manifest_sha256': digest(manifest),
            'delta_sha256': report['delta_sha256'], 'checks': checks,
            'payloads_file_sha256': hashlib.sha256((path/'payloads.json').read_bytes()).hexdigest(),
            'generation_attempts': 0, 'fresh_images': 0, 'valid_pairs': 0,
            'limitations': ['Prospective annotation, not historical recovery.',
                            'Provisional provider settings; not an operational selection.',
                            'No visual quality/improvement finding; VSG-2B remains BLOCKED/PENDING_VISUAL.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(review(args.run_directory), indent=2))
