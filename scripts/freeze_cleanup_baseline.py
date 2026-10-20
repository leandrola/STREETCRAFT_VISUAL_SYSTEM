#!/usr/bin/env python3
"""Freeze or verify the cleanup integrity baseline from the inventory branch."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/repository"
INVENTORY_REF = "cleanup/inventory"
INVENTORY_LIST = "development/cleanup/UNTOUCHABLE_HASH_PROVENANCE.csv"
INVENTORY_BASELINE = "development/cleanup/baseline_results.json"


def git_show(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{INVENTORY_REF}:{path}"], cwd=ROOT)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows() -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(git_show(INVENTORY_LIST).decode("utf-8"))))


def capture() -> int:
    records = []
    for row in rows():
        path = ROOT / row["path"]
        actual = digest(path) if path.is_file() else "MISSING"
        records.append(
            {
                "path": row["path"],
                "expected_sha256": row["sha256"],
                "actual_sha256": actual,
                "status": "MATCH" if actual == row["sha256"] else "MISMATCH",
                "basis": row["basis"],
            }
        )
    with (DOCS / "CLEANUP_2026_10_UNTOUCHABLE_HASHES.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    prior = json.loads(git_show(INVENTORY_BASELINE))
    summary = {
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "inventory_ref": INVENTORY_REF,
        "inventory_list": INVENTORY_LIST,
        "immutable_paths": len(records),
        "hash_matches": sum(record["status"] == "MATCH" for record in records),
        "hash_mismatches": [record for record in records if record["status"] != "MATCH"],
        "baseline_results": {
            "status": prior["status"],
            "head": prior["head"],
            "baseline_results_sha256": hashlib.sha256(git_show(INVENTORY_BASELINE)).hexdigest(),
            "dry_run_sha256": prior["dry_run_sha256"],
        },
    }
    (DOCS / "CLEANUP_2026_10_BASELINE.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not summary["hash_mismatches"] else 1


if __name__ == "__main__":
    raise SystemExit(capture())
