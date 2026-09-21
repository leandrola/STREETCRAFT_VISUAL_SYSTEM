import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'integration'))
from streetcraft_orchestrator import orchestrate


def scene(entity=None, *, mode='T01', profile='VP02'):
    if entity is None:
        entity={
            'entity_id':'E-BLDG','label':'storefront','kind':'ARCHITECTURE',
            'roles':['STRUCTURAL_CORE','IDENTITY_ANCHOR'],'preservation_level':'P0',
            'epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,
            'salience':{'identity_salience':1,'structural_dependency':1,'task_relevance':1,'relationship_centrality':0,'temporal_relevance':0}
        }
    return {'scene_id':'TEST','source_identity':'TEST_SOURCE','mode':mode,'profile':profile,'entities':[entity],'relationships':[]}


def ev(domain='MATERIALS', **kw):
    x={'evidence_unit_id':'E1','archive_id':'TEST','status':'CLASSIFIED','domain':domain,
       'provenance_level':'P3','transfer_risk':'LOW','visible_fact':'restrained material',
       'permitted_learning':['restrained response'],'forbidden_transfer':['exact geometry']}
    x.update(kw); return x

class OrchestratorTests(unittest.TestCase):
    def retriever(self, items):
        return lambda req:{'evidence_bundle_id':'EB-TEST','items':items,'conflicts':[],'negative_evidence':[]}

    def test_no_reference_path_reaches_generation_ready(self):
        r=orchestrate({'command_text':'/sc-2a','scene':scene()},archive_retriever=None)
        self.assertEqual(r['status'],'GENERATION_READY'); self.assertTrue(r['generation_ready'])
        self.assertEqual(r['resolved_config']['camera'],'CG-A')

    def test_sar2_required_reference_projects_into_cgc(self):
        e={'entity_id':'E-MAT','label':'brick behavior','kind':'SURFACE','roles':['CONTEXTUAL_SUPPORT'],
           'preservation_level':'P3','epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,
           'reference_domain':'MATERIALS','reference_required':True,'max_transfer_risk':'LOW','salience':{}}
        r=orchestrate({'command_text':'/sc-2a','scene':scene(e)},archive_retriever=self.retriever([ev()]))
        self.assertEqual(r['status'],'GENERATION_READY')
        self.assertEqual(r['reference_reasoning']['status'],'READY')
        self.assertEqual(r['cgc_final']['reference_reasoning']['generation_projection'][0]['domain'],'MATERIALS')

    def test_locked_unknown_is_never_queried(self):
        e={'entity_id':'E-HIDDEN','label':'hidden rear wall','kind':'ARCHITECTURE','roles':['UNKNOWN_REGION'],
           'preservation_level':'P5-D','epistemic_class':'UNKNOWN','confidence':'LOW','observed':False,'salience':{}}
        calls=[]
        r=orchestrate({'command_text':'/sc-rdr2-elevation','scene':scene(e,mode='T02')},archive_retriever=lambda req:calls.append(req))
        self.assertEqual(r['status'],'GENERATION_READY'); self.assertEqual(calls,[])
        self.assertIn('SAR2-E-HIDDEN',r['reference_reasoning']['locked_unknowns'])
        self.assertEqual(r['resolved_config']['camera'],'CG-F')
        self.assertIn('camera_non_frontal',r['cgc_final']['forbid'])

    def test_frozen_text_mutation_blocks_generation(self):
        r=orchestrate({'command_text':'/sc-2a','scene':scene(),
             'text_tokens':[{'token_id':'T1','literal':'TERMINAL DINER','confidence':.99,'preservation_level':'P0','identity_bearing':True}],
             'proposed_text':{'T1':'TERMINAL DINNER'}},archive_retriever=None)
        self.assertEqual(r['status'],'BLOCKED_PREFLIGHT')
        self.assertTrue(any(f.get('code')=='TEXT_MUTATION' for f in r['pre_generation_gate']['findings']))

    def test_t01_material_inflation_blocks(self):
        r=orchestrate({'command_text':'/sc-2a','scene':scene(),'material_intensity_delta':1},archive_retriever=None)
        self.assertEqual(r['status'],'BLOCKED_PREFLIGHT')
        self.assertTrue(any(f.get('code')=='MATERIAL_INTENSITY_DELTA_BLOCK' for f in r['pre_generation_gate']['findings']))

    def test_reference_failure_blocks_before_final_cgc(self):
        e={'entity_id':'E-MAT','label':'brick behavior','kind':'SURFACE','roles':['CONTEXTUAL_SUPPORT'],
           'preservation_level':'P3','epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,
           'reference_domain':'MATERIALS','reference_required':True,'salience':{}}
        r=orchestrate({'command_text':'/sc-2a','scene':scene(e)},archive_retriever=lambda req:{'items':[]})
        self.assertEqual(r['status'],'BLOCKED_REFERENCE'); self.assertNotIn('cgc_final',r)

    def test_fear_city_geo_reference_is_nontransferable(self):
        e={'entity_id':'FC-GEO','label':'authored location','kind':'REGION','roles':['CONTEXTUAL_SUPPORT'],
           'preservation_level':'P3','epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,
           'reference_domain':'REGIONAL_CHARACTER','reference_required':True,'max_transfer_risk':'HIGH','authored_world':True,'salience':{}}
        r=orchestrate({'command_text':'/sc-fear','scene':scene(e,mode='T06',profile='VP03'),'fear_city_confirmed':True},
                      archive_retriever=self.retriever([ev('REGIONAL_CHARACTER')]))
        self.assertEqual(r['status'],'BLOCKED_REFERENCE')

    def test_proposed_external_geo_blocks_confirmed_fear_city(self):
        r=orchestrate({'command_text':'/sc-fear','scene':scene(mode='T06',profile='VP03'),'fear_city_confirmed':True,
                       'proposed_geo_tokens':['New York']},archive_retriever=None)
        self.assertEqual(r['status'],'BLOCKED_PREFLIGHT')
        self.assertTrue(any(f.get('code')=='REGIONAL_LEAK' for f in r['pre_generation_gate']['findings']))

    def test_unknown_command_fails_cleanly(self):
        r=orchestrate({'command_text':'/sc-does-not-exist','scene':scene()},archive_retriever=None)
        self.assertEqual(r['status'],'COMMAND_ERROR')

    def test_cgc_preserves_scene_identity_locks(self):
        a={'entity_id':'A','label':'sign','kind':'SIGNAGE','roles':['IDENTITY_ANCHOR'],'preservation_level':'P1','epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,'salience':{}}
        b={'entity_id':'B','label':'wall','kind':'ARCHITECTURE','roles':['STRUCTURAL_CORE'],'preservation_level':'P0','epistemic_class':'OBSERVED','confidence':'HIGH','observed':True,'salience':{}}
        s={'scene_id':'REL','source_identity':'X','mode':'T01','profile':'VP02','entities':[a,b],
           'relationships':[{'relationship_id':'R1','subject':'A','predicate':'ATTACHED_TO','object':'B','protection':'PR0','epistemic_class':'OBSERVED','confidence':'HIGH'}]}
        r=orchestrate({'command_text':'/sc-2a','scene':s},archive_retriever=None)
        self.assertTrue(any(x.startswith('break_protected_relationships:A') for x in r['cgc_final']['forbid']))

if __name__=='__main__': unittest.main()
