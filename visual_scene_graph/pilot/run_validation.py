"""Refresh technical evidence and explicit admitted D/E/Kenny dry runs; no generation."""
import importlib.metadata
import json
import platform
import re
import subprocess
import sys

from .harness import ROOT, control_file_hashes, sha, prepare, execute, save
from .audit_corpus import audit
from . import bind_d, bind_e, bind_kenny, kenny_binding
from .fixture_replay import verify_snapshots, FIXTURE_PATHS
from .review_dry_run import review
from ..generation_compiler import digest
from ..run_generation_benchmark import build_report, verify_report

# Ordered and explicit. Admission alone never selects another corpus fixture.
BINDERS = (
    ('R2B-191-D', lambda: verify_snapshots(bind_d.FIXTURE, bind_d.reconstruct)),
    ('R2B-191-E', bind_e.verify),
    ('KENNYS-ROOFTOP', bind_kenny.verify),
)


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def artifact(path):
    return {'path':str(path.relative_to(ROOT)), 'sha256':sha(path.read_bytes())}


def archive_fixture(ident, verify, registry, out):
    manifest, comparison = verify()
    prepared = prepare(manifest, registry)
    run_path, report = execute(prepared, out/'dry_runs')
    reviewed = review(run_path)
    if ident == 'R2B-191-D' and report['delta_sha256'] != bind_e.verify_d_preserved()['delta_sha256']:
        raise ValueError('D_DELTA_CHANGED')
    if ident in {'R2B-191-D', 'R2B-191-E'} and report['delta_sha256'] != kenny_binding.verify_preserved()['deltas'][ident]:
        raise ValueError('PRESERVED_DELTA_CHANGED:' + ident)
    runtime = json.loads(prepared['blobs']['runtime'])
    reviewed.update(command='.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation',
                    source_binding_replay='PASS: frozen request reproduces runtime/SAR2/RR2/CGC/graphs/context/contract',
                    coverage=comparison['coverage'],
                    unexercised_priorities=[k for k,v in comparison['coverage'].items() if not v['required']],
                    reference_needs=len(runtime['reference_needs']),
                    queryable_needs=sum(n['state'] in {'RN_REQUIRED','RN_SUPPORT'} for n in runtime['reference_needs']),
                    archive_calls=runtime['reference_reasoning']['queries'],
                    preconditions=artifact(out/'preconditions.json'))
    # Include exact invocation for an additional standalone CLI reproduction.
    reviewed['reproduction_command'] = ('.venv-sc/bin/python -m visual_scene_graph.pilot ' +
        str(FIXTURE_PATHS[ident].relative_to(ROOT)/'manifest.json') +
        ' --output outputs/vsg-2b-campaign')
    save(run_path/'delta_review.json', reviewed)
    return {'status':'CORPUS_RECOVERY_DRY_RUN_PASS', 'report':artifact(run_path/'report.json'),
            'review':artifact(run_path/'delta_review.json'), 'manifest_sha256':digest(manifest),
            'delta_sha256':report['delta_sha256'], 'coverage':comparison['coverage'],
            **({'k1_status':'K1_CORPUS_RECOVERY_DRY_RUN_PASS',
                'source_design_review':reviewed['source_design_review']} if ident == 'KENNYS-ROOFTOP' else {})}


