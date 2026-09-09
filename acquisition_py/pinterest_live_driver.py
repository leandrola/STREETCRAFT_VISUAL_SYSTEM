#!/usr/bin/env python3
"""
Streetcraft Archive 1.0-F
Public Pinterest Live Acquisition Driver

Purpose:
- Resolve a public Pinterest board URL or pin.it short URL in a real browser.
- Scroll until the board stabilizes.
- Collect pin URLs and image candidates from the DOM.
- Emit a normalized connector snapshot.
- Never claim FULL unless completeness checks pass.

This driver intentionally performs ACQUISITION only.
Normalization and archive authority remain downstream responsibilities.
"""

from __future__ import annotations
import argparse
import asyncio
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

PIN_RE = re.compile(r"/pin/(\d+)")
PINIT_RE = re.compile(r"^https?://pin\.it/", re.I)

@dataclass
class AcquisitionDiagnostics:
    input_url: str
    resolved_url: str | None
    rounds: int
    stable_rounds: int
    unique_pin_count: int
    completeness: str
    completeness_reason: str
    page_title: str | None = None
    blocked_or_login: bool = False
    errors: list[str] | None = None

def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonicalize(url: str | None) -> str | None:
    if not url:
        return None
    u = url.strip()
    try:
        sp = urlsplit(u)
        return urlunsplit((sp.scheme.lower(), sp.netloc.lower(), sp.path.rstrip("/"), "", ""))
    except Exception:
        return u

def pin_id_from_url(url: str) -> str | None:
    m = PIN_RE.search(url or "")
    return m.group(1) if m else None

def choose_image(src: str | None, srcset: str | None) -> str | None:
    candidates: list[tuple[int, str]] = []
    if src:
        candidates.append((0, src))
    if srcset:
        for part in srcset.split(","):
            part = part.strip()
            if not part:
                continue
            bits = part.split()
            url = bits[0]
            score = 0
            if len(bits) > 1:
                dim = bits[1].lower()
                if dim.endswith("w") and dim[:-1].isdigit():
                    score = int(dim[:-1])
                elif dim.endswith("x"):
                    try:
                        score = int(float(dim[:-1]) * 1000)
                    except Exception:
                        pass
            candidates.append((score, url))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]

def make_record(pin_url: str, image_url: str | None, title: str | None,
                description: str | None, source_url: str | None,
                board_url: str, position: int) -> dict[str, Any]:
    pid = pin_id_from_url(pin_url)
    fp_source = "|".join([pid or "", canonicalize(pin_url) or "", canonicalize(image_url) or ""])
    return {
        "pin_id": pid,
        "pin_url": canonicalize(pin_url),
        "image_url": canonicalize(image_url),
        "source_url": canonicalize(source_url),
        "title": title.strip() if isinstance(title, str) and title.strip() else None,
        "description": description.strip() if isinstance(description, str) and description.strip() else None,
        "board_url": canonicalize(board_url),
        "position": position,
        "discovered_at": utcnow(),
        "fingerprint": hashlib.sha256(fp_source.encode("utf-8")).hexdigest()
    }

async def collect_from_page(page, board_url: str) -> list[dict[str, Any]]:
    raw = await page.evaluate(r"""
    () => {
      const rows = [];
      const seen = new Set();
      const anchors = Array.from(document.querySelectorAll('a[href*="/pin/"]'));
      for (const a of anchors) {
        let href;
        try { href = new URL(a.getAttribute('href'), location.href).href; }
        catch { continue; }
        const m = href.match(/\/pin\/(\d+)/);
        if (!m || seen.has(m[1])) continue;
        seen.add(m[1]);

        const img = a.querySelector('img') || a.closest('[data-test-id]')?.querySelector('img');
        const card = a.closest('[data-test-id]') || a.parentElement;
        const descNode = card?.querySelector('[data-test-id*="description"], [aria-label]');
        const sourceAnchor = card ? Array.from(card.querySelectorAll('a[href^="http"]'))
          .find(x => !x.href.includes('pinterest.') && !x.href.includes('/pin/')) : null;

        rows.push({
          pin_url: href,
          image_src: img?.currentSrc || img?.src || null,
          image_srcset: img?.getAttribute('srcset') || null,
          title: img?.alt || a.getAttribute('aria-label') || null,
          description: descNode?.textContent || null,
          source_url: sourceAnchor?.href || null
        });
      }
      return rows;
    }
    """)
    out = []
    for i, r in enumerate(raw):
        out.append(make_record(
            r.get("pin_url"),
            choose_image(r.get("image_src"), r.get("image_srcset")),
            r.get("title"),
            r.get("description"),
            r.get("source_url"),
            board_url,
            i
        ))
    return out

