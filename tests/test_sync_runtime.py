import importlib.util
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sync_runtime", ROOT / "runtime_py" / "sync_runtime.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_incremental_diff(tmp_path):
    dbp = tmp_path / "archive.db"
    s1 = ROOT / "examples" / "sync_snapshots" / "board-full-001.json"
    s2 = ROOT / "examples" / "sync_snapshots" / "board-full-002.json"
    r1 = mod.run_diff(dbp, s1)
    assert r1["counts"]["new"] == 2
    r2 = mod.run_diff(dbp, s2)
    assert r2["counts"]["new"] == 1
    assert r2["counts"]["changed"] == 1
    assert r2["counts"]["unchanged"] == 1
    assert r2["counts"]["missing"] == 0


def test_partial_never_marks_missing(tmp_path):
    dbp = tmp_path / "archive.db"
    full = mod.load_snapshot(ROOT / "examples" / "sync_snapshots" / "board-full-001.json")
    mod.run_diff(dbp, ROOT / "examples" / "sync_snapshots" / "board-full-001.json")
    partial = dict(full)
    partial["enumeration_mode"] = "PARTIAL"
    partial["items"] = partial["items"][:1]
    p = tmp_path / "partial.json"
    import json
    p.write_text(json.dumps(partial), encoding="utf-8")
    r = mod.run_diff(dbp, p)
    assert r["counts"]["missing"] == 0
