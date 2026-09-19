#!/usr/bin/env python3
import argparse,json
from pathlib import Path

WEIGHTS={"identity":25,"geometry":15,"camera":15,"text":10,"material":10,"occlusion":10,"reference_isolation":10,"atmosphere":5}

def verdict(result):
    scores=result.get("scores",{})
    total=sum(float(scores.get(k,0)) for k in WEIGHTS)
    critical=result.get("critical_failures",[])
    findings=result.get("findings",[])
    s3=sum(1 for f in findings if f.get("severity")=="S3")
    s2=sum(1 for f in findings if f.get("severity")=="S2")
    if critical or s3:
        status="FAIL"
    elif total < 85:
        status="FAIL"
    elif total < 90 or s2==1:
        status="REVIEW"
    elif s2>=2:
        status="FAIL"
    else:
        status="PASS"
    return {"case_id":result.get("case_id"),"score":round(total,2),"status":status,"critical_failures":critical,"s2":s2,"s3":s3}

def suite_verdict(results):
    rows=[verdict(r) for r in results]
    if not rows:
        return {"status":"NO_RESULTS","cases":[]}
    if any(r["status"]=="FAIL" for r in rows):
        status="FAIL"
    elif any(r["status"]=="REVIEW" for r in rows):
        status="REVIEW"
    else:
        status="PASS"
    return {"status":status,"average_score":round(sum(r["score"] for r in rows)/len(rows),2),"cases":rows}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("results_json")
    args=ap.parse_args()
    data=json.loads(Path(args.results_json).read_text())
    results=data["results"] if isinstance(data,dict) and "results" in data else data
    print(json.dumps(suite_verdict(results),indent=2))
