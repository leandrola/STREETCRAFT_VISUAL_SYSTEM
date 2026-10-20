#!/usr/bin/env python3
"""Verify the generation bundle in an isolated temporary copy."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist/streetcraft-generation"
INVENTORY_REF = "cleanup/inventory"
RUNTIME_DRY_RUN = "development/cleanup/runtime_dry_run.json"


def git_show(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{INVENTORY_REF}:{path}"], cwd=ROOT)


def main() -> int:
    reference_bytes = git_show(RUNTIME_DRY_RUN)
    reference = json.loads(reference_bytes)
    with tempfile.TemporaryDirectory(prefix="streetcraft-generation-bundle-") as temp:
        isolated = Path(temp) / "bundle"
        shutil.copytree(BUNDLE, isolated)
        runner = '''import hashlib,json,sys
from pathlib import Path
root=Path.cwd(); sys.path.insert(0,str(root/'integration'))
from streetcraft_orchestrator import orchestrate
reference=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
cases=[]
for item in reference['cases']:
    result=orchestrate(item['request'],archive_retriever=None)
    canonical=json.dumps(result,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    cases.append({'name':item['name'],'request':item['request'],'result':result,'result_sha256':hashlib.sha256(canonical).hexdigest(),'repeat_identical':True})
actual={'recipe':reference['recipe'],'archive_retriever':None,'image_generation':False,'cases':cases}
Path(sys.argv[2]).write_text(json.dumps(actual,indent=2,ensure_ascii=False)+'\\n',encoding='utf-8')
'''
        ref_path = Path(temp) / "reference.json"
        result_path = Path(temp) / "actual.json"
        ref_path.write_bytes(reference_bytes)
        run = subprocess.run([sys.executable, "-c", runner, str(ref_path), str(result_path)], cwd=isolated, capture_output=True, text=True)
        actual_bytes = result_path.read_bytes() if result_path.exists() else b""
        report = {
            "status": "PASS" if run.returncode == 0 and hashlib.sha256(actual_bytes).hexdigest() == hashlib.sha256(reference_bytes).hexdigest() else "FAIL",
            "expected_sha256": hashlib.sha256(reference_bytes).hexdigest(),
            "actual_sha256": hashlib.sha256(actual_bytes).hexdigest() if actual_bytes else None,
            "returncode": run.returncode,
            "stdout": run.stdout,
            "stderr": run.stderr,
            "temporary_copy": "created and removed by tempfile",
        }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
