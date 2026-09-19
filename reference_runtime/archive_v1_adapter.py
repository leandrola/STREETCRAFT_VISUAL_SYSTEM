#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path

def make_archive_v1_retriever(archive_root:str|Path, evidence:list[dict]):
    root=Path(archive_root)
    if not root.exists():
        raise FileNotFoundError(root)
    sys.path.insert(0,str(root))
    from runtime.retrieval.query_planner import plan_and_rank
    from runtime.integration.evidence_bundle import assemble_bundle
    from runtime.integration.negative_evidence import detect_negative_evidence

    def retrieve(request:dict)->dict:
        ranked=plan_and_rank(request,evidence)
        bundle=assemble_bundle(request,ranked)
        neg=[]
        for item in ranked:
            neg.extend(detect_negative_evidence(item,request))
        bundle["negative_evidence"]=neg
        return bundle
    return retrieve
