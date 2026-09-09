# Indexing Runtime

## Principle
Streetcraft stores documentary truth in structured records and treats search indexes as rebuildable projections.

## Canonical search document
Create one semantic document per Evidence Unit rather than one giant document per image.

Recommended composition:

ARCHIVE_ID: SCA-000742
EVIDENCE_UNIT: EU-004
DOMAIN: signage
SUBJECT: projecting storefront sign
OBSERVATION: enamel projecting sign mounted perpendicular to facade
PERMITTED_LEARNING: mounting geometry, relative scale, material behavior
FORBIDDEN_TRANSFER: business name, exact wording, geographic identity
PERIOD: 1960-1975 (0.78)
REGION: US Northeast (0.62)
PROVENANCE: P2
TAGS: projecting_sign, enamel_sign, storefront_signage

This makes retrieval evidence-scoped instead of image-scoped.

## Index families

### 1. Deterministic index
SQL columns and tags.
Use first.

### 2. Semantic index
Embeddings of Evidence Unit search documents.
Use for concept matching and synonymy.

### 3. Visual index
Perceptual hashes and optional visual embeddings.
Use for:
- duplicate/variant detection
- geometry/form support
- secondary reranking

Do not use visual index as the primary authority selector.

## Embedding abstraction
Persist an `embedding_locator`, not vendor-specific vector payloads in core schemas.

Required metadata:
- provider
- model
- dimensions
- external_key
- index_version

This permits future re-embedding without rewriting evidence records.

## Incremental indexing
On NEW:
- classify
- create/update evidence units
- emit semantic documents
- embed only new/changed documents

On UPDATED_METADATA:
- regenerate only affected semantic documents

On UPDATED_IMAGE:
- rerun duplicate detection
- rerun visual classification where needed
- invalidate affected embeddings/search documents

On provenance upgrade:
- no visual reprocessing required
- update deterministic ranking fields

## Index versioning
Every generated search document and embedding must carry an index version.

Example:
`SCA-IDX-1.0`

A new embedding model increments index implementation version, not Archive identity or schema identity.
