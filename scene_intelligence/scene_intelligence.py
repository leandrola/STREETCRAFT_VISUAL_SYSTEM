#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter,defaultdict
from typing import Iterable

VALID_ROLES={
"STRUCTURAL_CORE","IDENTITY_ANCHOR","RELATIONSHIP_ANCHOR","CONTEXTUAL_SUPPORT",
"TEMPORAL_EVIDENCE","TRANSIENT_OBJECT","OCCLUDER","REMOVAL_CANDIDATE","UNKNOWN_REGION"
}
ACTIONS={
"PRESERVE_EXACT","PRESERVE_RELATIONSHIP","PRESERVE_CHARACTER","PRESERVE_CONTEXT",
"TRANSFORM_SCOPED","REMOVE_AUTHORIZED","INFER_MINIMAL","UNKNOWN_LOCKED","FORBID_CHANGE"
}
REL_PROTECTION_RANK={"PRX":0,"PR2":1,"PR1":2,"PR0":3}

def salience_score(entity:dict)->dict:
    s=entity.get("salience",{})
    axes={
      "identity_salience":float(s.get("identity_salience",0)),
      "structural_dependency":float(s.get("structural_dependency",0)),
      "task_relevance":float(s.get("task_relevance",0)),
      "relationship_centrality":float(s.get("relationship_centrality",0)),
      "temporal_relevance":float(s.get("temporal_relevance",0)),
    }
    for k,v in axes.items():
        if not 0 <= v <= 1:
            raise ValueError(f"{k} outside 0..1")
    score=(.30*axes["identity_salience"]+.25*axes["structural_dependency"]+
           .20*axes["task_relevance"]+.15*axes["relationship_centrality"]+
           .10*axes["temporal_relevance"])
    band=("CRITICAL_ATTENTION" if score>=.75 else
          "MAJOR_ATTENTION" if score>=.50 else
          "SUPPORT_ATTENTION" if score>=.25 else
          "MINOR_ATTENTION")
    return {"score":round(score,4),"band":band,"axes":axes}

def relationship_locks(entity_id:str, relationships:list[dict])->dict:
    relevant=[r for r in relationships if entity_id in {r["subject"],r["object"]}]
    if not relevant:
        return {"max_protection":"PRX","relationships":[]}
    maxp=max(relevant,key=lambda r:REL_PROTECTION_RANK[r.get("protection","PRX")])["protection"]
    return {"max_protection":maxp,"relationships":[r["relationship_id"] for r in relevant if r.get("protection") in {"PR0","PR1"}]}

def resolve_entity_action(entity:dict, relationships:list[dict], mode:str)->dict:
    pl=entity["preservation_level"]
    roles=set(entity.get("roles",[]))
    observed=entity.get("observed",entity.get("epistemic_class")=="OBSERVED")
    removal_authorized=bool(entity.get("removal_authorized",False))
    multiview=bool(entity.get("multi_view_support",False))
    authored=bool(entity.get("authored_world",False))
    locks=relationship_locks(entity["entity_id"],relationships)
    relation_locked=locks["max_protection"] in {"PR0","PR1"}

    if pl=="P0": action="PRESERVE_EXACT"
    elif pl=="P1": action="PRESERVE_CHARACTER"
    elif pl=="P2": action="PRESERVE_CONTEXT"
    elif pl=="P3": action="TRANSFORM_SCOPED"
    elif pl=="P4": action="REMOVE_AUTHORIZED" if removal_authorized else "PRESERVE_CONTEXT"
    elif pl in {"P5-A","P5-B"}: action="INFER_MINIMAL" if multiview or entity.get("continuity_support",False) else "UNKNOWN_LOCKED"
    elif pl=="P5-C": action="INFER_MINIMAL" if multiview else "UNKNOWN_LOCKED"
    elif pl=="P5-D": action="UNKNOWN_LOCKED"
    else: raise ValueError(f"unknown preservation level {pl}")

    if mode=="T01" and observed and ("TRANSIENT_OBJECT" in roles or "OCCLUDER" in roles):
        if pl not in {"P0","P1"}: action="PRESERVE_CONTEXT"
    if mode=="T03" and ("REMOVAL_CANDIDATE" in roles or "TRANSIENT_OBJECT" in roles):
        if removal_authorized and pl=="P4": action="REMOVE_AUTHORIZED"
    if mode=="T06" and authored and ("STRUCTURAL_CORE" in roles or pl=="P0"):
        action="PRESERVE_EXACT"
    if relation_locked and action in {"REMOVE_AUTHORIZED","TRANSFORM_SCOPED"}:
        action="PRESERVE_RELATIONSHIP"
    if "UNKNOWN_REGION" in roles or entity.get("epistemic_class")=="UNKNOWN":
        if pl.startswith("P5"): action="UNKNOWN_LOCKED"
    return {"entity_id":entity["entity_id"],"action":action,"relationship_lock":relation_locked,
            "protected_relationships":locks["relationships"],"salience":salience_score(entity)}