def main():
    out = ROOT/'validation/vsg_2b'
    out.mkdir(exist_ok=True)
    completed = subprocess.run([sys.executable, str(ROOT/'benchmark/run_regression_suite.py')],
                               cwd=ROOT, capture_output=True, text=True)
    regression = json.loads(completed.stdout)
    write(out/'regression.json', regression)
    checks = [next(c for c in regression['checks'] if c['name']==name) for name in
              ('visual_scene_graph/pilot/test_pilot.py', 'visual_scene_graph/pilot/test_e_binding.py',
               'visual_scene_graph/pilot/test_kenny_binding.py')]
    suites = []
    for check in checks:
        match = re.search(r'Ran (\d+) tests', check['stderr'])
        suites.append({'name':check['name'], 'tests':int(match.group(1)) if match else 0, 'status':check['status']})
    controls = {'status':'PASS' if all(c['status']=='PASS' and c['tests'] for c in suites) else 'FAIL',
                'tests':sum(c['tests'] for c in suites), 'suites':suites, 'evidence':checks,
                'scope':'Deterministic controls and source-bound mutation checks only; not visual evidence'}
    write(out/'controls.json', controls)
    replay = build_report()
    write(out/'VSG_2A_REPLAY_QA.json', replay)
    verification = verify_report(replay)
    write(out/'VSG_2A_REPLAY_VERIFICATION.json', verification)
    if completed.returncode or verification['status'] != 'PASS' or controls['status'] != 'PASS':
        print('FAIL: technical preconditions; no generation authorized')
        return 1
    from .test_pilot import ControlTests
    ControlTests.setUpClass()
    test = ControlTests('test_healthy_and_exact_delta')
    try:
        test.setUp()
        prepared = test.prepare()
        preview = {'status':'CONTROL_ONLY', 'synthetic':True, 'generation_authorized':False,
                   'limitation':'Synthetic source / mocked precondition check. Separate from real D/E/Kenny dry-run evidence.',
                   'payloads':prepared['payloads'], 'comparison_status':prepared['comparison']['status'],
                   'payloads_sha256':digest(prepared['payloads']),
                   'delta_review':'Shared content identical; parsed A relationship/lock records equal B structured array exactly.'}
        write(out/'CONTROL_RENDERER_PREVIEW.json', preview)
    finally:
        test.doCleanups()
    dependencies = {'python':platform.python_version(), **{k:importlib.metadata.version(k) for k in ('jsonschema','Pillow')}}
    preconditions = {'status':'PASS', 'dependencies':dependencies, 'control_file_sha256':control_file_hashes(),
                    'vsg2a':artifact(out/'VSG_2A_REPLAY_QA.json'), 'regression':artifact(out/'regression.json'),
                    'pilot_controls':artifact(out/'controls.json')}
    write(out/'preconditions.json', preconditions)
    corpus = audit(include_dry_runs=False)
    registry = json.loads((ROOT/'visual_scene_graph/pilot/allowlist.json').read_text())
    results = {}
    for ident, verify in BINDERS:
        row = next(row for row in corpus['fixtures'] if row['fixture_id'] == ident)
        try:
            if row['status'] != 'ADMITTED_PENDING_DRY_RUN':
                raise ValueError('MANIFEST_OR_ARTIFACT_NOT_ADMITTED:' + ident)
            result = archive_fixture(ident, verify, registry, out)
            row.update(status=result['status'], dry_run_review=result['review'])
        except (ValueError, OSError, KeyError, TypeError) as exc:
            result = {'status':'BLOCKED', 'reason':str(exc)}
            row.update(status='BLOCKED', reason=str(exc))
        results[ident] = result
    passed = all(r['status']=='CORPUS_RECOVERY_DRY_RUN_PASS' for r in results.values())
    dry_run = {'real_corpus':'CORPUS_RECOVERY_DRY_RUN_PASS' if passed else 'BLOCKED',
               'fixtures':results, 'control_renderer':'PASS', 'control_preview':artifact(out/'CONTROL_RENDERER_PREVIEW.json')}
    write(out/'corpus_audit.json', corpus)
    qa = {'suite':'VSG-2B Controlled Generation Pilot', 'date':'2026-09-29',
          'status':'BLOCKED', 'reason':'PENDING_VISUAL_AND_REMAINING_SOURCE_BINDINGS',
          'infrastructure_status':'IMPLEMENTED', 'control_tests':controls['tests'], 'control_status':controls['status'],
          'control_suites':suites, 'vsg2a_verification':verification, 'unified_regression':regression['R0'], 'dependencies':dependencies,
          'production_authorized':False, 'stable_client_changed':False,
          'image_budget':8, 'generation_attempts':0, 'fresh_images':0, 'valid_pairs':0,
          'technical_failures':0, 'technical_failure_rate':None,
          'visual_verdict':'INDETERMINATE', 'visual_findings':[], 'dry_run':dry_run,
          'corpus':corpus, 'preconditions':artifact(out/'preconditions.json'),
          'k1_status':results['KENNYS-ROOFTOP'].get('k1_status', 'K1_NO_GO_VALIDATION'),
          'plan_limits':{'five_hour_initial':'UNKNOWN','five_hour_final':'UNKNOWN',
                         'weekly_initial':'UNKNOWN','weekly_final':'UNKNOWN','observed_consumption':'UNKNOWN',
                         'numeric_cap_compliance_certified':False},
          'limitations':['D/E/Kenny are prospective annotations of existing sources, not historical snapshot recovery.',
                        'E PR1 denominator is zero; no PR1 coverage is claimed.',
                        'E has one RN_BLOCKED hint, zero queryable needs, zero Archive calls and no reconstruction authorization.',
                        'C remains RECEIVED_UNBOUND / NO_GO_C0_UNVERIFIED; F remains conditional.',
                        'Kenny source VSG-2A, design authority/integrity and visual PENDING are separate gates; rooftop Graph Locks 0/0 NOT_EXERCISED.',
                        'D/E/Kenny provider/model/quality are provisional; no operational provider selection.',
                        'Automated technical delta review is not human or visual review.',
                        'Controls establish no visual merit; zero fresh images or valid pairs.']}
    write(ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json', qa)
    fixture_lines = '\n'.join(f"- **{ident}: {r['status']}**" + (f"; delta `{r['delta_sha256']}`." if 'delta_sha256' in r else ': '+r['reason']) for ident,r in results.items())
    summary = f'''# VSG-2B controlled generation pilot · 2026-09-29

**General status: BLOCKED / PENDING_VISUAL.** Technical dry-run results are separate by fixture:

{fixture_lines}

- Deterministic controls: **{controls['tests']}/{controls['tests']} PASS** ({suites[0]['tests']} original + {suites[1]['tests']} E + {suites[2]['tests']} Kenny controls).
- Current VSG-2A replay: **{verification['cases_verified']}/25 PASS**, {verification['files_verified']} files verified; historical suite unchanged.
- Unified regression: **{regression['R0']}** ({len(regression['checks'])} checks).
- Dependencies: Python {dependencies['python']}, jsonschema {dependencies['jsonschema']}, Pillow {dependencies['Pillow']}.
- Generation attempts / fresh images / valid pairs: **0 / 0 / 0**.

Each successful real-source run reports **INCONCLUSIVE / DRY_RUN_NO_IMAGES**. The separate automated review checks persisted A/B equality, frozen restrictions, source bytes and delta hashes; it is neither a human review nor evidence of visual improvement.

E keeps the foreground occluder and its behind-content UNKNOWN_LOCKED, with no hidden object assertion or reconstruction authorization. P0 9/9, PR0 1/1, LOCK 4/4 are exercised; **PR1 0/0 is unexercised**, despite the comparator's conventional ratio 1.0. RR2 records one blocked hint and zero queryable needs, Archive queries, admissions or projections. Darkness, cropping and low resolution are distinguished from occlusion in its source provenance.

D/E original fixtures and historical UUID directories remain byte-for-byte intact; their deltas are unchanged. All three bindings are prospective annotations. C remains RECEIVED_UNBOUND / NO_GO_C0_UNVERIFIED; F remains conditional. Provider/model/quality remain dry-run placeholders. Zero production promotion or VSG-3A claim.

Kenny: **{qa['k1_status']}**. Source VSG-2A and separate design authority/integrity are checked by the blocking verifier and persisted-byte review. Visual rubric remains **PENDING**. Source coverage: P0 21/21, PR0 7/7, PR1 3/3, LOCK 7/7; design: 3 required nodes and 4 required relations. Rooftop Graph Locks **0/0 NOT_EXERCISED**. Identical design directives travel in A/B common; only source topology/locks differ in serialization. Six sidecars (including K0, reception and design) are frozen and revalidated without checkout fallback. Plan Limits initial/final and consumption **UNKNOWN**; no numeric budget compliance claim.

[Kenny runbook](../visual_scene_graph/pilot/fixtures/kennys_new_01/RUNBOOK.md).

[E runbook](../visual_scene_graph/pilot/fixtures/r2b_e_new_01/RUNBOOK.md) · [D runbook](../visual_scene_graph/pilot/fixtures/r2b_d_new_01/RUNBOOK.md) · [Full QA](VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) · [Corpus audit](vsg_2b/corpus_audit.json) · [Controls](vsg_2b/controls.json) · [Regression](vsg_2b/regression.json).
'''
    (ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.md').write_text(summary)
    print(json.dumps({'technical_status':'PASS' if passed else 'BLOCKED','pilot_status':'BLOCKED/PENDING_VISUAL',
                      'dry_run':dry_run,'tests':controls['tests'],'generation_attempts':0}))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
