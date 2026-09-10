#!/usr/bin/env python3
"""
Streetcraft Archive 1.0-F4
Pinterest Acquisition Resolution + Enumeration Hardening

Purpose:
- preserve canonical board provenance
- enumerate the living board conservatively
- resolve the best reachable image asset for each pin
- never mark FULL unless enumeration quality is independently strong

No credentials are requested or stored by Streetcraft.
"""

from __future__ import annotations
import argparse, asyncio, hashlib, json, re, sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

PIN_RE = re.compile(r"/pin/(\d+)")
PINIMG_SIZE_RE = re.compile(
    r"(https?://i\.pinimg\.com)/(?:75x75_RS|136x136|170x|236x|474x|564x|736x)/",
    re.I
)
BLOCK_MARKERS = [
    "log in to pinterest", "sign up to see more",
    "continue with google", "continue with facebook",
    "something went wrong", "rate limit", "captcha"
]

@dataclass
class Diagnostics:
    input_url: str
    canonical_board_url: str
    resolved_url: str | None
    page_title: str | None
    rounds: int
    stable_rounds: int
    unique_pin_count: int
    visible_total_hint: int | None
    scroll_height_samples: list[int]
    blocked_or_login: bool
    persistent_profile_used: bool
    completeness: str
    completeness_reason: str
    resolution_stats: dict[str, int]
    errors: list[str] | None = None

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def canonicalize(url: str | None):
    if not url:
        return None
    sp = urlsplit(url.strip())
    return urlunsplit((sp.scheme.lower(), sp.netloc.lower(), sp.path.rstrip("/"), "", ""))

def pin_id_from_url(url: str | None):
    if not url: return None
    m = PIN_RE.search(url)
    return m.group(1) if m else None

def candidate_urls(url: str | None):
    if not url:
        return []
    vals = [url]
    if "i.pinimg.com" in url:
        vals.insert(0, PINIMG_SIZE_RE.sub(r"\1originals/", url, count=1))
        vals.append(PINIMG_SIZE_RE.sub(r"\1736x/", url, count=1))
        vals.append(PINIMG_SIZE_RE.sub(r"\1564x/", url, count=1))
    seen=[]
    for v in vals:
        if v and v not in seen:
            seen.append(v)
    return seen

async def reachable_image(request_ctx, url: str):
    try:
        r = await request_ctx.get(url, timeout=15000, fail_on_status_code=False)
        ctype = (r.headers.get("content-type") or "").lower()
        ok = 200 <= r.status < 400 and "image" in ctype
        size = int(r.headers.get("content-length") or "0")
        return ok, r.status, size
    except Exception:
        return False, 0, 0

async def best_image_url(request_ctx, dom_url: str | None):
    """
    Prefer originals when reachable, otherwise fall back to 736x/564x/DOM URL.
    This prevents dead /originals/ rewrites from entering the durable snapshot.
    """
    for cand in candidate_urls(dom_url):
        ok, status, size = await reachable_image(request_ctx, cand)
        if ok:
            tier = "originals" if "/originals/" in cand else (
                "736x" if "/736x/" in cand else (
                    "564x" if "/564x/" in cand else (
                        "236x" if "/236x/" in cand else "other"
                    )
                )
            )
            return cand, tier, status, size
    return dom_url, "unverified", 0, 0

async def body_text(page):
    try:
        return (await page.locator("body").inner_text(timeout=4000)).lower()
    except Exception:
        return ""

async def looks_blocked(page):
    txt = await body_text(page)
    return any(m in txt for m in BLOCK_MARKERS)

async def visible_total_hint(page):
    try:
        return await page.evaluate(r"""
        () => {
          const body = document.body.innerText || '';
          for (const p of [/([\d.,]+)\s+Pins?\b/i,/([\d.,]+)\s+pines?\b/i]) {
            const m = body.match(p);
            if (m) {
              const n = m[1].replace(/[.,](?=\d{3}\b)/g,'').replace(/[^\d]/g,'');
              if (n) return parseInt(n,10);
            }
          }
          return null;
        }
        """)
    except Exception:
        return None

