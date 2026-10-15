"""Synthetic geometry checks, not GPT generations or visual acceptance."""
import json
import tempfile
from pathlib import Path

from PIL import Image

import compose as pilot


def main():
    core, manifest = pilot.reference()
    with Image.open(pilot.HERE / "canvas.png") as im:
        canvas = im.copy()
    results = []
    cases = [("identity", 0, 0, 1.0, True),
             ("small_shift", 8, 0, 1.0, True),
             # Measured geometry is correct, but the frozen ambiguity margin
             # rejects this case (0.026 < 0.03). Preserve that pilot limitation.
             ("small_shift_and_scale_ambiguity", 5, -3, 1.012, False),
             ("excess_translation", 24, 0, 1.0, False),
             ("excess_scale", 0, 0, 1.06, False)]
    for name, dx, dy, scale, expected in cases:
        # Known forward geometry: source point p lands at C+s*(p-C)+d.
        inverse = (1/scale, 0, 800-(800+dx)/scale,
                   0, 1/scale, 450-(450+dy)/scale)
        synthetic = canvas.transform(pilot.SIZE, Image.Transform.AFFINE, inverse,
                                     Image.Resampling.BICUBIC, fillcolor=pilot.NEUTRAL)
        metrics = pilot.registration(synthetic, core)
        passed = metrics['accepted'] == expected
        if name == 'small_shift_and_scale_ambiguity':
            passed &= 'AMBIGUOUS_ALIGNMENT' in metrics['reasons']
        if name == 'excess_translation':
            passed &= 'POSITION_DRIFT' in metrics['reasons']
        if name == 'excess_scale':
            passed &= 'SCALE_DRIFT' in metrics['reasons']
        if expected and metrics['accepted']:
            passed &= abs(metrics['scale']-scale) <= 0.003
            passed &= all(abs(a-b) <= 1 for a, b in zip(metrics['center_drift_xy_px'], (dx, dy)))
            composite, _ = pilot.compose(synthetic, core, metrics)
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / 'composite.png'
                composite.save(path)
                passed &= pilot.verify_saved(path, core)['core_exact']
                # Actual one-channel corruption must fail the saved-pixel verifier.
                pixel = composite.getpixel(pilot.BOX[:2])
                composite.putpixel(pilot.BOX[:2], ((pixel[0]+1) % 256, *pixel[1:]))
                composite.save(path)
                try:
                    pilot.verify_saved(path, core)
                    passed = False
                except pilot.Rejected:
                    pass
        else:
            try:
                pilot.compose(synthetic, core, metrics)
                passed = False
            except pilot.Rejected:
                pass
        item = {'case': name, 'expected_acceptance': expected, 'pass': bool(passed),
                'known_geometry': {'dx': dx, 'dy': dy, 'scale': scale}, 'metrics': metrics}
        results.append(item)
        print(json.dumps(item), flush=True)
    # Nonuniform geometry must not be silently coerced into a uniform scale.
    nonuniform = canvas.transform(pilot.SIZE, Image.Transform.AFFINE,
                                  (1/1.02, 0, 800-800/1.02, 0, 1/0.98, 450-450/0.98),
                                  Image.Resampling.BICUBIC, fillcolor=pilot.NEUTRAL)
    m = pilot.registration(nonuniform, core)
    results.append({'case': 'nonuniform_geometry', 'pass': not m['accepted'], 'metrics': m})
    print(json.dumps(results[-1]), flush=True)
    for name, im in [('wrong_size', Image.new('RGB', (800, 450))),
                     ('wrong_mode', Image.new('RGBA', pilot.SIZE))]:
        try:
            pilot.registration(im, core)
            ok = False
        except pilot.Rejected:
            ok = True
        results.append({'case': name, 'pass': ok})
    # Explicit texture/correlation unit checks, without an expensive blank search.
    results.append({'case': 'untextured_patch_rejected',
                    'pass': pilot.ncc((128,)*100, (128,)*100) == -1.0})
    report = {'type': 'SYNTHETIC_LOCAL_GEOMETRY_ONLY', 'gpt_outputs': 0,
              'script_sha256': pilot.sha((pilot.HERE/'compose.py').read_bytes()),
              'check_script_sha256': pilot.sha(Path(__file__).read_bytes()),
              'all_pass': all(r['pass'] for r in results), 'checks': results}
    (pilot.HERE / 'LOCAL_CHECKS.json').write_text(json.dumps(report, indent=2)+'\n')
    return 0 if report['all_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
