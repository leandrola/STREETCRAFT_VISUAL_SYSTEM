# Streetcraft Archive Storage Architecture

## Purpose
Streetcraft Archive must remain useful as a Pinterest board grows indefinitely. Storage therefore separates durable documentary metadata from replaceable retrieval accelerators.

## Design principles
1. Archive identity is stable and independent of Pinterest.
2. Structured evidence is the source of truth for authority decisions.
3. Embeddings and visual fingerprints are indexes, not evidence authority.
4. Rebuilding an index must never require changing archive IDs.
5. The runtime must support incremental writes and selective re-indexing.
6. SVS releases must not contain the growing image corpus.

## Logical layers

### A. Registry layer
Stores stable item identity and source lifecycle.

Primary entities:
- archive_item
- source_record
- source_snapshot
- archive_relationship

### B. Evidence layer
Stores what an image is competent to teach Streetcraft.

Primary entities:
- evidence_unit
- evidence_attribute
- period_assertion
- region_assertion
- provenance_assertion
- transfer_constraint

### C. Retrieval layer
Stores disposable accelerators.

Primary entities:
- semantic_document
- semantic_embedding
- visual_fingerprint
- retrieval_tag
- retrieval_cache

### D. Governance layer
Stores human decisions and audit history.

Primary entities:
- classification_event
- provenance_event
- promotion_event
- schema_migration

## Recommended first implementation
SQLite is sufficient for the first production-sized Streetcraft Archive because the corpus is curated and grows intermittently rather than at web-scale.

Use SQLite for:
- registry
- evidence metadata
- provenance
- tags
- relationships
- audit history

Embedding vectors may be stored:
1. in a SQLite-compatible vector extension when available; or
2. in a separate local vector store keyed by `archive_id` and `evidence_unit_id`.

Streetcraft must not depend on a particular vector provider.

## Stable keys

### Archive item
`SCA-000001`

### Evidence Unit
`SCA-000001:EU-001`

### Source record
`SRC:pinterest:<provider_pin_id>`

### Relationship
`REL:<archive_id>:<archive_id>:<type>`

Evidence Units are scoped to one archive item and remain addressable even if their labels or confidence are later refined.

## Image bytes
The Archive architecture does not assume permanent local possession of Pinterest-hosted image bytes.

Possible policies:
- URL_ONLY: retain only source URL + metadata + fingerprints.
- CACHE_TEMPORARY: cache bytes only for ingestion/re-analysis.
- OWNER_ARCHIVE: retain a project-owned copy where rights/runtime policy permits.

Metadata and evidence remain valid even if `source_status=UNAVAILABLE`, but retrieval confidence should be penalized when the underlying source can no longer be inspected.

## Write path
NEW SOURCE
→ source identity check
→ perceptual duplicate check
→ create/update archive item
→ classify
→ persist evidence units
→ persist provenance/period/region assertions
→ generate retrieval document
→ compute optional embeddings/fingerprints
→ mark index state READY

## Read path
SVS Reference Need
→ deterministic eligibility filter
→ evidence-domain query
→ semantic candidate retrieval
→ optional visual similarity support
→ transfer-risk penalty
→ redundancy collapse
→ authority ranking
→ return 1–5 scoped candidates

## Rebuildability
The following may be deleted and regenerated without loss of documentary truth:
- semantic embeddings
- visual similarity index
- retrieval cache
- denormalized search documents

The following are durable:
- archive IDs
- evidence units
- provenance assertions
- human promotion decisions
- relationship graph
- classification history
