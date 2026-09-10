# Streetcraft Archive 1.0-F4

F4 is the final acquisition-hardening stage before Archive Snapshot 001.

The latest live run established:
- canonical board provenance is now correct
- enumeration returned `PARTIAL`
- items discovered in that run: `508`
- unique pin IDs in that run: `508`
- `/236x/` image URLs: `508`

Source: user-provided `target-board.snapshot(1).json`.

## F4 goals

### 1. Resolve real image assets
F4 does not blindly rewrite `/236x/` to `/originals/`.

For each DOM image URL, it attempts in order:
1. `/originals/`
2. `/736x/`
3. `/564x/`
4. DOM URL fallback

Only reachable image responses are accepted.

Each item now records:
- `image_url`
- `image_url_dom`
- `image_resolution_tier`
- `image_http_status`
- `image_content_length`

### 2. Stronger enumeration completeness
F4 requires two independent stability signals:
- unique pin count remains stable
- document scroll height remains stable

Only then can enumeration become `FULL`.

A visible Pinterest board-total remains diagnostic evidence only. It is not the Archive's permanent corpus size.

### 3. Preserve board provenance
Every item remains bound to:

`https://ar.pinterest.com/leolaudicina/us-image-archive`

### 4. No automatic content deletion
F4 still does not remove pins based on subject matter or visual similarity.
Exact/perceptual duplicate governance belongs after acquisition.

## Next gate

If the next F4 run returns:
- `enumeration_mode == FULL`
- canonical board preserved
- no duplicate pin IDs
- image resolution tiers primarily `originals`, `736x`, or `564x`

then Streetcraft may freeze **Archive Snapshot 001** and move on to image-level deduplication and Evidence Units.
