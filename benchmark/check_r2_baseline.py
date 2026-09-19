#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"benchmark/baselines/R2_VISUAL_BASELINE_1_8_1.json"

def dhash(path,hash_size=8):
    with Image.open(path) as im:
        im=im.convert("L").resize((hash_size+1,hash_size))
        px=list(im.getdata())
    value=0;bit=0
    for y in range(hash_size):
        row=y*(hash_size+1)
        for x in range(hash_size):
            if px[row+x]>px[row+x+1]: value|=1<<bit
            bit+=1
    return f"{value:016x}"

data=json.loads(BASE.read_text())
errors=[]
checked=0
for case in data["cases"]:
    for f in case["fixtures"]:
        p=ROOT/f["path"]
        checked+=1
        if not p.exists():
            errors.append({"path":f["path"],"error":"MISSING"}); continue
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        with Image.open(p) as im:
            dims=(im.width,im.height)
        if sha!=f["sha256"]: errors.append({"path":f["path"],"error":"SHA256","expected":f["sha256"],"actual":sha})
        if dhash(p)!=f["dhash"]: errors.append({"path":f["path"],"error":"DHASH"})
        if dims!=(f["width"],f["height"]): errors.append({"path":f["path"],"error":"DIMENSIONS"})
print(json.dumps({"result":"PASS" if not errors else "FAIL","cases":len(data["cases"]),"fixtures_checked":checked,"errors":errors},indent=2))
raise SystemExit(0 if not errors else 1)