async def dismiss_interstitials(page):
    sels = [
        'button[aria-label*="Close"]',
        'button[aria-label*="Cerrar"]',
        '[data-test-id="close-button"]',
        'div[role="dialog"] button'
    ]
    for sel in sels:
        try:
            loc = page.locator(sel)
            n = min(await loc.count(), 5)
            for i in range(n):
                try:
                    txt = (await loc.nth(i).inner_text(timeout=700)).strip().lower()
                except Exception:
                    txt = ""
                if txt in {"close","cerrar","x","not now","ahora no"} or not txt:
                    await loc.nth(i).click(timeout=1000)
                    await page.wait_for_timeout(300)
                    return
        except Exception:
            pass

async def collect_dom_rows(page):
    return await page.evaluate(r"""
    () => {
      const rows=[];
      const seen=new Set();
      for (const a of Array.from(document.querySelectorAll('a[href*="/pin/"]'))) {
        let href;
        try { href=new URL(a.getAttribute('href'), location.href).href; } catch { continue; }
        const m=href.match(/\/pin\/(\d+)/);
        if (!m || seen.has(m[1])) continue;
        seen.add(m[1]);
        const container=a.closest('[data-test-id]') || a.parentElement;
        const img=a.querySelector('img') || container?.querySelector('img');
        const src=img?.currentSrc || img?.src || null;
        const srcset=img?.getAttribute('srcset') || null;

        let best=src;
        if (srcset) {
          const opts=srcset.split(',').map(x=>x.trim().split(/\s+/)).filter(x=>x[0]);
          let bestScore=-1;
          for (const o of opts) {
            let s=0;
            if (o[1]?.endsWith('w')) s=parseInt(o[1])||0;
            if (o[1]?.endsWith('x')) s=Math.round((parseFloat(o[1])||0)*1000);
            if (s>bestScore) { bestScore=s; best=o[0]; }
          }
        }

        rows.push({
          pin_url: href,
          image_url: best,
          title: img?.alt || a.getAttribute('aria-label') || null,
          description: null
        });
      }
      return rows;
    }
    """)

def fingerprint(pin_id, pin_url, image_url):
    raw="|".join([pin_id or "", canonicalize(pin_url) or "", canonicalize(image_url) or ""])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

