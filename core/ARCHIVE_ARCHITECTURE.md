# Streetcraft Living Archive Architecture

## Objective
Maintain an indefinitely growing visual evidence corpus without embedding the corpus into SVS releases.

## Primary flow
PINTEREST BOARD
→ DISCOVERY
→ INGESTION
→ NORMALIZATION
→ DEDUPLICATION
→ VISUAL ANALYSIS
→ EVIDENCE UNITS
→ PROVENANCE / CONFIDENCE
→ RETRIEVAL INDEX
→ SVS REFERENCE REASONING

## Archive classes
DOCUMENTARY_EVIDENCE — default class for newly ingested pins.
INFLUENCE_REFERENCE — useful for visual knowledge but not source authority.
CANON_CANDIDATE — requires explicit promotion workflow.
CANONICAL — only human project owner may grant.
REJECTED — retained only if useful for provenance/history.

New Pinterest content MUST NOT auto-promote beyond DOCUMENTARY_EVIDENCE.

## Stable identity
Every image receives a Streetcraft Archive ID independent of Pinterest URL or filename:
SCA-000001, SCA-000002, ...

Pinterest IDs/URLs are provenance, not identity.

## Incremental sync
The archive stores source fingerprints and last-seen metadata.
Each sync:
1. enumerate current board pins;
2. compare source pin IDs/URLs/fingerprints;
3. ingest only unseen or materially changed pins;
4. preserve existing archive IDs;
5. never reprocess the entire corpus unless explicitly requested.

## Immutable vs mutable fields
Immutable:
- archive_id
- first_ingested_at
- original_source_url when known
- original_pin_id when known

Mutable:
- board membership
- caption
- inferred period/region
- domain labels
- confidence
- authority eligibility
- provenance resolution

## Deletion policy
If a pin disappears from Pinterest, do not silently delete the archive record.
Mark source_status=UNAVAILABLE and retain metadata/provenance. Image-byte retention depends on connector/legal/runtime policy.
