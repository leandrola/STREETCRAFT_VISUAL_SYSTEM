# Incremental Sync and Index

## Sync states
NEW
UNCHANGED
UPDATED_METADATA
UPDATED_IMAGE
SOURCE_UNAVAILABLE
DUPLICATE

## Index layers
Metadata index — deterministic fields.
Semantic index — text/domain concepts.
Visual similarity index — secondary retrieval signal only.
Evidence index — domain/property-level authority and confidence.

Reference Reasoning should primarily query the Evidence index. Visual similarity is supporting evidence, not the retrieval objective.

## Re-index triggers
- new item
- materially changed image
- analyst changes evidence classification
- provenance upgraded
- new Archive schema version requiring migration

Adding a new pin should not require rebuilding SVS or regenerating the full archive manifest.