async def acquire(args):
    from playwright.async_api import async_playwright

    errors=[]
    async with async_playwright() as p:
        persistent=bool(args.profile_dir)
        if persistent:
            ctx=await p.chromium.launch_persistent_context(
                user_data_dir=args.profile_dir,
                headless=not args.headed,
                viewport={"width":1440,"height":1100},
                locale="en-US",
                executable_path=args.chromium or None,
            )
            browser=None
        else:
            browser=await p.chromium.launch(headless=not args.headed, executable_path=args.chromium or None)
            ctx=await browser.new_context(viewport={"width":1440,"height":1100}, locale="en-US")

        page=ctx.pages[0] if ctx.pages else await ctx.new_page()
        page.set_default_timeout(args.timeout_ms)

        target=args.canonical_url or args.url
        try:
            await page.goto(target, wait_until="domcontentloaded")
            await page.wait_for_timeout(args.settle_ms)
        except Exception as e:
            errors.append(f"navigation:{e}")

        await dismiss_interstitials(page)
        resolved=page.url
        try: title=await page.title()
        except Exception: title=None
        total_hint=await visible_total_hint(page)

        union={}
        stable=0
        previous=-1
        scroll_heights=[]
        rounds=0

        for rounds in range(1, args.max_rounds+1):
            await dismiss_interstitials(page)
            try:
                rows=await collect_dom_rows(page)
                for r in rows:
                    pid=pin_id_from_url(r["pin_url"])
                    if not pid: continue
                    if pid not in union:
                        union[pid]={
                            "pin_id":pid,
                            "pin_url":canonicalize(r["pin_url"]),
                            "image_url_dom":canonicalize(r.get("image_url")),
                            "title":r.get("title"),
                            "description":r.get("description"),
                        }
            except Exception as e:
                errors.append(f"collect_{rounds}:{e}")

            try:
                h=await page.evaluate("() => (document.scrollingElement||document.documentElement).scrollHeight")
                scroll_heights.append(int(h))
            except Exception:
                scroll_heights.append(-1)

            count=len(union)
            if count==previous:
                stable+=1
            else:
                stable=0
            previous=count

            if stable>=args.stable_rounds:
                break

            try:
                await page.evaluate(r"""
                () => {
                  const s=document.scrollingElement||document.documentElement;
                  window.scrollTo(0, s.scrollHeight);
                }
                """)
            except Exception as e:
                errors.append(f"scroll_{rounds}:{e}")
            await page.wait_for_timeout(args.settle_ms)

        blocked=await looks_blocked(page)
        count=len(union)

        # Stronger FULL rule:
        # - no effective block
        # - count > 0
        # - pin count stable
        # - scroll height also stable for the same tail window
        sh=[x for x in scroll_heights if x >= 0]
        scroll_stable=False
        if len(sh) >= args.stable_rounds:
            tail=sh[-args.stable_rounds:]
            scroll_stable=(max(tail)-min(tail)) <= args.scroll_height_tolerance

        effective_block=blocked and count==0

        # Resolve image assets only after enumeration, avoiding expensive requests per scroll round.
        resolution_stats={"originals":0,"736x":0,"564x":0,"236x":0,"other":0,"unverified":0}
        items=[]
        for pos,(pid,r) in enumerate(union.items()):
            try:
                best,tier,status,size=await best_image_url(ctx.request, r.get("image_url_dom"))
            except Exception as e:
                errors.append(f"image_resolve_{pid}:{e}")
                best,tier,status,size=r.get("image_url_dom"),"unverified",0,0
            resolution_stats[tier]=resolution_stats.get(tier,0)+1
            items.append({
                "pin_id":pid,
                "pin_url":r["pin_url"],
                "image_url":canonicalize(best),
                "image_url_dom":r.get("image_url_dom"),
                "image_resolution_tier":tier,
                "image_http_status":status,
                "image_content_length":size,
                "source_url":None,
                "title":r.get("title"),
                "description":r.get("description"),
                "board_url":canonicalize(args.canonical_url or resolved),
                "position":pos,
                "discovered_at":utcnow(),
                "fingerprint":fingerprint(pid,r["pin_url"],best),
            })

        if effective_block:
            completeness="PARTIAL"
            reason="Pinterest interstitial/login prevented usable board enumeration."
        elif count>0 and stable>=args.stable_rounds and scroll_stable:
            completeness="FULL"
            reason=f"Enumeration stabilized at {count} unique pins and document scroll-height also stabilized."
        else:
            completeness="PARTIAL"
            reason=f"Observed {count} unique pins, but independent enumeration stability criteria were not both satisfied."

        snapshot={
            "connector":"pinterest_public_board",
            "snapshot_version":"1.0-F4",
            "requested_url":args.url,
            "board_url":canonicalize(args.canonical_url or resolved),
            "captured_at":utcnow(),
            "enumeration_mode":completeness,
            "items":items,
            "diagnostics":{
                "visible_total_hint":total_hint,
                "rounds":rounds,
                "stable_rounds":stable,
                "scroll_height_stable":scroll_stable,
                "blocked_or_login":blocked,
                "effective_block":effective_block,
                "persistent_profile_used":persistent,
                "unique_pin_count":count,
                "resolution_stats":resolution_stats,
            }
        }

        diag=Diagnostics(
            input_url=args.url,
            canonical_board_url=canonicalize(args.canonical_url or target),
            resolved_url=resolved,
            page_title=title,
            rounds=rounds,
            stable_rounds=stable,
            unique_pin_count=count,
            visible_total_hint=total_hint,
            scroll_height_samples=scroll_heights[-10:],
            blocked_or_login=blocked,
            persistent_profile_used=persistent,
            completeness=completeness,
            completeness_reason=reason,
            resolution_stats=resolution_stats,
            errors=errors or None,
        )

        await ctx.close()
        if browser: await browser.close()
        return snapshot,diag

def parser():
    ap=argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("-o","--output",default="snapshot.json")
    ap.add_argument("--canonical-url")
    ap.add_argument("--profile-dir")
    ap.add_argument("--headed",action="store_true")
    ap.add_argument("--max-rounds",type=int,default=160)
    ap.add_argument("--stable-rounds",type=int,default=9)
    ap.add_argument("--settle-ms",type=int,default=1700)
    ap.add_argument("--scroll-height-tolerance",type=int,default=32)
    ap.add_argument("--timeout-ms",type=int,default=30000)
    ap.add_argument("--chromium")
    return ap

def main():
    args=parser().parse_args()
    snapshot,diag=asyncio.run(acquire(args))
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(snapshot,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(asdict(diag),indent=2,ensure_ascii=False))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
