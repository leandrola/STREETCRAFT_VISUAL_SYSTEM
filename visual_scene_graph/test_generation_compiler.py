"""VSG-2A preservation, provenance and runtime-isolation regressions."""
from copy import deepcopy
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from visual_scene_graph.generation_compiler import (
    compile_generation_contract, validate_generation_contract, canonical_bytes,
    digest, normalize, seal, resolve_ref,
)
from visual_scene_graph.generation_comparator import compare_generation_contract, render_comparison
from visual_scene_graph.generation_cases import base_inputs, run_generation_cases, trace_inputs, orchestrate, retriever
from visual_scene_graph.causal_trace import build_causal_trace


class GenerationCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = base_inputs()
        cls.report = run_generation_cases()

    def compile(self, graph=None, context=None, **kw):
        return compile_generation_contract(graph if graph is not None else self.base['expected_graph'],
            sar2=self.base['sar2'], generation_context=context if context is not None else self.base['generation_context'], **kw)

    def compare(self, contract, graph=None, cgc=None, **kw):
        return compare_generation_contract(cgc if cgc is not None else self.base['stable_cgc'], contract,
            sar2=self.base['sar2'], expected_graph=self.base['expected_graph'],
            candidate_graph=graph if graph is not None else self.base['expected_graph'],
            generation_context=self.base['generation_context'], **kw)

    def test_controlled_corpus(self):
        self.assertGreaterEqual(self.report['cases'], 16)
        for row in self.report['results']:
            with self.subTest(row['case_id']):
                self.assertEqual(row['status'], 'PASS', row['checks'])

    def test_healthy_complete_coverage(self):
        r = self.compare(self.compile())
        self.assertEqual(r['status'], 'PASS', r['issues'])
        for p in ('P0', 'PR0', 'PR1', 'LOCK'):
            self.assertGreater(r['coverage'][p]['required'], 0)
            self.assertEqual(r['coverage'][p]['ratio'], 1.0)
        self.assertEqual(r['unresolved_required_mappings'], 0)
        self.assertEqual(sum(v for k, v in r['counts'].items() if k != 'equivalent'), 0)

    def test_schema_and_generator_schema_rejection(self):
        import jsonschema
        contract = self.compile()
        for name in ('vsg-generation-contract.schema.json', 'vsg-generation-comparison.schema.json'):
            schema = json.loads((ROOT/'schemas'/name).read_text())
            jsonschema.Draft202012Validator.check_schema(schema)
            jsonschema.validate(contract if 'contract' in name else self.compare(contract), schema)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(contract, json.loads((ROOT/'schemas/compact-generation-contract.schema.json').read_text()))

    def test_canonical_bytes_and_digest(self):
        a = self.compile(); b = self.compile()
        self.assertEqual(canonical_bytes(a), canonical_bytes(b))
        self.assertEqual(a['contract_sha256'], digest({k:v for k,v in a.items() if k!='contract_sha256'}))
        r = self.compare(a)
        self.assertEqual(r['report_sha256'], digest({k:v for k,v in r.items() if k!='report_sha256'}))
        self.assertEqual(r, self.compare(a))

    def test_shuffled_equivalent_sources(self):
        expected = self.compile()
        for seed in range(10):
            rng = random.Random(seed); graph = deepcopy(self.base['expected_graph']); sar2 = deepcopy(self.base['sar2'])
            for key in ('nodes', 'edges', 'reference_observations', 'functional_subgraphs'): rng.shuffle(graph[key])
            rng.shuffle(graph['graph_locks']['items'])
            for lock in graph['graph_locks']['items']:
                if 'protected_topology' in lock['expected']: rng.shuffle(lock['expected']['protected_topology'])
            for key in ('entities', 'relationships', 'action_plan', 'identity_anchors'): rng.shuffle(sar2[key])
            actual = compile_generation_contract(graph, sar2=sar2, generation_context=self.base['generation_context'])
            self.assertEqual(canonical_bytes(expected), canonical_bytes(actual))

    def test_property_coordinate_order_is_meaningful(self):
        g = deepcopy(self.base['expected_graph']); g['nodes'][0].setdefault('properties', {})['polygon'] = [[0, 0], [1, 0], [0, 1]]
        a = self.compile(g); g['nodes'][0]['properties']['polygon'].reverse()
        self.assertNotEqual(a['contract_sha256'], self.compile(g)['contract_sha256'])

    def test_duplicate_ids_fail_closed(self):
        for collection in ('nodes', 'edges'):
            g = deepcopy(self.base['expected_graph']); g[collection].append(deepcopy(g[collection][0]))
            with self.assertRaisesRegex(ValueError, 'AMBIGUOUS_ID'): self.compile(g)
        g = deepcopy(self.base['expected_graph']); g['graph_locks']['items'].append(deepcopy(g['graph_locks']['items'][0]))
        with self.assertRaisesRegex(ValueError, 'AMBIGUOUS_ID'): self.compile(g)

    def test_missing_explicit_policy_is_not_defaulted(self):
        c = deepcopy(self.base['generation_context']); del c['policies']['camera']
        with self.assertRaisesRegex(ValueError, 'MISSING_REQUIRED_POLICY'): self.compile(context=c)

    def test_unknown_policy_fails_closed(self):
        c = deepcopy(self.base['generation_context']); c['policies']['magic_default'] = True
        with self.assertRaisesRegex(ValueError, 'UNSUPPORTED_POLICY'): self.compile(context=c)
        cgc = deepcopy(self.base['stable_cgc']); cgc['magic_default'] = True
        self.assertIn('UNSUPPORTED_CGC_FIELD:magic_default', self.compare(self.compile(), cgc=cgc)['issues'])
        cgc = deepcopy(self.base['stable_cgc']); cgc['scene_intelligence']['extra_rule'] = True
        self.assertIn('UNSUPPORTED_CGC_SCENE_FIELD:extra_rule', self.compare(self.compile(), cgc=cgc)['issues'])
        del cgc['camera']
        self.assertEqual(self.compare(self.compile(), cgc=cgc)['status'], 'FAIL')

    def test_exact_text_is_not_normalized(self):
        graph = deepcopy(self.base['expected_graph'])
        next(n for n in graph['nodes'] if n['id'] == 'sign_01')['properties']['text'] = 'KENNY’S'
        report = self.compare(self.compile(graph), graph)
        self.assertEqual(next(r['classification'] for r in report['results'] if r['constraint_id']=='node:sign_01'), 'contradiction')

    def test_required_directive_missing_in_stable_cgc_fails(self):
        cgc = deepcopy(self.base['stable_cgc']); cgc['preserve'] = []
        r = self.compare(self.compile(), cgc=cgc)
        self.assertEqual(r['status'], 'FAIL')
        self.assertTrue(any('CGC_DIRECTIVE_MISSING:' in i for i in r['issues']))

    def test_unresolved_source_relation_fails(self):
        b = deepcopy(self.base); b['expected_graph']['edges'] = []
        r = compare_generation_contract(b['stable_cgc'], self.compile(), sar2=b['sar2'],
            expected_graph=b['expected_graph'], candidate_graph=self.base['expected_graph'], generation_context=b['generation_context'])
        self.assertEqual(r['status'], 'FAIL')
        self.assertTrue(any('UNRESOLVED_REQUIRED_RELATIONSHIP:' in i for i in r['issues']))

    def test_cardinality_reduction_and_expansion(self):
        for key, value in (('min', 0), ('max', 2)):
            c = self.compile(); n = next(c for c in c['constraints'] if c['id']=='node:sign_01')
            n['value']['cardinality'][key] = value
            r = self.compare(seal(c))
            self.assertEqual(next(r['classification'] for r in r['results'] if r['constraint_id']=='node:sign_01'), 'weakening')
            self.assertEqual(r['status'], 'FAIL')

    def test_source_invariants_not_discarded(self):
        s = deepcopy(self.base['sar2']); s['entities'][0]['source_invariants'] = ['never change geometry', 'retain identity']
        c = compile_generation_contract(self.base['expected_graph'], sar2=s, generation_context=self.base['generation_context'])
        self.assertEqual(next(x for x in c['constraints'] if x['id']=='node:'+s['entities'][0]['entity_id'])['value']['source_attributes']['source_invariants'], ['never change geometry', 'retain identity'])

    def test_all_lineage_resolves(self):
        c = self.compile()
        for constraint in c['constraints']:
            for r in constraint['source_refs']:
                resolve_ref(r, vsg=self.base['expected_graph'], sar2=self.base['sar2'], generation_context=self.base['generation_context'])
        graph = deepcopy(self.base['expected_graph'])
        graph['nodes'][0]['evidence']['evidence_id'] = 'UNAUTHORIZED_SOURCE'
        self.assertEqual(self.compare(self.compile(graph), graph)['status'], 'FAIL')

    def test_trace_links_are_verified(self):
        a = trace_inputs(self.base); t = build_causal_trace(**a)
        c = self.compile(causal_trace=t, trace_artifacts=a)
        self.assertEqual(self.compare(c, causal_trace=t, trace_artifacts=a)['status'], 'PASS')
        ids = {e['event_id'] for e in t['events']}
        for constraint in c['constraints']:
            self.assertLessEqual(set(constraint['trace_event_ids']), ids)
        t['trace_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'INVALID_CAUSAL_TRACE'): self.compile(causal_trace=t, trace_artifacts=a)

    def test_missing_trace_artifacts_rejected(self):
        t = build_causal_trace(**trace_inputs(self.base))
        with self.assertRaisesRegex(ValueError, 'INVALID_CAUSAL_TRACE'): self.compile(causal_trace=t)

    def test_trace_bound_to_exact_candidate(self):
        a = trace_inputs(self.base); t = build_causal_trace(**a)
        g = deepcopy(self.base['expected_graph']); g['nodes'][0]['label'] = 'changed'
        with self.assertRaisesRegex(ValueError, 'CAUSAL_TRACE_SOURCE_MISMATCH'): self.compile(g, causal_trace=t, trace_artifacts=a)

    def test_contract_hash_and_forged_digest_rejected(self):
        c = self.compile(); c['contract_sha256'] = '0'*64
        self.assertEqual(self.compare(c)['status'], 'FAIL')
        c = self.compile(); c['constraints'] = c['constraints'][1:]; c = seal(c)
        self.assertIn('CONTRACT_REPLAY_MISMATCH', self.compare(c)['issues'])

    def test_non_governing_is_enforced(self):
        c = self.compile(); c['governs_generation'] = True
        self.assertEqual(self.compare(seal(c))['status'], 'FAIL')

    def test_no_input_aliases(self):
        before = deepcopy(self.base); c = self.compile(); self.compare(c)
        c['constraints'][0]['value'] = None
        self.assertEqual(self.base, before)

    def test_ready_and_blocked_generator_unchanged(self):
        for observer in (False, True):
            for blocked in (False, True):
                request = deepcopy(self.base['request'])
                if not observer: request.pop('vsg')
                if blocked: request['material_intensity_delta'] = 1
                before = orchestrate(request, archive_retriever=retriever)
                self.assertEqual(before['generation_ready'], not blocked)
                c = self.compile(); self.compare(c)
                # No production route reads this key; explicit shadow data cannot
                # replace the active cgc_final or change the readiness decision.
                request['vsg_generation_contract'] = c
                after = orchestrate(request, archive_retriever=retriever)
                self.assertEqual(before, after)
                self.assertNotIn('vsg_generation_contract', after)

    def test_persisted_stable_cgc_snapshots(self):
        from visual_scene_graph.generation_cases import stored_cgc_snapshots
        rows = stored_cgc_snapshots()
        checked = [r for r in rows if r['status'] != 'UNAVAILABLE']
        self.assertEqual(len(checked), 5)
        self.assertEqual(sum(r['status'] == 'UNAVAILABLE' for r in rows), 3)
        for r in checked:
            self.assertEqual(r['status'], 'PASS', (r['case_id'], r['comparison']['issues']))

    def test_readable_summary(self):
        text = render_comparison(self.compare(self.compile()))
        self.assertIn('PASS', text); self.assertIn('governs_generation=false', text)
        row = self.report['results'][1]
        self.assertIn('omission: node:sign_01', render_comparison(row['comparison']))


if __name__ == '__main__':
    unittest.main()
