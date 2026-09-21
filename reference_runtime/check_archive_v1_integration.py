import sys, json
from pathlib import Path
SVS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SVS/"reference_runtime"))
from archive_aware_runtime import classify_reference_need, resolve_runtime, enrich_cgc
from archive_v1_adapter import make_archive_v1_retriever

if len(sys.argv)<2:
    raise SystemExit("usage: check_archive_v1_integration.py <archive_root>")
archive_root=Path(sys.argv[1])

evidence=[
{"evidence_unit_id":"EU-MAT","archive_id":"SCA-MAT","status":"CLASSIFIED","domain":"MATERIALS","confidence":.95,"provenance_level":"P4","transfer_risk":"LOW","domain_match":1,"compatibility":1,"transfer_safety":1,"semantic_similarity":.8,"visual_similarity":.3,"visible_fact":"Brick remains predominantly matte at street scale.","permitted_learning":["matte brick response","subtle mortar depth"],"forbidden_transfer":["exact facade geometry"],"anti_tags":[]},
{"evidence_unit_id":"EU-TXT","archive_id":"SCA-TXT","status":"CLASSIFIED","domain":"SIGNAGE","confidence":.9,"provenance_level":"P3","transfer_risk":"MEDIUM","domain_match":1,"compatibility":1,"transfer_safety":.8,"semantic_similarity":.9,"visual_similarity":.9,"visible_fact":"Projecting metal sign.","permitted_learning":["projecting mounting"],"semantic_specificity":1.0,"anti_tags":["TEXT_INVENTION"]},
{"evidence_unit_id":"EU-REG","archive_id":"SCA-REG","status":"CLASSIFIED","domain":"REGIONAL_CHARACTER","confidence":1,"provenance_level":"P4","transfer_risk":"MEDIUM","domain_match":1,"compatibility":1,"transfer_safety":.7,"semantic_similarity":1,"visual_similarity":1,"visible_fact":"Explicit New York regional marker.","permitted_learning":[],"anti_tags":["REGIONAL_LEAK"]}
]

retriever=make_archive_v1_retriever(archive_root,evidence)

need=classify_reference_need(
    specific_problem="Translate miniature brick into full-scale material behavior",
    target_domains=["MATERIALS"],
    source_sufficient=False,
    transformation_requires_detail=True,
    task_context="Fear City T06 material behavior",
    source_context="confirmed Fear City",
    min_provenance="P2",
    max_transfer_risk="MEDIUM",
    source_invariants=["authored geometry locked"],
    forbidden_transfers=["REGIONAL_LEAK"]
)
rr=resolve_runtime(needs=[need],profile="VP03",mode="T06",camera="CG-FC",archive_retriever=retriever,fear_city_confirmed=True)
assert rr["runtime_status"]=="READY"
assert [a["evidence_unit_id"] for a in rr["admissions"] if a["decision"]=="ADMITTED_SCOPED"]==["EU-MAT"]

cgc={"source_identity":"FEAR_CITY_CONFIRMED","mode":"T06","profile":"VP03","camera":"CG-FC","preserve":["authored geometry"],"transform":["material behavior"],"remove":[],"infer":[],"unknown":[],"forbid":["geographic import"],"semantic_text_lock":"STRICT","material_intensity_delta":1,"occlusion_locks":[]}
en=enrich_cgc(cgc,rr)
assert en["reference_runtime"]["generation_projection"][0]["domain"]=="MATERIALS"
print(json.dumps({"result":"PASS","runtime_status":rr["runtime_status"],"admitted":[a["evidence_unit_id"] for a in rr["admissions"]],"projected":len(en["reference_runtime"]["generation_projection"])},indent=2))
