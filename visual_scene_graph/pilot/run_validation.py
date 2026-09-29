"""Refresh technical evidence and admitted D dry run; never generate images."""
import importlib.metadata
import json
import platform
import re
import subprocess
import sys

from .harness import ROOT, control_file_hashes, sha, prepare, execute
from .audit_corpus import audit
from .bind_d import FIXTURE, reconstruct
from .review_dry_run import review
from ..generation_compiler import digest
from ..run_generation_benchmark import build_report, verify_report


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def artifact(path):
    return {'path':str(path.relative_to(ROOT)), 'sha256':sha(path.read_bytes())}


def main():
    out = ROOT/'validation/vsg_2b'
    out.mkdir(exist_ok=True)
    completed = subprocess.run([sys.executable, str(ROOT/'benchmark/run_regression_suite.py')],
                               cwd=ROOT, capture_output=True, text=True)
    regression = json.loads(completed.stdout)
    write(out/'regression.json', regression)
    check = next(c for c in regression['checks'] if c['name']=='visual_scene_graph/pilot/test_pilot.py')
    match = re.search(r'Ran (\d+) tests', check['stderr'])
    controls = {'status':check['status'], 'tests':int(match.group(1)) if match else None,
                'evidence':check, 'scope':'Synthetic deterministic controls only; not visual evidence'}
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
                   'limitation':'Synthetic source / mocked precondition check. Separate from real D dry-run evidence.',
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
    dry_run = {'real_corpus':'BLOCKED', 'control_renderer':'PASS',
               'control_preview':artifact(out/'CONTROL_RENDERER_PREVIEW.json')}
    d = next(row for row in corpus['fixtures'] if row['fixture_id'] == 'R2B-191-D')
    if d['status'] == 'ADMITTED_PENDING_DRY_RUN':
        snapshots, comparison = reconstruct()
        for name, value in snapshots.items():
            if json.loads((FIXTURE/(name+'.json')).read_text()) != value:
                raise ValueError('PROSPECTIVE_REPLAY_MISMATCH:' + name)
        manifest = json.loads((FIXTURE/'manifest.json').read_text())
        registry = json.loads((ROOT/'visual_scene_graph/pilot/allowlist.json').read_text())
        prepared = prepare(manifest, registry)
        run_path, report = execute(prepared, out/'dry_runs')
        reviewed = review(run_path)
        reviewed['command'] = '.venv-sc/bin/python -m visual_scene_graph.pilot.run_validation'
        reviewed['source_binding_replay'] = 'PASS: runtime/SAR2/RR2/CGC/graphs/context/contract from frozen request'
        reviewed['coverage'] = comparison['coverage']
        write(run_path/'delta_review.json', reviewed)
        d['status'] = 'CORPUS_RECOVERY_DRY_RUN_PASS'
        d['dry_run_review'] = artifact(run_path/'delta_review.json')
        dry_run.update(real_corpus='CORPUS_RECOVERY_DRY_RUN_PASS', report=artifact(run_path/'report.json'),
                       review=artifact(run_path/'delta_review.json'), delta_sha256=report['delta_sha256'])
    write(out/'corpus_audit.json', corpus)
    qa = {'suite':'VSG-2B Controlled Generation Pilot', 'date':'2026-09-29',
          'status':'BLOCKED', 'reason':'PENDING_VISUAL_AND_REMAINING_SOURCE_BINDINGS',
          'infrastructure_status':'IMPLEMENTED', 'control_tests':controls['tests'], 'control_status':'PASS',
          'vsg2a_verification':verification, 'unified_regression':regression['R0'], 'dependencies':dependencies,
          'production_authorized':False, 'stable_client_changed':False,
          'image_budget':8, 'generation_attempts':0, 'fresh_images':0, 'valid_pairs':0,
          'technical_failures':0, 'technical_failure_rate':None,
          'visual_verdict':'INDETERMINATE', 'visual_findings':[], 'dry_run':dry_run,
          'corpus':corpus, 'preconditions':artifact(out/'preconditions.json'),
          'limitations':['D is a prospective annotation of the existing source, not historical snapshot recovery.',
                        'Other fixtures remain unbound; Kenny roof is authorized design, never observed source.',
                        'D provider/model/quality are provisional; no provider capability or operational choice asserted.',
                        'No independent visual review or output comparison performed.',
                        'No historical candidate reused as a fresh output.',
                        'Synthetic tests establish controls only, not visual merit.']}
    write(ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json', qa)
    summary = f'''# VSG-2B controlled generation pilot · 2026-09-29

**General status: BLOCKED / PENDING_VISUAL.** The technical D milestone is **{dry_run['real_corpus']}**. The visual pilot is incomplete.

- Deterministic controls: **{controls['tests']}/{controls['tests']} PASS**, synthetic only.
- Current VSG-2A replay: **{verification['cases_verified']}/25 PASS**, {verification['files_verified']} files verified; historical suite unchanged.
- Unified regression: **{regression['R0']}** ({len(regression['checks'])} checks).
- Generation attempts / fresh images / valid pairs: **0 / 0 / 0**.
- Real D dry run: **INCONCLUSIVE / DRY_RUN_NO_IMAGES**; payload equality, snapshot hashes and delta reviewed separately from the renderer. No visual improvement claim.

D now has a new prospective source-bound annotation, replayable snapshots and an admitted manifest. P0, PR0, PR1 and LOCK coverage is nonempty and preserved. No historical request was recovered. Kenny's original JPEG is received and unbound; its observed facade must be separated from any authorized inferred rooftop design before admission. C/E remain unbound; F depends on coverage and budget review.

Provider/model/quality are explicit dry-run placeholders. Before future image generation, choose supported operational settings, version and re-admit the manifest, refresh controls, repeat the dry run and review its delta. This advance authorizes no image calls.

[Runbook](../visual_scene_graph/pilot/fixtures/r2b_d_new_01/RUNBOOK.md) · [Full QA](VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) · [Corpus audit](vsg_2b/corpus_audit.json) · [Controls](vsg_2b/controls.json) · [Regression](vsg_2b/regression.json).
'''
    (ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.md').write_text(summary)
    print(json.dumps({'technical_status':'PASS','pilot_status':'BLOCKED/PENDING_VISUAL',
                      'dry_run':dry_run,'tests':controls['tests'],'generation_attempts':0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
