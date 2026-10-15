"""Fail-closed local registration/composition. No model, network or SVS imports."""
import argparse
import hashlib
import io
import json
import math
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import PIL
from PIL import Image, ImageChops, ImageStat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FREEZE_COMMIT = "ce681b0c6df133e2f9900583ce9370d819e77d28"
PROMPT_COMMIT = "b62ad278d6bb09704b1358f316650b4dca5c0862"
BOX = (453, 61, 1147, 839)
CENTER = (800, 450)
SIZE = (1600, 900)
NEUTRAL = (128, 128, 128)
SAMPLE = (48, 54)
HALO = 4
THRESHOLDS = {
    "max_center_drift_px": 16, "max_scale_delta": 0.02,
    "min_global_ncc": 0.92, "min_quadrant_ncc": 0.80,
    "min_patch_stddev": 8, "min_distinct_alternative_margin": 0.03,
    "max_quadrant_residual_px": 1.5,
}


class Rejected(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def reference():
    """Verify all baselines against their committed bytes, not just a sidecar."""
    if PIL.__version__ != "12.3.0":
        raise Rejected("PILLOW_VERSION_MISMATCH")
    for name, commit in (("FREEZE.md", FREEZE_COMMIT), ("PROMPT.md", PROMPT_COMMIT),
                         ("CANVAS.json", PROMPT_COMMIT), ("core.png", PROMPT_COMMIT),
                         ("canvas.png", PROMPT_COMMIT)):
        frozen = subprocess.check_output(
            ["git", "show", f"{commit}:validation/spatial_pilot_d/{name}"], cwd=ROOT)
        if frozen != (HERE / name).read_bytes():
            raise Rejected(f"BASELINE_CHANGED:{name}")
    manifest = json.loads((HERE / "CANVAS.json").read_text())
    if sha((ROOT / manifest["source"]).read_bytes()) != manifest["source_sha256"]:
        raise Rejected("SOURCE_CHANGED")
    with Image.open(HERE / "core.png") as im:
        core = im.convert("RGB")
    if sha(core.tobytes()) != manifest["core_rgb_sha256"]:
        raise Rejected("CORE_PIXELS_CHANGED")
    return core, manifest


def vector(im, box):
    # Crop first: Pillow's resize(box=...) includes filter support OUTSIDE box,
    # which otherwise biases scale toward shrinking against the neutral border.
    return tuple(im.crop(box).resize(SAMPLE, Image.Resampling.BILINEAR).tobytes())


def ncc(a, b):
    n = len(a)
    sa, sb = sum(a), sum(b)
    va = sum(x*x for x in a) - sa*sa/n
    vb = sum(x*x for x in b) - sb*sb/n
    std_a, std_b = math.sqrt(max(0, va/n)), math.sqrt(max(0, vb/n))
    if min(std_a, std_b) < THRESHOLDS["min_patch_stddev"]:
        return -1.0
    return (sum(x*y for x, y in zip(a, b)) - sa*sb/n) / math.sqrt(va*vb)


def mapped_box(box, dx, dy, scale):
    return tuple(CENTER[i % 2] + (v-CENTER[i % 2])*scale + (dx if i % 2 == 0 else dy)
                 for i, v in enumerate(box))


def inside(box):
    return box[0] >= 0 and box[1] >= 0 and box[2] <= SIZE[0] and box[3] <= SIZE[1]


def registration(output, core):
    if output.size != SIZE or output.mode != "RGB":
        raise Rejected("EXPECTED_1600x900_RGB; no automatic resizing or color conversion")
    gray, core_gray = output.convert("L"), core.convert("L")
    template = vector(core_gray, (0, 0, *core.size))

    def score(dx, dy, scale):
        box = mapped_box(BOX, dx, dy, scale)
        return ncc(template, vector(gray, box)) if inside(box) else -1.0

    # Fixed search, identical for every run. Coarse 8 px / 0.01 scale;
    # fine 1 px / 0.002 scale; final scale refinement 0.001.
    coarse = [(score(dx, dy, s/100), dx, dy, s/100)
              for s in range(90, 111) for dx in range(-48, 49, 8)
              for dy in range(-48, 49, 8)]
    def rank(candidate):
        corr, dx, dy, scale = candidate
        return corr, -math.hypot(dx, dy), -abs(scale-1)

    best = max(coarse, key=rank)
    fine = [(score(dx, dy, scale), dx, dy, scale)
            for dx in range(max(-48, best[1]-4), min(48, best[1]+4)+1)
            for dy in range(max(-48, best[2]-4), min(48, best[2]+4)+1)
            for scale in (round(best[3]+ds/1000, 3) for ds in range(-10, 11, 2))
            if 0.90 <= scale <= 1.10]
    best = max(fine + [best], key=rank)
    best = max([best] + [(score(best[1], best[2], s), best[1], best[2], s)
                        for s in (round(best[3]-0.001, 3), round(best[3]+0.001, 3))
                        if 0.90 <= s <= 1.10], key=rank)
    corr, dx, dy, scale = best
    alternatives = [c for c, x, y, s in coarse
                    if math.hypot(x-dx, y-dy) > 8 or abs(s-scale) > 0.02000001]
    margin = corr - max(alternatives)
    quadrants = []
    for q in ((0, 0, 347, 389), (347, 0, 694, 389),
              (0, 389, 347, 778), (347, 389, 694, 778)):
        qref = vector(core_gray, q)
        qb = tuple(v + BOX[i % 2] for i, v in enumerate(q))
        mapped = mapped_box(qb, dx, dy, scale)
        aligned_corr = ncc(qref, vector(gray, mapped))
        # Prefer smallest correction when scores tie.
        locals_ = [(ncc(qref, vector(gray, (mapped[0]+x, mapped[1]+y,
                                           mapped[2]+x, mapped[3]+y))),
                    -math.hypot(x, y), x, y)
                   for x in range(-3, 4) for y in range(-3, 4)
                   if inside((mapped[0]+x, mapped[1]+y, mapped[2]+x, mapped[3]+y))]
        local = max(locals_)
        quadrants.append({"core_box": q, "ncc": aligned_corr,
                          "residual_xy_px": list(local[2:]), "residual_px": -local[1]})
    reasons = []
    if abs(dx) == 48 or abs(dy) == 48 or scale in (0.90, 1.10):
        reasons.append("SEARCH_BOUNDARY")
    if math.hypot(dx, dy) > THRESHOLDS["max_center_drift_px"]:
        reasons.append("POSITION_DRIFT")
    if abs(scale-1) > THRESHOLDS["max_scale_delta"]+1e-9:
        reasons.append("SCALE_DRIFT")
    if corr < THRESHOLDS["min_global_ncc"]:
        reasons.append("GLOBAL_CORRELATION_OR_TEXTURE")
    if margin < THRESHOLDS["min_distinct_alternative_margin"]:
        reasons.append("AMBIGUOUS_ALIGNMENT")
    if any(q["ncc"] < THRESHOLDS["min_quadrant_ncc"] for q in quadrants):
        reasons.append("QUADRANT_CORRELATION_OR_TEXTURE")
    if any(q["residual_px"] > THRESHOLDS["max_quadrant_residual_px"] for q in quadrants):
        reasons.append("LOCAL_DEFORMATION")
    halo = (BOX[0]-HALO, BOX[1]-HALO, BOX[2]+HALO, BOX[3]+HALO)
    if not inside(mapped_box(halo, dx, dy, scale)):
        reasons.append("CORE_HALO_COVERAGE")
    return {"accepted": not reasons, "reasons": reasons, "center_drift_xy_px": [dx, dy],
            "center_drift_px": math.hypot(dx, dy), "scale": scale,
            "scale_delta": scale-1, "global_ncc": corr, "alternative_margin": margin,
            "quadrants": quadrants, "thresholds": THRESHOLDS,
            "search_model": "uniform_scale_and_translation_only", "seed": "NOT_APPLICABLE"}


def compose(output, core, metrics):
    if not metrics["accepted"]:
        raise Rejected("ALINEACION_NO_CONFIABLE")
    dx, dy = metrics["center_drift_xy_px"]
    scale = metrics["scale"]
    # Pillow affine maps target coordinates to input coordinates.
    transform = (scale, 0, CENTER[0]*(1-scale)+dx,
                 0, scale, CENTER[1]*(1-scale)+dy)
    aligned = output.transform(SIZE, Image.Transform.AFFINE, transform,
                               Image.Resampling.BICUBIC, fillcolor=NEUTRAL)
    coverage = Image.new("L", SIZE, 255).transform(
        SIZE, Image.Transform.AFFINE, transform, Image.Resampling.NEAREST, fillcolor=0)
    pre = ImageChops.difference(aligned.crop(BOX), core)
    report = {"aligned_gpt_core_rgb_sha256": sha(aligned.crop(BOX).tobytes()),
              "gpt_core_equal_before_paste": not any(hi for lo, hi in pre.getextrema()),
              "gpt_core_mae_before_paste": statistics.mean(ImageStat.Stat(pre).mean),
              "uncovered_outer_pixels_filled_neutral": coverage.histogram()[0],
              "outer_fill_rgb": NEUTRAL, "halo_px": HALO,
              "halo_method": "nearest core edge extension, exterior alpha 4/5,3/5,2/5,1/5",
              "alignment_affine_target_to_input": transform}
    # Halo extends the core's edge pixels OUTSIDE the protected rectangle.
    # It never feathers inward, and opaque core paste runs last.
    result = aligned.copy()
    cp, rp, ap = core.load(), result.load(), aligned.load()
    for y in range(BOX[1]-HALO, BOX[3]+HALO):
        for x in range(BOX[0]-HALO, BOX[2]+HALO):
            if BOX[0] <= x < BOX[2] and BOX[1] <= y < BOX[3]:
                continue
            dist = max(BOX[0]-x, x-(BOX[2]-1), BOX[1]-y, y-(BOX[3]-1), 0)
            alpha = (HALO+1-dist)/(HALO+1)
            edge = cp[min(max(x-BOX[0], 0), core.width-1),
                      min(max(y-BOX[1], 0), core.height-1)]
            rp[x, y] = tuple(round(alpha*a+(1-alpha)*b) for a, b in zip(edge, ap[x, y]))
    result.paste(core, BOX[:2])
    return result, report


def verify_saved(path, core):
    with Image.open(path) as saved:
        if saved.mode != "RGB" or saved.size != SIZE:
            raise Rejected("SAVED_COMPOSITE_FORMAT")
        crop = saved.crop(BOX)
        mismatch = sum(a != b for a, b in zip(crop.tobytes(), core.tobytes()))
        if mismatch:
            raise Rejected(f"CORE_IDENTITY_FAILED:{mismatch}_channels")
        return {"core_exact": True, "different_channels": mismatch,
                "core_rgb_sha256": sha(crop.tobytes()),
                "composite_file_sha256": sha(Path(path).read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Original downloaded GPT output")
    parser.add_argument("--run-id", required=True, help="Unique run ID; never overwrite")
    parser.add_argument("--generator-model", required=True, help="Observed identifier or UNKNOWN")
    parser.add_argument("--generator-version", required=True, help="Observed version or UNKNOWN")
    parser.add_argument("--metadata-evidence", required=True, help="Operator declaration or evidence path")
    parser.add_argument("--generation-id", required=True, help="ChatGPT ID or UNKNOWN")
    parser.add_argument("--generated-at", required=True, help="Observed timestamp or UNKNOWN")
    args = parser.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.run_id):
        parser.error("run-id must contain only ASCII letters, digits, '-' or '_'")
    run = HERE / "runs" / args.run_id
    run.mkdir(parents=True, exist_ok=False)
    record = {"run_id": args.run_id, "processed_at": datetime.now(timezone.utc).isoformat(),
              "freeze_commit": FREEZE_COMMIT, "prompt_commit": PROMPT_COMMIT,
              "script_sha256": sha(Path(__file__).read_bytes()), "pillow": PIL.__version__,
              "generator_model": args.generator_model, "generator_version": args.generator_version,
              "metadata_evidence": args.metadata_evidence, "generation_id": args.generation_id,
              "generated_at": args.generated_at, "status": "BLOQUEADO",
              "visual_evaluation": "NOT_PERFORMED; Lean required", "visual_pass": False}
    try:
        core, manifest = reference()
        record["baseline"] = manifest
        data = args.input.read_bytes()
        record["input_file_sha256"] = sha(data)
        # Preserve original bytes even when decoding or format validation fails.
        (run / "input.original").write_bytes(data)
        with Image.open(io.BytesIO(data)) as im:
            if im.format not in ("PNG", "JPEG") or getattr(im, "n_frames", 1) != 1:
                raise Rejected("EXPECTED_SINGLE_FRAME_PNG_OR_JPEG")
            im.load()
            output = im.copy()
        metrics = registration(output, core)
        record["alignment"] = metrics
        if not metrics["accepted"]:
            raise Rejected("ALINEACION_NO_CONFIABLE")
        result, changes = compose(output, core, metrics)
        target = run / "composite.png"
        result.save(target)
        record["composition"] = changes
        record["verification"] = verify_saved(target, core)
        record["status"] = "TECHNICAL_COMPOSITION_PASS_VISUAL_UNEVALUATED"
    except (Rejected, OSError, ValueError, subprocess.CalledProcessError) as exc:
        record["blocker"] = str(exc)
    finally:
        (run / "result.json").write_text(json.dumps(record, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0 if record["status"].startswith("TECHNICAL_COMPOSITION_PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
