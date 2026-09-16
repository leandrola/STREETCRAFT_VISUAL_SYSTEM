#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run_py(rel,args=None,cwd=None):
    cmd=[sys.executable,str(ROOT/rel)]+(args or [])
    r=subprocess.run(cmd,cwd=str(cwd or ROOT),capture_output=True,text=True)
    return {"name":rel,"status":"PASS" if r.returncode==0 else "FAIL","stdout":r.stdout.strip(),"stderr":r.stderr.strip(),"returncode":r.returncode}

def hash_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive-root")
    ap.add_argument("--output",default=str(ROOT/"validation/REGRESSION_REPORT_1_8_1.json"))
    args=ap.parse_args()

    checks=[]

    required=[
      "command_invocation/resolve_commands.py",
      "hardening/operational_hardening.py",
      "reference_runtime/archive_aware_runtime.py",
      "benchmark/BENCHMARK_CASES.json",
      "benchmark/fixtures/GOLDEN_FIXTURES.json"
    ]
    missing=[x for x in required if not (ROOT/x).exists()]
    checks.append({"name":"required_modules","status":"PASS" if not missing else "FAIL","missing":missing})

    json_errors=[]
    for p in ROOT.rglob("*.json"):
        try: json.loads(p.read_text(encoding="utf-8"))
        except Exception as e: json_errors.append({"file":str(p.relative_to(ROOT)),"error":str(e)})
    checks.append({"name":"json_integrity","status":"PASS" if not json_errors else "FAIL","errors":json_errors})

    baseline=json.loads((ROOT/"benchmark/baselines/GOVERNING_FILES_1_7_BASELINE.json").read_text())["files"]
    drift=[]
    for rel,expected in baseline.items():
        p=ROOT/rel
        actual=hash_file(p) if p.exists() else None
        if actual!=expected:
            drift.append({"file":rel,"expected":expected,"actual":actual})
    checks.append({"name":"governing_file_drift","status":"PASS" if not drift else "FAIL","drift":drift})

    fixture_manifest=json.loads((ROOT/"benchmark/fixtures/GOLDEN_FIXTURES.json").read_text())
    bad=[]
    for f in fixture_manifest["fixtures"]:
        p=ROOT/f["path"]
        actual=hash_file(p) if p.exists() else None
        if actual!=f["sha256"]:
            bad.append({"fixture":f["fixture_id"],"path":f["path"],"expected":f["sha256"],"actual":actual})
    checks.append({"name":"golden_fixture_integrity","status":"PASS" if not bad else "FAIL","failures":bad})

    tests=[
      run_py("benchmark/check_r2_baseline.py",cwd=ROOT),
      run_py("command_invocation/test_commands.py",cwd=ROOT/"command_invocation"),
      run_py("hardening/test_operational_hardening.py",cwd=ROOT/"hardening"),
      run_py("scene_intelligence/test_scene_intelligence.py",cwd=ROOT/"scene_intelligence"),
      run_py("reference_runtime/test_archive_aware_runtime.py",cwd=ROOT),
      run_py("validation/camera_routing/validate_matrix.py",cwd=ROOT),
      run_py("validation/camera_routing/validate_l3.py",cwd=ROOT),
    ]
    if args.archive_root:
        tests.append(run_py("reference_runtime/test_archive_v1_integration.py",[args.archive_root],cwd=ROOT))

    checks.extend(tests)
    automated_pass=all(x["status"]=="PASS" for x in checks)

    report={
      "suite":"SVS 1.8 Regression & Benchmark Suite",
      "R0_automated_regression":"PASS" if automated_pass else "FAIL",
      "R1_fixture_integrity":next(x["status"] for x in checks if x["name"]=="golden_fixture_integrity"),
      "R2a_visual_baseline":"PASS" if next((x for x in checks if x.get("name")=="benchmark/check_r2_baseline.py"),{"status":"FAIL"})["status"]=="PASS" else "FAIL",
      "R2b_candidate_regression":"NOT_REQUIRED_FOR_FRAMEWORK_RELEASE",
      "release_gate":"PASS_FRAMEWORK_RELEASE" if automated_pass else "FAIL",
      "checks":checks
    }
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if automated_pass else 1)

if __name__=="__main__":
    main()
