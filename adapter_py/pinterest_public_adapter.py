"""Streetcraft Archive 1.0-E public Pinterest normalization layer.

Network/browser acquisition is intentionally separate. This module normalizes
structured Pinterest-like records or embedded JSON already acquired by an
authorized runtime.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

TRACKING_KEYS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "source", "share_id", "invite_code"
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_url(url: str | None) -> str | None:
    if not url:
        return None
    try:
        p = urlsplit(url)
        q = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if k.lower() not in TRACKING_KEYS]
        return urlunsplit((p.scheme or "https", p.netloc, p.path, urlencode(q), ""))
    except Exception:
        return url


def canonical_pin_url(pin_id: str, candidate: str | None = None) -> str:
    if pin_id:
        return f"https://www.pinterest.com/pin/{pin_id}/"
    if candidate:
        return clean_url(candidate) or candidate
    raise ValueError("pin id or pin url required")


def extract_pin_id(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value)
    if s.isdigit():
        return s
    m = re.search(r"/pin/(?:[^/]*--)?(\d+)(?:/|$)", s)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{6,})\b", s)
    return m.group(1) if m else None


def best_image_url(obj: dict[str, Any]) -> str | None:
    candidates: list[tuple[int, str]] = []
    for key in ("image_url", "image", "url"):
        v = obj.get(key)
        if isinstance(v, str) and v.startswith("http"):
            candidates.append((0, v))
    images = obj.get("images")
    if isinstance(images, dict):
        for _, rec in images.items():
            if isinstance(rec, dict):
                u = rec.get("url")
                if isinstance(u, str) and u.startswith("http"):
                    w = int(rec.get("width") or 0)
                    h = int(rec.get("height") or 0)
                    candidates.append((w * h, u))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return clean_url(candidates[0][1])


def nested_get(obj: dict[str, Any], *paths: str) -> Any:
    for p in paths:
        cur: Any = obj
        ok = True
        for part in p.split("."):
            if not isinstance(cur, dict) or part not in cur:
                ok = False
                break
            cur = cur[part]
        if ok and cur not in (None, ""):
            return cur
    return None


def normalize_pin(raw: dict[str, Any], board_url: str, position: int | None = None, discovered_at: str | None = None) -> dict[str, Any] | None:
    pin_id = extract_pin_id(nested_get(raw, "id", "pin_id", "provider_item_id", "url", "pin_url"))
    pin_url = nested_get(raw, "pin_url", "url", "link")
    if not pin_id and pin_url:
        pin_id = extract_pin_id(pin_url)
    image_url = best_image_url(raw)
    if not pin_id or not image_url:
        return None
    source_url = nested_get(raw, "source_url", "link", "domain_metadata.link")
    if source_url == pin_url:
        source_url = None
    title = nested_get(raw, "title", "grid_title", "rich_summary.display_name")
    description = nested_get(raw, "description", "description_html", "seo_description")
    out = {
        "provider": "pinterest",
        "provider_item_id": pin_id,
        "pin_url": canonical_pin_url(pin_id, pin_url),
        "image_url": image_url,
        "source_url": clean_url(source_url) if isinstance(source_url, str) else None,
        "title": str(title).strip() if title else None,
        "description": str(description).strip() if description else None,
        "board_url": clean_url(board_url) or board_url,
        "position": position,
        "discovered_at": discovered_at or utc_now_iso(),
        "provider_updated_at": nested_get(raw, "updated_at", "provider_updated_at"),
        "content_fingerprint": sha256((pin_id + "|" + image_url).encode("utf-8")).hexdigest()
    }
    return out


def normalize_records(records: Iterable[dict[str, Any]], board_url: str, discovered_at: str | None = None) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pos, raw in enumerate(records):
        pin = normalize_pin(raw, board_url=board_url, position=pos, discovered_at=discovered_at)
        if not pin:
            continue
        if pin["provider_item_id"] in seen:
            continue
        seen.add(pin["provider_item_id"])
        result.append(pin)
    return result


def walk_json_for_pin_candidates(root: Any) -> list[dict[str, Any]]:
    """Conservative recursive candidate discovery for already acquired JSON."""
    out: list[dict[str, Any]] = []
    stack = [root]
    visited = 0
    while stack:
        cur = stack.pop()
        visited += 1
        if visited > 250000:
            break
        if isinstance(cur, dict):
            pid = extract_pin_id(cur.get("id") or cur.get("pin_id") or cur.get("url"))
            if pid and best_image_url(cur):
                out.append(cur)
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return out


def extract_embedded_json(html: str) -> list[Any]:
    """Extract JSON script blocks from saved/rendered HTML.

    Pinterest markup changes; this is a normalization aid, not a promise that
    every live page exposes complete board state in HTML.
    """
    payloads: list[Any] = []
    for m in re.finditer(r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>', html, flags=re.I | re.S):
        text = m.group(1).strip()
        if not text:
            continue
        try:
            payloads.append(json.loads(text))
        except json.JSONDecodeError:
            pass
    return payloads


def pins_from_html(html: str, board_url: str, discovered_at: str | None = None) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for payload in extract_embedded_json(html):
        candidates.extend(walk_json_for_pin_candidates(payload))
    return normalize_records(candidates, board_url=board_url, discovered_at=discovered_at)


def build_connector_snapshot(pins: list[dict[str, Any]], *, board_locator: str, canonical_board_url: str | None, enumeration_type: str, acquisition_method: str, complete: bool, diagnostics: list[str] | None = None, acquired_at: str | None = None) -> dict[str, Any]:
    enumeration_type = enumeration_type.upper()
    if enumeration_type == "FULL" and not complete:
        raise ValueError("FULL snapshot requires verified complete enumeration")
    if enumeration_type not in {"FULL", "PARTIAL", "DELTA"}:
        raise ValueError("invalid enumeration type")
    return {
        "provider": "pinterest",
        "board_locator": board_locator,
        "canonical_board_url": canonical_board_url,
        "enumeration_type": enumeration_type,
        "complete": bool(complete),
        "acquired_at": acquired_at or utc_now_iso(),
        "acquisition_method": acquisition_method,
        "diagnostics": diagnostics or [],
        "items": pins
    }
