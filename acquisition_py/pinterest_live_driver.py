#!/usr/bin/env python3
from __future__ import annotations
import argparse, asyncio, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

PIN_RE = re.compile(r"/pin/(\d+)")
BLOCK_MARKERS = [
    "log in to pinterest", "sign up to see more", "continue with google",
    "continue with facebook", "something went wrong", "we couldn't find", "rate limit"
]

def utcnow():
    return datetime.now(timezone.utc).isoformat()

def canonicalize(url):
    if not url:
        return None
    sp = urlsplit(url.strip())
    return urlunsplit((sp.scheme.lower(), sp.netloc.lower(), sp.path.rstrip('/'), '', ''))

def pin_id_from_url(url):
    m = PIN_RE.search(url or '')
    return m.group(1) if m else None

def choose_image(src, srcset):
    candidates = []
    if src:
        candidates.append((0, src))
    if srcset:
        for part in srcset.split(','):
            bits = part.strip().split()
            if not bits:
                continue
            score = 0
            if len(bits) > 1 and bits[1].endswith('w') and bits[1][:-1].isdigit():
                score = int(bits[1][:-1])
            candidates.append((score, bits[0]))
    return max(candidates, default=(0, None), key=lambda x: x[0])[1]

def make_record(pin_url, image_url, title, description, source_url, board_url, position):
    pid = pin_id_from_url(pin_url)
    fp = '|'.join([pid or '', canonicalize(pin_url) or '', canonicalize(image_url) or ''])
    return {
        'pin_id': pid,
        'pin_url': canonicalize(pin_url),
        'image_url': canonicalize(image_url),
        'source_url': canonicalize(source_url),
        'title': title.strip() if isinstance(title, str) and title.strip() else None,
        'description': description.strip() if isinstance(description, str) and description.strip() else None,
        'board_url': canonicalize(board_url),
        'position': position,
        'discovered_at': utcnow(),
        'fingerprint': hashlib.sha256(fp.encode('utf-8')).hexdigest(),
    }

async def collect_from_page(page, board_url):
    raw = await page.evaluate("""
    () => {
      const rows = [];
      const seen = new Set();
      for (const a of Array.from(document.querySelectorAll('a[href*="/pin/"]'))) {
        let href;
        try { href = new URL(a.getAttribute('href'), location.href).href; }
        catch { continue; }
        const m = href.match(/\/pin\/(\d+)/);
        if (!m || seen.has(m[1])) continue;
        seen.add(m[1]);
        const card = a.closest('[data-test-id]') || a.parentElement;
        const img = a.querySelector('img') || card?.querySelector('img');
        const sourceAnchor = card ? Array.from(card.querySelectorAll('a[href^="http"]'))
          .find(x => !x.href.includes('pinterest.') && !x.href.includes('/pin/')) : null;
        rows.push({
          pin_url: href,
          image_src: img?.currentSrc || img?.src || null,
          image_srcset: img?.getAttribute('srcset') || null,
          title: img?.alt || a.getAttribute('aria-label') || null,
          description: null,
          source_url: sourceAnchor?.href || null
        });
      }
      return rows;
    }
    """)
    return [
        make_record(
            r.get('pin_url'), choose_image(r.get('image_src'), r.get('image_srcset')),
            r.get('title'), r.get('description'), r.get('source_url'), board_url, i
        ) for i, r in enumerate(raw)
    ]

async def body_text(page):
    try:
        return (await page.locator('body').inner_text(timeout=5000)).lower()
    except Exception:
        return ''

async def looks_blocked(page):
    text = await body_text(page)
    return any(marker in text for marker in BLOCK_MARKERS)

async def visible_total_hint(page):
    try:
        return await page.evaluate("""
        () => {
          const body = document.body.innerText || '';
          const m = body.match(/([\d,.]+)\s+(?:Pins?|pines?)\b/i);
          if (!m) return null;
          const raw = m[1].replace(/[.,](?=\d{3}\b)/g, '').replace(/[^\d]/g, '');
          return raw ? parseInt(raw, 10) : null;
        }
        """)
    except Exception:
        return None

async def dismiss_interstitial(page):
    for selector in [
        'button[aria-label*="Close"]', 'button[aria-label*="Cerrar"]',
        '[data-test-id="close-button"]'
    ]:
        try:
            loc = page.locator(selector)
            if await loc.count():
                await loc.first.click(timeout=1000)
                await page.wait_for_timeout(500)
                return
        except Exception:
            pass

