# 1.0-F Live Acquisition Driver

## Objective

Acquire a real public Pinterest board through a browser and hand a normalized snapshot to the existing 1.0-E adapter / 1.0-D sync layers.

Target board configured for the project:

`https://pin.it/5SbUv5Agi`

## Safety invariant

Scroll stability alone is **not** proof of a complete board enumeration.

The driver emits `FULL` only when:
1. the board reaches a stable pin count,
2. a visible/independent board total is available,
3. the acquired unique-pin count satisfies that total,
4. no login/block condition is detected.

Otherwise it emits `PARTIAL`.

This preserves the 1.0-D missing-item firewall.

## Acquisition strategy

1. Open the supplied URL in Chromium.
2. Allow redirects, including `pin.it` → canonical Pinterest URL.
3. Wait for the public board shell.
4. Collect unique `/pin/{id}` anchors.
5. Capture the best DOM image candidate, title/alt text and accessible source URL when present.
6. Scroll to page end repeatedly.
7. Stop after a configurable number of stable rounds.
8. Look for a visible board-total hint.
9. Emit FULL only when completeness can be proven.
10. Save diagnostics with every snapshot.

## Deliberate separation

The browser driver is not permitted to decide:
- historical period,
- geography,
- Evidence Unit authority,
- Canon status,
- relevance to a source image.

Those remain downstream Streetcraft responsibilities.

## Runtime requirements

Python 3.11+ and Playwright.

```bash
pip install -r requirements-live.txt
playwright install chromium
```

Run:

```bash
python acquisition_py/pinterest_live_driver.py   "https://pin.it/5SbUv5Agi"   -o snapshots/pinterest-board.json
```

If Pinterest serves a login/interstitial in headless mode, run once with:

```bash
python acquisition_py/pinterest_live_driver.py   "https://pin.it/5SbUv5Agi"   --headed   -o snapshots/pinterest-board.json
```

The adapter does not require your Pinterest credentials. It is designed for a public board only.
