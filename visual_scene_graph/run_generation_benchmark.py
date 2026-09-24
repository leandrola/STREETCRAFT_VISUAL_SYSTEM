"""VSG-2A reproducible shadow benchmark, artifact comparison and QA verification.

python -m visual_scene_graph.run_generation_benchmark
python -m visual_scene_graph.run_generation_benchmark --input snapshots.json --output report.json
python -m visual_scene_graph.run_generation_benchmark --verify validation/VSG_2A_GENERATION_COMPILER_QA.json
"""
import argparse
import hashlib
import json
from pathlib import Path

from .generation_compiler import ROOT, compile_generation_contract, digest
from .generation_comparator import compare_generation_contract, render_comparison
from .generation_cases import run_generation_cases, stored_cgc_snapshots

HASHED_FILES = [
    'visual_scene_graph/generation_compiler.py', 'visual_scene_graph/generation_comparator.py',
    'visual_scene_graph/generation_cases.py', 'visual_scene_graph/test_generation_compiler.py',
    'visual_scene_graph/run_generation_benchmark.py', 'visual_scene_graph/VSG_2A_GENERATION_COMPILER_SHADOW.md',
    'visual_scene_graph/fixtures/generation_compiler_cases.json', 'visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json',
    'schemas/vsg-generation-contract.schema.json', 'schemas/vsg-generation-comparison.schema.json',
    'schemas/compact-generation-contract.schema.json', 'schemas/visual-scene-graph-vsg0.schema.json',
    'schemas/visual-scene-graph-vsg1.schema.json', 'visual_scene_graph/vsg_observer.py',
    'visual_scene_graph/graph_locks.py', 'visual_scene_graph/causal_trace.py', 'visual_scene_graph/causal_cases.py',
    'visual_scene_graph/diagnostic_benchmark/diagnostic_engine.py',
    'visual_scene_graph/diagnostic_benchmark/run_benchmark.py',
    'scene_intelligence/scene_intelligence.py', 'hardening/operational_hardening.py',
    'integration/streetcraft_orchestrator.py', 'reference_runtime/reference_reasoning.py',
    'benchmark/run_regression_suite.py', 'benchmark/r2b_1_9_1/RUN_STATUS.json',
    'README.md', 'STREETCRAFT.md', 'ROADMAP.md', 'CHANGELOG.md', 'PACKAGE_MANIFEST.json',
]

HASHED_FILES += [f'validation/cgc_e2e/results/CGC-E2E-{i:02}.json' for i in range(1, 9)]

def file_hashes():
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in HASHED_FILES}


def build_report():
    report = run_generation_cases()
    report['stored_cgc_snapshots'] = stored_cgc_snapshots()
    if any(r['status'] == 'FAIL' for r in report['stored_cgc_snapshots']): report['status'] = 'FAIL'
    report['file_sha256'] = file_hashes()
    report['limitations'] = [
        'Structured snapshots only; no pixel extraction or generation authority.',
        'VSG-1 lacks priorities/actions and global policies: SAR2 and an explicit generation_context are mandatory.',
        'Global policies are explicit passthroughs; semantic scene preservation is independently compared against stable CGC.',
        'Stable CGC omits node attributes and Graph Locks; immutable source VSG supplies those baseline restrictions.',
        'Opaque/free-text policies require exact content. Unsupported CGC fields and ambiguous mappings fail closed.',
        'Cardinality 1..1 denotes each unique source node occurrence; explicit property cardinalities are also retained.',
    ]
    report['qa_sha256'] = digest(report)
    return report


def verify_report(report):
    errors = []
    if report.get('file_sha256') != file_hashes(): errors.append('FILE_HASH_MISMATCH')
    if report.get('qa_sha256') != digest({k:v for k,v in report.items() if k!='qa_sha256'}): errors.append('QA_HASH_MISMATCH')
    replay = build_report()
    # Extra recorded regression evidence is permitted but remains digest-bound.
    for key, value in replay.items():
        if key != 'qa_sha256' and report.get(key) != value: errors.append('REPLAY_MISMATCH:' + key)
    return {'status': 'FAIL' if errors else 'PASS', 'errors': errors,
            'files_verified': len(HASHED_FILES), 'cases_verified': replay['cases']}


def compare_input(data):
    contract = compile_generation_contract(data['candidate_graph'], sar2=data['sar2'],
        generation_context=data['generation_context'], causal_trace=data.get('causal_trace'),
        trace_artifacts=data.get('trace_artifacts'))
    report = compare_generation_contract(data['stable_cgc'], contract, sar2=data['sar2'],
        expected_graph=data['expected_graph'], candidate_graph=data['candidate_graph'],
        generation_context=data['generation_context'], causal_trace=data.get('causal_trace'),
        trace_artifacts=data.get('trace_artifacts'))
    return {'status': report['status'], 'contract': contract, 'comparison': report,
            'summary': render_comparison(report)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument('--verify', type=Path)
    choice.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.verify:
        report = verify_report(json.loads(args.verify.read_text()))
    elif args.input:
        report = compare_input(json.loads(args.input.read_text()))
    else:
        report = build_report()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'results', 'contract', 'comparison', 'file_sha256', 'stored_cgc_snapshots'}}, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
