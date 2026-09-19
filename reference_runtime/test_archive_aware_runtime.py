import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'reference_runtime'))
from archive_aware_runtime import *
n0=classify_reference_need(specific_problem='source sufficient',target_domains=['MATERIALS'],source_sufficient=True,transformation_requires_detail=False);assert n0['state']=='RN_NONE'
nb=classify_reference_need(specific_problem='unreadable exact sign',target_domains=['SIGNAGE'],source_sufficient=False,transformation_requires_detail=True,hard_locked_unknown=True);assert nb['state']=='RN_BLOCKED'
nr=classify_reference_need(specific_problem='full-scale brick behavior',target_domains=['MATERIALS'],source_sufficient=False,transformation_requires_detail=True);assert nr['state']=='RN_REQUIRED'
assert archive_request_from_need(nr,profile='VP02',mode='T01')['max_results']<=5
item={'evidence_unit_id':'EU-1','domain':'MATERIALS','status':'CLASSIFIED','transfer_risk':'LOW','permitted_learning':['brick reflectance'],'visible_fact':'matte brick'}
a=admit_candidate(item,nr,camera='CG-A');assert a['decision']=='ADMITTED_SCOPED'
sign={'evidence_unit_id':'EU-S','domain':'SIGNAGE','status':'CLASSIFIED','transfer_risk':'LOW','semantic_specificity':1.0,'anti_tags':['TEXT_INVENTION'],'permitted_learning':['sign mounting']}
ns=classify_reference_need(specific_problem='sign form',target_domains=['SIGNAGE'],source_sufficient=False,transformation_requires_detail=False);assert admit_candidate(sign,ns,camera='CG-A')['decision']=='ADMITTED_NEGATIVE_ONLY'
cam={'evidence_unit_id':'EU-C','domain':'CAMERA','status':'CLASSIFIED','transfer_risk':'LOW'}
nc=classify_reference_need(specific_problem='camera example',target_domains=['CAMERA'],source_sufficient=False,transformation_requires_detail=False);assert admit_candidate(cam,nc,camera='CG-S')['decision']=='ADMITTED_NEGATIVE_ONLY'
def retriever(req):return {'evidence_bundle_id':'EB-X','items':[item],'conflicts':[],'negative_evidence':[]}
rr=resolve_runtime(needs=[nr],profile='VP02',mode='T01',camera='CG-A',archive_retriever=retriever);assert rr['runtime_status']=='READY';assert len(rr['admissions'])==1
cgc={'source_identity':'REAL_PHOTO','mode':'T01','profile':'VP02','camera':'CG-A'};en=enrich_cgc(cgc,rr);assert len(en['reference_runtime']['generation_projection'])==1
un=resolve_runtime(needs=[nr],profile='VP02',mode='T01',camera='CG-A',archive_retriever=None);assert un['runtime_status']=='ARCHIVE_UNAVAILABLE'
print('PASS 10/10 archive-aware runtime unit tests')
