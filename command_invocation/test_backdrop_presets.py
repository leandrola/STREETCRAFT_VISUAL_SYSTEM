"""Behavioral contracts only; does not rate generated images or print samples."""
from copy import deepcopy
import itertools
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'command_invocation'))
sys.path.insert(0,str(ROOT/'integration'))
sys.path.insert(0,str(ROOT))
from resolve_commands import resolve
from backdrop_presets import build_backdrop_contract, contract_sha256, validate_backdrop_contract
from streetcraft_orchestrator import orchestrate

LONG={
 'BD01':'/sc-vp02 /sc-t02 /sc-cg-f /sc-rdr2-elevation /sc-bd01',
 'BD02':'/sc-vp02 /sc-t08 /sc-cg-f /sc-rdr2-elevation /sc-preserve /sc-bd02'}


def request(preset='BD01'):
    scene=json.loads((ROOT/'visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json').read_text())
    scene['entities'].append({'entity_id':'hidden_01','label':'hidden rear wall','kind':'OCCLUDED_REGION',
        'roles':['UNKNOWN_REGION'],'preservation_level':'P5-D','epistemic_class':'UNKNOWN',
        'observed':False,'confidence':'LOW','salience':{}})
    return {'command_text':'/sc-'+preset.lower(),'scene':scene}


