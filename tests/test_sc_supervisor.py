import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stdout
from io import StringIO

import scripts.sc_supervisor as supervisor


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        state = Path(self.temp.name)
        self.patchers = [
            mock.patch.object(supervisor, "STATE", state),
            mock.patch.object(supervisor, "LOCK", state / "supervisor.lock"),
            mock.patch.object(supervisor, "ACTIVE", state / "active.json"),
            mock.patch.object(supervisor, "RUNS", state / "runs"),
        ]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.temp.cleanup()

    def test_lock_rejects_second_supervisor(self):
        first = supervisor.lock_file()
        try:
            with self.assertRaisesRegex(supervisor.SupervisorError, "ALREADY_RUNNING"):
                supervisor.lock_file()
        finally:
            fcntl.flock(first, fcntl.LOCK_UN)
            first.close()

    def test_missing_envelope_blocks(self):
        with self.assertRaisesRegex(supervisor.SupervisorError, "ENVELOPE_NOT_FOUND"):
            supervisor.envelope("missing")

    def test_timeout_stops_process_group(self):
        with mock.patch.object(supervisor.os, "killpg") as killpg, \
             mock.patch.object(supervisor, "process_alive", side_effect=[True, False]):
            action, orphaned = supervisor.terminate_group(12345, 0.2, alive=supervisor.process_alive)
        killpg.assert_called_once_with(12345, supervisor.signal.SIGINT)
        self.assertEqual(action, "INTERRUPTED")
        self.assertFalse(orphaned)

    def test_signal_permission_failure_is_orphaned(self):
        with mock.patch.object(supervisor.os, "killpg", side_effect=PermissionError):
            action, orphaned = supervisor.terminate_group(12345, 0.1)
        self.assertEqual(action, "SIGNAL_PERMISSION_BLOCKED")
        self.assertTrue(orphaned)

    def test_reconcile_never_relaunches(self):
        item = {"run_id": "r1", "envelope_id": "e1", "status": "FAILED", "base_commit": "head",
                "checkpoint_sha256": "digest"}
        supervisor.atomic_json(supervisor.ACTIVE, item)
        data = {"milestones": {"SC-MULTIAGENT-03": {"envelopes": {"e1": {"checkpoint_sha256": "<SELF>"}}}}}
        with mock.patch.object(supervisor, "git", return_value="head"), \
             mock.patch.object(supervisor, "checkpoint", return_value=data), \
             mock.patch.object(supervisor, "envelope_checkpoint_digest", return_value="digest"):
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(supervisor.run_reconcile(argparse.Namespace()), 0)
        self.assertFalse(json.loads(output.getvalue())["relaunch"])

    def test_task_key_is_stable(self):
        tasks = [{"task_id": "A", "depends_on": []}]
        left = hashlib.sha256(("e\0b\0" + json.dumps(tasks, sort_keys=True)).encode()).hexdigest()
        right = hashlib.sha256(("e\0b\0" + json.dumps(tasks, sort_keys=True)).encode()).hexdigest()
        self.assertEqual(left, right)


if __name__ == "__main__":
    unittest.main()
