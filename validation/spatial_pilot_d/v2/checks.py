"""Synthetic phase-1 checks. No generated images, real-output or seam claims."""
import importlib.util
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image
import compose as pilot


def main():
    core, _ = pilot.v1.reference()
    with Image.open(pilot.HERE.parent / "canvas.png") as im:
        canvas = im.copy()
    results = []
    def add(name, ok, **details):
        results.append({"case": name, "pass": bool(ok), **details})
        print(name, "PASS" if ok else "FAIL", flush=True)

    # Execute every existing v1 check without overwriting historical LOCAL_CHECKS.
    spec = importlib.util.spec_from_file_location("old_checks", pilot.HERE.parent / "check_composition.py")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    old.pilot = pilot.v1
    reports = []
    original_write = Path.write_text
    def capture(path, data, *args, **kwargs):
        if path == pilot.HERE.parent / "LOCAL_CHECKS.json":
            reports.append(json.loads(data))
            return len(data)
        return original_write(path, data, *args, **kwargs)
    with patch.object(Path, "write_text", capture):
        code = old.main()
    add("v1_existing_suite", code == 0 and len(reports[0]["checks"]) == 9,
        checks=reports[0]["checks"])

    same, n = pilot.normalize(canvas)
    add("canonical_identity", same.tobytes() == canvas.tobytes() and n["interpolation"] == "NONE")
    with Image.open(pilot.HERE / "native_core.png") as im:
        native_core = im.copy()
    with Image.open(pilot.HERE / "native_canvas.png") as im:
        add("native_candidate_core_identity", im.size == (1672, 941) and
            im.crop((473, 64, 1198, 877)).tobytes() == native_core.tobytes())

    cases = [("normalized_dx0", 0, 1.0, True, None),
             ("normalized_dx8", 8, 1.0, True, None),
             ("normalized_dx24", 24, 1.0, False, "POSITION_DRIFT"),
             # Keep observed ambiguity failures; within-limit does not imply PASS.
             ("normalized_scale_1_01_ambiguity", 0, 1.01, False, "AMBIGUOUS_ALIGNMENT"),
             ("normalized_scale_1_002_ambiguity", 0, 1.002, False, "AMBIGUOUS_ALIGNMENT"),
             ("normalized_scale_within_inclusive_limit", 0, 1.02, True, None),
             ("normalized_scale_outside", 0, 1.03, False, "SCALE_DRIFT")]
    accepted = 0
    for name, dx, scale, expected, reason in cases:
        sim = canvas.transform(pilot.v1.SIZE, Image.Transform.AFFINE,
            (1/scale, 0, 800-(800+dx)/scale, 0, 1/scale, 450-450/scale),
            Image.Resampling.BICUBIC, fillcolor=pilot.v1.NEUTRAL)
        raw = sim.resize((1672, 941), Image.Resampling.LANCZOS)
        normalized, norm = pilot.normalize(raw)
        if name == "normalized_dx0":
            repeat, _ = pilot.normalize(raw)
            add("raw_1672_deterministic_normalization", normalized.tobytes() == repeat.tobytes()
                and norm["scale_x"] == 1600/1672 and norm["scale_y"] == 900/941
                and norm["nonuniform_resize"], normalization=norm)
        m = pilot.register(normalized, core)
        ok = m["accepted"] == expected and abs(m["scale"]-scale) <= .003
        ok &= abs(m["center_drift_xy_px"][0]-dx) <= 1
        if reason:
            ok &= reason in m["reasons"]
        add(name, ok, expected_accepted=expected, metrics=m)
        if m["accepted"]:
            accepted += 1
            composite, _ = pilot.v1.compose(normalized, core, m)
            with tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp) / "test.png"
                composite.save(target)
                verify = pilot.v1.verify_saved(target, core)
                add(name+"_zero_channels", verify["different_channels"] == 0, verification=verify)
                p = composite.getpixel(pilot.v1.BOX[:2])
                composite.putpixel(pilot.v1.BOX[:2], ((p[0]+1)%256, p[1], p[2]))
                composite.save(target)
                try:
                    pilot.v1.verify_saved(target, core)
                    corrupt_rejected = False
                except pilot.v1.Rejected as exc:
                    corrupt_rejected = str(exc) == "CORE_IDENTITY_FAILED:1_channels"
                add(name+"_one_channel_rejected", corrupt_rejected)
    sim = canvas.transform(pilot.v1.SIZE, Image.Transform.AFFINE,
        (1/1.02, 0, 800-800/1.02, 0, 1/.98, 450-450/.98),
        Image.Resampling.BICUBIC, fillcolor=pilot.v1.NEUTRAL)
    norm, _ = pilot.normalize(sim.resize((1672, 941), Image.Resampling.LANCZOS))
    m = pilot.register(norm, core)
    add("normalized_nonuniform_deformation", not m["accepted"] and "LOCAL_DEFORMATION" in m["reasons"], metrics=m)
    for name, image in (("unapproved_size", Image.new("RGB", (1672, 940))),
                        ("wrong_mode", Image.new("RGBA", (1672, 941)))):
        try:
            pilot.normalize(image)
            rejected = False
        except pilot.v1.Rejected:
            rejected = True
        add(name+"_rejected", rejected)
    report = {"scope": "SYNTHETIC_SIZE_AND_RESIDUAL_ALIGNMENT_ONLY", "real_runs": 0,
              "phase1_all_pass": all(x["pass"] for x in results) and accepted == 3,
              "checks": results, "deferred_checks": {
                  "seam_good_reference": "NOT_RUN_PHASE_3_DEPENDS_ON_PHASE_2",
                  "seam_bad_plus8": "NOT_RUN_PHASE_3_DEPENDS_ON_PHASE_2"}}
    (pilot.HERE / "CHECKS.json").write_text(json.dumps(report, indent=2)+"\n")
    return 0 if report["phase1_all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
