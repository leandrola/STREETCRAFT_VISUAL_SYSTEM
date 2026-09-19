import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"patch"))
from svs_1_9_1_patch import *

# 1 exact numeral freezes
t=classify_text_token("315",.99,"P1",identity_bearing=True,numeral=True)
assert t["state"]=="FROZEN_EXACT"
# 2 mutation is S3
r=validate_candidate_text(t,"313")
assert r["status"]=="FAIL" and r["severity"]=="S3" and r["code"]=="TEXT_MUTATION"
# 3 exact stays exact
assert validate_candidate_text(t,"315")["status"]=="PASS"
# 4 CBGB freezes
cb=classify_text_token("CBGB",.99,"P1",True,False)
assert cb["state"]=="FROZEN_EXACT"
# 5 low confidence masks
lo=classify_text_token(None,.2,"P2")
assert lo["state"]=="MASK_GRAPHIC_ONLY"
# 6 graphic-only readable text is S3
assert validate_candidate_text(lo,"FRESH PRODUCE")["code"]=="TEXT_INVENTION"
# 7 ambiguity pass
assert validate_candidate_text(lo,None)["status"]=="PASS"
# 8 render hint is non-semantic
assert low_confidence_render_hint(lo)["readable_text"] is False
# 9 New York blocked in FC
fg=fear_city_geographic_gate(["NEW YORK"],["TANNER STREET","JERICHO STREET"])
assert fg["status"]=="FAIL" and fg["severity"]=="S3"
# 10 authored Tanner allowed
assert fear_city_geographic_gate(["TANNER STREET"],["TANNER STREET"])["status"]=="PASS"
# 11 unknown external geography also blocked
assert fear_city_geographic_gate(["SOME REAL CITY"],["TANNER STREET"])["status"]=="FAIL"
# 12 explicit geo override requires review, not silent pass
assert fear_city_geographic_gate(["NEW YORK"],[],True)["status"]=="REVIEW_REQUIRED"

features=[
 {"id":"mat","domain":"MATERIALS","feature_type":"material","value":"matte brick","target_entity_id":"WALL"},
 {"id":"cam","domain":"CAMERA","feature_type":"camera","value":"oblique"},
 {"id":"txt","domain":"SIGNAGE","feature_type":"text","value":"NEW SHOP","semantic_specificity":1},
 {"id":"geo","domain":"REGIONAL_CHARACTER","feature_type":"geography","value":"NEW YORK"},
 {"id":"prop","domain":"STREET_FURNITURE","feature_type":"prop","value":"newspaper box","target_entity_id":None},
 {"id":"wet","domain":"LIGHT_ATMOSPHERE","feature_type":"atmosphere","property":"surface_wetness","value":"WET"}
]
# 13 material scoped transfer allowed
rb=reference_bleed_preflight(features,allowed_domains={"MATERIALS","CAMERA","SIGNAGE","REGIONAL_CHARACTER","STREET_FURNITURE","LIGHT_ATMOSPHERE"},source_entity_ids={"WALL"},camera_lock="CG-FC",fear_city_confirmed=True,source_authored_geo_tokens={"TANNER STREET"},source_states={"surface_wetness":"DRY"})
assert any(x["id"]=="mat" for x in rb["admitted"])
# 14 camera transfer rejected
assert any(x["id"]=="cam" and "CAMERA_LOCK" in x["reasons"] for x in rb["rejected"])
# 15 ref text semantics rejected
assert any(x["id"]=="txt" and "REFERENCE_TEXT_SEMANTICS_FORBIDDEN" in x["reasons"] for x in rb["rejected"])
# 16 geography rejected
assert any(x["id"]=="geo" and "FEAR_CITY_GEOGRAPHIC_NULL_LOCK" in x["reasons"] for x in rb["rejected"])
# 17 unscoped prop rejected
assert any(x["id"]=="prop" and "UNSCOPED_REFERENCE_OBJECT" in x["reasons"] for x in rb["rejected"])
# 18 wetness rejected
assert any(x["id"]=="wet" and "UNAUTHORIZED_WETNESS_IMPORT" in x["reasons"] for x in rb["rejected"])
# 19 preflight fails critical
assert rb["status"]=="FAIL"
# 20 full gate blocks exact token mutation
g=patch_pre_generation_gate(text_tokens=[dict(t,token_id="NUM315")],proposed_text={"NUM315":"313"},fear_city_confirmed=False,reference_features=[],allowed_domains=set())
assert g["status"]=="BLOCK_GENERATION"
# 21 full gate blocks FC geography
g2=patch_pre_generation_gate(text_tokens=[],proposed_text={},fear_city_confirmed=True,proposed_geo_tokens=["NEW YORK"],source_authored_geo_tokens=["TANNER STREET"],reference_features=[],allowed_domains=set())
assert g2["status"]=="BLOCK_GENERATION"
# 22 clean gate passes
g3=patch_pre_generation_gate(text_tokens=[dict(t,token_id="NUM315")],proposed_text={"NUM315":"315"},fear_city_confirmed=True,proposed_geo_tokens=["TANNER STREET"],source_authored_geo_tokens=["TANNER STREET"],reference_features=[features[0]],allowed_domains={"MATERIALS"},source_entity_ids={"WALL"},camera_lock="CG-FC",source_states={"surface_wetness":"DRY"})
assert g3["status"]=="PASS"
# 23 high-confidence P2 non-identity is partial not frozen
p=classify_text_token("SALE",.9,"P2",False,False)
assert p["state"]=="MASK_PARTIAL"
# 24 partial completion risk is review
assert validate_candidate_text(p,"SALE TODAY")["status"]=="REVIEW"
print("PASS 24/24 SVS 1.9.1 patch tests")
