"""python -m visual_scene_graph.pilot MANIFEST --output DIRECTORY [--generate]"""
import argparse
import json
import jsonschema
from pathlib import Path

from .harness import CommandGenerator, ROOT, execute, prepare


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--reviewed-delta', help='Hash of manifest + A/B payloads manually reviewed after dry run')
    parser.add_argument('--adapter-command', nargs='+', help='Trusted local argv speaking the documented JSON protocol')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        allowlist = json.loads((ROOT/'visual_scene_graph/pilot/allowlist.json').read_text())
        prepared = prepare(manifest, allowlist)
        generator = CommandGenerator(args.adapter_command, manifest['generation']['provider'], manifest['generation']['model']) if args.adapter_command else None
        path, report = execute(prepared, args.output, generator=generator, dry_run=not args.generate, reviewed_delta=args.reviewed_delta)
        print(json.dumps({'path':str(path), **report}, indent=2))
        return 1 if report['status'] == 'BLOCKED' or report['technical_failures'] else 0
    except (ValueError, OSError, KeyError, TypeError, jsonschema.ValidationError) as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
