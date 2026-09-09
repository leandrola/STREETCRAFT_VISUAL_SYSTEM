#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
driver = ROOT / "acquisition_py" / "pinterest_live_driver.py"
out = ROOT / "snapshots" / "target-board.snapshot.json"
out.parent.mkdir(exist_ok=True)

cmd = [sys.executable, str(driver), "https://pin.it/5SbUv5Agi", "-o", str(out)]
raise SystemExit(subprocess.call(cmd))
