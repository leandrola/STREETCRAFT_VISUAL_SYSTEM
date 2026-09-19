import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from resolve_commands import resolve

cases=[
("/sc-core",{"profile":"VP00","mode":"T01","camera":"AUTO"}),
("/sc-classic",{"profile":"VP01","mode":"T01","camera":"AUTO"}),
("/sc-2",{"profile":"VP02","mode":"T01","camera":"AUTO"}),
("/sc-2a",{"profile":"VP02","camera":"CG-A"}),
("/sc-2b",{"profile":"VP02","camera":"CG-B"}),
("/sc-rdr2-elevation",{"profile":"VP02","mode":"T02","camera":"CG-F","identity_lock":"STRICT","occlusion_lock":"LOCKED_UNKNOWN","frontalization":"STRICT","aspect_ratio":"16:9","street_presence":"MINIMAL"}),
("/sc-2f",{"profile":"VP02","mode":"T02","camera":"CG-F","aspect_ratio":"16:9"}),
("/sc-rdr2-front",{"profile":"VP02","mode":"T02","camera":"CG-F","street_presence":"MINIMAL"}),
("/sc-elevation",{"profile":"VP02","mode":"T02","camera":"CG-F","identity_lock":"STRICT"}),
("/sc-2 /sc-front",{"profile":"VP02","mode":"T01","camera":"CG-F","frontalization":"STRICT"}),
("/sc-fear",{"profile":"VP03","mode":"T06","camera":"CG-FC"}),
("/sc-fear2",{"profile":"VP02","mode":"T06","explicit_fear_city_profile_override":True}),
("/sc-2 /sc-clean",{"profile":"VP02","mode":"T03"}),
("/sc-core /sc-lock /sc-preserve /sc-noinvent",{"camera":"CG-S","preservation":"STRICT_OBSERVED_EVIDENCE","uncertainty":"STRICT_UNKNOWN_PRESERVATION"}),
("/sc-rdr2b",{"profile":"VP02","camera":"CG-B"}),
]
passed=0
for text,expect in cases:
    r=resolve(text);assert r["status"]=="OK",(text,r)
    for k,v in expect.items():assert r["config"][k]==v,(text,k,r["config"][k],v)
    passed+=1
errors=[
 ("/sc-core /sc-2","PROFILE_CONFLICT"),
 ("/sc-fear /sc-2","PROFILE_CONFLICT"),
 ("/sc-rdr2-elevation /sc-core","PROFILE_CONFLICT"),
 ("/sc-foobar","UNKNOWN_COMMAND"),
]
for text,err in errors:
    assert resolve(text)["error"]==err,(text,resolve(text))
    passed+=1
print(f"PASS {passed}/19 CIL 1.1 tests")
