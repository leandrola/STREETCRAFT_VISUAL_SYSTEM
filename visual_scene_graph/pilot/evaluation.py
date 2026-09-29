"""Consume separately authored, blind visual evidence; never score contracts."""
import json
from pathlib import Path

from .harness import PilotBlocked, save, sha, validate
from ..generation_compiler import digest


def evaluate(run_dir, review):
    run_dir = Path(run_dir)
    validate(review, 'review')
    report = json.loads((run_dir / 'report.json').read_text())
    manifest = json.loads((run_dir / 'manifest.json').read_text())
    mapping = json.loads((run_dir / 'private_branch_map.json').read_text())
    if report['technical_failures'] or len(report['images']) != 2:
        raise PilotBlocked('NOT_A_VALID_PAIR')
    if review['run_id'] != report['run_id'] or review['source_sha256'] != sha((run_dir / 'source.image').read_bytes()):
        raise PilotBlocked('REVIEW_PROVENANCE_MISMATCH')
    payloads = json.loads((run_dir / 'payloads.json').read_text())
    if digest({'manifest': manifest, 'payloads': payloads}) != report['delta_sha256']:
        raise PilotBlocked('RUN_INPUTS_CHANGED')
    if sha((run_dir/'source.image').read_bytes()) != manifest['artifacts']['source']['sha256']:
        raise PilotBlocked('FROZEN_SOURCE_CHANGED')
    originals = {r['path']: r for r in report['images']}
    if mapping != {r['path']: r['branch'] for r in report['images']}:
        raise PilotBlocked('BRANCH_MAP_CHANGED')
    criteria = [r['constraint_id'] for r in manifest['rubric']]
    seen, observations = set(), {}
    for item in review['images']:
        path = item['path']
        if (path not in mapping or path in seen or originals[path]['sha256'] != item['sha256']
                or sha((run_dir / path).read_bytes()) != item['sha256']):
            raise PilotBlocked('REVIEW_IMAGE_MISMATCH')
        seen.add(path)
        rows = item['observations']
        if sorted(r['constraint_id'] for r in rows) != sorted(criteria):
            raise PilotBlocked('INCOMPLETE_REVIEW')
        for row in rows:
            x0, y0, x1, y1 = row['region']
            if x1 <= x0 or y1 <= y0 or (row['preserved'] == 'YES' and row['severity'] != 'S0'):
                raise PilotBlocked('INVALID_VISUAL_FINDING')
        observations[mapping[path]] = {r['constraint_id']: r for r in rows}
    a, b = observations['A'], observations['B']
    s3 = any(r['severity'] == 'S3' for rows in observations.values() for r in rows.values())
    unknown = any(r['preserved'] == 'UNKNOWN' for rows in observations.values() for r in rows.values())
    regressions = [k for k in a if (a[k]['preserved'] == 'YES' and b[k]['preserved'] == 'NO') or b[k]['severity'] > a[k]['severity']]
    improvements = [k for k in a if a[k]['preserved'] == 'NO' and b[k]['preserved'] == 'YES']
    protected_loss = [r['constraint_id'] for r in manifest['rubric'] if
        r['priority'] in {'P0','PR0','PR1','LOCK'} and b[r['constraint_id']]['preserved'] == 'NO']
    unauthorized = [r['constraint_id'] for r in manifest['rubric'] if r['category'] == 'unauthorized_change' and b[r['constraint_id']]['preserved'] == 'NO']
    failure = bool(s3 or regressions or protected_loss or unauthorized)
    verdict = 'WORSE' if failure else ('INDETERMINATE' if unknown else ('BETTER' if improvements else 'TIE'))
    result = {'run_id': report['run_id'], 'fixture_id': manifest['fixture_id'],
              'status': 'FAIL' if failure else ('PASS' if verdict == 'BETTER' and report['seed_controlled'] else 'INCONCLUSIVE'),
              'verdict': verdict, 'improvements': improvements, 'regressions': regressions,
              'protected_loss': protected_loss, 'unauthorized_changes': unauthorized, 's3': s3, 'review_sha256': sha(json.dumps(review,sort_keys=True).encode()),
              'limitation': None if report['seed_controlled'] else 'UNCONTROLLED_VARIATION'}
    save(run_dir / 'review.submitted.json', review)
    save(run_dir / 'evaluation.json', result)
    if failure:
        # Campaign execution checks this stop marker before any subsequent call.
        marker = run_dir.parent / 'STOP'
        if not marker.exists():
            marker.write_text('Critical visual failure in ' + report['run_id'] + '\n')
    return result


def close_campaign(run_dirs, selected_fixtures, regression_passed):
    """All selected fixtures must have valid evidence; at least one improvement."""
    results = [json.loads((Path(p) / 'evaluation.json').read_text()) for p in run_dirs]
    complete = (len(selected_fixtures) >= 4 and len(set(selected_fixtures)) == len(selected_fixtures)
                and sorted(r['fixture_id'] for r in results) == sorted(selected_fixtures))
    if any(r['status'] == 'FAIL' for r in results):
        status = 'FAIL'
    elif (complete and regression_passed and any(r['status'] == 'PASS' for r in results)
          and all(r['verdict'] in {'BETTER','TIE'} and not r['limitation'] for r in results)):
        status = 'PASS'
    else:
        status = 'INCONCLUSIVE'
    return {'status': status, 'results': results, 'production_authorized': False}
