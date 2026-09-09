"""Reference implementation of the Streetcraft Archive 1.0-D sync diff.

This module intentionally consumes a normalized connector snapshot. It does not
scrape Pinterest and does not assign documentary authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def provider_item_key(item: dict[str, Any]) -> str:
    ext = item.get("external_id")
    if ext:
        return f"id:{ext}"
    return "url:" + item["pin_url"].strip()


def source_fingerprint(item: dict[str, Any]) -> str:
    material = {
        "pin_url": item.get("pin_url"),
        "image_url": item.get("image_url"),
        "image_reference": item.get("image_reference"),
        "caption": item.get("caption"),
        "outbound_source_url": item.get("outbound_source_url"),
        "provider_updated_at": item.get("provider_updated_at"),
    }
    raw = json.dumps(material, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class DiffResult:
    new: list[dict[str, Any]]
    changed: list[dict[str, Any]]
    unchanged: list[dict[str, Any]]
    missing_keys: list[str]


def ensure_sync_tables(db: sqlite3.Connection) -> None:
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS sync_item_state (
          provider TEXT NOT NULL,
          provider_item_key TEXT NOT NULL,
          archive_id TEXT,
          source_fingerprint TEXT,
          content_fingerprint TEXT,
          provider_updated_at TEXT,
          first_seen_at TEXT NOT NULL,
          last_seen_at TEXT NOT NULL,
          last_run_id TEXT,
          runtime_status TEXT NOT NULL DEFAULT 'DISCOVERED',
          PRIMARY KEY (provider, provider_item_key)
        );
        """
    )


def diff_snapshot(db: sqlite3.Connection, snapshot: dict[str, Any]) -> DiffResult:
    ensure_sync_tables(db)
    provider = snapshot["provider"]
    rows = db.execute(
        "SELECT provider_item_key, source_fingerprint FROM sync_item_state WHERE provider = ?",
        (provider,),
    ).fetchall()
    known = {k: fp for k, fp in rows}

    new, changed, unchanged = [], [], []
    seen_keys: set[str] = set()
    for item in snapshot["items"]:
        key = provider_item_key(item)
        seen_keys.add(key)
        fp = source_fingerprint(item)
        enriched = dict(item)
        enriched["provider_item_key"] = key
        enriched["source_fingerprint"] = fp
        if key not in known:
            new.append(enriched)
        elif known[key] != fp:
            changed.append(enriched)
        else:
            unchanged.append(enriched)

    missing = []
    if snapshot["enumeration_mode"] == "FULL":
        missing = sorted(set(known) - seen_keys)

    return DiffResult(new, changed, unchanged, missing)


def apply_seen_state(db: sqlite3.Connection, snapshot: dict[str, Any], diff: DiffResult, run_id: str) -> None:
    now = snapshot.get("enumerated_at") or utcnow()
    provider = snapshot["provider"]
    for item in diff.new + diff.changed + diff.unchanged:
        key = item["provider_item_key"]
        existing = db.execute(
            "SELECT first_seen_at, archive_id FROM sync_item_state WHERE provider=? AND provider_item_key=?",
            (provider, key),
        ).fetchone()
        first_seen = existing[0] if existing else now
        archive_id = existing[1] if existing else None
        status = "CLASSIFICATION_PENDING" if item in diff.new + diff.changed else "INDEXED"
        db.execute(
            """
            INSERT INTO sync_item_state(provider, provider_item_key, archive_id, source_fingerprint,
              provider_updated_at, first_seen_at, last_seen_at, last_run_id, runtime_status)
            VALUES(?,?,?,?,?,?,?,?,?)
            ON CONFLICT(provider, provider_item_key) DO UPDATE SET
              source_fingerprint=excluded.source_fingerprint,
              provider_updated_at=excluded.provider_updated_at,
              last_seen_at=excluded.last_seen_at,
              last_run_id=excluded.last_run_id,
              runtime_status=excluded.runtime_status
            """,
            (provider, key, archive_id, item["source_fingerprint"], item.get("provider_updated_at"),
             first_seen, now, run_id, status),
        )
    db.commit()


def load_snapshot(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_diff(db_path: str | Path, snapshot_path: str | Path) -> dict[str, Any]:
    snapshot = load_snapshot(snapshot_path)
    run_id = "SYNC-" + uuid.uuid4().hex[:12].upper()
    with sqlite3.connect(db_path) as db:
        diff = diff_snapshot(db, snapshot)
        apply_seen_state(db, snapshot, diff, run_id)
    return {
        "run_id": run_id,
        "provider": snapshot["provider"],
        "board_url": snapshot["board_url"],
        "enumeration_mode": snapshot["enumeration_mode"],
        "counts": {
            "seen": len(snapshot["items"]),
            "new": len(diff.new),
            "changed": len(diff.changed),
            "unchanged": len(diff.unchanged),
            "missing": len(diff.missing_keys),
            "failed": 0,
        },
        "new_keys": [x["provider_item_key"] for x in diff.new],
        "changed_keys": [x["provider_item_key"] for x in diff.changed],
        "missing_keys": diff.missing_keys,
    }