async def looks_blocked(page) -> bool:
    txt = (await page.locator("body").inner_text(timeout=5000)).lower()
    markers = [
        "log in to pinterest", "sign up to see more", "continue with google",
        "something went wrong", "we couldn't find", "rate limit"
    ]
    return any(m in txt for m in markers)

async def acquire(url: str, headless: bool, max_rounds: int, stable_target: int,
                  settle_ms: int, timeout_ms: int, executable_path: str | None) -> tuple[dict, AcquisitionDiagnostics]:
    try:
        from playwright.async_api import async_playwright
    except Exception as e:
        raise RuntimeError(
            "Playwright is required. Install with: pip install playwright && playwright install chromium"
        ) from e

    errors = []
    async with async_playwright() as p:
        launch_args = {"headless": headless}
        if executable_path:
            launch_args["executable_path"] = executable_path
        browser = await p.chromium.launch(**launch_args)
        ctx = await browser.new_context(
            viewport={"width": 1440, "height": 1100},
            locale="en-US",
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0 Safari/537.36")
        )
        page = await ctx.new_page()
        page.set_default_timeout(timeout_ms)

        try:
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(settle_ms)
        except Exception as e:
            errors.append(f"navigation: {e}")

        resolved = page.url
        title = None
        try:
            title = await page.title()
        except Exception:
            pass

        blocked = False
        try:
            blocked = await looks_blocked(page)
        except Exception:
            pass

        union: dict[str, dict] = {}
        stable = 0
        previous = -1
        rounds = 0

        for rounds in range(1, max_rounds + 1):
            try:
                records = await collect_from_page(page, resolved)
                for r in records:
                    key = r.get("pin_id") or r.get("pin_url")
                    if key:
                        union[key] = r
                count = len(union)
                if count == previous:
                    stable += 1
                else:
                    stable = 0
                previous = count
                if stable >= stable_target:
                    break
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(settle_ms)
            except Exception as e:
                errors.append(f"round_{rounds}: {e}")
                break

        # We can verify stability, but Pinterest does not expose a reliable public total.
        # Therefore default is PARTIAL unless a total-count hint can be independently verified.
        total_hint = None
        try:
            total_hint = await page.evaluate(r"""
            () => {
              const body = document.body.innerText || '';
              const m = body.match(/([\d,]+)\s+Pins?\b/i);
              return m ? parseInt(m[1].replace(/,/g,''), 10) : null;
            }
            """)
        except Exception:
            pass

        count = len(union)
        if blocked:
            completeness = "PARTIAL"
            reason = "Pinterest login/block/interstitial detected."
        elif total_hint is not None and count >= total_hint and stable >= stable_target:
            completeness = "FULL"
            reason = f"Observed {count} unique pins, satisfying visible total hint {total_hint}, after stabilization."
        else:
            completeness = "PARTIAL"
            reason = (
                "Enumeration stabilized but no independently verifiable board total was available. "
                "Safety policy forbids claiming FULL from scroll stability alone."
            )

        items = list(union.values())
        items.sort(key=lambda x: x.get("position", 0))
        for idx, item in enumerate(items):
            item["position"] = idx

        snapshot = {
            "connector": "pinterest_public_board",
            "snapshot_version": "1.0-F",
            "requested_url": url,
            "board_url": canonicalize(resolved),
            "captured_at": utcnow(),
            "enumeration_mode": completeness,
            "items": items,
            "diagnostics": {
                "visible_total_hint": total_hint,
                "rounds": rounds,
                "stable_rounds": stable,
                "blocked_or_login": blocked
            }
        }

        diag = AcquisitionDiagnostics(
            input_url=url,
            resolved_url=resolved,
            rounds=rounds,
            stable_rounds=stable,
            unique_pin_count=count,
            completeness=completeness,
            completeness_reason=reason,
            page_title=title,
            blocked_or_login=blocked,
            errors=errors or None
        )
        await browser.close()
        return snapshot, diag

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("-o", "--output", default="snapshot.json")
    ap.add_argument("--headed", action="store_true", help="Show browser window.")
    ap.add_argument("--max-rounds", type=int, default=80)
    ap.add_argument("--stable-rounds", type=int, default=5)
    ap.add_argument("--settle-ms", type=int, default=1800)
    ap.add_argument("--timeout-ms", type=int, default=30000)
    ap.add_argument("--chromium", help="Optional path to Chromium/Chrome executable.")
    args = ap.parse_args()

    snapshot, diag = asyncio.run(acquire(
        args.url, not args.headed, args.max_rounds, args.stable_rounds,
        args.settle_ms, args.timeout_ms, args.chromium
    ))
    Path(args.output).write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(asdict(diag), indent=2, ensure_ascii=False))
    print(f"Wrote: {args.output}", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
