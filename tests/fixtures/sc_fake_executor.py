#!/usr/bin/env python3
"""Local fake JSONL executor for SC supervisor behavior checks."""

import json
import sys

prompt = sys.stdin.read()
print(json.dumps({"type": "thread.started", "thread_id": "fake-readonly-thread"}), flush=True)
print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "READ_ONLY_PASS"},
                  "prompt_received": bool(prompt)}), flush=True)
print(json.dumps({"type": "turn.completed", "usage": "FAKE_NO_REMOTE_USAGE"}), flush=True)
