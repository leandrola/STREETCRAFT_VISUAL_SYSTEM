#!/usr/bin/env python3
"""Apply Lean's inventory decisions without changing repository sources."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent


def read_csv(name: str) -> list[dict]:
    with (OUT / name).open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def is_bd(path: str) -> bool:
    return path in {
        "command_invocation/COMMANDS.json",
        "command_invocation/BACKDROP_PRESETS.json",
        "command_invocation/BACKDROP_PRESETS.md",
        "command_invocation/backdrop_presets.py",
        "command_invocation/test_backdrop_presets.py",
        "schemas/backdrop-contract.schema.json",
        "validation/BACKDROP_PRESETS_QA.json",
        "validation/BD_VISUAL_VALIDATION_BENCHMARK.json",
        "validation/BD_VISUAL_VALIDATION_BENCHMARK.md",
    }


def is_decided_visual_material(path: str) -> bool:
    return path.startswith((
        "reference/assets/",
        "benchmark/r2b_1_9_1/",
        "outputs/",
    ))


def archive_group(path: str) -> str:
    parts = Path(path).parts
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return parts[0]


def main() -> None:
    original = read_csv("classification.csv")
    immutable = {row["path"] for row in read_csv("UNTOUCHABLE_HASH_PROVENANCE.csv")}
    runtime = {row["path"] for row in read_csv("EXECUTION_READ_PATHS.csv")}
    final = []
    for row in original:
        path = row["path"]
        category = row["category"]
        rationale = row["reason"]
        if path == "ROADMAP.md":
            category = "KEEP_NEXT_MILESTONE"
            rationale = "Decisión Lean: única documentación dedicada hallada del próximo hito Build Kit; no existe lectura runtime demostrada."
        elif is_bd(path):
            category = "KEEP_RUNTIME"
            rationale = "Decisión Lean: BD01/BD02 estable; CIL, catálogo, contrato, pruebas y benchmark visual se conservan."
        elif path in runtime:
            category = "KEEP_RUNTIME"
            rationale = "Lectura/import observado desde el runtime estable; conservar su ruta."
        elif path in immutable:
            category = "KEEP_GOVERNANCE"
            rationale = "Ruta atada a hash/procedencia/manifiesto autoritativo; conservar exactamente en esta ubicación."
        elif is_decided_visual_material(path):
            category = "ARCHIVE"
            rationale = "Decisión Lean: material visual sin lectura runtime ni vínculo hash/procedencia; archivable tras plan separado."
        final.append({
            **row,
            "final_category": category,
            "final_rationale": rationale,
            "immutable_hash_or_provenance": str(path in immutable).lower(),
            "runtime_read_or_import": str(path in runtime).lower(),
        })
    fields = list(final[0])
    write_csv("CLASSIFICATION_CANDIDATE.csv", final, fields)

    by_path = {row["path"]: row for row in final}
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in final:
        if row["final_category"] == "ARCHIVE":
            groups[archive_group(row["path"] )].append(row)
    risk_rows = []
    for folder, items in sorted(groups.items()):
        immutable_paths = [r["path"] for r in items if r["immutable_hash_or_provenance"] == "true"]
        runtime_paths = [r["path"] for r in items if r["runtime_read_or_import"] == "true"]
        status = "APTA_CON_PLAN_DE_RETIRO" if not immutable_paths and not runtime_paths else "NO_APTA"
        risk_rows.append({
            "group": folder,
            "archive_files": len(items),
            "bytes": sum(int(r["bytes"]) for r in items),
            "hash_or_provenance_bound": len(immutable_paths),
            "runtime_read_or_import": len(runtime_paths),
            "can_leave_main": status,
            "risk": "No route-level hash/provenance or runtime read in this candidate group." if status.startswith("APTA") else "Contains immutable or runtime paths; retain in main.",
            "paths": " | ".join(r["path"] for r in items),
        })
    write_csv(
        "ARCHIVE_EXIT_CANDIDATES.csv",
        risk_rows,
        ["group", "archive_files", "bytes", "hash_or_provenance_bound", "runtime_read_or_import", "can_leave_main", "risk", "paths"],
    )

    build_kit = [r for r in final if r["final_category"] == "KEEP_NEXT_MILESTONE"]
    report = {
        "status": "CERRADO",
        "decisions_applied": {
            "reference_assets_r2b_outputs": "Keep only runtime or immutable hash/provenance paths; classify remaining visual material ARCHIVE.",
            "build_kit": "KEEP_NEXT_MILESTONE; dedicated material identified in ROADMAP.md. Nominal 1:64 occurrences under BD01/BD02 remain KEEP_RUNTIME.",
            "bd01_bd02": "KEEP_RUNTIME including requested catalog, specification, tests, schema and visual validation artifacts.",
            "archive_pinterest_maps": "No reclassification to ARCHIVE solely from name; preserve pending provenance triage.",
        },
        "build_kit": {
            "files": [r["path"] for r in build_kit],
            "bytes": sum(int(r["bytes"]) for r in build_kit),
            "runtime_read_or_import": any(r["runtime_read_or_import"] == "true" for r in build_kit),
            "separation_proposal": "At a future authorized move, place un-hashed Build Kit-only documents under docs/build_kit/ and exclude that directory from the generation-chat attachment. Do not move ROADMAP.md or any path in UNTOUCHABLE_HASH_PROVENANCE.csv before replacing every recorded hash/reference.",
        },
        "archive_groups": len(risk_rows),
        "archive_groups_apta": sum(r["can_leave_main"].startswith("APTA") for r in risk_rows),
        "limits": [
            "This is a candidate classification, not an authorization to remove or move any path.",
            "A group can be functionally closed but retained because frozen hashes/provenance require its exact path.",
        ],
    }
    (OUT / "STEP2_ARCHIVE_RECONCILIATION.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
