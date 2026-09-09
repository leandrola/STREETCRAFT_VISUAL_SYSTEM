# Pin Normalization Contract

## Required normalized fields

```json
{
  "provider": "pinterest",
  "provider_item_id": "123456789",
  "pin_url": "https://www.pinterest.com/pin/123456789/",
  "image_url": "https://...",
  "source_url": null,
  "title": null,
  "description": null,
  "board_url": "https://www.pinterest.com/.../.../",
  "position": null,
  "discovered_at": "2026-09-08T00:00:00Z",
  "provider_updated_at": null,
  "content_fingerprint": null
}
```

## Null policy
Unknown metadata stays `null`.
Do not replace unknown values with guessed historical, geographic, commercial, or semantic information.

## Text policy
Pinterest title/description are provenance metadata, not documentary truth.
They may aid retrieval but cannot override what the image itself establishes.

## Duplicate policy
Within a single enumeration:
1. same `provider_item_id` → one pin;
2. same canonical `pin_url` → one pin;
3. visually duplicated/reposted pins with different IDs remain separate provider records until Archive duplicate analysis links them.

## Snapshot mapping
The normalized records are mapped to `connector-snapshot.schema.json`.
Snapshot metadata must state:
- provider
- board locator
- canonical board URL if known
- enumeration type
- acquisition timestamp
- acquisition method
- diagnostics