def validate_relationships(entities:list[dict], relationships:list[dict])->list[str]:
    ids={e["entity_id"] for e in entities}; warnings=[]
    for r in relationships:
        if r["subject"] not in ids or r["object"] not in ids: warnings.append(f"DANGLING_RELATIONSHIP:{r['relationship_id']}")
        if r.get("protection")=="PR0" and r.get("epistemic_class")=="UNKNOWN": warnings.append(f"PR0_UNKNOWN_EVIDENCE:{r['relationship_id']}")
    return warnings

def derive_reference_need_hints(entities:list[dict], actions:list[dict], mode:str)->list[dict]:
    by_id={e["entity_id"]:e for e in entities}; hints=[]
    for a in actions:
        e=by_id[a["entity_id"]]; action=a["action"]
        if action=="UNKNOWN_LOCKED":
            hints.append({"entity_id":e["entity_id"],"state":"RN_BLOCKED","reason":"Scene evidence is locked unknown; generic references cannot create exact content."})
        elif action=="TRANSFORM_SCOPED" and e.get("reference_domain"):
            hints.append({"entity_id":e["entity_id"],"state":"RN_REQUIRED" if e.get("reference_required",False) else "RN_SUPPORT","target_domains":[e["reference_domain"]],"reason":"Scoped transformation may require documentary implementation evidence."})
        elif action=="INFER_MINIMAL" and not e.get("multi_view_support",False):
            hints.append({"entity_id":e["entity_id"],"state":"RN_SUPPORT","reason":"Minimum reconstruction may benefit from scoped evidence, but source continuity remains primary."})
    return hints

def build_scene_analysis_record(*, scene_id:str, source_identity:str, mode:str, profile:str, entities:list[dict], relationships:list[dict])->dict:
    warnings=validate_relationships(entities,relationships)
    actions=[resolve_entity_action(e,relationships,mode) for e in entities]
    identity_anchors=[e["entity_id"] for e in entities if "IDENTITY_ANCHOR" in set(e.get("roles",[]))]
    unknown_locks=[a["entity_id"] for a in actions if a["action"]=="UNKNOWN_LOCKED"]
    hints=derive_reference_need_hints(entities,actions,mode)
    return {"scene_id":scene_id,"source_identity":source_identity,"mode":mode,"profile":profile,"entities":entities,"relationships":relationships,"action_plan":actions,"identity_anchors":identity_anchors,"unknown_locks":unknown_locks,"reference_need_hints":hints,"warnings":warnings}

def project_scene_to_cgc(cgc:dict, sar2:dict)->dict:
    out=dict(cgc); entities={e["entity_id"]:e for e in sar2["entities"]}
    preserve=[]; remove=[]; infer=[]; unknown=[]; forbid=[]
    for a in sar2["action_plan"]:
        eid=a["entity_id"]; label=entities[eid].get("label",eid); act=a["action"]
        if act in {"PRESERVE_EXACT","PRESERVE_CHARACTER","PRESERVE_CONTEXT","PRESERVE_RELATIONSHIP"}: preserve.append(f"{eid}:{label}:{act}")
        elif act=="REMOVE_AUTHORIZED": remove.append(f"{eid}:{label}")
        elif act=="INFER_MINIMAL": infer.append(f"{eid}:{label}:MINIMAL")
        elif act=="UNKNOWN_LOCKED": unknown.append(f"{eid}:{label}"); forbid.append(f"resolve_exact_unknown:{eid}")
        elif act=="FORBID_CHANGE": forbid.append(f"change:{eid}")
        if a.get("relationship_lock"): forbid.append(f"break_protected_relationships:{eid}")
    out["preserve"]=list(dict.fromkeys(out.get("preserve",[])+preserve)); out["remove"]=list(dict.fromkeys(out.get("remove",[])+remove)); out["infer"]=list(dict.fromkeys(out.get("infer",[])+infer)); out["unknown"]=list(dict.fromkeys(out.get("unknown",[])+unknown)); out["forbid"]=list(dict.fromkeys(out.get("forbid",[])+forbid))
    out["scene_intelligence"]={"scene_id":sar2["scene_id"],"identity_anchors":sar2["identity_anchors"],"protected_relationships":[r for r in sar2["relationships"] if r.get("protection") in {"PR0","PR1"}],"entity_actions":sar2["action_plan"],"unknown_locks":sar2["unknown_locks"],"reference_need_hints":sar2["reference_need_hints"]}
    return out
