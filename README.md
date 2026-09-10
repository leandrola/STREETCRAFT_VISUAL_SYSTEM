# Streetcraft Archive 1.0-F

Streetcraft Archive is the living documentary-evidence layer used by the Streetcraft Visual System.

It is designed around a public Pinterest board curated manually and growing indefinitely. The human workflow remains: find an image → save it to the board → done.

## 1.0-E adds
- Public Pinterest Board Adapter contract
- canonical-board / short-link resolution boundary
- normalized pin extraction contract
- FULL snapshot production rules
- parser for Pinterest-like embedded JSON and normalized connector payloads
- defensive deduplication by pin identity
- source/image URL normalization
- adapter diagnostics and degraded-mode behavior
- executable adapter tests with local fixtures

## Architecture boundary
- SVS = visual governance and transformation decisions
- Archive = living documentary evidence
- Canon = explicitly promoted high-authority references
- Pinterest = current public intake surface
- Public Board Adapter = replaceable discovery/normalization layer
- GPT = primary classifier/reasoning runtime

## Target board
The intended upstream is the user's public Pinterest board shared via:
`https://pin.it/5SbUv5Agi`

This URL is treated as configuration, not as permanent identity. The adapter should resolve and store the canonical board URL when a runtime with public-web/browser access is available.

## Important behavior
The adapter does not grant Pinterest authority over Streetcraft. It only enumerates documentary candidates.

A failed or partial Pinterest fetch must never be emitted as `FULL`. Only a verified complete board enumeration may produce a `FULL` connector snapshot capable of marking older pins as missing.

## Recommended reading order
1. `core/ARCHIVE_ARCHITECTURE.md`
2. `adapter/PUBLIC_PINTEREST_BOARD_ADAPTER.md`
3. `adapter/PIN_NORMALIZATION_CONTRACT.md`
4. `sync/CONNECTOR_SYNC_RUNTIME.md`
5. `sync/NORMALIZED_CONNECTOR_SNAPSHOT.md`
6. `pipeline/INGESTION_CLASSIFICATION_PIPELINE.md`
7. `storage/STORAGE_ARCHITECTURE.md`
8. `runtime/RETRIEVAL_RUNTIME.md`
9. `runtime/SVS_INTEGRATION_CONTRACT.md`

## Current implementation boundary
1.0-E includes a tested parser/normalizer and snapshot builder, but the live Pinterest network/browser driver is intentionally not claimed as complete. Pinterest pages can require JavaScript, redirects, authentication challenges, or anti-automation handling depending on runtime. The adapter therefore separates **acquisition** from **normalization**.

A compliant acquisition driver must provide either:
- resolved public-board HTML containing sufficient embedded state, or
- a structured list of public pin records gathered by an authorized browser/connector.

The 1.0-E normalizer then converts that acquisition result into the Streetcraft connector snapshot expected by 1.0-D.

## 1.0-F4 — Target Board Correction

1.0-F adds an executable Playwright acquisition layer for a public Pinterest board.

Target upstream:
`https://pin.it/5SbUv5Agi`

The driver resolves redirects in a real browser, enumerates `/pin/` URLs, scrolls until stable, captures image candidates and emits a connector snapshot.

**Important:** this release does not claim that the target board was successfully acquired from the ChatGPT runtime. Outbound DNS/network access to `pin.it` was unavailable here. The package therefore ships the live driver and a conservative completeness gate, but contains no fabricated board data.

See `acquisition/LIVE_ACQUISITION_DRIVER.md`.

Correction F1: target upstream URL updated to the user-confirmed public board. No runtime, schema, authority, or retrieval behavior changed.


## F2 live-board acquisition
Use `python acquisition_py/bootstrap_target_board.py` once if Pinterest requires login, then `python acquisition_py/run_target_board.py` for normal sync. Current verified board identity: `https://ar.pinterest.com/leolaudicina/us-image-archive`; current visible total: 536.


## F3
F3 hardens canonical board provenance and high-resolution image acquisition before Archive Snapshot 001 is frozen. See `acquisition/F3_ARCHIVE_ACQUISITION_HARDENING.md`.


## F4
F4 resolves the highest reachable Pinterest image asset and requires independent pin-count + scroll-height stability before `FULL`. See `acquisition/F4_RESOLUTION_ENUMERATION_HARDENING.md`.
