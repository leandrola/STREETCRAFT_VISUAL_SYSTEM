#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

def choose_transform_camera(geometry):
    if geometry in {"corner","deep_oblique"}:
        return "CG-B"
    return "CG-A"

def compute(case):
    x=case["input"]
    source=x["source_identity"]
    mode=x.get("explicit_mode")
    profile=x.get("explicit_profile")
    transform=bool(x.get("camera_transform_authorized"))
    source_cam=x.get("source_camera_family","UNKNOWN")
    geometry=x.get("geometry","frontal")
    override=bool(x.get("fear_city_override"))

    result={"fear_city_identity":"NOT_APPLICABLE"}

    if source=="FEAR_CITY_CONFIRMED":
        result["fear_city_identity"]="CONFIRMED"
        if not override:
            result.update(mode="T06",profile="VP03",camera="CG-FC")
            return result
        result["mode"]=mode or "T06"
        result["profile"]=profile or "VP03"
        result["camera"]="CG-FC"
        return result

    if source=="MINIATURE_UNKNOWN":
        result["fear_city_identity"]="UNRESOLVED"
        result["mode"]=mode or "T01"
        result["profile"]=profile or "VP00"
        if result["mode"]=="T01" or not transform:
            result["camera"]="CG-S"
        else:
            result["camera"]=choose_transform_camera(geometry)
        return result

    result["mode"]=mode or "T01"
    result["profile"]=profile or "VP00"

    if result["mode"]=="T01":
        result["camera"]=source_cam if source_cam in {"CG-A","CG-B"} else "CG-S"
    elif transform:
        result["camera"]=choose_transform_camera(geometry)
    else:
        result["camera"]=source_cam if source_cam in {"CG-A","CG-B"} else "CG-S"

    if result["mode"]=="T01":
        if x.get("source_contains_people"):
            result["people_policy"]="PRESERVE"
        if x.get("source_contains_vehicles"):
            result["vehicle_policy"]="PRESERVE"
    else:
        if result["profile"] in {"VP00","VP01","VP02"} and not x.get("source_contains_people",False):
            result["people_policy"]="ABSENT_DEFAULT"
        if result["profile"] in {"VP00","VP01","VP02"} and not x.get("source_contains_vehicles",False):
            result["vehicle_policy"]="ABSENT_DEFAULT"
    return result

def validate_case(case):
    actual=compute(case)
    failures=[]
    for key,allowed in case["expected"].items():
        if key not in actual:
            # Optional policy fields are only required when explicitly expected.
            failures.append(f"{key}: missing")
        elif actual[key] not in allowed:
            failures.append(f"{key}: got {actual[key]!r}, expected one of {allowed!r}")
    return actual,failures

if __name__=="__main__":
    matrix=Path(__file__).with_name("CAMERA_ROUTING_VALIDATION_MATRIX.json")
    d=json.loads(matrix.read_text(encoding="utf-8"))
    results=[]
    for c in d["structural_cases"]:
        actual,failures=validate_case(c)
        results.append({"id":c["id"],"pass":not failures,"actual":actual,"failures":failures})
    passed=sum(1 for r in results if r["pass"])
    report={"matrix_version":d["matrix_version"],"passed":passed,"total":len(results),"status":"PASS" if passed==len(results) else "FAIL","results":results}
    out=Path(__file__).with_name("STRUCTURAL_VALIDATION_RESULTS.json")
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"status":report["status"],"passed":passed,"total":len(results)},indent=2))
    raise SystemExit(0 if report["status"]=="PASS" else 1)
