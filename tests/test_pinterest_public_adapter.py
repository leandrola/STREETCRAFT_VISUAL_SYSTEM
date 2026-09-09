import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "adapter_py"))

from pinterest_public_adapter import normalize_records, build_connector_snapshot, pins_from_html

FIX = ROOT / "tests" / "fixtures" / "pinterest_structured_records.json"


def test_normalize_structured_records():
    raw = json.loads(FIX.read_text())
    pins = normalize_records(raw, "https://www.pinterest.com/example/board/", discovered_at="2026-09-08T21:00:00Z")
    assert len(pins) == 2
    assert pins[0]["provider_item_id"] == "111111111111"
    assert pins[0]["pin_url"] == "https://www.pinterest.com/pin/111111111111/"
    assert pins[0]["image_url"].endswith("/originals/a/b/c.jpg")
    assert pins[0]["source_url"] == "https://example.org/archive/item1"


def test_full_guard():
    try:
        build_connector_snapshot([], board_locator="x", canonical_board_url=None, enumeration_type="FULL", acquisition_method="fixture", complete=False)
    except ValueError:
        pass
    else:
        raise AssertionError("FULL must require complete enumeration")


def test_partial_allowed():
    snap = build_connector_snapshot([], board_locator="x", canonical_board_url=None, enumeration_type="PARTIAL", acquisition_method="fixture", complete=False)
    assert snap["enumeration_type"] == "PARTIAL"


def test_embedded_json_html():
    html = '''<html><script type="application/json">{"resources":[{"id":"444444444444","images":{"orig":{"url":"https://i.pinimg.com/originals/x/y/z.jpg","width":800,"height":1200}}}]}</script></html>'''
    pins = pins_from_html(html, "https://www.pinterest.com/example/board/", discovered_at="2026-09-08T21:00:00Z")
    assert len(pins) == 1
    assert pins[0]["provider_item_id"] == "444444444444"
