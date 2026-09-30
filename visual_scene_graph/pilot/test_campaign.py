"""G0 controls using synthetic pairs/reviews only; no real provider or visual merit."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from visual_scene_graph.pilot import campaign
from visual_scene_graph.pilot.evaluation import close_campaign, evaluate
from visual_scene_graph.pilot.harness import CommandGenerator, execute, PilotBlocked
from visual_scene_graph.generation_compiler import digest
from visual_scene_graph.pilot import test_pilot


class CampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_pilot.ControlTests.setUpClass()

    def setUp(self):
        self.control = test_pilot.ControlTests('test_healthy_and_exact_delta')
        self.control.setUp()
        self.addCleanup(self.control.doCleanups)
        self.root = self.control.root
        self.policy = campaign.load_policy()
        self.policy['fixtures'] = {'SYNTHETIC-' + k: v for k, v in self.policy['fixtures'].items()}
        for key in ('global_selection', 'partial_selection'):
            self.policy[key] = ['SYNTHETIC-' + k for k in self.policy[key]]
        self.selected = self.policy['global_selection']
        self.registry = {'version': '1.0.0', 'fixtures': {}}
        self.paths = []
        for ident in self.selected:
            self.control.manifest['fixture_id'] = ident
            manifest = self.control.manifest
            entry = {'status': 'ADMITTED', 'manifest_sha256': digest(manifest)}
            self.control.allow = {'version': '1.0.0', 'fixtures': {ident: entry}}
            self.registry['fixtures'][ident] = entry
            self.policy['fixtures'][ident].update(entry)
            self.policy['fixtures'][ident]['phenomena'] = {
                k: ['identity'] for k in self.policy['fixtures'][ident]['phenomena']}
            out, report = self.control.pair()
            review = self.control.review(out)
            a_path = next(r['path'] for r in report['images'] if r['branch'] == 'A')
            row = next(r for image in review['images'] if image['path'] == a_path
                       for r in image['observations'] if r['constraint_id'] == 'identity')
            row.update(preserved='NO', severity='S1')
            evaluate(out, review)
            self.paths.append(out)
        self.policy_path = self.root/'policy.json'
        self.registry_path = self.root/'registry.json'
        self.write_policy()
        self.registry_path.write_text(json.dumps(self.registry))
        for name, value in [('ROOT', self.root), ('POLICY_PATH', self.policy_path),
                            ('REGISTRY_PATH', self.registry_path)]:
            mocked = patch.object(campaign, name, value)
            mocked.start()
            self.addCleanup(mocked.stop)

    def write_policy(self):
        self.policy_path.write_text(json.dumps(self.policy))

    def close(self, paths=None, selected=None, regression=True):
        return close_campaign(self.paths if paths is None else paths,
                              self.selected if selected is None else selected, regression)

    def blocked(self, reason, **kwargs):
        result = self.close(**kwargs)
        self.assertNotEqual(result['status'], 'PASS')
        self.assertIn(reason, ' '.join(result['reasons']))
        self.assertFalse(result['production_authorized'])

    def mutate(self, filename, change, index=0):
        path = self.paths[index]/filename
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def reevaluate(self, change):
        out = self.paths[0]
        review = json.loads((out/'review.submitted.json').read_text())
        change(review)
        (out/'review.submitted.json').unlink()
        (out/'evaluation.json').unlink()
        return evaluate(out, review)

    def test_four_synthetic_eligible_pairs_can_pass_logic_only(self):
        before = {p: p.read_bytes() for d in self.paths for p in d.rglob('*') if p.is_file()}
        result = self.close()
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['missing_phenomena'], [])
        self.assertEqual(result['generation_attempts'], 8)
        self.assertFalse(result['production_authorized'])
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_four_distinct_without_reference_isolation(self):
        self.policy['fixtures']['SYNTHETIC-R2B-191-C']['phenomena'] = {'cg_f_camera': ['identity']}
        self.write_policy()
        self.blocked('MISSING_REQUIRED_PHENOMENA')

    def test_blocked_c(self):
        self.policy['fixtures']['SYNTHETIC-R2B-191-C']['status'] = 'BLOCKED'
        self.write_policy()
        self.blocked('FIXTURE_NOT_ADMITTED_FOR_CAMPAIGN')

    def test_three_favorable_pairs_are_partial_only(self):
        # Remove the fourth synthetic attempt from this temporary campaign only.
        import shutil
        shutil.rmtree(self.paths[-1])
        result = self.close(paths=self.paths[:3], selected=self.selected[:3])
        self.assertEqual(result['status'], 'INCONCLUSIVE')
        self.assertEqual(result['scope'], 'PARTIAL_D_E_KENNY')
        self.assertEqual(result['missing_phenomena'], ['reference_isolation'])

    def test_f_does_not_automatically_extend_selection(self):
        self.blocked('SELECTION_OUTSIDE_CAMPAIGN_SCOPE', selected=self.selected+['SYNTHETIC-R2B-191-F'])

    def test_empty_phenomenon_denominator(self):
        self.policy['fixtures']['SYNTHETIC-R2B-191-C']['phenomena']['reference_isolation'] = []
        self.write_policy()
        self.blocked('EMPTY_PHENOMENON_COVERAGE')

    def test_unknown_rubric_criterion_is_not_coverage(self):
        self.policy['fixtures']['SYNTHETIC-R2B-191-C']['phenomena']['reference_isolation'] = ['invented']
        self.write_policy()
        self.blocked('EMPTY_OR_UNBOUND_PHENOMENON')

    def test_zero_priority_denominator(self):
        self.mutate('comparison.json', lambda c: c['coverage']['LOCK'].update(required=0, preserved=0))
        self.blocked('PERSISTED_PREPARATION_CHANGED')

    def test_missing_review(self):
        (self.paths[0]/'review.submitted.json').unlink()
        self.blocked('INVALID_CAMPAIGN_EVIDENCE')

    def test_forged_cached_evaluation(self):
        self.mutate('evaluation.json', lambda e: e.update(improvements=['invented']))
        self.blocked('EVALUATION_REPLAY_MISMATCH')

    def test_s3_fails_and_stop_blocks(self):
        self.reevaluate(lambda r: r['images'][0]['observations'][0].update(preserved='NO', severity='S3'))
        result = self.close()
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('CAMPAIGN_STOPPED', result['reasons'])

    def test_unknown_is_inconclusive(self):
        self.reevaluate(lambda r: r['images'][0]['observations'][0].update(preserved='UNKNOWN', severity='S0'))
        self.blocked('UNRESOLVED_VISUAL_RESULT_OR_SEED')

    def test_required_phenomenon_loss_in_both_branches_is_not_coverage(self):
        def missing_identity(review):
            for image in review['images']:
                next(r for r in image['observations'] if r['constraint_id'] == 'identity').update(
                    preserved='NO', severity='S1')
        self.reevaluate(missing_identity)
        self.blocked('MISSING_REQUIRED_PHENOMENA')

    def test_uncontrolled_seed_is_not_pass(self):
        # Rebind this synthetic fixture and all corresponding input receipts to null.
        out = self.paths[0]
        manifest = json.loads((out/'manifest.json').read_text())
        manifest['generation']['seed'] = None
        (out/'manifest.json').write_text(json.dumps(manifest))
        ident = manifest['fixture_id']
        self.registry['fixtures'][ident]['manifest_sha256'] = digest(manifest)
        self.registry_path.write_text(json.dumps(self.registry))
        self.policy['fixtures'][ident]['manifest_sha256'] = digest(manifest)
        self.write_policy()
        inputs = {}
        for branch in ('A', 'B'):
            p = out/(branch+'.input.json')
            value = json.loads(p.read_text()); value['seed'] = None
            p.write_text(json.dumps(value)); inputs[branch] = digest(value)
            self.mutate(branch+'.attempt.json', lambda r, b=branch: r.update(input_sha256=inputs[b]))
            self.mutate(branch+'.output.json', lambda r, b=branch: (r.update(input_sha256=inputs[b]), r['metadata'].update(seed=None)))
        def update_report(report):
            report.update(seed_controlled=False, delta_sha256=digest({
                'manifest': manifest, 'payloads': json.loads((out/'payloads.json').read_text())}))
            for row in report['images']:
                row.update(input_sha256=inputs[row['branch']]); row['metadata']['seed'] = None
        self.mutate('report.json', update_report)
        self.reevaluate(lambda r: None)
        self.blocked('UNRESOLVED_VISUAL_RESULT_OR_SEED')

    def test_stop_alone_prevents_pass(self):
        (self.paths[0].parent/'STOP').write_text('Operator STOP')
        self.blocked('CAMPAIGN_STOPPED')

    def test_repeated_fixture(self):
        self.blocked('DUPLICATE_FIXTURE_OR_RUN', paths=self.paths[:3]+[self.paths[0]])

    def test_ninth_attempt_even_when_omitted(self):
        extra = self.paths[0].parent/'interrupted'
        extra.mkdir(); (extra/'A.attempt.json').write_text('{}')
        self.blocked('GENERATION_BUDGET_EXHAUSTED')
        with self.assertRaisesRegex(PilotBlocked, 'BUDGET_EXHAUSTED'):
            execute(self.control.prepare(), extra.parent, dry_run=False)

    def test_missing_attempt(self):
        (self.paths[0]/'A.attempt.json').unlink()
        self.blocked('INVALID_PAIR_ATTEMPTS')

    def test_receipt_tampering(self):
        self.mutate('A.output.json', lambda r: r['metadata'].update(model='other'))
        self.blocked('RECEIPT_MISMATCH')

    def test_registry_admission_required(self):
        self.registry['fixtures'][self.selected[0]]['status'] = 'PENDING_EVIDENCE'
        self.registry_path.write_text(json.dumps(self.registry))
        self.blocked('FIXTURE_NOT_AUTHORIZED')

    def test_regression_required(self):
        self.blocked('REGRESSION_NOT_PASS', regression=False)

    def test_policy_cannot_drop_critical_phenomenon(self):
        self.policy['required_phenomena'].remove('reference_isolation')
        self.write_policy()
        self.blocked('INVALID_CAMPAIGN_EVIDENCE')

    def test_checked_in_policy_remains_blocked(self):
        original = Path(__file__).with_name('campaign_policy.json')
        with patch.object(campaign, 'POLICY_PATH', original):
            policy = campaign.load_policy()
            self.assertEqual(policy['fixtures']['R2B-191-C']['status'], 'BLOCKED')
            self.assertEqual(policy['fixtures']['R2B-191-F']['status'], 'CONDITIONAL')
            self.blocked('FIXTURE_NOT_ADMITTED_FOR_CAMPAIGN')


class CommandBridgeTests(unittest.TestCase):
    def test_json_stdio_fake_bridge_contract_only(self):
        # Echoes synthetic bytes; never connects to a provider or creates pilot evidence.
        source = """import json,sys
