from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

GEO_TERMS={
    "new york","nyc","manhattan","brooklyn","bronx","queens","staten island",
    "chicago","boston","philadelphia","los angeles","san francisco","detroit"
}

def _norm(x:str)->str:
    return " ".join((x or "").strip().lower().split())

def classify_text_token(literal:str|None, confidence:float|None, preservation_level:str="P2", identity_bearing:bool=False, numeral:bool=False)->dict:
    c=0.0 if confidence is None else float(confidence)
    lit=(literal or "").strip()
    exact_authority=preservation_level in {"P0","P1"} or identity_bearing or numeral
    if lit and c>=0.85 and exact_authority:
        state="FROZEN_EXACT"
    elif c>=0.50:
        state="MASK_PARTIAL"
    else:
        state="MASK_GRAPHIC_ONLY"
    return {"literal":lit,"confidence":c,"state":state,"preservation_level":preservation_level,"identity_bearing":identity_bearing,"numeral":numeral}

def validate_candidate_text(token:dict, candidate_semantics:str|None)->dict:
    cand=(candidate_semantics or "").strip()
    state=token["state"]
    if state=="FROZEN_EXACT":
        if cand!=token["literal"]:
            return {"status":"FAIL","severity":"S3","code":"TEXT_MUTATION","expected":token["literal"],"actual":cand}
        return {"status":"PASS","severity":"S0","code":"EXACT_TOKEN_PRESERVED"}
    if state=="MASK_GRAPHIC_ONLY":
        if cand:
            return {"status":"FAIL","severity":"S3","code":"TEXT_INVENTION","expected":"NON_SEMANTIC_GRAPHIC_ONLY","actual":cand}
        return {"status":"PASS","severity":"S0","code":"AMBIGUITY_PRESERVED"}
    # partial tokens may carry only known fragments; safest runtime contract is no completed semantic string
    if cand and token.get("literal") and cand!=token["literal"]:
        return {"status":"REVIEW","severity":"S2","code":"PARTIAL_TEXT_COMPLETION_RISK","expected":token["literal"],"actual":cand}
    return {"status":"PASS","severity":"S0","code":"PARTIAL_TEXT_CONSTRAINED"}

def low_confidence_render_hint(token:dict)->dict:
    state=token["state"]
    if state=="FROZEN_EXACT":
        return {"semantic_mode":"EXACT","literal":token["literal"]}
    if state=="MASK_PARTIAL":
        return {"semantic_mode":"PARTIAL_ONLY","known_fragment":token["literal"],"complete_words":False}
    return {"semantic_mode":"GRAPHIC_ONLY","literal":None,"readable_text":False}

def fear_city_geographic_gate(proposed_geo_tokens:Iterable[str], source_authored_geo_tokens:Iterable[str]=(), explicit_override:bool=False)->dict:
    authored={_norm(x) for x in source_authored_geo_tokens if x}
    blocked=[]; allowed=[]
    for raw in proposed_geo_tokens:
        n=_norm(raw)
        if n in authored:
            allowed.append(raw); continue
        is_real_geo = n in GEO_TERMS or any(term in n for term in GEO_TERMS)
        if is_real_geo:
            blocked.append(raw)
        else:
            # unknown external geography is still blocked in confirmed Fear City unless authored
            blocked.append(raw)
    if blocked and not explicit_override:
        return {"status":"FAIL","severity":"S3","code":"REGIONAL_LEAK","blocked":blocked,"allowed":allowed}
    if blocked and explicit_override:
        return {"status":"REVIEW_REQUIRED","severity":"S2","code":"GEOGRAPHY_OVERRIDE_REQUIRES_REVIEW","blocked":blocked,"allowed":allowed}
    return {"status":"PASS","severity":"S0","code":"GEOGRAPHIC_NULL_LOCK_OK","blocked":[],"allowed":allowed}

