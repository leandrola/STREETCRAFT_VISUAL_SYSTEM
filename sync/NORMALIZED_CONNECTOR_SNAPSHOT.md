# Normalized Connector Snapshot

Every connector must translate provider-specific data into this boundary before Archive logic runs.

Required board fields:
- provider
- board_url
- board_external_id when available
- enumerated_at
- enumeration_mode: FULL | PARTIAL | DELTA
- items[]

Required item fields:
- external_id when available
- pin_url
- image_url or image_reference when available
- title/caption when available
- outbound_source_url when available
- provider_updated_at when available

Optional connector hints are never documentary facts.

The Archive owns:
- SCA IDs
- fingerprints
- deduplication
- GPT analysis
- evidence/confidence
- provenance
- authority
- indexing
- Canon governance
