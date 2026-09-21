"""Real Archive software with explicitly synthetic evidence; not a live corpus test."""
import sys,json,hashlib
from pathlib import Path
from archive_v1_adapter import make_archive_v1_retriever
from archive_aware_runtime import classify_reference_need
from reference_reasoning import resolve_reference,enrich_cgc

archive=Path(sys.argv[1]).resolve()
checks=[]
def evidence(eid='TEST-MAT',domain='MATERIALS',**kw):
    obj=dict(evidence_unit_id=eid,archive_id='SYNTHETIC-TEST-ONLY',status='CLASSIFIED',domain=domain,confidence=.95,provenance_level='P4',transfer_risk='LOW',visible_fact='Matte brick response',permitted_learning=['matte response'],forbidden_transfer=['exact facade geometry'],semantic_similarity=.8,visual_similarity=.3)
    obj.update(kw);return obj

def need(key='N1',domain='MATERIALS',**kw):
    obj=classify_reference_need(specific_problem='Material behavior',target_domains=[domain],source_sufficient=False,transformation_requires_detail=True,min_provenance='P2',**kw)
    obj['need_id']=key;return obj

def run(ns,items,**kw):
    return resolve_reference(needs=ns,profile='VP03',mode='T06',camera='CG-FC',archive_retriever=make_archive_v1_retriever(archive,items),fear_city_confirmed=True,**kw)
def check(name,condition,record):
    assert condition,name
    checks.append({'name':name,'status':'PASS','record':record})

r=run([need()],[evidence()]);check('scoped_material_admission',r['status']=='READY' and len(r['generation_projection'])==1,r)
check('bundle_provenance_retained',bool(r['trace'][0]['evidence_bundle_ids']),r)
c={'preserve':['authored geometry'],'forbid':['regional import']};out=enrich_cgc(c,r);check('cgc_locks_preserved',out['preserve']==c['preserve'] and out['forbid']==c['forbid'],r)
r=run([need(domain='REGIONAL_CHARACTER')],[evidence(domain='REGIONAL_CHARACTER',anti_tags=['REGIONAL_LEAK'])]);check('fear_city_geography_excluded',r['status']=='BLOCKED_REQUIRED' and not r['generation_projection'],r)
check('negative_evidence_retained',any(t.get('negative_evidence') for t in r['trace']),r)
r=run([need(domain='SIGNAGE')],[evidence(domain='SIGNAGE',semantic_specificity=1,anti_tags=['TEXT_INVENTION'])]);check('text_invention_excluded',not r['generation_projection'] and r['status']=='BLOCKED_REQUIRED',r)
r=run([need(domain='CAMERA')],[evidence(domain='CAMERA')]);check('camera_locked',not r['generation_projection'],r)
r=run([need()],[evidence(provenance_level='P1')]);check('provenance_floor',r['status']=='BLOCKED_REQUIRED',r)
r=run([need()],[evidence(),evidence('TEST-MAT-2',visible_fact='Glossy brick response')]);check('bundle_conflicts_preserved',r['status']=='BLOCKED_REQUIRED' and any(a['decision']=='REVIEW_REQUIRED' for a in r['admissions']),r)
r=run([need()],[evidence()],query_budget=0);check('zero_budget_blocks_required',r['queries']==0 and r['status']=='BLOCKED_REQUIRED',r)
r=run([need('N1'),need('N2')],[evidence()]);check('identical_queries_cached',r['queries']==1 and r['status']=='READY',r)
r=run([need(hard_locked_unknown=True)],[evidence()]);check('unknown_not_queried',r['queries']==0 and r['locked_unknowns']==['N1'],r)
report={'status':'PASS','test_count':len(checks),'scope':'REAL_ARCHIVE_SOFTWARE_WITH_SYNTHETIC_TEST_EVIDENCE','live_classified_collection':'NOT_AVAILABLE_IN_ARCHIVE_PACKAGE','archive_modules':{str(p.relative_to(archive)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((archive/'runtime').rglob('*.py'))},'checks':checks}
out=Path(__file__).resolve().parents[1]/'validation/REFERENCE_REASONING_ARCHIVE_INTEGRATION.json';out.write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS {len(checks)}/{len(checks)} real Archive software integration; synthetic evidence explicitly labeled.')
