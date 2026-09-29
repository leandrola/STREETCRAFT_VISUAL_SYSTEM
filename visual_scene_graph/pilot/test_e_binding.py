"""E mutation controls over frozen source bytes; never visual or provider evidence."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from integration.streetcraft_orchestrator import orchestrate
from visual_scene_graph.generation_compiler import compile_generation_contract, digest, seal
from visual_scene_graph.vsg_observer import build_visual_scene_graph
from visual_scene_graph.pilot.bind_e import FIXTURE, check_occlusion, empty_retriever, reconstruct, verify_d_preserved
from visual_scene_graph.pilot import bind_d
from visual_scene_graph.pilot.fixture_replay import verify_snapshots
from visual_scene_graph.pilot.harness import ROOT, ARTIFACTS, PilotBlocked, execute, prepare, sha
from visual_scene_graph.pilot.review_dry_run import review


class EBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = json.loads((FIXTURE/'manifest.json').read_text())
        self.data = {k: json.loads((ROOT/r['path']).read_text()) for k, r in self.manifest['artifacts'].items() if k != 'source'}
        self.source = (ROOT/self.manifest['artifacts']['source']['path']).read_bytes()
        # Test admission is local to temporary mutations. Actual preconditions are
        # exercised by run_validation after this suite, avoiding circular evidence.
        gate = patch('visual_scene_graph.pilot.harness.check_preconditions')
        gate.start()
        self.addCleanup(gate.stop)
        self.provider = Mock()
        self.addCleanup(self.provider.generate.assert_not_called)
        self.freeze()

    def freeze(self):
        for k in ARTIFACTS:
            raw = self.source if k == 'source' else json.dumps(self.data[k]).encode()
            (self.root/k).write_bytes(raw)
            self.manifest['artifacts'][k].update(path=k, sha256=sha(raw))
        self.allow = {'version':'1.0.0', 'fixtures':{'R2B-191-E':{'status':'ADMITTED', 'manifest_sha256':digest(self.manifest)}}}

    def prepare(self):
        return prepare(self.manifest, self.allow, self.root)

    def recompile(self):
        self.data['contract'] = compile_generation_contract(self.data['candidate_graph'],
            sar2=self.data['sar2'], generation_context=self.data['generation_context'])
        self.freeze()

    def blocked(self, reason='COMPARISON_FAILED'):
        with self.assertRaisesRegex(PilotBlocked, reason):
            prepared = self.prepare()
            execute(prepared, self.root/'runs', generator=self.provider, dry_run=False)

    def node(self, ident):
        return next(n for n in self.data['candidate_graph']['nodes'] if n['id'] == ident)

    def test_healthy_unknown_no_evidence_and_real_replay(self):
        manifest, comparison = verify_snapshots(FIXTURE, reconstruct)
        self.assertEqual(comparison['status'], 'PASS')
        self.assertEqual(comparison['coverage']['PR1']['required'], 0)
        self.assertNotIn('PR1', manifest['required_priorities'])
        unknown = self.node('hidden_01')
        self.assertFalse(unknown['observed'])
        self.assertEqual(unknown['epistemic_class'], 'UNKNOWN')
        self.assertEqual(self.data['rr2']['queries'], 0)
        self.assertEqual(self.data['rr2']['generation_projection'], [])
        self.assertEqual(self.data['rr2']['need_results'], {'SAR2-hidden_01':'LOCKED_UNKNOWN'})
        out, report = execute(self.prepare(), self.root/'runs', generator=self.provider)
        self.assertEqual(report['reason'], 'DRY_RUN_NO_IMAGES')
        self.assertEqual(review(out)['status'], 'PASS')
        rubric = {r['constraint_id'] for r in manifest['rubric']}
        self.assertTrue({'unknown:hidden_01', 'directive:infer', 'policy:reference_reasoning'} <= rubric)

    def test_unknown_does_not_depend_on_node_type(self):
        request = deepcopy(self.data['request'])
        hidden = next(e for e in request['scene']['entities'] if e['entity_id'] == 'hidden_01')
        hidden['kind'] = 'SURFACE'  # ordinary, still unknown, no specific hidden object
        runtime = orchestrate(request, archive_retriever=empty_retriever)
        graph = build_visual_scene_graph(runtime['sar2'], reference_reasoning=runtime['reference_reasoning'], reference_needs=runtime['reference_needs'])
        self.assertEqual(next(n for n in graph['nodes'] if n['id']=='hidden_01')['type'], 'unclassified')
        check_occlusion(runtime, graph)

    def test_unknown_cannot_become_exact_observation(self):
        self.node('hidden_01').update(observed=True, epistemic_class='OBSERVED')
        self.node('hidden_01')['properties']['exact_content'] = 'specific hidden vehicle'
        self.recompile()
        self.blocked()

    def test_occluder_removed(self):
        self.data['candidate_graph']['nodes'] = [n for n in self.data['candidate_graph']['nodes'] if n['id'] != 'occluder_01']
        self.recompile()
        self.blocked()

    def test_occluder_displaced(self):
        self.node('occluder_01')['evidence']['region'] = [0, 0, .2, .2]
        self.node('occluder_01')['properties']['silhouette_polygon'] = [[0,0],[.2,0],[.2,.2],[0,.2]]
        self.recompile()
        self.blocked()

    def test_occlusion_lock_absent(self):
        ledger = self.data['candidate_graph']['graph_locks']
        ledger['items'] = [l for l in ledger['items'] if l['type'] != 'OCCLUSION_LOCK']
        self.recompile()
        self.blocked()

    def test_occlusion_lock_detached(self):
        c = next(c for c in self.data['contract']['constraints'] if c['id'] == 'edge:rel_foreground_occludes_unknown')
        c['lock_ids'] = []
        self.data['contract'] = seal(self.data['contract'])
        self.freeze()
        self.blocked()

    def test_occlusion_wrong_endpoint(self):
        self.data['candidate_graph']['edges'][0]['to'] = 'left_facades_01'
        self.recompile()
        self.blocked()

    def test_exact_inference_unauthorized(self):
        self.data['generation_context']['directives']['infer'] = ['hidden_01: exact hidden facade with windows']
        self.recompile()
        self.blocked()

    def test_reference_fill_blocked_in_contract_and_runtime(self):
        feature = {'domain':'ARCHITECTURE', 'feature_type':'geometry', 'target_entity_id':'hidden_01', 'value':'specific hidden facade'}
        self.data['generation_context']['policies']['reference_features'] = [feature]
        self.recompile()
        self.blocked()
        request = deepcopy(self.data['request'])
        request['reference_features'] = [feature]
        runtime = orchestrate(request, archive_retriever=empty_retriever)
        self.assertNotEqual(runtime['status'], 'GENERATION_READY')
        self.assertNotEqual(runtime['pre_generation_gate']['status'], 'PASS')
        self.assertEqual(runtime['reference_reasoning']['queries'], 0)

    def test_lock_coverage_zero_is_not_pass(self):
        report = deepcopy(self.prepare()['comparison'])
        report['coverage']['LOCK'] = {'required':0, 'preserved':0, 'ratio':1.0}
        with patch('visual_scene_graph.pilot.harness.compare_generation_contract', return_value=report):
            self.blocked('EMPTY_OR_INCOMPLETE_COVERAGE:LOCK')

    def test_source_tamper(self):
        (self.root/'source').write_bytes(b'not the source')
        self.blocked('ARTIFACT_HASH_MISMATCH:source')

    def test_manifest_tamper(self):
        self.manifest['generation']['model'] = 'CHANGED'
        self.blocked('FIXTURE_NOT_AUTHORIZED')

    def test_preflight_blocked(self):
        self.data['runtime']['pre_generation_gate']['status'] = 'BLOCK_GENERATION'
        self.data['cgc_final']['pre_generation_gate']['status'] = 'BLOCK_GENERATION'
        self.data['runtime']['cgc_final'] = deepcopy(self.data['cgc_final'])
        self.freeze()
        self.blocked('BLOCKED_PREFLIGHT')

    def test_initial_creation_never_overwrites(self):
        before = {p.name:sha(p.read_bytes()) for p in FIXTURE.iterdir() if p.is_file()}
        result = subprocess.run([sys.executable, '-m', 'visual_scene_graph.pilot.bind_e', '--freeze'], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('E_ALREADY_FROZEN', result.stderr)
        self.assertEqual(before, {p.name:sha(p.read_bytes()) for p in FIXTURE.iterdir() if p.is_file()})

    def test_d_preserved_and_replayed_with_same_delta(self):
        baseline = verify_d_preserved()
        manifest, comparison = verify_snapshots(bind_d.FIXTURE, bind_d.reconstruct)
        self.assertEqual(digest(manifest), baseline['manifest_sha256'])
        registry = json.loads((ROOT/'visual_scene_graph/pilot/allowlist.json').read_text())
        prepared = prepare(manifest, registry)
        self.assertEqual(comparison['status'], 'PASS')
        self.assertEqual(digest({'manifest':manifest, 'payloads':prepared['payloads']}), baseline['delta_sha256'])


if __name__ == '__main__':
    unittest.main()
