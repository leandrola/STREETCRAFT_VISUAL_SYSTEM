# Archive Migration Policy

Archive schema evolution must preserve Streetcraft Archive identity and documentary lineage.

## Version domains
- Archive schema version: structure of durable records.
- Classifier version: GPT extraction behavior.
- Index version: semantic/visual search implementation.
- SVS version: transformation governance.

These versions must remain independent.

## Migration rules
1. Never change `archive_id` because of schema migration.
2. Never silently overwrite a human Canon promotion/demotion decision.
3. Preserve previous classifier outputs in audit history when reclassification materially changes authority.
4. Re-embedding does not require reclassification.
5. Retrieval index migration must be rebuildable from durable evidence records.
6. If a new schema cannot represent an old uncertainty state exactly, retain the original payload in migration history.
