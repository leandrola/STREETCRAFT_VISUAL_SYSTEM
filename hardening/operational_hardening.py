from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

TEXT_STATES={"LEGIBLE_EXACT","PARTIAL","ILLEGIBLE","OCCLUDED","ABSENT"}

def text_policy(state:str)->dict:
    if state not in TEXT_STATES:
        raise ValueError("unknown text state")
    return {
        "LEGIBLE_EXACT":{"copy_semantics":True,"invent_semantics":False,"preserve_uncertainty":False},
        "PARTIAL":{"copy_semantics":"KNOWN_ONLY","invent_semantics":False,"preserve_uncertainty":True},
        "ILLEGIBLE":{"copy_semantics":False,"invent_semantics":False,"preserve_uncertainty":True},
        "OCCLUDED":{"copy_semantics":False,"invent_semantics":False,"preserve_uncertainty":True},
        "ABSENT":{"copy_semantics":False,"invent_semantics":False,"preserve_uncertainty":False},
    }[state]

def material_delta_allowed(mode:str, requested:int, evidence_support:bool=False)->bool:
    if mode in {"T01","T03"}:
        return requested == 0
    if mode == "T06":
        return requested in (0,1) and (requested == 0 or evidence_support)
    return requested == 0

def occlusion_policy(authoritative_views:int=1, explicit_reconstruction:bool=False)->str:
    if explicit_reconstruction:
        return "EXPLICIT_RECONSTRUCTION"
    if authoritative_views >= 2:
        return "MULTIVIEW_CONSTRAINED"
    return "LOCKED_UNKNOWN"

def build_contract(source_identity:str, mode:str, profile:str, camera:str, *,
                   preserve:Iterable[str]=(), transform:Iterable[str]=(),
                   remove:Iterable[str]=(), infer:Iterable[str]=(),
                   unknown:Iterable[str]=(), forbid:Iterable[str]=(),
                   semantic_text_lock:str="STRICT", material_intensity_delta:int=0,
                   occlusion_locks:Iterable[str]=()):
    if semantic_text_lock not in {"STRICT","NORMAL","EXPLICIT_OVERRIDE"}:
        raise ValueError("invalid semantic text lock")
    if not -1 <= material_intensity_delta <= 3:
        raise ValueError("invalid material intensity delta")
    return {
        "source_identity":source_identity,
        "mode":mode,
        "profile":profile,
        "camera":camera,
        "preserve":list(preserve),
        "transform":list(transform),
        "remove":list(remove),
        "infer":list(infer),
        "unknown":list(unknown),
        "forbid":list(forbid),
        "semantic_text_lock":semantic_text_lock,
        "material_intensity_delta":material_intensity_delta,
        "occlusion_locks":list(occlusion_locks),
    }

def micro_drift_verdict(findings:list[dict])->dict:
    severity_rank={"S0":0,"S1":1,"S2":2,"S3":3}
    counts={k:0 for k in severity_rank}
    for f in findings:
        s=f.get("severity","S0")
        if s not in severity_rank:
            raise ValueError("invalid severity")
        counts[s]+=1
    if counts["S3"]>0:
        status="FAIL"
    elif counts["S2"]>=2:
        status="REVISION_REQUIRED"
    elif counts["S2"]==1:
        status="REVIEW"
    else:
        status="PASS"
    return {"status":status,"counts":counts}
