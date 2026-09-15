from operational_hardening import *

assert text_policy("ILLEGIBLE")["invent_semantics"] is False
assert text_policy("PARTIAL")["preserve_uncertainty"] is True
assert material_delta_allowed("T01",0)
assert not material_delta_allowed("T01",1)
assert material_delta_allowed("T06",1,True)
assert not material_delta_allowed("T06",1,False)
assert occlusion_policy(1,False)=="LOCKED_UNKNOWN"
assert occlusion_policy(2,False)=="MULTIVIEW_CONSTRAINED"
c=build_contract("REAL_PHOTO","T01","VP02","CG-S",unknown=["illegible sign"])
assert c["semantic_text_lock"]=="STRICT"
assert micro_drift_verdict([{"severity":"S3"}])["status"]=="FAIL"
assert micro_drift_verdict([{"severity":"S2"},{"severity":"S2"}])["status"]=="REVISION_REQUIRED"
assert micro_drift_verdict([{"severity":"S1"}])["status"]=="PASS"
print("PASS 12/12 operational hardening tests")
