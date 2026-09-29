"""Small shared replay boundary for explicitly selected prospective fixtures."""
import json

from .harness import ROOT, sha, validate

FIXTURE_PATHS = {
    'R2B-191-D': ROOT / 'visual_scene_graph/pilot/fixtures/r2b_d_new_01',
    'R2B-191-E': ROOT / 'visual_scene_graph/pilot/fixtures/r2b_e_new_01',
}


def verify_snapshots(fixture, reconstruct):
    snapshots, comparison = reconstruct()
    for name, value in snapshots.items():
        if json.loads((fixture / (name + '.json')).read_text()) != value:
            raise ValueError('PROSPECTIVE_REPLAY_MISMATCH:' + name)
    manifest = json.loads((fixture / 'manifest.json').read_text())
    validate(manifest, 'manifest')
    for name, record in manifest['artifacts'].items():
        path = (ROOT / record['path']).resolve()
        if not path.is_relative_to(ROOT) or sha(path.read_bytes()) != record['sha256']:
            raise ValueError('ARTIFACT_HASH_MISMATCH:' + name)
    return manifest, comparison
