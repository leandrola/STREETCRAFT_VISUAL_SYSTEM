# Public Pinterest Board Adapter

## Purpose
Convert a manually curated public Pinterest board into a provider-neutral Streetcraft connector snapshot.

The adapter is an intake mechanism only. It does not classify visual evidence, promote Canon, or make Streetcraft transformation decisions.

## Input
A public-board locator, preferably configured as both:
- `shared_url`: short/share URL supplied by the curator
- `canonical_board_url`: populated after successful resolution

Current configured shared URL:
`https://pin.it/5SbUv5Agi`

## Two-stage design

### Stage A — Acquisition
A browser, connector, scraper, or future MCP obtains board data.

Allowed acquisition outputs:
1. fully rendered public-board HTML / embedded JSON state;
2. structured pin records from a browser/connector;
3. Pinterest API response only if it enumerates the intended public board completely and legally.

Stage A is environment-specific and replaceable.

### Stage B — Normalization
Provider-specific fields are reduced to the Streetcraft pin record:
- `pin_id`
- `pin_url`
- `image_url`
- `source_url` when present
- `title`
- `description`
- `board_url`
- `position` when stable
- `discovered_at`
- `provider_updated_at` when available
- `content_fingerprint` when available

Stage B is implemented in `adapter_py/pinterest_public_adapter.py`.

## Enumeration completeness
`FULL` is a privileged assertion.

Emit `FULL` only when the acquisition driver can verify that:
- it reached the canonical board;
- it exhausted pagination / infinite scroll / cursor enumeration;
- no provider error interrupted enumeration;
- duplicate collapse completed;
- the final count is internally consistent when Pinterest exposes one.

Otherwise emit `PARTIAL`.

A `PARTIAL` snapshot may add or update records but cannot mark unseen prior items as missing.

## Identity
Primary provider identity is Pinterest `pin_id`.

Do not use image URL as the durable primary identity because CDNs and transformations can change.

If `pin_id` is absent, the adapter may create a temporary provider key from canonical `pin_url`, but this should remain lower confidence and should be reconciled later.

## Canonicalization
- strip tracking query parameters from pin/source URLs when safe;
- prefer canonical `https://www.pinterest.com/pin/<id>/` form when pin ID is known;
- preserve the original source URL separately;
- never infer the original documentary source from Pinterest description text alone.

## Image selection
Prefer the highest-quality publicly exposed still image representing the pin.

Do not treat Pinterest UI screenshots, profile avatars, board covers, recommendation tiles, or ads as archive items.

## Safety / governance
The connector must not:
- reinterpret images;
- invent missing pin metadata;
- classify geographic identity from appearance;
- promote evidence to Canon;
- delete archive history because a page load failed.