class BackdropTests(unittest.TestCase):
    def test_short_long_equivalence(self):
        for p in LONG:
            short=resolve('/sc-'+p.lower());long=resolve(LONG[p])
            self.assertEqual(short['status'],'OK');self.assertEqual(short['config'],long['config'])
            self.assertEqual(short['config']['mode'],'T02' if p=='BD01' else 'T08')

    def test_order_independence(self):
        for p in LONG:
            expected=resolve(LONG[p])['config']
            for tokens in itertools.permutations(LONG[p].split()):
                self.assertEqual(resolve(' '.join(tokens))['config'],expected)

    def test_conflicts(self):
        for text in ['/sc-bd01 /sc-bd02','/sc-bd01 /sc-clean','/sc-bd02 /sc-t02',
                     '/sc-bd01 /sc-t08','/sc-bd02 /sc-auto','/sc-bd01 /sc-2b',
                     '/sc-bd01 /sc-fear','/sc-bd02 /sc-lock']:
            for tokens in (text.split(),list(reversed(text.split()))):
                self.assertEqual(resolve(' '.join(tokens))['status'],'ERROR',tokens)

    def test_selectors_and_aliases(self):
        self.assertEqual(resolve('/sc-vp02 /sc-t08 /sc-cg-f')['config']['mode'],'T08')
        self.assertEqual(resolve('/sc-vp02 /sc-core')['error'],'PROFILE_CONFLICT')
        self.assertEqual(resolve('/sc-elevation /sc-bd02')['config'],resolve('/sc-bd02')['config'])
        self.assertEqual(resolve('/sc-bd01 /sc-bd01')['config'],resolve('/sc-bd01')['config'])

    def test_preserve_modifier_restricts_bd01(self):
        r=request();r['command_text']+=' /sc-preserve';out=orchestrate(r)
        c=out['cgc_final']['backdrop_contract']
        self.assertEqual(c['scope']['recomposition'],'NO_MAJOR_RECOMPOSITION')
        self.assertIn('relocate major masses',c['forbidden_operations'])
        self.assertNotIn('reorganize unprotected masses',c['allowed_operations'])

    def test_contract_propagates_to_final_cgc(self):
        for p in LONG:
            out=orchestrate(request(p));c=out['cgc_final']['backdrop_contract']
            self.assertEqual(out['status'],'GENERATION_READY')
            self.assertEqual(c,out['cgc_draft']['backdrop_contract'])
            self.assertEqual(c['preset'],p);self.assertEqual(c['base_profile'],'VP02')
            self.assertEqual(c['framing']['aspect_ratio'],'16:9')
            self.assertEqual(c['print_target']['nominal_scale'],'1:64')
            self.assertEqual(c['visual_validation'],'PENDING')
            self.assertTrue(set(c['forbidden_operations'])<=set(out['cgc_final']['forbid']))

    def test_bd01_recomposition_and_bd02_layout(self):
        a=orchestrate(request())['cgc_final']['backdrop_contract']
        b=orchestrate(request('BD02'))['cgc_final']['backdrop_contract']
        self.assertEqual(a['scope']['recomposition'],'UNPROTECTED_REGIONS_ONLY')
        self.assertEqual(b['scope']['recomposition'],'NO_MAJOR_RECOMPOSITION')
        self.assertIn('REFERENCE_LAYOUT',b['internal_locks'])
        self.assertEqual(a['primary_priority'],'BACKDROP_USABILITY')
        self.assertEqual(b['primary_priority'],'STRUCTURAL_FIDELITY')

    def test_p0_pr0_pr1_and_unknowns_preserved(self):
        for p in LONG:
            out=orchestrate(request(p));c=out['cgc_final']['backdrop_contract'];s=out['sar2']
            self.assertIn('hidden_01',c['scope']['locked_unknown_ids'])
            for e in s['entities']:
                if e['preservation_level']=='P0':self.assertIn(e['entity_id'],c['scope']['protected_node_ids'])
            for r in s['relationships']:
                if r['protection'] in {'PR0','PR1'}:self.assertIn(r['relationship_id'],c['scope']['protected_relationship_ids'])
            self.assertIn('resolve_exact_unknown:hidden_01',out['cgc_final']['forbid'])
            self.assertEqual(out['reference_reasoning']['queries'],0)

    def test_wide_format_and_scale_options(self):
        r=request();r['backdrop']={'aspect_ratio':'20:10','target_scale':'1:87'}
        out=orchestrate(r);c=out['cgc_final']
        self.assertEqual(c['aspect_ratio'],'2:1')
        self.assertEqual(out['resolved_config']['aspect_ratio'],'2:1')
        self.assertEqual(c['cil']['resolved']['aspect_ratio'],'2:1')
        self.assertEqual(c['backdrop_contract']['print_target']['nominal_scale'],'1:87')

    def test_invalid_options_fail(self):
        for options in [{'aspect_ratio':'1:1'},{'aspect_ratio':'9:16'},{'aspect_ratio':'0:1'},
                        {'aspect_ratio':'wide'},{'target_scale':'64'},{'target_scale':'1:0'},
                        {'unlock_geometry':True},[]]:
            r=request();r['backdrop']=options
            with self.assertRaises(ValueError):orchestrate(r)

    def test_hash_replay_and_schema(self):
        import jsonschema
        schema=json.loads((ROOT/'schemas/backdrop-contract.schema.json').read_text())
        jsonschema.Draft202012Validator.check_schema(schema)
        for p in LONG:
            out=orchestrate(request(p));c=out['cgc_final']['backdrop_contract']
            jsonschema.validate(c,schema)
            self.assertEqual(contract_sha256(c),c['contract_sha256'])
            self.assertEqual(validate_backdrop_contract(c,out['resolved_config'],out['sar2'])['status'],'PASS')
            forged=deepcopy(c);forged['scope']['locked_unknown_ids']=[];forged['contract_sha256']=contract_sha256(forged)
            self.assertEqual(validate_backdrop_contract(forged,out['resolved_config'],out['sar2'])['status'],'FAIL')

    def test_reordering_and_no_mutation(self):
        r=request();before=deepcopy(r);a=orchestrate(r)['cgc_final']['backdrop_contract']
        self.assertEqual(r,before)
        r['scene']['entities'].reverse();r['scene']['relationships'].reverse()
        self.assertEqual(a,orchestrate(r)['cgc_final']['backdrop_contract'])

    def test_existing_commands_remain_opt_out(self):
        r=request();r['command_text']='/sc-rdr2-elevation';out=orchestrate(r)
        self.assertNotIn('backdrop_contract',out['cgc_final'])
        self.assertNotIn('backdrop_preset',out['resolved_config'])
        self.assertEqual(out['resolved_config']['mode'],'T02')

    def test_preflight_cannot_be_bypassed(self):
        for p in LONG:
            r=request(p);r['material_intensity_delta']=1
            out=orchestrate(r);self.assertFalse(out['generation_ready'])
            self.assertEqual(out['status'],'BLOCKED_PREFLIGHT')
            r=request(p);r['text_tokens']=[{'token_id':'T1','literal':"KENNY'S",'confidence':0.99,'preservation_level':'P0','identity_bearing':True}]
            r['proposed_text']={'T1':'OTHER SHOP'}
            self.assertFalse(orchestrate(r)['generation_ready'])

    def test_vsg_shadow_accepts_backdrop_as_explicit_policy(self):
        from visual_scene_graph.generation_compiler import POLICIES,DIRECTIVES,compile_generation_contract,project_scene_to_cgc
        from visual_scene_graph.generation_comparator import compare_generation_contract
        for p in LONG:
            r=request(p);r['vsg']={'mode':'OBSERVER'};o=orchestrate(r);cgc=o['cgc_final'];graph=o['visual_scene_graph']
            scene_directives=project_scene_to_cgc({k:[] for k in DIRECTIVES},o['sar2'])
            context={'policies':{k:v for k,v in cgc.items() if k in POLICIES},
                'directives':{k:[v for v in cgc[k] if v not in scene_directives[k]] for k in DIRECTIVES}}
            shadow=compile_generation_contract(graph,sar2=o['sar2'],generation_context=context)
            report=compare_generation_contract(cgc,shadow,sar2=o['sar2'],expected_graph=graph,candidate_graph=graph,generation_context=context)
            self.assertEqual(report['status'],'PASS',report['issues'])
            self.assertFalse(shadow['governs_generation'])


if __name__=='__main__':unittest.main()
