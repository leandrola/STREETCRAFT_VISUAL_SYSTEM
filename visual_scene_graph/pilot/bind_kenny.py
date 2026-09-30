"""Create or replay K1; no admission, provider or Archive calls."""
import argparse
import json
from . import kenny_binding as k1
from .harness import ROOT, sha, validate
from .fixture_replay import verify_snapshots
from ..generation_compiler import digest

FIXTURE = k1.FIXTURE


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode()


def reconstruct():
    request = json.loads((FIXTURE/'request.json').read_text())
    sidecars = k1.load_sidecars(request)
    expected = k1.make_request(json.loads(sidecars['observations.json']), json.loads(sidecars['design.json']))
    k1.require(request == expected, 'REQUEST_AUTHORITY_OR_DIRECTIVES')
    k1.require(sha((ROOT/k1.SOURCE_PATH).read_bytes()) == k1.SOURCE_SHA, 'SOURCE_HASH')
    return k1.build_snapshots(request)


def make_manifest(snapshots):
    artifacts = {}
    for name in ('request', *snapshots, 'source'):
        path = ROOT/k1.SOURCE_PATH if name == 'source' else FIXTURE/(name+'.json')
        raw = encoded(snapshots[name]) if name in snapshots else path.read_bytes()
        artifacts[name] = dict(path=str(path.relative_to(ROOT)), sha256=sha(raw),
            provenance='Prospective K1 source/design binding; source facts only in SAR2/VSG. Request k1_binding records pin original JPEG, K0, reception, observations, design and provenance; mandatory frozen-byte verifier. No historical snapshot recovery or rooftop observation.')
    rubric=[]
    for c in snapshots['contract']['constraints']:
        rubric.append(dict(constraint_id=c['id'], priority=c['priority'], target=c['id'],
            category='lock' if c['id'].startswith('lock:') else 'identity',
            criterion='Preserve the exact source constraint and its authority. Facade proportions, opening rhythm and KSR topology remain unchanged; exact main sign/banner literals remain. Unreadable microtext and original unseen geometry remain unknown. S3 for P0/PR0 violation, invented literal or design relabeled observed.'))
    d=json.loads((FIXTURE/'design.json').read_text())
    for r in d['nodes']+d['relationships']:
        rubric.append(dict(constraint_id='design:'+r['id'], category='relation', priority='REQUIRED',
            target=r['id'], criterion='Execute this REQUIRED prospective design component/relation from KENNYS_ROOFTOP_DESIGN_V1; never score fidelity to an original roof. S3 if absent, relation broken or facade changed. '+json.dumps(r,ensure_ascii=False)))
    for ident,rule in d['visual_rules'].items():
        rubric.append(dict(constraint_id='design:'+ident,category='identity',priority='REQUIRED',target=ident,
                          criterion=rule+' S3 if required volumetric structure is absent; finish-only deviations S2.'))
    rubric.extend([
        dict(constraint_id='identity',category='identity',priority='REQUIRED',target='observed facade',criterion='KOBS-01..12 and KSR-01..10 govern observed preservation and uncertainty. Rooftop original remains unknown.'),
        dict(constraint_id='unauthorized_change',category='unauthorized_change',priority='REQUIRED',target='source/design boundary',criterion='S3: source redesign, invented text or observed status, excluded component or geography. No rooftop source-lock coverage claimed. '+ ' '.join(d['prohibitions']))])
    manifest=dict(schema_version='1.0.0',fixture_id=k1.IDENT,pilot_enabled=True,
        source_binding=dict(source_identity=k1.SOURCE_ID,attested_by='Codex, native JPEG inspection and prospective annotation, 2026-09-29',
            evidence='JPEG '+k1.SOURCE_SHA+' (736x414); K0 '+k1.RECORDS['k0.md'][1]+'. Separate KENNYS_SOURCE_OBS_V1 and KENNYS_ROOFTOP_DESIGN_V1. Exact sidecar paths/hashes in request.k1_binding, checked in replay/prepare/execute and persisted review.'),
        artifacts=artifacts,required_priorities=['P0','PR0','PR1','LOCK'],
        generation=dict(provider='DRY_RUN_ONLY_UNSELECTED_PROVIDER',model='DRY_RUN_ONLY_UNSELECTED_MODEL',seed=None,
            parameters=dict(size='736x736',quality='DRY_RUN_ONLY_UNSELECTED',output_format='png')),rubric=rubric)
    validate(manifest,'manifest')
    return manifest


def verify():
    k1.verify_preserved()
    manifest, comparison=verify_snapshots(FIXTURE,reconstruct)
    snapshots={k:json.loads((ROOT/r['path']).read_text()) for k,r in manifest['artifacts'].items() if k not in {'request','source'}}
    k1.require(manifest == make_manifest(snapshots), 'MANIFEST_REPLAY')
    return manifest,comparison


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    args=parser.parse_args()
    k1.verify_preserved()
    if args.freeze:
        k1.require(not (FIXTURE/'manifest.json').exists(), 'ALREADY_FROZEN')
        request=k1.make_request(json.loads((FIXTURE/'observations.json').read_text()),json.loads((FIXTURE/'design.json').read_text()))
        with (FIXTURE/'request.json').open('xb') as h:h.write(encoded(request))
        snapshots,comparison=reconstruct()
        manifest=make_manifest(snapshots)
        for name,value in {**snapshots,'manifest':manifest}.items():
            with (FIXTURE/(name+'.json')).open('xb') as h:h.write(encoded(value))
    manifest,comparison=verify()
    print(json.dumps(dict(status='PASS',manifest_sha256=digest(manifest),coverage=comparison['coverage'],
                         design_nodes=3,design_relations=4,archive_calls=0,visual='PENDING')))


if __name__=='__main__':
    main()
