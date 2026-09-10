# 1.0-F2 — Pinterest Acquisition Fix

F2 is evidence-driven. The first real snapshot resolved the canonical board correctly and exposed 536 Pins, but anonymous/headless acquisition returned zero items behind a Pinterest login/interstitial.

## First run

```bash
python acquisition_py/bootstrap_target_board.py
```

A visible Chromium window opens. If Pinterest asks for login, sign in directly on Pinterest. Streetcraft never receives or stores your password. When the board is visible, return to Terminal and press ENTER. The session remains local in `.browser-profile/`.

## Later runs

```bash
python acquisition_py/run_target_board.py
```

## FULL gate

Current observed completeness target: 536 unique pins. F2 declares FULL only when the acquired count reaches the expected total and enumeration stabilizes. Otherwise it stays PARTIAL.
