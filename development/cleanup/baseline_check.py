#!/usr/bin/env python3
"""Run selected existing checks in a temporary copy; preserve repository bytes."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'development/cleanup'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def save(name,obj):
    path=OUT/name
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    return digest(path.read_bytes())

def main():
    # Only tracked files are copied; no Git metadata, browser data, environment,
    # existing outputs or cleanup report is copied into the test sandbox.
    paths=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().strip('\0').split('\0')
    temp=Path(tempfile.mkdtemp(prefix='streetcraft-inventory-baseline-'))
    checkout=temp/'repo'; checkout.mkdir()
    for rel in paths:
        source=ROOT/rel
        target=checkout/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target,follow_symlinks=False)
    tmp=temp/'tmp'; tmp.mkdir()
    # Extra Python write guard catches an accidental write back to the live repo.
    support=temp/'support'; support.mkdir()
    (support/'sitecustomize.py').write_text('''import os, sys
from pathlib import Path
allowed=Path(os.environ["SC_INVENTORY_TEST_ROOT"]).resolve()
def guard(event,args):
    if event=="open" and isinstance(args[0],(str,bytes,os.PathLike)):
        mode,flags=args[1:3]
        writing=(isinstance(mode,str) and any(c in mode for c in "wax+")) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing:
            path=Path(os.fsdecode(args[0])).resolve()
            if path!=allowed and allowed not in path.parents and str(path)!="/dev/null":
                raise PermissionError("Inventory test write outside disposable copy: "+str(path))
sys.addaudithook(guard)
''')
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(support)+os.pathsep+str(checkout),'SC_INVENTORY_TEST_ROOT':str(temp),'TMPDIR':str(tmp)}
    checks=[]
    def run(label,argv,cwd=checkout):
        start=time.monotonic()
        try:
            result=subprocess.run([sys.executable,*argv],cwd=cwd,env=env,capture_output=True,text=True,timeout=90)
            rec={'name':label,'argv':[sys.executable,*argv],'cwd':str(cwd),'exit_code':result.returncode,'status':'PASS' if result.returncode==0 else 'FAIL','stdout':result.stdout,'stderr':result.stderr,'elapsed_seconds':round(time.monotonic()-start,4)}
        except subprocess.TimeoutExpired as exc:
            rec={'name':label,'status':'BLOCKED_TIMEOUT','error':str(exc)}
        checks.append(rec)
        print(label,rec['status'],flush=True)
        return rec
    for rel in [
        'command_invocation/test_commands.py',
        'command_invocation/test_backdrop_presets.py',
        'hardening/test_operational_hardening.py',
        'reference_runtime/test_archive_aware_runtime.py',
        'reference_runtime/test_reference_reasoning.py',
        'scene_intelligence/test_scene_intelligence.py',
        'integration/test_streetcraft_orchestrator.py',
        'validation/test_patch_1_9_1.py',
        'validation/test_single_client_1_10_0.py',
        'benchmark/check_r2_baseline.py',
        'validation/camera_routing/validate_matrix.py',
        'validation/camera_routing/validate_l3.py',
    ]:
        rec=run(rel,[str(checkout/rel)])
        if rec['status']!='PASS':
            break
    if all(c['status']=='PASS' for c in checks):
        run('SC03 supervisor unit tests',['-m','unittest','discover','-s','tests','-p','test_sc_supervisor.py','-v'])

    # Dry execution through the same orchestration function, no image vendor,
    # no VSG mode, no Archive substitute. Missing references remain blocked.
    dry_code='''import copy, hashlib, json, sys
from pathlib import Path
root=Path.cwd()
sys.path.insert(0,str(root/'integration'))
from streetcraft_orchestrator import orchestrate
requests=[]
for p in sorted((root/'validation/cgc_e2e/requests').glob('*.json')):
    request=json.loads(p.read_text())
    if request.get('vsg',{}).get('mode','OFF')!='OFF':
        continue
    requests.append((str(p.relative_to(root)),request))
entity={'entity_id':'E-BLDG','label':'storefront','kind':'ARCHITECTURE','roles':['STRUCTURAL_CORE','IDENTITY_ANCHOR'],'preservation_level':'P0','epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,'salience':{'identity_salience':1,'structural_dependency':1,'task_relevance':1,'relationship_centrality':0,'temporal_relevance':1}}
scene={'scene_id':'INVENTORY-BASELINE','source_identity':'INVENTORY-SYNTHETIC-NO-IMAGE','mode':'T01','profile':'VP02','entities':[entity],'relationships':[]}
for command in ['/sc-2a','/sc-rdr2-elevation','/sc-core /sc-lock /sc-preserve /sc-noinvent','/sc-fear','/sc-bd01','/sc-bd02','/sc-does-not-exist']:
    request={'command_text':command,'scene':copy.deepcopy(scene)}
    requests.append(('synthetic:'+command,request))
request={'command_text':'/sc-2a','scene':copy.deepcopy(scene),'text_tokens':[{'token_id':'T1','literal':'TERMINAL DINER','confidence':0.99,'preservation_level':'P0','identity_bearing':True}],'proposed_text':{'T1':'TERMINAL DINNER'}}
requests.append(('synthetic:semantic-mutation',request))
cases=[]
for name,request in requests:
    first=orchestrate(request,archive_retriever=None)
    second=orchestrate(request,archive_retriever=None)
    canonical=json.dumps(first,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    assert first==second, name
    cases.append({'name':name,'request':request,'result':first,'result_sha256':hashlib.sha256(canonical).hexdigest(),'repeat_identical':True})
data={'recipe':'SHA256 UTF-8 JSON sort_keys=True separators=(comma,colon) ensure_ascii=False; exact complete result, no normalization','archive_retriever':None,'image_generation':False,'cases':cases}
Path('dry_run.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\\n')
print(json.dumps({'cases':len(cases),'statuses':[c['result']['status'] for c in cases],'repeat_identical':True}))
'''
    if all(c['status']=='PASS' for c in checks):
        run('Deterministic orchestration dry run',['-c',dry_code])
        if (checkout/'dry_run.json').exists():
            shutil.copy2(checkout/'dry_run.json',OUT/'runtime_dry_run.json')
    versions={name:importlib.metadata.version(name) for name in ['Pillow','jsonschema']}
    report={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'python':sys.version,'interpreter':sys.executable,'dependencies':versions,'temporary_copy':str(checkout),'copied_tracked_files':len(paths),'checks':checks,'status':'PASS_LOCAL' if all(c['status']=='PASS' for c in checks) else 'BLOCKED_LOCAL_CHECK','excluded':['Unified regression runner: includes closed VSG/pilot suites and writes stored evidence; constituent stable checks selected instead','GLIGEN/scaffold tests','Standalone VSG/pilot suites','Live supervisor/model calls, SC06 implementer and reviewer, SC05 pilot','Image generation and visual re-evaluation'],'external_archive':'NOT_RUN: runtime not part of this repository; real Archive re-execution requires verified external module bytes','dry_run_sha256':digest((OUT/'runtime_dry_run.json').read_bytes()) if (OUT/'runtime_dry_run.json').exists() else None,'limits':['PASS_LOCAL does not close SC04/05/06 or prove visual equivalence','Existing orchestrator tests include non-governing observer regression; no structural GLIGEN call','Temporary test copy retained for reproducibility; original evidence untouched']}
    h=save('baseline_results.json',report)
    save('baseline_result_hash.json',{'file':'baseline_results.json','sha256':h})
    print(json.dumps({'status':report['status'],'baseline_sha256':h,'temporary_copy':str(checkout)}))

if __name__=='__main__':
    main()
