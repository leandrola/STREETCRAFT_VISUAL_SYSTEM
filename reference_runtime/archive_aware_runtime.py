#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
import hashlib

ARCHIVE_DOMAINS={
"ARCHITECTURE","STOREFRONT","SIGNAGE","MATERIALS","WEATHERING",
"STREET_FURNITURE","TRANSIT_INFRASTRUCTURE","INDUSTRIAL","URBAN_RESIDUE",
"PEOPLE_ACTIVITY","VEHICLES","CAMERA","LIGHT_ATMOSPHERE","RAIN_SNOW_ASPHALT",
"TEMPORAL_LAYERING","REGIONAL_CHARACTER"
}
RISK_ORDER={"LOW":0,"MEDIUM":1,"HIGH":2}

def make_need_id(seed:str)->str:
    return "RN-"+hashlib.sha256(seed.encode()).hexdigest()[:12].upper()

def classify_reference_need(*, specific_problem:str, target_domains:list[str],
                            source_sufficient:bool, transformation_requires_detail:bool,
                            hard_locked_unknown:bool=False, task_context:str="",
                            source_context:str="", min_provenance:str="P1",
                            max_transfer_risk:str="MEDIUM", max_results:int=3,
                            source_invariants:list[str]|None=None,
                            forbidden_transfers:list[str]|None=None,
                            region:str|None=None, period:str|None=None)->dict:
    bad=set(target_domains)-ARCHIVE_DOMAINS
    if bad:
        raise ValueError(f"unknown Archive domain(s): {sorted(bad)}")
    if hard_locked_unknown:
        state="RN_BLOCKED"
        blocked_reason="Hard-locked unknown cannot be legitimately filled by generic Archive evidence."
    elif source_sufficient:
        state="RN_NONE"
        blocked_reason=None
    elif transformation_requires_detail:
        state="RN_REQUIRED"
        blocked_reason=None
    else:
        state="RN_SUPPORT"
        blocked_reason=None
    seed="|".join([specific_problem,",".join(sorted(target_domains)),task_context,source_context])
    return {
        "need_id":make_need_id(seed),
        "state":state,
        "target_domains":target_domains,
        "specific_problem":specific_problem,
        "task_context":task_context,
        "source_context":source_context,
        "min_provenance":min_provenance,
        "max_transfer_risk":max_transfer_risk,
        "max_results":max(1,min(max_results,5)),
        "source_invariants":source_invariants or [],
        "forbidden_transfers":forbidden_transfers or [],
        "region":region,
        "period":period,
        "blocked_reason":blocked_reason
    }

def archive_request_from_need(need:dict, *, profile:str, mode:str)->dict|None:
    if need["state"] in {"RN_NONE","RN_BLOCKED"}:
        return None
    return {
        "need_id":need["need_id"],
        "profile":profile,
        "mode":mode,
        "target_domains":need["target_domains"],
        "task_context":need["task_context"],
        "source_context":need.get("source_context",""),
        "min_provenance":need.get("min_provenance","P1"),
        "max_transfer_risk":need.get("max_transfer_risk","MEDIUM"),
        "max_results":need.get("max_results",3),
        "source_invariants":need.get("source_invariants",[]),
        "forbidden_transfers":need.get("forbidden_transfers",[]),
        "region":need.get("region"),
        "period":need.get("period")
    }

def _has_tag(item:dict, tag:str)->bool:
    vals=set(item.get("anti_tags",[]))|set(item.get("retrieval_tags",[]))|set(item.get("forbidden_transfer",[]))
    return tag in vals

def admit_candidate(item:dict, need:dict, *, camera:str,
                    semantic_text_lock:str="STRICT",
                    occlusion_locked:bool=False,
                    fear_city_confirmed:bool=False)->dict:
    reasons=[]
    domain=item.get("domain","")
    decision="ADMITTED_SCOPED"

    if item.get("status") in {"UNUSABLE","REJECTED"}:
        decision="REJECTED"; reasons.append("candidate_status_block")
    elif domain not in set(need.get("target_domains",[])):
        decision="REJECTED"; reasons.append("domain_mismatch")
    elif RISK_ORDER.get(item.get("transfer_risk","HIGH"),2) > RISK_ORDER.get(need.get("max_transfer_risk","MEDIUM"),1):
        decision="REJECTED"; reasons.append("transfer_risk_above_ceiling")
    elif set(need.get("forbidden_transfers",[])).intersection(set(item.get("retrieval_tags",[]))):
        decision="REJECTED"; reasons.append("forbidden_transfer_tag")
    elif semantic_text_lock=="STRICT" and domain=="SIGNAGE" and (
        item.get("semantic_specificity",0)>0.5 or _has_tag(item,"TEXT_INVENTION")
    ):
        # Sign form/material can still be useful, but not exact invented wording.
        if item.get("permitted_learning"):
            decision="ADMITTED_NEGATIVE_ONLY" if _has_tag(item,"TEXT_INVENTION") else "REVIEW_REQUIRED"
            reasons.append("semantic_text_lock_limits_transfer")
        else:
            decision="REJECTED"; reasons.append("semantic_text_lock")
    elif occlusion_locked and item.get("fills_hidden_geometry",False):
        decision="REJECTED"; reasons.append("occlusion_lock")
    elif camera in {"CG-S","CG-FC"} and domain=="CAMERA":
        decision="ADMITTED_NEGATIVE_ONLY"; reasons.append("camera_authority_locked")
    elif fear_city_confirmed and (
        domain=="REGIONAL_CHARACTER" or _has_tag(item,"REGIONAL_LEAK")
    ):
        decision="ADMITTED_NEGATIVE_ONLY"; reasons.append("fear_city_geographic_identity_lock")
    elif item.get("bundle_conflict",False):
        decision="REVIEW_REQUIRED"; reasons.append("evidence_conflict")
    else:
        reasons.append("eligible_scoped_evidence")

    if _has_tag(item,"CANON_BY_SIMILARITY"):
        decision="ADMITTED_NEGATIVE_ONLY"
        reasons.append("canon_by_similarity_forbidden")

    return {
        "evidence_unit_id":item.get("evidence_unit_id",""),
        "archive_id":item.get("archive_id"),
        "decision":decision,
        "domain":domain,
        "reasons":reasons,
        "permitted_learning":item.get("permitted_learning",[]),
        "forbidden_transfer":item.get("forbidden_transfer",[]),
        "visible_fact":item.get("visible_fact"),
        "provenance_level":item.get("provenance_level"),
        "authority_score":item.get("authority_score",0.0),
        "retrieval_score":item.get("retrieval_score",0.0),
        "transfer_risk":item.get("transfer_risk","HIGH"),
    }

