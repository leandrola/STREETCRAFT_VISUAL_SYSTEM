"""Run RR2 against a separately installed Archive and explicit evidence catalog."""
import argparse,json,hashlib
from pathlib import Path
from archive_v1_adapter import make_archive_v1_retriever
from reference_reasoning_v2 import resolve_reference_v2

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive-root',required=True,type=Path)
    p.add_argument('--evidence',required=True,type=Path,help='JSON array of classified Evidence Units; no generated fallback')
    p.add_argument('--request',required=True,type=Path,help='JSON object: needs, profile, mode, camera and optional RR2 controls')
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    if a.output.resolve() in {a.evidence.resolve(),a.request.resolve()}:
        p.error('Output must not overwrite input')
    raw=a.evidence.read_bytes();items=json.loads(raw)
    if not isinstance(items,list) or any(not isinstance(x,dict) for x in items):
        p.error('Evidence must be an array of objects')
    req=json.loads(a.request.read_bytes())
    allowed={'needs','profile','mode','camera','query_budget','allow_support','semantic_text_lock','occlusion_locked','fear_city_confirmed'}
    if not isinstance(req,dict) or set(req)-allowed:
        p.error('Unknown request fields')
    result=resolve_reference_v2(**req,archive_retriever=make_archive_v1_retriever(a.archive_root,items))
    result['input_provenance']={'evidence_sha256':hashlib.sha256(raw).hexdigest(),'request_sha256':hashlib.sha256(a.request.read_bytes()).hexdigest(),'evidence_count':len(items),'archive_modules':{str(q.relative_to(a.archive_root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted((a.archive_root/'runtime').rglob('*.py'))}}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'queries':result['queries'],'evidence_count':len(items)}))
    return 0 if result['status']=='READY' else 2

if __name__=='__main__':raise SystemExit(main())
