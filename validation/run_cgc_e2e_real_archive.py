#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
import jsonschema
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'integration'))
sys.path.insert(0,str(ROOT/'reference_runtime'))
from streetcraft_orchestrator import orchestrate
from archive_v1_adapter import make_archive_v1_retriever

def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--archive-root',required=True,type=Path)
 a=ap.parse_args(); archive=a.archive_root.resolve()
 identity=json.loads((ROOT/'validation/rr2_real_archive/ARCHIVE_RUNTIME_IDENTITY.json').read_text())
 identity_checks=[]
 for rec in identity['checks']:
  p=archive/rec['path']; actual=sha(p) if p.exists() else None
  identity_checks.append({'path':rec['path'],'expected_sha256':rec['expected_sha256'],'actual_sha256':actual,'match':actual==rec['expected_sha256']})
 if not all(x['match'] for x in identity_checks):
  raise SystemExit('Archive runtime identity mismatch')
 evidence_path=ROOT/'reference_runtime/real_catalog/REAL_EVIDENCE_CATALOG_V1.json'
 evidence=json.loads(evidence_path.read_text()); retriever=make_archive_v1_retriever(archive,evidence)
 schema=json.loads((ROOT/'schemas/compact-generation-contract.schema.json').read_text())
 req_dir=ROOT/'validation/cgc_e2e/requests'; out_dir=ROOT/'validation/cgc_e2e/results'; out_dir.mkdir(parents=True,exist_ok=True)
 cases=[]
 for rp in sorted(req_dir.glob('CGC-E2E-*.json')):
  raw=json.loads(rp.read_text()); expected=raw.pop('_validation_expected')
  result=orchestrate(raw,archive_retriever=retriever)
  if 'cgc_final' in result:
   jsonschema.validate(result['cgc_final'],schema)
  result['input_provenance']={
   'evidence_sha256':sha(evidence_path),'request_sha256':sha(rp),'evidence_count':len(evidence),
   'archive_modules':{str(p.relative_to(archive)):sha(p) for p in sorted((archive/'runtime').rglob('*.py'))}
  }
  cid=rp.stem; checks=[result['status']==expected]
  if cid=='CGC-E2E-01':
   checks += [result['reference_reasoning']['queries']==1,
              result['cgc_final']['reference_reasoning']['generation_projection'][0]['domain']=='MATERIALS']
  elif cid=='CGC-E2E-02':
   checks += [result['reference_reasoning']['queries']==0,'SAR2-E-HIDDEN' in result['reference_reasoning']['locked_unknowns'],
              result['resolved_config']['camera']=='CG-F','camera_non_frontal' in result['cgc_final']['forbid']]
  elif cid=='CGC-E2E-03': checks += [result['reference_reasoning']['status']=='BLOCKED_REQUIRED']
  elif cid=='CGC-E2E-04': checks += [result['reference_reasoning']['status']=='BLOCKED_REQUIRED']
  elif cid=='CGC-E2E-05':
   rejects=result['reference_reasoning']['trace'][0].get('screen_rejections',[])
   checks += [any(x.get('reason')=='DUPLICATE_CONTENT_FINGERPRINT' for x in rejects)]
  elif cid=='CGC-E2E-06':
   checks += [any(a.get('decision')=='REVIEW_REQUIRED' for a in result['reference_reasoning']['admissions'])]
  elif cid=='CGC-E2E-07':
   checks += [result['reference_reasoning']['queries']==1,result['reference_reasoning']['need_results'].get('N-REQ')=='SATISFIED_EVIDENCE',
              result['reference_reasoning']['need_results'].get('N-SUP')=='UNRESOLVED']
  elif cid=='CGC-E2E-08':
   checks += [any(f.get('code')=='TEXT_MUTATION' for f in result['pre_generation_gate']['findings'])]
  ok=all(checks)
  (out_dir/f'{cid}.json').write_text(json.dumps(result,indent=2)+'\n')
  cases.append({'case_id':cid,'expected':expected,'actual':result['status'],'status':'PASS' if ok else 'FAIL',
                'queries':result['reference_reasoning']['queries'],'bundle_ids':[bid for t in result['reference_reasoning']['trace'] for bid in t.get('evidence_bundle_ids',[])],
                'request_sha256':result['input_provenance']['request_sha256']})
 summary={'suite':'CGC_END_TO_END_REAL_ARCHIVE_V1','status':'PASS' if all(c['status']=='PASS' for c in cases) else 'FAIL',
          'case_count':len(cases),'passed':sum(c['status']=='PASS' for c in cases),'archive_runtime_identity':'PASS',
          'archive_verified_modules':len(identity_checks),'evidence_sha256':sha(evidence_path),'cases':cases}
 (ROOT/'validation/CGC_END_TO_END_REAL_ARCHIVE_V1.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
 return 0 if summary['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
