# Pinterest Connector Contract

The connector may be implemented through MCP or any future integration. SVS must not depend on Pinterest-specific APIs.

## Required capabilities
LIST_BOARD_ITEMS(board_url)
GET_ITEM_METADATA(item_id)
GET_ITEM_IMAGE(item_id) when technically/legal permitted
GET_SOURCE_LINK(item_id)

Optional:
GET_ITEM_UPDATED_AT
GET_BOARD_UPDATED_AT

## Sync output
For each pin return normalized connector data:
- external_id
- board_id
- pin_url
- image_url or image_reference
- title/caption
- outbound_source_url
- first_seen_at if available
- updated_at if available

## Connector responsibilities
- authentication/transport when needed
- pagination
- rate-limit handling
- external identifiers
- raw source metadata

## Archive responsibilities
- Streetcraft IDs
- visual analysis
- deduplication
- evidence units
- confidence
- provenance resolution
- retrieval index
- Canon governance

## Safety rule
A connector never decides that an item is Canonical.
