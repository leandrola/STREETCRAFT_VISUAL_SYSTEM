#!/usr/bin/env python3
"""Run unified Streetcraft orchestration with the real Archive adapter."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'integration'))
sys.path.insert(0,str(ROOT/'reference_runtime'))
from streetcraft_orchestrator import orchestrate
from archive_v1_adapter import make_archive_v1_retriever

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive-root',required=True,type=Path)
    ap.add_argument('--evidence',required=True,type=Path)
    ap.add_argument('--request',required=True,type=Path)
    ap.add_argument('--output',required=True,type=Path)
    a=ap.parse_args()
    evidence=json.loads(a.evidence.read_text())
    request=json.loads(a.request.read_text())
    result=orchestrate(request,archive_retriever=make_archive_v1_retriever(a.archive_root,evidence))
    result['input_provenance']={
        'evidence_sha256':sha(a.evidence),'request_sha256':sha(a.request),
        'evidence_count':len(evidence),
        'archive_modules':{str(p.relative_to(a.archive_root)):sha(p) for p in sorted((a.archive_root/'runtime').rglob('*.py'))}
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'generation_ready':result['generation_ready'],
                      'queries':result['reference_reasoning']['queries']}))
    return 0 if result['status'] in {'GENERATION_READY','BLOCKED_REFERENCE','BLOCKED_PREFLIGHT','REVIEW_REQUIRED'} else 2
if __name__=='__main__': raise SystemExit(main())