def reference_bleed_preflight(features:list[dict], *, allowed_domains:set[str], source_entity_ids:set[str]|None=None, camera_lock:str|None=None, fear_city_confirmed:bool=False, source_authored_geo_tokens:set[str]|None=None, source_states:dict|None=None)->dict:
    source_entity_ids=source_entity_ids or set()
    source_authored_geo_tokens=source_authored_geo_tokens or set()
    source_states=source_states or {}
    admitted=[]; rejected=[]
    for f in features:
        reasons=[]
        dom=f.get("domain")
        typ=f.get("feature_type")
        if dom not in allowed_domains:
            reasons.append("DOMAIN_OUT_OF_SCOPE")
        if typ=="camera" and camera_lock in {"CG-S","CG-FC"}:
            reasons.append("CAMERA_LOCK")
        if typ=="text" and f.get("semantic_specificity",1)>0:
            reasons.append("REFERENCE_TEXT_SEMANTICS_FORBIDDEN")
        if typ=="geography" and fear_city_confirmed:
            val=_norm(str(f.get("value","")))
            if val not in {_norm(x) for x in source_authored_geo_tokens}:
                reasons.append("FEAR_CITY_GEOGRAPHIC_NULL_LOCK")
        if typ in {"geometry","prop"}:
            target=f.get("target_entity_id")
            if not target or target not in source_entity_ids:
                reasons.append("UNSCOPED_REFERENCE_OBJECT")
        if typ=="atmosphere":
            prop=f.get("property")
            val=f.get("value")
            if prop=="surface_wetness" and source_states.get("surface_wetness")=="DRY" and val=="WET":
                reasons.append("UNAUTHORIZED_WETNESS_IMPORT")
            if prop=="haze" and source_states.get("haze")=="ABSENT" and val not in {"ABSENT",None}:
                reasons.append("UNAUTHORIZED_HAZE_IMPORT")
        if reasons:
            x=dict(f); x["decision"]="REJECTED"; x["reasons"]=reasons; rejected.append(x)
        else:
            x=dict(f); x["decision"]="ADMITTED_SCOPED"; x["reasons"]=["SCOPED_TRANSFER_OK"]; admitted.append(x)
    critical=any(any(r in {"FEAR_CITY_GEOGRAPHIC_NULL_LOCK","REFERENCE_TEXT_SEMANTICS_FORBIDDEN","CAMERA_LOCK"} for r in x["reasons"]) for x in rejected)
    return {"status":"FAIL" if critical else ("REVIEW" if rejected else "PASS"),"admitted":admitted,"rejected":rejected}

def patch_pre_generation_gate(*, text_tokens:list[dict], proposed_text:dict[str,str|None], fear_city_confirmed:bool=False, proposed_geo_tokens:list[str]|None=None, source_authored_geo_tokens:list[str]|None=None, reference_features:list[dict]|None=None, allowed_domains:set[str]|None=None, source_entity_ids:set[str]|None=None, camera_lock:str|None=None, source_states:dict|None=None)->dict:
    findings=[]
    for t in text_tokens:
        key=t.get("token_id") or t.get("literal")
        res=validate_candidate_text(t, proposed_text.get(key))
        if res["status"]!="PASS": findings.append(res)
    if fear_city_confirmed:
        g=fear_city_geographic_gate(proposed_geo_tokens or [], source_authored_geo_tokens or [])
        if g["status"]!="PASS": findings.append(g)
    rb=reference_bleed_preflight(reference_features or [],allowed_domains=allowed_domains or set(),source_entity_ids=source_entity_ids,camera_lock=camera_lock,fear_city_confirmed=fear_city_confirmed,source_authored_geo_tokens=set(source_authored_geo_tokens or []),source_states=source_states)
    if rb["status"]!="PASS":
        findings.append({"status":rb["status"],"severity":"S3" if rb["status"]=="FAIL" else "S2","code":"REFERENCE_BLEED_PREFLIGHT","detail":rb["rejected"]})
    s3=any(x.get("severity")=="S3" for x in findings)
    return {"status":"BLOCK_GENERATION" if s3 else ("REVIEW_REQUIRED" if findings else "PASS"),"findings":findings,"reference_preflight":rb}
