"""Refresh local technical evidence; never generate images or claim visual PASS."""
import importlib.metadata
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

from .harness import ROOT, control_file_hashes, sha
from .audit_corpus import audit
from ..generation_compiler import digest
from ..run_generation_benchmark import build_report, verify_report


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def main():
    out = ROOT/'validation/vsg_2b'
    out.mkdir(exist_ok=True)
    # Unified runner includes pilot controls. Its established output path is preserved.
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
    corpus = audit()
    write(out/'corpus_audit.json', corpus)
    if completed.returncode or verification['status'] != 'PASS' or controls['status'] != 'PASS':
        print('FAIL: technical preconditions; no generation authorized')
        return 1
    # Keep a reviewable A/B expression preview, explicitly outside the admitted corpus.
    from .test_pilot import ControlTests
    ControlTests.setUpClass()
    test = ControlTests('test_healthy_and_exact_delta')
    try:
        test.setUp()
        prepared = test.prepare()
        preview = {'status':'CONTROL_ONLY', 'synthetic':True, 'generation_authorized':False,
                   'limitation':'Synthetic source / mocked precondition check. No real corpus manifest is ready.',
                   'payloads':prepared['payloads'], 'comparison_status':prepared['comparison']['status'],
                   'payloads_sha256':digest(prepared['payloads']),
                   'delta_review':'Shared content identical; parsed A relationship/lock records equal B structured array exactly.'}
        write(out/'CONTROL_RENDERER_PREVIEW.json', preview)
    finally:
        test.doCleanups()
    dependencies = {'python':platform.python_version(), **{k:importlib.metadata.version(k) for k in ('jsonschema','Pillow')}}
    def artifact(path):
        return {'path':str(path.relative_to(ROOT)), 'sha256':sha(path.read_bytes())}
    preconditions = {'status':'PASS', 'dependencies':dependencies, 'control_file_sha256':control_file_hashes(),
                    'vsg2a':artifact(out/'VSG_2A_REPLAY_QA.json'), 'regression':artifact(out/'regression.json'),
                    'pilot_controls':artifact(out/'controls.json')}
    write(out/'preconditions.json', preconditions)
    qa = {'suite':'VSG-2B Controlled Generation Pilot', 'date':'2026-09-29',
          'status':'BLOCKED', 'reason':'MISSING_FROZEN_SOURCE_BINDINGS',
          'infrastructure_status':'IMPLEMENTED', 'control_tests':controls['tests'], 'control_status':'PASS',
          'vsg2a_verification':verification, 'unified_regression':regression['R0'], 'dependencies':dependencies,
          'production_authorized':False, 'stable_client_changed':False,
          'image_budget':8, 'generation_attempts':0, 'fresh_images':0, 'valid_pairs':0,
          'technical_failures':0, 'technical_failure_rate':None,
          'visual_verdict':'INDETERMINATE', 'visual_findings':[],
          'dry_run':{'real_corpus':'BLOCKED', 'control_renderer':'PASS', 'control_preview':artifact(out/'CONTROL_RENDERER_PREVIEW.json')},
          'corpus':corpus, 'preconditions':artifact(out/'preconditions.json'),
          'limitations':['No frozen source-to-snapshot bindings; user confirmed unavailable.',
                        'No local provider bridge configured; session image tool exists but source gate blocks generation.',
                        'No independent visual review or output comparison performed.',
                        'No historical candidate reused as a fresh output.',
                        'Fifth pair and retries require a versioned plan/budget change.',
                        'Synthetic tests establish controls only, not visual merit.']}
    write(ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json', qa)
    summary = f'''# VSG-2B controlled generation pilot · 2026-09-29

**BLOCKED: MISSING_FROZEN_SOURCE_BINDINGS.** The user confirmed that the missing snapshots / Kenny source are unavailable. The isolated harness is implemented; the visual pilot is not complete and production is not authorized.

- Deterministic pilot controls: **{controls['tests']}/{controls['tests']} PASS**.
- VSG-2A replay: **25/25 PASS**, current 42-file manifest verified. Original baseline also verified before edits; historical QA retained unchanged.
- Unified regression: **PASS** ({len(regression['checks'])} checks).
- Dependencies: Python {dependencies['python']}, jsonschema {dependencies['jsonschema']}, Pillow {dependencies['Pillow']}.
- Generation attempts / fresh images / valid pairs: **0 / 0 / 0**. Technical failure rate and visual scores are not applicable.
- Real-corpus dry run: **BLOCKED**. Synthetic control renderer preview: **PASS**, no generation authorization or visual evidence.

R2B C/D/E/F original source files have recorded SHA-256 hashes, but lack frozen request/SAR2/RR2/CGC bindings. Kenny has structured fixtures but no traceable source image. No defensible substitution was found. All five registry entries remain `PENDING_EVIDENCE`.

The session has image-generation capability. Missing corpus evidence is the primary blocker; `NO_GENERATOR` is only the harness result for an otherwise admissible run without a configured local bridge.

The provider adapter uses an explicit local JSON protocol; it has not been exercised against a real image provider. Blind review and closure controls have deterministic tests only. Resume by supplying source-bound snapshots and an attested manifest, admitting its hash, refreshing preconditions, reviewing the dry-run payload delta, configuring a real provider bridge, then generating and reviewing each pair within the eight-image budget. Do not infer visual PASS from the technical checks.

[Harness / operational specification](../visual_scene_graph/pilot/README.md) · [Full QA](VSG_2B_CONTROLLED_GENERATION_PILOT_QA.json) · [Corpus audit](vsg_2b/corpus_audit.json) · [Controls](vsg_2b/controls.json) · [Regression](vsg_2b/regression.json) · [Current VSG-2A replay](vsg_2b/VSG_2A_REPLAY_QA.json) · [Control-only payload preview](vsg_2b/CONTROL_RENDERER_PREVIEW.json).
'''
    (ROOT/'validation/VSG_2B_CONTROLLED_GENERATION_PILOT_QA.md').write_text(summary)
    print(json.dumps({'technical_status':'PASS','pilot_status':'BLOCKED','tests':controls['tests'],'generation_attempts':0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
