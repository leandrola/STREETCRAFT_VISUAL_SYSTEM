"""Inventory original sources and exact prospective admission; no visual claims."""
import json
from .harness import ROOT, sha
from ..generation_compiler import digest


def audit(*, include_dry_runs=True):
    specs = [('KENNYS-ROOFTOP', None, ['observed facade preservation', 'authorized rooftop design (pending graph)']),
             ('R2B-191-C','jpg',['Reference Isolation','authored geography']),
             ('R2B-191-D','jpg',['Semantic Text Lock']),
             ('R2B-191-E','jpg',['Occlusion Lock']),
             ('R2B-191-F','png',['CG-F camera'])]
    registry = json.loads((ROOT/'visual_scene_graph/pilot/allowlist.json').read_text())
    rows = []
    for ident, ext, phenomena in specs:
        source = (ROOT/'benchmark/r2b_1_9_1/evidence_2026_09_21'/f'{ident}_source.{ext}' if ext else
                  ROOT/'visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg')
        row = {'fixture_id':ident, 'critical':True, 'conditional':ident=='R2B-191-F',
               'phenomena':phenomena, 'status':'BLOCKED',
               'source':{'path':str(source.relative_to(ROOT)), 'sha256':sha(source.read_bytes())} if source.exists() else None,
               'source_status':'RECEIVED_UNBOUND' if source.exists() else 'MISSING',
               'reason':'MISSING_FROZEN_REQUEST_SAR2_RR2_CGC_BINDING', 'substitution':None, 'fresh_pairs':0}
        if ident == 'R2B-191-D':
            path = ROOT/'visual_scene_graph/pilot/fixtures/r2b_d_new_01/manifest.json'
            if path.exists():
                manifest = json.loads(path.read_text())
                entry = registry['fixtures'][ident]
                intact = all(sha((ROOT/r['path']).read_bytes()) == r['sha256'] for r in manifest['artifacts'].values())
                if intact and entry['status'] == 'ADMITTED' and entry['manifest_sha256'] == digest(manifest):
                    row.update(status='ADMITTED_PENDING_DRY_RUN', source_status='BOUND_PROSPECTIVELY',
                               reason='PENDING_VISUAL', manifest=str(path.relative_to(ROOT)),
                               manifest_sha256=digest(manifest), historical_recovery=False)
                    if include_dry_runs:
                        from .review_dry_run import review
                        reviews = (ROOT/'validation/vsg_2b/dry_runs').glob('*/delta_review.json')
                        for evidence in sorted(reviews, key=lambda p: p.stat().st_mtime, reverse=True):
                            try:
                                recorded = json.loads(evidence.read_text())
                                verified = review(evidence.parent)
                                if recorded['manifest_sha256'] == digest(manifest) and recorded['delta_sha256'] == verified['delta_sha256']:
                                    row.update(status='CORPUS_RECOVERY_DRY_RUN_PASS',
                                               dry_run_review={'path':str(evidence.relative_to(ROOT)), 'sha256':sha(evidence.read_bytes())})
                                    break
                            except (ValueError, OSError, KeyError, TypeError):
                                continue
        if ident == 'KENNYS-ROOFTOP':
            row['scope_record'] = 'visual_scene_graph/pilot/fixtures/kennys/reception.json'
            row['rooftop_provenance'] = 'AUTHORIZED_INFERENCE; not observed in source'
        rows.append(row)
    return {'status':'BLOCKED','reason':'PENDING_VISUAL_AND_REMAINING_SOURCE_BINDINGS','fixtures':rows,
            'initial_image_budget':8,'conditional_fifth_pair':'Requires a versioned budget change after coverage review',
            'generator_capability':'No local provider bridge configured; D settings explicitly provisional and dry-run only.',
            'user_confirmation':'Kenny source received 2026-09-29; user confirms no other rooftop view. New plausible rooftop design authorized, preserving observed facade.'}


if __name__ == '__main__':
    print(json.dumps(audit(),indent=2))