async def acquire(args):
    try:
        from playwright.async_api import async_playwright
    except Exception as e:
        raise RuntimeError('Install Playwright: pip install playwright && playwright install chromium') from e

    errors = []
    async with async_playwright() as p:
        persistent = bool(args.profile_dir)
        if persistent:
            ctx = await p.chromium.launch_persistent_context(
                user_data_dir=args.profile_dir,
                headless=not (args.headed or args.bootstrap_login),
                viewport={'width': 1440, 'height': 1100},
                locale='en-US',
                executable_path=args.chromium or None,
            )
            browser = None
        else:
            browser = await p.chromium.launch(
                headless=not (args.headed or args.bootstrap_login),
                executable_path=args.chromium or None,
            )
            ctx = await browser.new_context(viewport={'width': 1440, 'height': 1100}, locale='en-US')

        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        page.set_default_timeout(args.timeout_ms)
        target = args.canonical_url or args.url
        await page.goto(target, wait_until='domcontentloaded')
        await page.wait_for_timeout(args.settle_ms)

        if args.bootstrap_login:
            print('\nA browser window is open.', file=sys.stderr)
            print('If Pinterest requests login, sign in directly on Pinterest.', file=sys.stderr)
            print('Streetcraft does not receive or store your password.', file=sys.stderr)
            await asyncio.to_thread(input, 'When the board is visible, press ENTER here... ')

        await dismiss_interstitial(page)
        resolved = page.url
        hint = await visible_total_hint(page)
        expected = args.expected_total or hint

        union = {}
        stable = 0
        previous = -1
        rounds = 0
        for rounds in range(1, args.max_rounds + 1):
            await dismiss_interstitial(page)
            try:
                for rec in await collect_from_page(page, resolved):
                    key = rec.get('pin_id') or rec.get('pin_url')
                    if key:
                        union[key] = rec
            except Exception as e:
                errors.append(f'collect_{rounds}: {e}')

            count = len(union)
            stable = stable + 1 if count == previous else 0
            previous = count
            if expected and count >= expected:
                stable = max(stable, args.stable_rounds)
            if stable >= args.stable_rounds:
                break

            try:
                await page.evaluate('window.scrollBy(0, Math.max(window.innerHeight * 2.5, 1800))')
            except Exception as e:
                errors.append(f'scroll_{rounds}: {e}')
            await page.wait_for_timeout(args.settle_ms)

        blocked = await looks_blocked(page)
        count = len(union)
        effective_block = blocked and count == 0
        full = (
            not effective_block and expected is not None and
            count >= expected and stable >= args.stable_rounds
        )
        mode = 'FULL' if full else 'PARTIAL'
        reason = (
            f'Observed {count} unique pins and satisfied expected total {expected}.' if full else
            f'Observed {count} unique pins; expected total is {expected}. FULL criteria not satisfied.'
        )

        items = list(union.values())
        items.sort(key=lambda x: (x.get('position', 0), x.get('pin_id') or ''))
        for i, item in enumerate(items):
            item['position'] = i

        snapshot = {
            'connector': 'pinterest_public_board',
            'snapshot_version': '1.0-F2',
            'requested_url': args.url,
            'board_url': canonicalize(resolved),
            'captured_at': utcnow(),
            'enumeration_mode': mode,
            'items': items,
            'diagnostics': {
                'visible_total_hint': hint,
                'expected_total': expected,
                'rounds': rounds,
                'stable_rounds': stable,
                'blocked_or_login': blocked,
                'effective_block': effective_block,
                'persistent_profile_used': persistent,
                'completeness_reason': reason,
                'errors': errors or None,
            }
        }
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding='utf-8')
        print(json.dumps({
            'resolved_url': resolved,
            'unique_pin_count': count,
            'expected_total': expected,
            'enumeration_mode': mode,
            'blocked_or_login': blocked,
            'effective_block': effective_block,
        }, indent=2, ensure_ascii=False))
        print(f'Wrote: {args.output}', file=sys.stderr)

        await ctx.close()
        if browser:
            await browser.close()


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('-o', '--output', default='snapshot.json')
    ap.add_argument('--canonical-url')
    ap.add_argument('--expected-total', type=int)
    ap.add_argument('--profile-dir', help='Persistent Chromium profile directory.')
    ap.add_argument('--bootstrap-login', action='store_true')
    ap.add_argument('--headed', action='store_true')
    ap.add_argument('--max-rounds', type=int, default=120)
    ap.add_argument('--stable-rounds', type=int, default=7)
    ap.add_argument('--settle-ms', type=int, default=1500)
    ap.add_argument('--timeout-ms', type=int, default=30000)
    ap.add_argument('--chromium')
    return ap.parse_args()

if __name__ == '__main__':
    asyncio.run(acquire(parse_args()))
