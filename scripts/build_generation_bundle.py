#!/usr/bin/env python3
"""Build the ignored, payload-only Streetcraft generation bundle."""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist/streetcraft-generation"
INVENTORY_REF = "cleanup/inventory"
EXECUTION_LIST = "development/cleanup/EXECUTION_READ_PATHS.csv"
EXCLUDED_PREFIXES = (
    "validation/", "benchmark/", "specs/", "development/", "legacy/",
    "release_decisions/", "visual_scene_graph/", "outputs/",
)
VSG_RUNTIME_EXCEPTION = {
    "visual_scene_graph/vsg_observer.py": "Imported unconditionally by integration/streetcraft_orchestrator.py.",
    "visual_scene_graph/graph_locks.py": "Imported by visual_scene_graph/vsg_observer.py.",
}
DOCUMENTATION_AND_CONTRACTS = {
    "STREETCRAFT.md", "CHEAT_SHEET.md", "agent/AGENT_PROTOCOL.md",
    "command_invocation/COMMAND_INVOCATION_LAYER.md",
    "command_invocation/CG_F_FRONTAL_ELEVATION.md",
    "command_invocation/BACKDROP_PRESETS.md",
    "scene_intelligence/SCENE_ANALYSIS_RECORD_V2.md",
    "scene_intelligence/SCENE_TO_CGC.md",
    "hardening/OPERATIONAL_HARDENING.md",
    "hardening/COMPACT_GENERATION_CONTRACT.md",
    "hardening/OCCLUSION_LOCKS.md",
    "patch/PATCH_RUNTIME_ORDER.md",
    "reference_runtime/REFERENCE_REASONING_2.md",
    "reference_runtime/ARCHIVE_AWARE_REFERENCE_RUNTIME.md",
    "schemas/compact-generation-contract.schema.json",
    "schemas/scene-analysis-record-v2.schema.json",
    "schemas/reference-need.schema.json",
    "schemas/evidence-admission.schema.json",
    "schemas/backdrop-contract.schema.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{INVENTORY_REF}:{path}"], cwd=ROOT)


def execution_paths() -> set[str]:
    return {row["path"] for row in csv.DictReader(git_show(EXECUTION_LIST).decode().splitlines())}


def all_modules() -> dict[str, list[str]]:
    modules: dict[str, list[str]] = {}
    for path in ROOT.rglob("*.py"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "dist/", ".venv", ".venv-sc/")):
            continue
        modules.setdefault(path.stem, []).append(rel)
    return modules


def local_imports(rel: str, modules: dict[str, list[str]]) -> set[str]:
    tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"), filename=rel)
    found: set[str] = set()
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [item.name for item in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module]
        for name in names:
            candidates = modules.get(name.split(".")[-1], [])
            if len(candidates) == 1:
                found.add(candidates[0])
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            # Explicit runtime reads in this runtime use sibling filenames.
            if re.fullmatch(r"[A-Za-z0-9_.-]+\.(?:json|jsonl|md)", node.value):
                sibling = (Path(rel).parent / node.value).as_posix()
                if (ROOT / sibling).is_file():
                    found.add(sibling)
    return found


def closure() -> tuple[set[str], dict[str, str], list[dict]]:
    seeds = execution_paths()
    modules = all_modules()
    reasons = {path: "execution_seed" for path in seeds}
    pending = list(seeds)
    while pending:
        current = pending.pop()
        if not current.endswith(".py"):
            continue
        for dependency in local_imports(current, modules):
            if dependency not in seeds:
                seeds.add(dependency)
                pending.append(dependency)
                reasons[dependency] = f"AST import or explicit sibling read from {current}"
    for path in DOCUMENTATION_AND_CONTRACTS:
        if not (ROOT / path).is_file():
            raise FileNotFoundError(path)
        seeds.add(path)
        reasons.setdefault(path, "generation documentation/contract/schema")
    excluded_hits = []
    for path in sorted(seeds):
        if path.startswith(EXCLUDED_PREFIXES):
            if path in VSG_RUNTIME_EXCEPTION:
                excluded_hits.append({"path": path, "allowed": True, "reason": VSG_RUNTIME_EXCEPTION[path]})
            else:
                excluded_hits.append({"path": path, "allowed": False, "reason": reasons[path]})
    return seeds, reasons, excluded_hits


def build() -> int:
    paths, reasons, excluded_hits = closure()
    rejected = [hit for hit in excluded_hits if not hit["allowed"]]
    if rejected:
        raise SystemExit(json.dumps({"status": "BLOCKED", "excluded_closure_hits": rejected}, indent=2))
    execution = execution_paths()
    unplanned = sorted(paths - execution)
    if len(unplanned) > 25:
        raise SystemExit(json.dumps({"status": "BLOCKED", "unplanned_count": len(unplanned), "limit": 25}, indent=2))
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    manifest = []
    for rel in sorted(paths):
        source = ROOT / rel
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        source_hash = sha256(source)
        copied_hash = sha256(target)
        if source_hash != copied_hash:
            raise RuntimeError(f"copy hash mismatch: {rel}")
        manifest.append({"path": rel, "source_path": rel, "sha256": source_hash, "bytes": source.stat().st_size, "reason": reasons[rel]})
    payload = {
        "format": "streetcraft-generation-bundle-v1",
        "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "payload_files": manifest,
        "manifest_self_excluded": "MANIFEST.json is metadata, not payload; self-hashing is recursive.",
        "excluded_closure_hits": excluded_hits,
        "unplanned_inclusions": [{"path": path, "reason": reasons[path]} for path in unplanned],
        "doubtful": [
            {"path": "reference_runtime/archive_v1_adapter.py", "hypothesis": "Required by the CLI for an external Archive root; dry run with archive_retriever=None does not execute that external runtime."},
            {"path": "visual_scene_graph/vsg_observer.py", "hypothesis": "Runtime dependency only; non-governing observer behavior remains unchanged."},
            {"path": "visual_scene_graph/graph_locks.py", "hypothesis": "Transitive runtime dependency of vsg_observer.py; no other VSG module is included."},
        ],
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "files": len(manifest), "bytes": sum(item["bytes"] for item in manifest), "unplanned": len(unplanned), "excluded_hits": excluded_hits}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
