"""Deterministic source resize and neutral canvas; no generative model calls."""
import hashlib
import json
import subprocess
from pathlib import Path

import PIL
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FREEZE_COMMIT = "ce681b0c6df133e2f9900583ce9370d819e77d28"
SOURCE = ROOT / "benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg"
SOURCE_SHA = "282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc"
BOX = (453, 61, 1147, 839)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if PIL.__version__ != "12.3.0":
        raise SystemExit("Pillow version differs from freeze; stop")
    frozen = subprocess.check_output([
        "git", "show", f"{FREEZE_COMMIT}:validation/spatial_pilot_d/FREEZE.md"
    ], cwd=ROOT)
    if frozen != (HERE / "FREEZE.md").read_bytes():
        raise SystemExit("Freeze changed; stop")
    if sha(SOURCE.read_bytes()) != SOURCE_SHA:
        raise SystemExit("Source hash differs from freeze; stop")
    with Image.open(SOURCE) as source:
        if source.size != (347, 389) or source.mode != "RGB":
            raise SystemExit("Unexpected source format; stop")
        core = source.resize((694, 778), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (1600, 900), (128, 128, 128))
    canvas.paste(core, BOX[:2])
    # Exclusive create: never overwrite a persisted baseline.
    for name, im in (("core.png", core), ("canvas.png", canvas)):
        with (HERE / name).open("xb") as target:
            im.save(target, format="PNG")
    with Image.open(HERE / "canvas.png") as saved:
        if saved.crop(BOX).tobytes() != core.tobytes():
            raise SystemExit("Saved canvas core mismatch")
    manifest = {
        "freeze_commit": FREEZE_COMMIT,
        "freeze_sha256": sha(frozen),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA,
        "source_size": [347, 389],
        "pillow_version": PIL.__version__,
        "method": "Pillow RGB decode; resize LANCZOS; PNG RGB lossless",
        "scale_xy": [2, 2],
        "core_size": [694, 778],
        "canvas_size": [1600, 900],
        "neutral_rgb": [128, 128, 128],
        "core_box_xyxy_exclusive": list(BOX),
        "core_file_sha256": sha((HERE / "core.png").read_bytes()),
        "core_rgb_sha256": sha(core.tobytes()),
        "canvas_file_sha256": sha((HERE / "canvas.png").read_bytes()),
        "canvas_rgb_sha256": sha(canvas.tobytes()),
        "prepare_script_sha256": sha(Path(__file__).read_bytes()),
        "saved_canvas_core_exact": True,
        "generated_by_model": False,
    }
    with (HERE / "CANVAS.json").open("x") as target:
        json.dump(manifest, target, indent=2)
        target.write("\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
