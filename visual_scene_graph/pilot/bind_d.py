"""Prospective D snapshot construction/replay; never admits or generates images."""
from copy import deepcopy
import argparse
import json

from integration.streetcraft_orchestrator import orchestrate
from ..generation_compiler import DIRECTIVES, POLICIES, compile_generation_contract, digest
from ..generation_comparator import compare_generation_contract
from ..vsg_observer import build_visual_scene_graph
from .harness import ROOT, image_valid, sha, validate

FIXTURE = ROOT / 'visual_scene_graph/pilot/fixtures/r2b_d_new_01'


def empty_retriever(request):
    raise ValueError('UNEXPECTED_ARCHIVE_QUERY: D has no reference needs')


def reconstruct():
    request = json.loads((FIXTURE / 'request.json').read_text())
    provenance = json.loads((FIXTURE / 'source_provenance.json').read_text())
    source = provenance['source']
    raw = (ROOT / source['path']).read_bytes()
    if sha(raw) != source['sha256']:
        raise ValueError('SOURCE_HASH_MISMATCH')
    dimensions = image_valid(raw)
    if dimensions != {'format': 'JPEG', 'width': 347, 'height': 389}:
        raise ValueError('SOURCE_DIMENSIONS_MISMATCH')
    runtime = orchestrate(request, archive_retriever=empty_retriever)
    if runtime['status'] != 'GENERATION_READY' or runtime['pre_generation_gate']['status'] != 'PASS':
        raise ValueError('ORCHESTRATION_NOT_READY')
    if runtime['reference_needs'] or runtime['reference_reasoning']['generation_projection']:
        raise ValueError('UNEXPECTED_REFERENCE_NEEDS')
    cgc, sar2 = runtime['cgc_final'], runtime['sar2']
    graph = build_visual_scene_graph(sar2, reference_reasoning=runtime['reference_reasoning'],
                                     reference_needs=runtime['reference_needs'])
    context = {'policies': {k: deepcopy(v) for k, v in cgc.items() if k in POLICIES},
               'directives': {k: deepcopy(request.get(k, [])) for k in DIRECTIVES}}
    contract = compile_generation_contract(graph, sar2=sar2, generation_context=context)
    candidate = deepcopy(graph)  # Equivalent input encoding, never an observed output graph.
    comparison = compare_generation_contract(cgc, contract, sar2=sar2,
        expected_graph=graph, candidate_graph=candidate, generation_context=context)
    if comparison['status'] != 'PASS' or comparison['unresolved_required_mappings']:
        raise ValueError('COMPARISON_FAILED:' + repr(comparison['issues']))
    for priority in ('P0', 'PR0', 'PR1', 'LOCK'):
        c = comparison['coverage'][priority]
        if not c['required'] or c['required'] != c['preserved']:
            raise ValueError('EMPTY_OR_INCOMPLETE_COVERAGE:' + priority)
    return {'runtime': runtime, 'sar2': sar2, 'rr2': runtime['reference_reasoning'],
            'cgc_final': cgc, 'expected_graph': graph, 'candidate_graph': candidate,
            'generation_context': context, 'contract': contract}, comparison


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true', help='Create missing snapshots exclusively; never overwrite')
    args = parser.parse_args()
    data, comparison = reconstruct()
    for name, value in data.items():
        path = FIXTURE / (name + '.json')
        if args.freeze:
            with path.open('x') as handle:
                json.dump(value, handle, indent=2, ensure_ascii=False)
                handle.write('\n')
        elif json.loads(path.read_text()) != value:
            raise ValueError('REPLAY_MISMATCH:' + name)
    if not args.freeze:
        manifest = json.loads((FIXTURE / 'manifest.json').read_text())
        validate(manifest, 'manifest')
        for name, record in manifest['artifacts'].items():
            if sha((ROOT / record['path']).read_bytes()) != record['sha256']:
                raise ValueError('ARTIFACT_HASH_MISMATCH:' + name)
        print(json.dumps({'status': 'PASS', 'manifest_sha256': digest(manifest),
                          'coverage': comparison['coverage'], 'archive_calls': 0}))
    else:
        print(json.dumps({'status': 'FROZEN', 'coverage': comparison['coverage'], 'archive_calls': 0}))


if __name__ == '__main__':
    main()
