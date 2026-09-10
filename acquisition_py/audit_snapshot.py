#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, hashlib
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit, urlunsplit

PIN_RE = re.compile(r"/pin/(\d+)")
SIZE_RE = re.compile(r"(https?://i\.pinimg\.com)/(?:75x75_RS|136x136|170x|236x|474x|564x|736x)/", re.I)

def canon(url):
    if not url: return None
    s = urlsplit(url.strip())
    return urlunsplit((s.scheme.lower(), s.netloc.lower(), s.path.rstrip("/"), "", ""))

def upgrade(url):
    if not url: return None
    return SIZE_RE.sub(r"\1originals/", url, count=1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot")
    ap.add_argument("--board-url", required=True)
    ap.add_argument("--output")
    args = ap.parse_args()
    p = Path(args.snapshot)
    data = json.loads(p.read_text(encoding="utf-8"))
    items = data.get("items", [])

    ids = [x.get("pin_id") for x in items if x.get("pin_id")]
    urls = [canon(x.get("pin_url")) for x in items if x.get("pin_url")]
    fps = [x.get("fingerprint") for x in items if x.get("fingerprint")]
    image_urls = [x.get("image_url") for x in items if x.get("image_url")]

    report = {
        "release": "1.0-F3",
        "input_snapshot_version": data.get("snapshot_version"),
        "item_count": len(items),
        "unique_pin_ids": len(set(ids)),
        "duplicate_pin_ids": [k for k,v in Counter(ids).items() if v > 1],
        "unique_pin_urls": len(set(urls)),
        "duplicate_pin_urls": [k for k,v in Counter(urls).items() if v > 1],
        "unique_fingerprints": len(set(fps)),
        "duplicate_fingerprints": [k for k,v in Counter(fps).items() if v > 1],
        "image_url_count": len(image_urls),
        "pinimg_236x_count": sum("/236x/" in u for u in image_urls),
        "pinimg_originals_count": sum("/originals/" in u for u in image_urls),
        "board_url_in_snapshot": data.get("board_url"),
        "configured_canonical_board": args.board_url,
        "all_items_board_match_before_normalization":
            all(canon(x.get("board_url")) == canon(args.board_url) for x in items),
        "note": "Different pin IDs may still contain the same underlying photograph. Perceptual deduplication remains a later image-level audit."
    }

    if args.output:
        for x in items:
            x["board_url"] = canon(args.board_url)
            x["image_url"] = upgrade(x.get("image_url"))
        data["board_url"] = canon(args.board_url)
        data["snapshot_version"] = "1.0-F3-normalized"
        data.setdefault("diagnostics", {})["f3_offline_normalization"] = {
            "canonical_board_restored": True,
            "pinimg_urls_upgraded_to_originals_candidates": True,
            "network_validation_required": True
        }
        Path(args.output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
