import unittest
from copy import deepcopy
from archive_aware_runtime import classify_reference_need
from reference_reasoning import resolve_reference, enrich_cgc

class ReferenceReasoningTests(unittest.TestCase):
    def need(self, key='A', **kw):
        args=dict(specific_problem='matte brick behavior',target_domains=['MATERIALS'],source_sufficient=False,transformation_requires_detail=True,min_provenance='P2')
        args.update(kw);n=classify_reference_need(**args);n['need_id']=key;return n
    def evidence(self, **kw):
        e=dict(evidence_unit_id='E1',domain='MATERIALS',provenance_level='P3',transfer_risk='LOW',visible_fact='Matte brick',permitted_learning=['matte response'])
        e.update(kw);return e
    def run_engine(self, needs, items=None, **kw):
        args=dict(needs=needs,profile='VP02',mode='T01',camera='CG-S',archive_retriever=lambda req:{'items':items if items is not None else [self.evidence()]})
        args.update(kw);return resolve_reference(**args)
    def test_no_query_for_sufficient_and_locked(self):
        r=self.run_engine([self.need('A',source_sufficient=True),self.need('B',hard_locked_unknown=True)],archive_retriever=lambda _:self.fail('Unexpected query'))
        self.assertEqual(r['queries'],0);self.assertEqual(r['locked_unknowns'],['B'])
    def test_required_unavailable_blocks(self):
        r=self.run_engine([self.need()],archive_retriever=None)
        self.assertEqual(r['status'],'BLOCKED_REQUIRED');self.assertFalse(r['generation_projection'])
    def test_optional_failure_does_not_block(self):
        r=self.run_engine([self.need(transformation_requires_detail=False)],archive_retriever=None)
        self.assertEqual(r['status'],'READY')
    def test_required_first_under_budget(self):
        a=self.need('A',transformation_requires_detail=False);a['specific_problem']='optional'
        r=self.run_engine([a,self.need('Z')],query_budget=1)
        self.assertEqual(r['need_results']['Z'],'SATISFIED_EVIDENCE');self.assertEqual(r['queries'],1)
    def test_identical_request_cache(self):
        r=self.run_engine([self.need('A'),self.need('B')]);self.assertEqual(r['queries'],1)
    def test_different_problem_not_cached(self):
        b=self.need('B');b['specific_problem']='mortar depth'
        self.assertEqual(self.run_engine([self.need(),b])['queries'],2)
    def test_cycle_rejected_before_queries(self):
        a=self.need();b=self.need('B');a['depends_on']=['B'];b['depends_on']=['A']
        with self.assertRaises(ValueError):self.run_engine([a,b],archive_retriever=lambda _:self.fail('Query'))
    def test_missing_dependency_rejected(self):
        a=self.need();a['depends_on']=['X']
        with self.assertRaises(ValueError):self.run_engine([a])
    def test_locked_dependency_blocks(self):
        b=self.need('B');b['depends_on']=['A']
        r=self.run_engine([self.need(hard_locked_unknown=True),b]);self.assertEqual(r['queries'],0);self.assertEqual(r['status'],'BLOCKED_REQUIRED')
    def test_provenance_enforced(self):
        r=self.run_engine([self.need()],[self.evidence(provenance_level='P1')]);self.assertEqual(r['status'],'BLOCKED_REQUIRED')
    def test_duplicate_not_independent(self):
        e=self.evidence();r=self.run_engine([self.need()],[e,e]);self.assertEqual(len(r['admissions']),1)
    def test_conflicting_duplicate_review(self):
        r=self.run_engine([self.need()],[self.evidence(),self.evidence(visible_fact='Glossy brick')]);self.assertEqual(r['status'],'BLOCKED_REQUIRED');self.assertFalse(r['generation_projection'])
    def test_fear_city_geography_not_projected(self):
        n=self.need(target_domains=['REGIONAL_CHARACTER']);r=self.run_engine([n],[self.evidence(domain='REGIONAL_CHARACTER')],fear_city_confirmed=True)
        self.assertFalse(r['generation_projection']);self.assertEqual(r['status'],'BLOCKED_REQUIRED')
    def test_text_invention_not_projected(self):
        r=self.run_engine([self.need(target_domains=['SIGNAGE'])],[self.evidence(domain='SIGNAGE',semantic_specificity=1)])
        self.assertFalse(r['generation_projection'])
    def test_cgc_copy_and_block(self):
        c={'preserve':['geometry']};r=self.run_engine([self.need()]);o=enrich_cgc(c,r);o['preserve'].clear();self.assertEqual(c['preserve'],['geometry'])
        with self.assertRaises(ValueError):enrich_cgc(c,self.run_engine([self.need()],[]))
    def test_inputs_unchanged(self):
        n=[self.need()];e=[self.evidence()];before=deepcopy((n,e));self.run_engine(n,e);self.assertEqual((n,e),before)

if __name__=='__main__':unittest.main()
