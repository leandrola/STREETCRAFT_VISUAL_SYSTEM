#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,json,ast,hashlib
ROOT=Path(__file__).resolve().parents[1]

def run(rel,cwd=None):
 p=ROOT/rel
 r=subprocess.run([sys.executable,str(p)],cwd=str(cwd or p.parent),capture_output=True,text=True)
 return {"name":rel,"status":"PASS" if r.returncode==0 else "FAIL","stdout":r.stdout.strip(),"stderr":r.stderr.strip()}

checks=[]
# JSON
errors=[]
for p in ROOT.rglob('*.json'):
 try:json.loads(p.read_text(encoding='utf-8'))
 except Exception as e:errors.append({'file':str(p.relative_to(ROOT)),'error':str(e)})
checks.append({'name':'json_integrity','status':'PASS' if not errors else 'FAIL','errors':errors})
# syntax
syntax_errors=[]
for p in ROOT.rglob('*.py'):
 try:ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
 except Exception as e:syntax_errors.append({'file':str(p.relative_to(ROOT)),'error':str(e)})
checks.append({'name':'python_syntax','status':'PASS' if not syntax_errors else 'FAIL','errors':syntax_errors})
# core deterministic tests
checks += [
 run('command_invocation/test_commands.py',ROOT/'command_invocation'),
 run('hardening/test_operational_hardening.py',ROOT/'hardening'),
 run('reference_runtime/test_archive_aware_runtime.py',ROOT),
 run('reference_runtime/test_reference_reasoning.py',ROOT/'reference_runtime'),
 run('scene_intelligence/test_scene_intelligence.py',ROOT/'scene_intelligence'),
 run('visual_scene_graph/test_vsg_observer.py',ROOT),
 run('integration/test_streetcraft_orchestrator.py',ROOT),
 run('validation/test_patch_1_9_1.py',ROOT),
 run('validation/test_single_client_1_10_0.py',ROOT),
]
# Exact embedded visuals have a provenance manifest; verify current bytes against recorded git blob ids.
prov=json.loads((ROOT/'RECONSTRUCTION_PROVENANCE.json').read_text())
def git_blob(p):
 b=p.read_bytes();return hashlib.sha1(f'blob {len(b)}'.encode()+b'\0'+b).hexdigest()
asset_bad=[]
for rec in prov['exact_embedded_assets']:
 p=ROOT/rec['path']
 if not p.exists() or git_blob(p)!=rec['git_blob_sha']:
  asset_bad.append(rec['path'])
checks.append({'name':'exact_embedded_asset_identity','status':'PASS' if not asset_bad else 'FAIL','failures':asset_bad})
remote=json.loads((ROOT/'benchmark/fixtures/REMOTE_BINARY_FIXTURES.json').read_text())
l2_bad=[r['path'] for r in remote['fixtures'] if not (ROOT/r['path']).exists() or git_blob(ROOT/r['path'])!=r['git_blob_sha']]
checks.append({'name':'historical_l2_embedded_identity','status':'PASS' if len(remote['fixtures'])==7 and not l2_bad else 'FAIL','fixture_count':len(remote['fixtures']),'failures':l2_bad})
gold=json.loads((ROOT/'benchmark/fixtures/GOLDEN_FIXTURES.json').read_text())
golden_bad=[r['path'] for r in gold['fixtures'] if not (ROOT/r['path']).exists() or hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['sha256']]
checks.append({'name':'golden_fixture_integrity','status':'PASS' if not golden_bad else 'FAIL','fixtures_checked':len(gold['fixtures']),'failures':golden_bad})
checks.append(run('benchmark/check_r2_baseline.py',ROOT))
status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
r2b=json.loads((ROOT/'benchmark/r2b_1_9_1/RUN_STATUS.json').read_text())
real_archive_path=ROOT/'validation/RR2_REAL_ARCHIVE_VALIDATION_V1.json'
real_archive=json.loads(real_archive_path.read_text()) if real_archive_path.exists() else {'status':'PENDING'}
cgc_path=ROOT/'validation/CGC_END_TO_END_REAL_ARCHIVE_V1.json'
cgc=json.loads(cgc_path.read_text()) if cgc_path.exists() else {'status':'PENDING'}
promotion_ready=(status=='PASS' and r2b.get('status')=='PASS' and r2b.get('s3_count')==0 and (r2b.get('global_score') or 0)>=90 and real_archive.get('status')=='PASS' and cgc.get('status')=='PASS')
final_gate_path=ROOT/'validation/RELEASE_GATE_1_10_0_FINAL.json'
final_gate=json.loads(final_gate_path.read_text()) if final_gate_path.exists() else {}
stable_promotion=bool(promotion_ready and final_gate.get('stable_promotion') is True and final_gate.get('status')=='PASS')
report={'suite':'SVS 1.10.0 Unified Client Regression','base_release':'SVS 1.9.1 / CIL 1.1','R0':status,'R1_current_embedded_assets':next(c['status'] for c in checks if c['name']=='exact_embedded_asset_identity'),'R2b_visual':r2b.get('status','PENDING'),'R2b_global_score':r2b.get('global_score'),'R2b_s3':r2b.get('s3_count'),'RR2_real_archive':real_archive.get('status','PENDING'),'CGC_end_to_end':cgc.get('status','PENDING'),'promotion_ready':promotion_ready,'stable_promotion':stable_promotion,'release_status':'STABLE' if stable_promotion else ('PROMOTION_READY' if promotion_ready else 'GATED'),'pending':[] if promotion_ready else ['unmet technical gate'],'checks':checks}
out=ROOT/'validation/INTEGRATION_QA.json';out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if status=='PASS' else 1)
