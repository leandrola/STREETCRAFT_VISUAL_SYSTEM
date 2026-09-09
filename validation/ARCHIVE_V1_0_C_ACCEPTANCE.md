# Streetcraft Archive 1.0-C Acceptance Criteria

PASS when all are true:

- Archive IDs remain independent of Pinterest IDs/URLs.
- Structured Evidence Units remain durable source-of-truth records.
- Search indexes are explicitly rebuildable.
- Pinterest remains an intake surface only.
- Retrieval is Evidence Unit scoped, not whole-image similarity driven.
- Visual similarity is secondary and capped.
- Duplicate variants cannot create false corroboration.
- Zero-result retrieval is valid.
- Archive cannot silently relax authority thresholds.
- Canon status cannot overwrite source authority.
- SVS owns final transformation decisions.
- Embedding provider/model can change without changing archive identity.
- SQLite is sufficient as the recommended first metadata store but is not a permanent architectural dependency.
