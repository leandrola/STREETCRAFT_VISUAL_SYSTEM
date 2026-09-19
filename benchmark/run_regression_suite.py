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
 run('scene_intelligence/test_scene_intelligence.py',ROOT/'scene_intelligence'),
 run('validation/test_patch_1_9_1.py',ROOT),
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
checks.append({'name':'historical_l2_remote_fixture_registry','status':'PASS' if len(remote.get('fixtures',[]))==7 else 'FAIL','remote_fixture_count':len(remote.get('fixtures',[])),'note':'provenance registry only; exact bytes not embedded'})
status='PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL'
report={'suite':'SVS 1.9.1 Reconstructed Deterministic Regression','R0':status,'R1_current_embedded_assets':next(c['status'] for c in checks if c['name']=='exact_embedded_asset_identity'),'R2b_visual':'REQUIRED_PENDING','stable_promotion':False,'checks':checks}
out=ROOT/'validation/REGRESSION_REPORT_1_9_1_RECONSTRUCTED.json';out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if status=='PASS' else 1)
