"""Synthetic control tests: never evidence of visual quality or pilot PASS."""
from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import unittest
from unittest.mock import patch

from PIL import Image

from visual_scene_graph.generation_cases import base_inputs, retriever
from visual_scene_graph.generation_compiler import compile_generation_contract, digest, seal
from visual_scene_graph.pilot.harness import ARTIFACTS, PilotBlocked, execute, prepare, sha
from visual_scene_graph.pilot.evaluation import evaluate, close_campaign


class ControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = base_inputs()

    def setUp(self):
        gate = patch('visual_scene_graph.pilot.harness.check_preconditions')
        gate.start()
        self.addCleanup(gate.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        b = deepcopy(self.base)
        self.data = {'request':b['request'], 'runtime':b['runtime'], 'sar2':b['sar2'],
                     'rr2':b['runtime']['reference_reasoning'], 'cgc_final':b['stable_cgc'],
                     'expected_graph':b['expected_graph'], 'candidate_graph':deepcopy(b['expected_graph']),
                     'generation_context':b['generation_context'],
                     'contract':compile_generation_contract(b['expected_graph'],sar2=b['sar2'],generation_context=b['generation_context'])}
        buffer = BytesIO()
        Image.new('RGB',(4,4),'white').save(buffer,format='PNG')
        self.source = buffer.getvalue()
        self.manifest = {'schema_version':'1.0.0','fixture_id':'CONTROL_ONLY','pilot_enabled':True,
            'source_binding':{'source_identity':b['sar2']['source_identity'], 'attested_by':'unit-test', 'evidence':'SYNTHETIC; not visual evidence'},
            'artifacts':{},'required_priorities':['P0','PR0','PR1','LOCK'],
            'generation':{'provider':'test','model':'fake','seed':7,'parameters':{'size':'4x4','quality':'standard','output_format':'png'}},
            'rubric':[{'constraint_id':c['id'],'category':'lock' if c['priority']=='LOCK' else 'relation',
                       'priority':c['priority'],'target':c['id'],'criterion':'Preserve approved source constraint'}
                      for c in self.data['contract']['constraints'] if c['priority'] in {'P0','PR0','PR1','LOCK'} or c['id'].startswith('edge:')] +
                     [{'constraint_id':k,'category':k,'priority':'REQUIRED','target':'whole image','criterion':'Compare source and output'} for k in ('identity','unauthorized_change')]}
        self.freeze()

    def freeze(self):
        for k in ARTIFACTS:
            raw = self.source if k=='source' else json.dumps(self.data[k]).encode()
            (self.root/k).write_bytes(raw)
            self.manifest['artifacts'][k] = {'path':k,'sha256':sha(raw),'provenance':'synthetic control test'}
        self.authorize()

    def authorize(self):
        self.allow = {'version':'1.0.0','fixtures':{'CONTROL_ONLY':{'status':'ADMITTED','manifest_sha256':digest(self.manifest)}}}

    def prepare(self):
        return prepare(self.manifest,self.allow,self.root)

    def blocked(self, code):
        with self.assertRaisesRegex(PilotBlocked,code):
            self.prepare()

    def test_healthy_and_exact_delta(self):
        p = self.prepare()
        self.assertEqual(p['comparison']['status'],'PASS')
        self.assertEqual(p['payloads']['A']['common'],p['payloads']['B']['common'])
        self.assertEqual([json.loads(x) for x in p['payloads']['A']['relations_and_locks'].splitlines()],p['payloads']['B']['relations_and_locks'])
        from visual_scene_graph.pilot.review_dry_run import review
        out, report = execute(p, self.root/'review')
        self.assertEqual(review(out)['status'], 'PASS')
        # Equal branches and a recomputed delta must not conceal shared CGC loss.
        payloads = json.loads((out/'payloads.json').read_text())
        for branch in ('A', 'B'):
            payloads[branch]['common']['stable_cgc']['source_identity'] = 'OTHER_SOURCE'
        (out/'payloads.json').write_text(json.dumps(payloads))
        report['delta_sha256'] = digest({'manifest':p['manifest'], 'payloads':payloads})
        (out/'report.json').write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'DRY_RUN_REVIEW_FAILED'):
            review(out)

    def test_disabled(self):
        self.manifest['pilot_enabled']=False
        self.authorize()
        self.blocked('PILOT_DISABLED')

    def test_unauthorized(self):
        self.allow['fixtures']={}
        self.blocked('FIXTURE_NOT_AUTHORIZED')

    def test_manifest_tamper(self):
        self.manifest['generation']['model']='other'
        self.blocked('FIXTURE_NOT_AUTHORIZED')

    def test_artifact_tamper(self):
        (self.root/'contract').write_text('{}')
        self.blocked('HASH_MISMATCH')

    def test_resealed_contract_tamper(self):
        self.data['contract']['constraints'][0]['value']='changed'
        self.data['contract']=seal(self.data['contract'])
        self.freeze()
        self.blocked('COMPARISON_FAILED')

    def test_mapping_incomplete(self):
        self.data['cgc_final']['scene_intelligence']['entity_actions'].pop()
        self.data['runtime']['cgc_final']=deepcopy(self.data['cgc_final'])
        self.freeze()
        self.blocked('COMPARISON_FAILED')

    def test_blocked_runtime_states(self):
        for status in ('REVIEW_REQUIRED','BLOCKED_PREFLIGHT','UNAVAILABLE'):
            self.data['runtime']['status']=status
            self.freeze()
            self.blocked('NOT_GENERATION_READY')

    def test_preflight(self):
        self.data['runtime']['pre_generation_gate']['status']='FAIL'
        self.freeze()
        self.blocked('BLOCKED_PREFLIGHT')

    def test_policies_diverge(self):
        self.data['generation_context']['policies']['semantic_text_lock']='NORMAL'
        self.freeze()
        self.blocked('COMPARISON_FAILED')

    def test_unknown_cgc_field(self):
        self.data['cgc_final']['extra']='lost?'
        self.data['runtime']['cgc_final']=deepcopy(self.data['cgc_final'])
        self.freeze()
        self.blocked('COMPARISON_FAILED')

    def test_candidate_is_not_baseline(self):
        self.manifest['artifacts']['expected_graph']=deepcopy(self.manifest['artifacts']['candidate_graph'])
        self.authorize()
        self.blocked('CANDIDATE_USED_AS_BASELINE')

    def test_dry_run_no_calls_and_append_only(self):
        p=self.prepare()
        a,r=execute(p,self.root/'runs')
        b,s=execute(p,self.root/'runs')
        self.assertNotEqual(a,b)
        self.assertEqual(r['images'],[])
        self.assertEqual(r['reason'],'DRY_RUN_NO_IMAGES')
        self.assertEqual(r['delta_sha256'],s['delta_sha256'])
        self.manifest['generation']['provider'] = 'DRY_RUN_ONLY_UNSELECTED'
        self.authorize()
        provisional = self.prepare()
        _, dry = execute(provisional, self.root/'provisional')
        fake = self.fake()
        _, blocked = execute(provisional, self.root/'provisional', generator=fake,
                             dry_run=False, reviewed_delta=dry['delta_sha256'])
        self.assertEqual(blocked['reason'], 'PROVISIONAL_GENERATION_CONFIGURATION')
        self.assertEqual(fake.calls, 0)

    def test_provider_absent(self):
        p=self.prepare()
        _,dry=execute(p,self.root/'runs')
        _,r=execute(p,self.root/'runs',dry_run=False,reviewed_delta=dry['delta_sha256'])
        self.assertEqual((r['status'],r['reason']),('BLOCKED','NO_GENERATOR'))

    def test_review_required(self):
        _,r=execute(self.prepare(),self.root/'runs',dry_run=False)
        self.assertEqual(r['reason'],'DELTA_REVIEW_REQUIRED')

    def fake(self,invalid=False):
        outer=self
        class Fake:
            provider='test'; model='fake'; calls=0
            def generate(self,request):
                self.calls+=1
                outer.assertEqual(set(request),{'source_base64','payload','provider','model','seed','parameters'})
                return (b'broken' if invalid else outer.source), {k:deepcopy(request[k]) for k in ('provider','model','seed','parameters')} | {'generation_id':str(self.calls)}
        return Fake()

    def pair(self):
        p=self.prepare()
        _,dry=execute(p,self.root/'runs')
        fake=self.fake()
        out,r=execute(p,self.root/'runs',generator=fake,dry_run=False,reviewed_delta=dry['delta_sha256'])
        self.assertEqual(fake.calls,2)
        return out,r

    def review(self,out):
        packet=json.loads((out/'review_packet'/'blind_review.json').read_text())
        return {'run_id':packet['run_id'],'reviewer':'control test','blind':True,'source_sha256':packet['source_sha256'],
            'disagreements':[], 'images':[dict(item,observations=[{'constraint_id':c['constraint_id'],'preserved':'YES','severity':'S0',
               'region':[0,0,1,1],'justification':'Synthetic control only'} for c in self.manifest['rubric']]) for item in packet['images']]}

    def test_generator_failure_stops_pair_and_campaign(self):
        p=self.prepare()
        _,dry=execute(p,self.root/'runs')
        fake=self.fake(invalid=True)
        _,r=execute(p,self.root/'runs',generator=fake,dry_run=False,reviewed_delta=dry['delta_sha256'])
        self.assertEqual(fake.calls,1)
        self.assertEqual(r['reason'],'TECHNICAL_FAILURE')
        with self.assertRaisesRegex(PilotBlocked,'PREVIOUS_PAIR'):
            execute(p,self.root/'runs',generator=fake,dry_run=False,reviewed_delta=dry['delta_sha256'])

    def test_blind_review_tie_is_not_pass(self):
        out,_=self.pair()
        result=evaluate(out,self.review(out))
        self.assertEqual((result['status'],result['verdict']),('INCONCLUSIVE','TIE'))
        self.assertEqual(close_campaign([out],['CONTROL_ONLY'],True)['status'],'INCONCLUSIVE')

    def test_s3_stops_campaign(self):
        out,_=self.pair()
        review=self.review(out)
        row=review['images'][0]['observations'][0]
        row.update(preserved='NO',severity='S3')
        self.assertEqual(evaluate(out,review)['status'],'FAIL')
        self.assertTrue((out.parent/'STOP').exists())

    def test_budget(self):
        root=self.root/'runs'
        root.mkdir()
        for i in range(7):
            p=root/str(i); p.mkdir(); (p/'A.attempt.json').write_text('{}')
        with self.assertRaisesRegex(PilotBlocked,'BUDGET_EXHAUSTED'):
            execute(self.prepare(),root,dry_run=False)

    def test_provider_model_mismatch(self):
        p=self.prepare()
        _,dry=execute(p,self.root/'runs')
        fake=self.fake(); fake.model='other'
        _,result=execute(p,self.root/'runs',generator=fake,dry_run=False,reviewed_delta=dry['delta_sha256'])
        self.assertEqual(result['reason'],'PROVIDER_MODEL_MISMATCH')
        self.assertEqual(fake.calls,0)

    def test_review_cannot_omit_findings(self):
        out,_=self.pair()
        review=self.review(out)
        review['images'][0]['observations'].pop()
        with self.assertRaisesRegex(PilotBlocked,'INCOMPLETE_REVIEW'):
            evaluate(out,review)

    def test_review_image_tampering(self):
        out,_=self.pair()
        review=self.review(out)
        review['images'][0]['sha256']='0'*64
        with self.assertRaisesRegex(PilotBlocked,'REVIEW_IMAGE_MISMATCH'):
            evaluate(out,review)

    def test_request_replay_mismatch(self):
        self.data['request']['scene']['entities'][0]['label']='a different building'
        self.freeze()
        self.blocked('REQUEST_SAR2_REPLAY_MISMATCH')

    def test_preconditions_fail_closed(self):
        with patch('visual_scene_graph.pilot.harness.check_preconditions',side_effect=PilotBlocked('STALE_PRECONDITIONS')):
            self.blocked('STALE_PRECONDITIONS')

    def test_missing_source(self):
        (self.root/'source').unlink()
        self.blocked('MISSING_ARTIFACT:source')

    def test_source_hash_mismatch(self):
        (self.root/'source').write_bytes(b'changed')
        self.blocked('ARTIFACT_HASH_MISMATCH:source')

    def test_source_binding_mismatch(self):
        self.manifest['source_binding']['source_identity']='OTHER_SOURCE'
        self.authorize()
        self.blocked('SOURCE_BINDING_MISMATCH')

    def test_empty_required_coverage(self):
        from visual_scene_graph.generation_comparator import compare_generation_contract
        p=self.prepare()
        comparison=deepcopy(p['comparison'])
        comparison['coverage']['PR0']={'required':0,'preserved':0,'ratio':1.0}
        with patch('visual_scene_graph.pilot.harness.compare_generation_contract', return_value=comparison):
            self.blocked('EMPTY_OR_INCOMPLETE_COVERAGE')

    def test_rubric_cannot_downgrade_critical_priority(self):
        self.manifest['rubric'][0]['priority']='OPTIONAL'
        self.authorize()
        self.blocked('RUBRIC_PRIORITY_MISMATCH')

    def test_review_cannot_replace_output_and_hash(self):
        out,_=self.pair()
        review=self.review(out)
        item=review['images'][0]
        changed=b'replaced'
        (out/item['path']).write_bytes(changed)
        item['sha256']=sha(changed)
        with self.assertRaisesRegex(PilotBlocked,'REVIEW_IMAGE_MISMATCH'):
            evaluate(out,review)

    def test_review_cannot_swap_branch_map(self):
        out,_=self.pair()
        review=self.review(out)
        path=out/'private_branch_map.json'
        mapping=json.loads(path.read_text())
        path.write_text(json.dumps({k:'B' if v=='A' else 'A' for k,v in mapping.items()}))
        with self.assertRaisesRegex(PilotBlocked,'BRANCH_MAP_CHANGED'):
            evaluate(out,review)

    def test_normal_route_unchanged(self):
        from integration.streetcraft_orchestrator import orchestrate
        self.prepare()
        self.assertEqual(orchestrate(self.base['request'],archive_retriever=retriever),self.base['runtime'])


if __name__=='__main__':
    unittest.main()