def resolve_runtime(*, needs:list[dict], profile:str, mode:str, camera:str,
                    archive_retriever:Callable[[dict],dict]|None,
                    semantic_text_lock:str="STRICT",
                    occlusion_locked:bool=False,
                    fear_city_confirmed:bool=False)->dict:
    admissions=[]
    bundle_ids=[]
    negative=[]
    unresolved=[]
    any_query=False
    archive_unavailable=False

    for need in needs:
        state=need["state"]
        if state=="RN_NONE":
            continue
        if state=="RN_BLOCKED":
            unresolved.append(need["need_id"])
            continue
        req=archive_request_from_need(need,profile=profile,mode=mode)
        if req is None:
            continue
        any_query=True
        if archive_retriever is None:
            archive_unavailable=True
            unresolved.append(need["need_id"])
            continue
        try:
            bundle=archive_retriever(req)
        except Exception:
            archive_unavailable=True
            unresolved.append(need["need_id"])
            continue

        if bundle.get("evidence_bundle_id"):
            bundle_ids.append(bundle["evidence_bundle_id"])
        negative.extend(bundle.get("negative_evidence",[]))

        items=bundle.get("items",[])
        if not items:
            unresolved.append(need["need_id"])
            continue

        # annotate bundle-level conflicts so admission knows review is required
        conflict_ids=set()
        for c in bundle.get("conflicts",[]):
            if c.get("leading_evidence_unit_id"):
                conflict_ids.add(c["leading_evidence_unit_id"])
            conflict_ids.update(c.get("dissenting_evidence_unit_ids",[]))

        local_admitted=0
        for item in items[:need.get("max_results",3)]:
            x=dict(item)
            if x.get("evidence_unit_id") in conflict_ids:
                x["bundle_conflict"]=True
            rec=admit_candidate(
                x,need,camera=camera,
                semantic_text_lock=semantic_text_lock,
                occlusion_locked=occlusion_locked,
                fear_city_confirmed=fear_city_confirmed
            )
            admissions.append(rec)
            if rec["decision"]=="ADMITTED_SCOPED":
                local_admitted += 1
        if local_admitted==0 and need["state"]=="RN_REQUIRED":
            unresolved.append(need["need_id"])

    if archive_unavailable and unresolved:
        status="ARCHIVE_UNAVAILABLE"
    elif any(n["state"]=="RN_BLOCKED" for n in needs):
        status="BLOCKED" if not admissions else "PARTIAL"
    elif unresolved:
        status="REFERENCE_UNRESOLVED" if not admissions else "PARTIAL"
    elif any(a["decision"]=="REVIEW_REQUIRED" for a in admissions):
        status="REVIEW"
    elif admissions:
        status="READY"
    elif not any_query:
        status="NOT_NEEDED"
    else:
        status="REFERENCE_UNRESOLVED"

    return {
        "runtime_status":status,
        "needs":needs,
        "admissions":admissions,
        "evidence_bundle_ids":bundle_ids,
        "negative_evidence":negative,
        "unresolved_needs":sorted(set(unresolved)),
        "authority_map":"RAM-1.0"
    }

def enrich_cgc(cgc:dict, runtime_record:dict)->dict:
    out=dict(cgc)
    out["reference_runtime"]=runtime_record
    # Project only scoped, auditable evidence into generation.
    projected=[]
    for a in runtime_record.get("admissions",[]):
        if a["decision"]=="ADMITTED_SCOPED":
            projected.append({
                "evidence_unit_id":a["evidence_unit_id"],
                "domain":a["domain"],
                "visible_fact":a.get("visible_fact"),
                "permitted_learning":a.get("permitted_learning",[]),
                "forbidden_transfer":a.get("forbidden_transfer",[])
            })
    out["reference_runtime"]["generation_projection"]=projected
    return out
