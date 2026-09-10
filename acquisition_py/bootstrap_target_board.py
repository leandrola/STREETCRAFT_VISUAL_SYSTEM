#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
cmd = [
    sys.executable, str(ROOT / 'acquisition_py' / 'pinterest_live_driver.py'),
    'https://pin.it/5SbUv5Agi',
    '--canonical-url', 'https://ar.pinterest.com/leolaudicina/us-image-archive',
    '--expected-total', '536',
    '--profile-dir', str(ROOT / '.browser-profile'),
    '--bootstrap-login', '--headed',
    '-o', str(ROOT / 'snapshots' / 'target-board.snapshot.json')
]
raise SystemExit(subprocess.call(cmd))
