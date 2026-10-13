#!/usr/bin/env python3
"""Bounded local supervisor for SC-MULTIAGENT-03.

Operational files live under .git/sc-supervisor and never replace CHECKPOINT.json.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "development/coordination/CHECKPOINT.json"
STATE = ROOT / ".git/sc-supervisor"
LOCK = STATE / "supervisor.lock"
ACTIVE = STATE / "active.json"
RUNS = STATE / "runs"
TERMINAL = {"COMPLETED", "FAILED", "TIMED_OUT", "STOPPED", "BLOCKED", "ORPHANED_OR_UNKNOWN"}


class SupervisorError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def checkpoint() -> dict:
    return json.loads(CHECKPOINT.read_text(encoding="utf-8"))


def envelope_checkpoint_digest(data: dict, envelope_id: str) -> str:
    projected = json.loads(json.dumps(data))
    projected["milestones"]["SC-MULTIAGENT-03"]["envelopes"][envelope_id]["checkpoint_sha256"] = "<SELF>"
    encoded = json.dumps(projected, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def envelope(envelope_id: str) -> dict:
    data = checkpoint()
    envelopes = data.get("milestones", {}).get("SC-MULTIAGENT-03", {}).get("envelopes", {})
    if envelope_id not in envelopes:
        raise SupervisorError("ENVELOPE_NOT_FOUND")
    item = envelopes[envelope_id]
    required = {
        "objective", "tasks", "base_commit", "checkpoint_sha256", "orchestrator_model",
        "implementer_model", "verifier_model", "max_codex_turns", "max_wall_seconds",
        "max_subagents", "max_open_implementations", "max_commits", "push", "additional_spend",
        "max_images", "stop_conditions", "resume_policy", "prompt"
    }
    if required - set(item):
        raise SupervisorError("ENVELOPE_INVALID")
    if not item["tasks"] or item["max_codex_turns"] < 1 or item["max_wall_seconds"] < 1:
        raise SupervisorError("ENVELOPE_INVALID")
    task_ids = [task.get("task_id") for task in item["tasks"]]
    if None in task_ids or len(set(task_ids)) != len(task_ids):
        raise SupervisorError("ENVELOPE_INVALID_TASKS")
    known = set(task_ids)
    if any(not set(task.get("depends_on", [])) <= known for task in item["tasks"]):
        raise SupervisorError("DEPENDENCY_INCOMPLETE")
    if item["max_images"] != 0 or item["additional_spend"] != 0:
        raise SupervisorError("ENVELOPE_OUT_OF_SCOPE")
    if item["max_subagents"] > 3 or item["max_open_implementations"] > 2:
        raise SupervisorError("ENVELOPE_OUT_OF_SCOPE")
    if item["base_commit"] != git("rev-parse", "HEAD"):
        raise SupervisorError("BASE_MISMATCH")
    if item["checkpoint_sha256"] != envelope_checkpoint_digest(data, envelope_id):
        raise SupervisorError("CHECKPOINT_MISMATCH")
    return item


def lock_file():
    STATE.mkdir(parents=True, exist_ok=True)
    handle = LOCK.open("a+", encoding="utf-8")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        handle.close()
        raise SupervisorError("ALREADY_RUNNING") from exc
    return handle


def process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def terminate_group(pid: int, grace: float, alive=process_alive) -> tuple[str, bool]:
    for sig, label in ((signal.SIGINT, "INTERRUPTED"), (signal.SIGTERM, "TERMINATED")):
        try:
            os.killpg(pid, sig)
        except ProcessLookupError:
            return label, False
        except PermissionError:
            return "SIGNAL_PERMISSION_BLOCKED", True
        deadline = time.monotonic() + grace
        while time.monotonic() < deadline:
            if not alive(pid):
                return label, False
            time.sleep(0.05)
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        return "KILLED", False
    except PermissionError:
        return "SIGNAL_PERMISSION_BLOCKED", True
    time.sleep(0.05)
    return "KILLED", alive(pid)


def codex_command(model: str) -> list[str]:
    binary = os.environ.get("SC_CODEX_BIN", "codex")
    return [binary, "-a", "never", "exec", "--json", "--strict-config", "-m", model,
            "-s", "read-only", "-C", str(ROOT), "-"]


def run_start(args: argparse.Namespace) -> int:
    lock = lock_file()
    try:
        item = envelope(args.envelope)
        command = json.loads(args.executor_json) if args.executor_json else codex_command(item["orchestrator_model"])
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            raise SupervisorError("EXECUTOR_INVALID")
        run_id = str(uuid.uuid4())
        task_key = hashlib.sha256((args.envelope + "\0" + item["base_commit"] + "\0" +
                                   json.dumps(item["tasks"], sort_keys=True)).encode()).hexdigest()
        run_dir = RUNS / run_id
        run_dir.mkdir(parents=True)
        output_path = run_dir / "events.jsonl"
        error_path = run_dir / "stderr.log"
        started_wall = time.time()
        started_mono = time.monotonic()
        with output_path.open("w", encoding="utf-8") as output, error_path.open("w", encoding="utf-8") as error:
            proc = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.PIPE, stdout=output, stderr=error,
                                    text=True, start_new_session=True)
            meta = {"run_id": run_id, "envelope_id": args.envelope, "task_key": task_key,
                    "pid": proc.pid, "started_at_epoch": started_wall, "status": "RUNNING",
                    "base_commit": item["base_commit"], "checkpoint_sha256": item["checkpoint_sha256"],
                    "invocations": 1, "max_codex_turns": item["max_codex_turns"],
                    "max_wall_seconds": item["max_wall_seconds"], "usage": "UNKNOWN"}
            atomic_json(run_dir / "run.json", meta)
            atomic_json(ACTIVE, meta)
            assert proc.stdin is not None
            proc.stdin.write(item["prompt"])
            proc.stdin.close()
            timed_out = False
            orphaned = False
            try:
                proc.wait(timeout=item["max_wall_seconds"])
            except subprocess.TimeoutExpired:
                timed_out = True
                _, orphaned = terminate_group(proc.pid, args.grace_seconds, alive=lambda _: proc.poll() is None)
                if not orphaned:
                    proc.wait(timeout=max(args.grace_seconds, 0.2))
        elapsed = time.monotonic() - started_mono
        events = []
        for line in output_path.read_text(encoding="utf-8").splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                events.append({"type": "invalid_jsonl"})
        completed = any(event.get("type") == "turn.completed" for event in events)
        head_matches = item["base_commit"] == git("rev-parse", "HEAD")
        checkpoint_matches = item["checkpoint_sha256"] == envelope_checkpoint_digest(checkpoint(), args.envelope)
        if orphaned:
            status = "ORPHANED_OR_UNKNOWN"
        elif timed_out:
            status = "TIMED_OUT"
        elif not head_matches or not checkpoint_matches:
            status = "BLOCKED"
        elif proc.returncode == 0 and completed:
            status = "COMPLETED"
        else:
            status = "FAILED"
        meta.update({"status": status, "exit_code": proc.returncode, "elapsed_seconds": elapsed,
                     "turn_completed_event": completed, "head_matches": head_matches,
                     "checkpoint_matches": checkpoint_matches, "finished_at_epoch": time.time()})
        atomic_json(run_dir / "run.json", meta)
        atomic_json(ACTIVE, meta)
        print(json.dumps(meta, sort_keys=True))
        return 0 if status == "COMPLETED" else 2
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()


def read_active() -> dict:
    if not ACTIVE.exists():
        raise SupervisorError("NO_RUN")
    return json.loads(ACTIVE.read_text(encoding="utf-8"))


def run_status(_: argparse.Namespace) -> int:
    active = read_active()
    observed = dict(active)
    observed["process_alive"] = process_alive(active["pid"]) if active["status"] == "RUNNING" else False
    observed["checkpoint_observed_sha256"] = sha256(CHECKPOINT)
    observed["checkpoint_projection_matches"] = active["checkpoint_sha256"] == envelope_checkpoint_digest(
        checkpoint(), active["envelope_id"])
    observed["head_observed"] = git("rev-parse", "HEAD")
    print(json.dumps({"checkpoint": checkpoint()["milestones"]["SC-MULTIAGENT-03"],
                      "process_observation": observed}, sort_keys=True))
    return 0


def run_stop(args: argparse.Namespace) -> int:
    active = read_active()
    if active["status"] != "RUNNING" or not process_alive(active["pid"]):
        print(json.dumps({"status": active["status"], "action": "NO_RUNNING_PROCESS"}))
        return 0
    action, orphaned = terminate_group(active["pid"], args.grace_seconds)
    active.update({"status": "ORPHANED_OR_UNKNOWN" if orphaned else "STOPPED",
                   "stop_action": action, "finished_at_epoch": time.time()})
    atomic_json(RUNS / active["run_id"] / "run.json", active)
    atomic_json(ACTIVE, active)
    print(json.dumps(active, sort_keys=True))
    return 2 if orphaned else 0


def run_reconcile(_: argparse.Namespace) -> int:
    active = read_active()
    result = {"run_id": active["run_id"], "status": active["status"], "relaunch": False,
              "head_matches": active["base_commit"] == git("rev-parse", "HEAD"),
              "checkpoint_matches": active["checkpoint_sha256"] == envelope_checkpoint_digest(checkpoint(), active["envelope_id"]),
              "action": "INSPECT_EVIDENCE_AND_CHECKPOINT; DO_NOT_RELAUNCH_AUTOMATICALLY"}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["head_matches"] and result["checkpoint_matches"] else 2


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start")
    start.add_argument("--envelope", required=True)
    start.add_argument("--executor-json", help="Explicit argv for a local fake executor in tests")
    start.add_argument("--grace-seconds", type=float, default=2.0)
    start.set_defaults(func=run_start)
    status = sub.add_parser("status"); status.set_defaults(func=run_status)
    stop = sub.add_parser("stop"); stop.add_argument("--grace-seconds", type=float, default=2.0); stop.set_defaults(func=run_stop)
    reconcile = sub.add_parser("reconcile"); reconcile.set_defaults(func=run_reconcile)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        return args.func(args)
    except (SupervisorError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
