"""Versioned normalization and residual alignment; no generator or visual PASS."""
import argparse
import importlib.util
import io
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import PIL
from PIL import Image, ImageChops, ImageStat

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("spatial_v1", HERE.parent / "compose.py")
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)


def normalize(im):
    if PIL.__version__ != "12.3.0":
        raise v1.Rejected("PILLOW_VERSION_MISMATCH")
    if im.mode != "RGB" or im.size not in ((1600, 900), (1672, 941)):
        raise v1.Rejected("UNSUPPORTED_RAW_SIZE_OR_MODE")
    if im.getexif().get(274, 1) != 1:
        raise v1.Rejected("EXIF_ORIENTATION_NOT_IDENTITY")
    w, h = im.size
    sx, sy = 1600/w, 900/h
    identity = im.size == v1.SIZE
    result = im.copy() if identity else im.resize(v1.SIZE, Image.Resampling.LANCZOS)
    return result, {
        "original_size": [w, h], "original_mode": im.mode,
        "normalized_size": list(result.size), "normalized_mode": result.mode,
        "method": "IDENTITY" if identity else "Pillow.Image.resize",
        "interpolation": "NONE" if identity else "LANCZOS",
        "pillow": PIL.__version__, "scale_x": sx, "scale_y": sy,
        "scale_x_fraction": [1600, w], "scale_y_fraction": [900, h],
        "raw_to_canonical_pixel_edge_affine": [sx, 0, 0, 0, sy, 0],
        "inverse_pixel_center_affine": [1/sx, 0, .5/sx-.5, 0, 1/sy, .5/sy-.5],
        "original_aspect_ratio": w/h, "normalized_aspect_ratio": 1600/900,
        "aspect_ratio_correction": sx/sy, "nonuniform_resize": sx != sy,
        "crop": False, "normalized_rgb_sha256": v1.sha(result.tobytes()),
    }


def register(normalized, core):
    metrics = v1.registration(normalized, core)
    metrics["residual_scale_after_normalization"] = metrics["scale"]
    metrics["residual_dx_dy_canonical_px"] = metrics["center_drift_xy_px"]
    metrics["normalization_scale_included_in_residual"] = False
    return metrics


def core_difference(im, core):
    crop = im.crop(v1.BOX)
    diff = ImageChops.difference(crop, core)
    return {"rgb_sha256": v1.sha(crop.tobytes()),
            "different_channels": sum(a != b for a, b in zip(crop.tobytes(), core.tobytes())),
            "mae": sum(ImageStat.Stat(diff).mean)/3}


def frozen_reference():
    path = HERE / "FREEZE.json"
    relative = path.relative_to(v1.ROOT).as_posix()
    commit = subprocess.check_output(
        ["git", "log", "-1", "--format=%H", "--", relative], cwd=v1.ROOT).decode().strip()
    if not commit or subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"], cwd=v1.ROOT) != path.read_bytes():
        raise v1.Rejected("V2_FREEZE_NOT_COMMITTED_OR_CHANGED")
    freeze = json.loads(path.read_text())
    for name, digest in freeze["files_sha256"].items():
        if v1.sha((v1.ROOT / name).read_bytes()) != digest:
            raise v1.Rejected(f"FROZEN_FILE_CHANGED:{name}")
    core, baseline = v1.reference()
    return core, baseline, commit, v1.sha(path.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--original-download-attested", required=True, action="store_true")
    parser.add_argument("--expected-sha256", required=True)
    for field in ("metadata-evidence", "generation-id", "generated-at",
                  "generator-model", "generator-version"):
        parser.add_argument("--"+field, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        parser.error("Invalid run ID")
    if not re.fullmatch(r"[a-f0-9]{64}", args.expected_sha256):
        parser.error("Expected SHA-256 must identify original downloaded bytes")
    # No partial run directories for missing inputs or an unfrozen protocol.
    core, baseline, commit, freeze_sha = frozen_reference()
    data = args.input.read_bytes()
    run = HERE / "runs" / args.run_id
    run.mkdir(parents=True, exist_ok=False)
    (run / "input.original").write_bytes(data)
    record = {"protocol": "SPATIAL-PILOT-D-v2", "freeze_commit": commit,
              "freeze_sha256": freeze_sha, "run_id": args.run_id,
              "processed_at": datetime.now(timezone.utc).isoformat(),
              "input_file_sha256": v1.sha(data), "provenance": vars(args) | {"input": str(args.input)},
              "status": "REJECTED", "alignment_gate": "NOT_RUN",
              "seam_gate": "NOT_RUN_PHASE_3_PENDING",
              "core_pixel_identity": "NOT_APPLICABLE_NO_COMPOSITE",
              "no_new_legible_text": "PENDING_HUMAN_INSPECTION_RAW_AND_COMPOSITE",
              "visual_evaluable": False, "pipeline_visual_scores": "NOT_YET_EVALUATED"}
    try:
        if record["input_file_sha256"] != args.expected_sha256:
            raise v1.Rejected("ORIGINAL_HASH_MISMATCH")
        with Image.open(io.BytesIO(data)) as im:
            record["original"] = {"size": list(im.size), "mode": im.mode, "format": im.format}
            if im.format not in ("PNG", "JPEG") or getattr(im, "n_frames", 1) != 1:
                raise v1.Rejected("EXPECTED_SINGLE_FRAME_PNG_OR_JPEG")
            im.load()
            normalized, record["normalization"] = normalize(im)
        normalized.save(run / "normalized.png")
        record["normalized_file_sha256"] = v1.sha((run / "normalized.png").read_bytes())
        record["normalized_core_before_registration"] = core_difference(normalized, core)
        m = register(normalized, core)
        record["alignment"] = m
        record["alignment_gate"] = "PASS" if m["accepted"] else "REJECTED"
        dx, dy = m["center_drift_xy_px"]
        s = m["scale"]
        candidate = normalized.transform(v1.SIZE, Image.Transform.AFFINE,
            (s, 0, 800*(1-s)+dx, 0, s, 450*(1-s)+dy),
            Image.Resampling.BICUBIC, fillcolor=v1.NEUTRAL)
        record["gpt_core_at_candidate_alignment_before_paste"] = core_difference(candidate, core)
        if not m["accepted"]:
            raise v1.Rejected("ALINEACION_NO_CONFIABLE")
        composite, record["composition"] = v1.compose(normalized, core, m)
        target = run / "composite_diagnostic.png"
        composite.save(target)
        record["core_pixel_identity"] = "FAIL_UNTIL_SAVED_VERIFICATION"
        record["verification"] = v1.verify_saved(target, core)
        record["core_pixel_identity"] = "PASS"
        record["status"] = "ACCEPTED_ALIGNMENT_ONLY"
    except (v1.Rejected, OSError, ValueError) as exc:
        record["rejection_reason"] = str(exc)
    (run / "result.json").write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps(record, indent=2))
    return 0 if record["status"] == "ACCEPTED_ALIGNMENT_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
