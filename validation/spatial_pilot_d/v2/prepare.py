"""Build deterministic non-generative native candidate, then freeze tested files."""
import argparse
import json
from pathlib import Path

from PIL import Image
import compose as pilot


def native():
    _, baseline = pilot.v1.reference()
    with Image.open(pilot.v1.ROOT / baseline["source"]) as source:
        core = source.resize((725, 813), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1672, 941), pilot.v1.NEUTRAL)
    canvas.paste(core, (473, 64))
    manifest = {"protocol": "SPATIAL-PILOT-D-v2", "enabled_for_runs": False,
                "reason": "NO_NATIVE_INPUT_OUTPUT_STABILITY_EVIDENCE",
                "source": baseline["source"], "source_sha256": baseline["source_sha256"],
                "source_size": [347, 389], "pillow": pilot.PIL.__version__,
                "method": "Source RGB direct resize LANCZOS; PNG lossless",
                "source_scale_x": 725/347, "source_scale_y": 813/389,
                "canvas_size": [1672, 941], "core_size": [725, 813],
                "core_box_xyxy_exclusive": [473, 64, 1198, 877],
                "neutral_rgb": [128, 128, 128], "crop": False, "artifacts": {}}
    for name, im in (("native_core.png", core), ("native_canvas.png", canvas)):
        with (pilot.HERE / name).open("xb") as stream:
            im.save(stream, format="PNG")
        with Image.open(pilot.HERE / name) as saved:
            assert saved.tobytes() == im.tobytes()
        manifest["artifacts"][name] = {"file_sha256": pilot.v1.sha((pilot.HERE / name).read_bytes()),
                                     "rgb_sha256": pilot.v1.sha(im.tobytes())}
    with Image.open(pilot.HERE / "native_canvas.png") as saved:
        assert saved.crop((473, 64, 1198, 877)).tobytes() == core.tobytes()
    with (pilot.HERE / "NATIVE_CANVAS.json").open("x") as stream:
        stream.write(json.dumps(manifest, indent=2)+"\n")


def freeze():
    checks = json.loads((pilot.HERE / "CHECKS.json").read_text())
    if not checks["phase1_all_pass"]:
        raise SystemExit("TESTS_NOT_PASSING")
    files = [p for p in pilot.HERE.parent.iterdir() if p.is_file()]
    files += [p for p in pilot.HERE.iterdir()
              if p.is_file() and p.name != "FREEZE.json"]
    record = {"protocol": "SPATIAL-PILOT-D-v2", "scope": "PHASE_1_SIZE_ONLY",
              "base_commit": "421627deb3aa9c2ffe4e349a1ef71273601619b1",
              "policy": "EXPLICIT_LANCZOS_1672x941_TO_1600x900_OR_CANONICAL_IDENTITY",
              "thresholds": pilot.v1.THRESHOLDS,
              "files_sha256": {p.relative_to(pilot.v1.ROOT).as_posix(): pilot.v1.sha(p.read_bytes())
                               for p in sorted(files)}}
    with (pilot.HERE / "FREEZE.json").open("x") as stream:
        stream.write(json.dumps(record, indent=2)+"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("native", "freeze"))
    args = parser.parse_args()
    native() if args.operation == "native" else freeze()
