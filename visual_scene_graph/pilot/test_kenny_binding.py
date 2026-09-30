"""K1 mutation and bypass controls; temporary admission only, zero provider calls."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from visual_scene_graph.pilot import kenny_binding as k, bind_kenny
from visual_scene_graph.pilot.harness import ROOT, prepare, execute, sha
from visual_scene_graph.pilot.fixture_replay import verify_snapshots
from visual_scene_graph.pilot.review_dry_run import review
from visual_scene_graph.generation_compiler import digest


class KennyBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.manifest=json.loads((k.FIXTURE/'manifest.json').read_text())
        for rec in [*self.manifest['artifacts'].values(),*k.binding_records().values()]:
            target=self.root/rec['path']; target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((ROOT/rec['path']).read_bytes())
        self.registry={'version':'1.0.0','fixtures':{k.IDENT:{'status':'ADMITTED','manifest_sha256':digest(self.manifest)}}}
        # Avoid circular test evidence: production preconditions checked by validation.
        gate=patch('visual_scene_graph.pilot.harness.check_preconditions')
        gate.start(); self.addCleanup(gate.stop)
        self.provider=Mock();self.addCleanup(self.provider.generate.assert_not_called)

    def prepare(self):
        return prepare(self.manifest,self.registry,self.root)

    def mutate_artifact(self,name,change):
        path=self.root/self.manifest['artifacts'][name]['path']
        value=json.loads(path.read_text());change(value)
        path.write_text(json.dumps(value,ensure_ascii=False))
        self.manifest['artifacts'][name]['sha256']=sha(path.read_bytes())
        self.registry['fixtures'][self.manifest['fixture_id']]['manifest_sha256']=digest(self.manifest)

    def blocked(self,pattern='K1_'):
        with self.assertRaisesRegex(ValueError,pattern):self.prepare()

    def test_real_replay_and_persisted_design_bytes(self):
        m,c=bind_kenny.verify()
        self.assertEqual(c['status'],'PASS')
        p=self.prepare()
        out,report=execute(p,self.root/'runs',generator=self.provider)
        result=review(out)
        self.assertEqual(result['source_design_review']['status'],'PASS')
        self.assertEqual(report['reason'],'DRY_RUN_NO_IMAGES')
        for name,raw in p['sidecars'].items():self.assertEqual((out/'sidecars'/name).read_bytes(),raw)
        for side in ('A','B'):
            self.assertEqual(p['payloads'][side]['common']['stable_cgc']['infer'],sorted(json.loads(p['blobs']['request'])['infer']))
        self.assertFalse(result['source_design_review']['rooftop_graph_locks']['exercised'])

    def test_missing_each_sidecar(self):
        for name,(path,_) in k.RECORDS.items():
            with self.subTest(name=name):
                p=self.root/path;raw=p.read_bytes();p.unlink()
                self.blocked('K1_MISSING_SIDECAR');p.write_bytes(raw)

    def test_altered_sidecar_even_with_rehashed_binding(self):
        path=self.root/k.RECORDS['design.json'][0]
        d=json.loads(path.read_text());d['nodes'][0]['observed']=True
        path.write_text(json.dumps(d))
        self.mutate_artifact('request',lambda r:r['k1_binding']['design.json'].update(sha256=sha(path.read_bytes())))
        self.blocked('K1_BINDING_RECORDS_CHANGED')

    def test_design_observed_semantics(self):
        d=json.loads((k.FIXTURE/'design.json').read_text());d['nodes'][0].update(observed=True,epistemic_class='OBSERVED')
        with self.assertRaisesRegex(ValueError,'K1_DESIGN_OBSERVED'):k.verify_design(d)

    def test_fourth_component(self):
        d=json.loads((k.FIXTURE/'design.json').read_text());d['nodes'].append(dict(d['nodes'][0],id='kd_skylight'))
        with self.assertRaisesRegex(ValueError,'K1_DESIGN_COMPONENTS'):k.verify_design(d)

    def test_lost_component(self):
        d=json.loads((k.FIXTURE/'design.json').read_text());d['nodes'].pop()
        with self.assertRaisesRegex(ValueError,'K1_DESIGN_COMPONENTS'):k.verify_design(d)

    def test_wrong_relation_endpoint(self):
        d=json.loads((k.FIXTURE/'design.json').read_text());d['relationships'][1]['object']='ks_facade'
        with self.assertRaisesRegex(ValueError,'K1_DESIGN_RELATIONSHIPS'):k.verify_design(d)

    def test_missing_or_extra_relation(self):
        for extra in (False,True):
            d=json.loads((k.FIXTURE/'design.json').read_text())
            if extra:d['relationships'].append(dict(d['relationships'][0],id='KDR-05'))
            else:d['relationships'].pop()
            with self.assertRaisesRegex(ValueError,'K1_DESIGN_RELATIONSHIPS'):k.verify_design(d)

    def test_design_in_sar2(self):
        self.mutate_artifact('sar2',lambda r:r['entities'].append(dict(r['entities'][0],entity_id='kd_roof',observed=True)))
        self.blocked('K1_DESIGN_IN_SOURCE')

    def test_design_in_candidate_graph(self):
        self.mutate_artifact('candidate_graph',lambda r:r['nodes'].append(dict(r['nodes'][0],id='kd_roof',observed=True)))
        self.blocked('K1_SNAPSHOT_REPLAY:candidate_graph')

    def test_removed_infer(self):
        self.mutate_artifact('request',lambda r:r['infer'].pop())
        self.blocked('K1_REQUEST_AUTHORITY_OR_DIRECTIVES')

    def test_rewritten_forbid(self):
        self.mutate_artifact('request',lambda r:r['forbid'].__setitem__(0,'permit redesign'))
        self.blocked('K1_REQUEST_AUTHORITY_OR_DIRECTIVES')

    def test_cgc_directive_loss(self):
        self.mutate_artifact('cgc_final',lambda r:r['infer'].pop())
        self.blocked('K1_SNAPSHOT_REPLAY:cgc_final')

    def test_context_directive_loss(self):
        self.mutate_artifact('generation_context',lambda r:r['directives']['forbid'].pop())
        self.blocked('K1_SNAPSHOT_REPLAY:generation_context')

    def test_facade_anchor_changed_and_rehashed(self):
        def change(r):r['scene']['entities'][0]['region']=[0,0,1,1]
        self.mutate_artifact('request',change)
        self.blocked('K1_REQUEST_AUTHORITY_OR_DIRECTIVES')

    def test_source_modified_and_manifest_rehashed(self):
        rec=self.manifest['artifacts']['source'];p=self.root/rec['path']
        p.write_bytes(p.read_bytes()+b'changed source bytes')
        rec['sha256']=sha(p.read_bytes());self.registry['fixtures'][k.IDENT]['manifest_sha256']=digest(self.manifest)
        self.blocked('K1_SOURCE_HASH')

    def test_uncertainty_removed(self):
        self.mutate_artifact('request',lambda r:r['unknown'].clear())
        self.blocked('K1_REQUEST_AUTHORITY_OR_DIRECTIVES')

    def test_sale_strip_not_exact_sign_lock(self):
        p=self.prepare();g=json.loads(p['blobs']['expected_graph'])
        n=next(n for n in g['nodes'] if n['id']=='ks_sale_strip')
        self.assertFalse(n['locks']['semantic'])
        self.assertNotIn('text',n.get('properties',{}))
        self.assertEqual(json.loads(p['blobs']['cgc_final'])['text_render_plan']['tokens'][-1]['state'],'MASK_PARTIAL')

    def test_prepare_cannot_bypass_verifier(self):
        with patch.object(k,'verify_bundle',side_effect=ValueError('K1_SENTINEL')) as gate:
            self.blocked('K1_SENTINEL');gate.assert_called_once()

    def test_replay_cannot_bypass_verifier(self):
        # Mock reconstruction so the shared replay boundary must invoke the gate itself.
        snapshots={name:json.loads((ROOT/r['path']).read_text()) for name,r in self.manifest['artifacts'].items() if name not in {'request','source'}}
        with patch.object(k,'verify_bundle',side_effect=ValueError('K1_SENTINEL')) as gate:
            with self.assertRaisesRegex(ValueError,'K1_SENTINEL'):
                verify_snapshots(k.FIXTURE,lambda:(snapshots,{}))
            gate.assert_called_once()

    def test_execute_cannot_bypass_sidecar_gate(self):
        p=self.prepare();p['sidecars']={}
        with self.assertRaisesRegex(ValueError,'K1_SIDECAR_SET'):
            execute(p,self.root/'runs',generator=self.provider)
        self.assertFalse(list((self.root/'runs').glob('*/report.json')))

    def test_execute_directive_tamper(self):
        p=self.prepare();p['payloads']['A']['common']['stable_cgc']['infer']=[]
        with self.assertRaisesRegex(ValueError,'K1_EXECUTION_DIRECTIVE_BYPASS'):execute(p,self.root/'runs')

    def test_rename_fixture_does_not_bypass_gate(self):
        self.manifest['fixture_id']='UNRELATED'
        self.registry['fixtures']['UNRELATED']={'status':'ADMITTED','manifest_sha256':digest(self.manifest)}
        self.blocked('K1_IDENTITY_BYPASS')

    def test_persisted_review_never_falls_back_to_checkout(self):
        out,_=execute(self.prepare(),self.root/'runs')
        (out/'sidecars/design.json').unlink()
        with self.assertRaisesRegex(ValueError,'K1_MISSING_SIDECAR'):review(out)

    def test_persisted_sidecar_tamper(self):
        out,_=execute(self.prepare(),self.root/'runs')
        (out/'sidecars/k0.md').write_text('changed authority')
        with self.assertRaisesRegex(ValueError,'K1_SIDECAR_HASH'):review(out)

    def test_de_c_preserved(self):
        self.assertTrue(k.verify_preserved()['files'])


if __name__=='__main__':unittest.main()
