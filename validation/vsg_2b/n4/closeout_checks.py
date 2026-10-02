"""N4R static controls, not model execution or a causal consumer probe.

python closeout_checks.py --repo . --assets /tmp/vsg_n4 --output /tmp/n4r-checks.json
Uses set-valued dependency propagation through pinned PLMS control flow. A nonempty
set means a possible dependency, not a measured effect; an empty set proves absence
only under the listed assumptions (including no hidden cross-step model state).
"""
import argparse
import ast
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path


def temporal(steps, beta, keep_mask):
    assert steps >= 4 and 0 <= beta <= 1 and keep_mask in (0, 1)
    # PNDM leading spacing, steps_offset=1, skip_prk_steps=True.
    ts = [i * (1000 // steps) + 1 for i in range(steps)]
    timesteps = list(reversed(ts[:-1] + ts[-2:-1] + ts[-1:]))
    gate_end = int(beta * len(timesteps))
    ets, previous, cur_sample, rows = [], set(), set(), []
    for counter, timestep in enumerate(timesteps):
        sample = set() if keep_mask else previous.copy()
        direct = {counter} if counter < gate_end else set()
        # Future UNet stateless in eval mode; source/text/RNG held identical.
        model_output = sample | direct
        if counter != 1:
            ets = ets[-3:] + [model_output]
        if len(ets) == 1 and counter == 0:
            effective = model_output
            cur_sample = sample.copy()
        elif len(ets) == 1 and counter == 1:
            effective = model_output | ets[-1]
            sample = cur_sample
            cur_sample = set()
        else:
            # 2-, 3-, 4-term Adams-Bashforth all have nonzero coefficients.
            effective = set().union(*ets)
        previous = sample | effective
        rows.append(dict(index=counter, timestep=timestep,
                         relation_enabled=counter < gate_end,
                         direct_relation_steps=sorted(direct),
                         output_may_depend_on_steps=sorted(previous)))
    return dict(inference_steps=steps, actual_loop_calls=len(timesteps),
                beta=beta, mask_keep_value=keep_mask, gate_end_index=gate_end,
                last_possible_relation_dependent_index=max(
                    (r['index'] for r in rows if r['output_may_depend_on_steps']), default=None),
                final_possible_dependency=bool(previous), rows=rows)


def run(repo, assets):
    old = repo / 'validation/vsg_2b/n4/audit_static.py'
    spec = importlib.util.spec_from_file_location('n4_existing_auditor', old)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    measured = module.audit(repo, assets)
    # Historical script's descriptive counter omitted its extra known-ID assert.
    measured['successful_tokenizer_path_invocations_corrected'] = measured['tokenizer_invocations'] + 1
    measured['counter_correction'] = 'Includes tokenize(hello world!) known-ID assertion; original auditor unchanged.'
    pipeline = Path('/tmp/vsg_n3_sources/code/src/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py')
    pipe_tree = ast.parse(pipeline.read_text())
    call = next(n for n in ast.walk(pipe_tree) if isinstance(n, ast.FunctionDef) and n.name == '__call__')
    defaults = dict(zip([a.arg for a in call.args.args][-len(call.args.defaults):], call.args.defaults))
    assert ast.literal_eval(defaults['num_inference_steps']) == 50
    assert ast.literal_eval(defaults['gligen_scheduled_sampling_beta']) == 0.3
    scheduler = assets / 'diffusers/src/diffusers/schedulers/scheduling_pndm.py'
    src = scheduler.read_text()
    assert 'self.ets = self.ets[-3:]' in src and 'sample = self.cur_sample' in src
    assert '(55 * self.ets[-1] - 59 * self.ets[-2] + 37 * self.ets[-3] - 9 * self.ets[-4])' in src
    cases = [temporal(50, .3, 1), temporal(50, 1., 1), temporal(50, .3, 0)]
    assert cases[0]['actual_loop_calls'] == 51
    assert cases[0]['gate_end_index'] == 15
    assert cases[0]['last_possible_relation_dependent_index'] == 17
    assert not cases[0]['final_possible_dependency']
    assert cases[1]['final_possible_dependency'] and cases[2]['final_possible_dependency']
    sweep = []
    for steps in [10, 20, 30, 50, 100]:
        c = temporal(steps, .3, 1)
        assert not c['final_possible_dependency']
        sweep.append({k: v for k, v in c.items() if k != 'rows'})
    # Native pixels preserved by edge padding, no source resize or interior crop.
    width, height, canvas = 347, 389, 512
    left, top = (canvas-width)//2, (canvas-height)//2
    geometry = dict(source=[width, height], canvas=[canvas, canvas],
                    padding_ltrb=[left, top, canvas-width-left, canvas-height-top],
                    crop_back_ltrb=[left, top, left+width, top+height],
                    source_pixels_preserved_by_coordinate_map=True,
                    visual_identity_after_vae='NOT_RUN')
    payload = json.loads((repo / 'validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f/payloads.json').read_text())
    nodes = []
    for row in payload['A']['common']['approved_source_restrictions']:
        if not row['id'].startswith('node:'):
            continue
        evidence = row['value']['evidence']
        box = [Fraction(str(x)) for x in evidence['region']]
        mapped = [(box[i]*(width if i % 2 == 0 else height)+(left if i % 2 == 0 else top))/canvas for i in range(4)]
        inverse = [(mapped[i]*canvas-(left if i % 2 == 0 else top))/(width if i % 2 == 0 else height) for i in range(4)]
        assert inverse == box and all(0 <= x <= 1 for x in mapped)
        nodes.append(dict(id=row['id'][5:], label=row['value']['label'],
                          evidence=evidence, transformed_region=[float(x) for x in mapped],
                          exact_rational_region=[str(x) for x in mapped],
                          inverse_coordinate_check='PASS'))
    assert len(nodes) == 5
    return dict(tokenization=measured, symbolic_temporal_cases=cases,
                symbolic_default_schedule_sweep=sweep, geometry=geometry, nodes=nodes,
                checks='PASS_STATIC_ONLY', causal_probe='NOT_RUN', model_forwards=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--assets', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.repo, args.assets)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(dict(checks=result['checks'],
                         final_dependency=[c['final_possible_dependency'] for c in result['symbolic_temporal_cases']],
                         strings=len(result['tokenization']['strings']), nodes=len(result['nodes']))))
