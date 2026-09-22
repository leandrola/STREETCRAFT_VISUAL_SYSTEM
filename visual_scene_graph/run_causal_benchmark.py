"""Reproduce VSG-1.5 QA from controlled snapshots; no generation side effects.

Usage: python -m visual_scene_graph.run_causal_benchmark --output /path/qa.json
Verify a stored report: python -m visual_scene_graph.run_causal_benchmark --verify /path/qa.json
"""
import argparse
import hashlib
import json
from pathlib import Path

from .causal_cases import ROOT, run_causal_cases
from .causal_trace import canonical_sha256, validate_causal_trace

HASHED_FILES = [
    "visual_scene_graph/causal_trace.py", "visual_scene_graph/causal_cases.py",
    "visual_scene_graph/test_causal_trace.py", "visual_scene_graph/run_causal_benchmark.py",
    "visual_scene_graph/VSG_1_5_CAUSAL_TRACE.md", "visual_scene_graph/vsg_observer.py",
    "visual_scene_graph/graph_locks.py", "visual_scene_graph/diagnostic_benchmark/diagnostic_engine.py",
    "visual_scene_graph/diagnostic_benchmark/run_benchmark.py", "visual_scene_graph/diagnostic_benchmark/cases.json",
    "visual_scene_graph/fixtures/kennys_rooftop_vsg0.json", "visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json",
    "schemas/vsg-causal-trace.schema.json", "benchmark/run_regression_suite.py",
    "integration/streetcraft_orchestrator.py", "reference_runtime/reference_reasoning.py",
    "ROADMAP.md", "CHANGELOG.md", "README.md", "STREETCRAFT.md", "PACKAGE_MANIFEST.json",
]


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report():
    report = run_causal_cases()
    report["file_sha256"] = {path: file_hash(ROOT / path) for path in HASHED_FILES}
    report["limitations"] = [
        "Controlled structured snapshots; no pixel-level image understanding or real-image graph extraction.",
        "Diagnostic Benchmark defines primary-stage attribution. No production VSG-to-CGC compiler or generation authority.",
        "One deterministic primary cause; only connected downstream findings are symptoms. Independent findings remain separate.",
        "Unavailable or inconsistent inputs produce INCOMPLETE, not reconstructed stages or an invented root.",
        "Expected source graph and expected Graph Locks are caller-supplied evidence; confidence describes exact structured comparisons.",
    ]
    return report


def verify_report(report):
    errors = []
    if set(report.get("file_sha256", {})) != set(HASHED_FILES):
        errors.append("FILE_HASH_COVERAGE")
    for path, expected in report.get("file_sha256", {}).items():
        if path not in HASHED_FILES:
            continue
        if not (ROOT / path).is_file() or file_hash(ROOT / path) != expected:
            errors.append("FILE_HASH_MISMATCH:" + path)
    current = run_causal_cases()
    for key, value in current.items():
        if canonical_sha256(report.get(key)) != canonical_sha256(value):
            errors.append("BENCHMARK_REPLAY_MISMATCH:" + key)
    for row in report.get("results", []):
        result = validate_causal_trace(row["trace"], row["artifacts"])
        if result["status"] != "PASS":
            errors.append("INVALID_TRACE:" + row["case_id"])
    return {"status": "FAIL" if errors else "PASS", "errors": errors,
            "files_verified": len(report.get("file_sha256", {})), "traces_verified": len(report.get("results", []))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        result = verify_report(json.loads(args.verify.read_text()))
    else:
        report = build_report()
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        result = {k: v for k, v in report.items() if k not in {"results", "file_sha256"}}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
