#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from collections import Counter

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("snapshot")
    args=ap.parse_args()
    d=json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    items=d.get("items",[])
    ids=[x.get("pin_id") for x in items if x.get("pin_id")]
    tiers=Counter(x.get("image_resolution_tier","unknown") for x in items)
    boards=Counter(x.get("board_url") for x in items)
    report={
        "snapshot_version":d.get("snapshot_version"),
        "enumeration_mode":d.get("enumeration_mode"),
        "item_count":len(items),
        "unique_pin_ids":len(set(ids)),
        "duplicate_pin_ids":[k for k,v in Counter(ids).items() if v>1],
        "resolution_tiers":dict(tiers),
        "board_urls":dict(boards),
        "all_board_urls_match_top_level":all(x.get("board_url")==d.get("board_url") for x in items),
        "all_images_resolved_above_236":
            all((x.get("image_resolution_tier") not in {"236x","unverified","unknown"}) for x in items)
            if items else False
    }
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
