#!/usr/bin/env python3
"""Close inventory step 3 from existing read-only inventory annexes."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent


def is_hash_source(path: str) -> bool:
    name = Path(path).name.lower()
    if path in {
        "development/coordination/CHECKPOINT.json",
        "SVS_1_10_0_SHA256SUMS.json",
        "PACKAGE_MANIFEST.json",
        "RECONSTRUCTION_PROVENANCE.json",
    }:
        return True
    return path.startswith("validation/sc_multiagent/") and any(
        token in name for token in ("manifest", "provenance", "receipt", "entry_evidence")
    )


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    protected = json.loads((OUT / "protected_references.json").read_text())
    reachability = json.loads((OUT / "reachability.json").read_text())
    classification = {
        row["path"]: row
        for row in csv.DictReader((OUT / "classification.csv").open(encoding="utf-8"))
    }
    authoritative_sources = sorted(
        {r["source"] for r in protected["references"] if is_hash_source(r["source"])}
    )
    immutable = set(authoritative_sources)
    exact_records = []
    for record in protected["references"]:
        if record["source"] in authoritative_sources:
            for target in record["targets"]:
                immutable.add(target)
                row = classification.get(target, {})
                exact_records.append(
                    {
                        "source": record["source"],
                        "pointer": record["pointer"],
                        "reference": record["reference"],
                        "path": target,
                        "resolution": record["resolution"],
                        "sha256": row.get("sha256", ""),
                        "git_state": row.get("git_state", ""),
                    }
                )
    immutable_rows = []
    for path in sorted(immutable):
        row = classification.get(path, {})
        sources = sorted({r["source"] for r in protected["references"] if path in r["targets"] and is_hash_source(r["source"])})
        immutable_rows.append(
            {
                "path": path,
                "sha256": row.get("sha256", ""),
                "git_state": row.get("git_state", ""),
                "basis": "authoritative_source" if path in authoritative_sources else "resolved_hash_or_provenance_reference",
                "authoritative_sources": " | ".join(sources),
            }
        )
    write_csv(
        "UNTOUCHABLE_HASH_PROVENANCE.csv",
        immutable_rows,
        ["path", "sha256", "git_state", "basis", "authoritative_sources"],
    )
    write_csv(
        "STEP3_HASH_REFERENCE_DETAILS.csv",
        exact_records,
        ["source", "pointer", "reference", "path", "resolution", "sha256", "git_state"],
    )

    runtime = sorted(set(reachability["executable_runtime"]))
    write_csv(
        "EXECUTION_READ_PATHS.csv",
        [
            {
                "path": path,
                "sha256": classification.get(path, {}).get("sha256", ""),
                "basis": "AST_import_or_explicit_runtime_read",
            }
            for path in runtime
        ],
        ["path", "sha256", "basis"],
    )

    unresolved_rows = []
    for record in protected["unresolved"]:
        if is_hash_source(record["source"]):
            group = "a_hash_or_provenance"
            subtype = "external_or_historical_reference_retained_in_authoritative_record"
        elif record["source"] in runtime:
            group = "b_execution"
            subtype = "dynamic_or_external_runtime_input"
        else:
            group = "c_documentary"
            if record["resolution"] == "external":
                subtype = "external_link_or_command_token"
            elif record["reference"].startswith("/"):
                subtype = "historical_absolute_path"
            else:
                subtype = "broken_or_non_normalized_documentary_reference"
        unresolved_rows.append(
            {
                "group": group,
                "subtype": subtype,
                "source": record["source"],
                "pointer": record["pointer"],
                "reference": record["reference"],
                "resolution": record["resolution"],
            }
        )
    write_csv(
        "STEP3_UNRESOLVED_BY_TYPE.csv",
        unresolved_rows,
        ["group", "subtype", "source", "pointer", "reference", "resolution"],
    )
    summary = {
        "status": "CERRADO",
        "method": "Classifies every previously unresolved manifest/provenance reference by source role. Resolves group (a) only into the immutable path list; runtime imports/reads are separately listed and documentary references are retained as external, historical, or broken/non-normalized.",
        "authoritative_sources": authoritative_sources,
        "immutable_path_count": len(immutable_rows),
        "runtime_execution_path_count": len(runtime),
        "unresolved_by_group": dict(Counter(row["group"] for row in unresolved_rows)),
        "unresolved_documentary_by_subtype": dict(
            Counter(row["subtype"] for row in unresolved_rows if row["group"] == "c_documentary")
        ),
        "limits": [
            "An unresolved authoritative reference remains preserved in its source record; it cannot create a local immutable path without a resolved local target.",
            "External Archive runtime inputs remain external and are not fabricated from this repository.",
            "Documentary broken/non-normalized links are reported, not repaired, in this read-only phase.",
        ],
    }
    (OUT / "STEP3_REFERENCE_TRIAGE.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