r=json.load(sys.stdin)
assert set(r)=={'source_base64','payload','provider','model','seed','parameters'}
assert set(r['payload'])=={'common','relations_and_locks'}
print(json.dumps({'image_base64':r['source_base64'],'metadata':{
 **{k:r[k] for k in ('provider','model','seed','parameters')},'generation_id':'FAKE-ONLY'}}))
"""
        bridge = CommandGenerator([sys.executable, '-c', source], 'fake', 'contract-test')
        for payload in ({'common': {}, 'relations_and_locks': ''},
                        {'common': {}, 'relations_and_locks': []}):
            request = {'source_base64': 'ZmFrZQ==', 'payload': payload,
                       'provider': 'fake', 'model': 'contract-test', 'seed': None,
                       'parameters': {'size': '4x4', 'quality': 'standard', 'output_format': 'png'}}
            raw, metadata = bridge.generate(request)
            self.assertEqual(raw, b'fake')
            self.assertEqual(metadata['parameters'], request['parameters'])
            self.assertIsNone(metadata['seed'])
            self.assertEqual(metadata['generation_id'], 'FAKE-ONLY')

    def test_invalid_bridge_response_is_rejected(self):
        for response in ({'image_base64': 'AA=='},
                         {'image_base64': 'AA==', 'metadata': {'provider': 'other', 'model': 'm', 'generation_id': 'x'}}):
            bridge = CommandGenerator([sys.executable, '-c', 'print('+repr(json.dumps(response))+')'], 'fake', 'm')
            with self.assertRaises(ValueError):
                bridge.generate({})

    def test_bridge_must_report_seed_even_when_null_and_exact_parameters(self):
        request = {'provider': 'fake', 'model': 'm', 'seed': None,
                   'parameters': {'size': '4x4', 'quality': 'standard', 'output_format': 'png'}}
        for missing in ('seed', 'parameters'):
            metadata = {**request, 'generation_id': 'FAKE-ONLY'}
            del metadata[missing]
            response = {'image_base64': 'AA==', 'metadata': metadata}
            bridge = CommandGenerator([sys.executable, '-c', 'print('+repr(json.dumps(response))+')'], 'fake', 'm')
            with self.assertRaisesRegex(ValueError, 'PROVIDER_SETTINGS_MISMATCH'):
                bridge.generate(request)


if __name__ == '__main__':
    unittest.main()
