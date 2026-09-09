# Archive 1.0-D — Connector & Sync Runtime

## Purpose
Turn a growing public board into incremental Streetcraft Archive updates without making Pinterest the database or granting source authority to the connector.

The runtime is provider-agnostic. A Pinterest connector is one adapter that emits a normalized board snapshot.

## Human workflow
Save image to public board → next sync discovers it → only new/changed items enter the ingestion pipeline.

No manual tagging is required.

## Runtime flow

CONNECTOR ENUMERATION
→ NORMALIZE
→ COMPARE WITH SYNC STATE
→ NEW / CHANGED / UNCHANGED / MISSING
→ ACQUIRE IMAGE REFERENCE
→ FINGERPRINT
→ EXACT / NEAR DUPLICATE CHECK
→ CLASSIFICATION QUEUE
→ GPT CLASSIFIER
→ VALIDATE
→ SQLITE TRANSACTION
→ INDEX QUEUE
→ COMMIT SYNC STATE
→ AUDIT

## Item state machine

### NEW
Provider item has never been recorded.

Action:
1. allocate SCA identity only after minimum acquisition succeeds;
2. insert `archive_item` and `source_record`;
3. queue classification;
4. do not make the item retrievable until validation passes.

### UNCHANGED
External identifier and source fingerprint are unchanged.

Action:
- update `last_seen_at`;
- do not reclassify;
- do not regenerate embeddings.

### CHANGED
Metadata or content fingerprint changed.

Action:
- preserve SCA identity;
- record a sync event;
- re-run only stages affected by the change;
- if image bytes changed, re-run duplicate review + classification + indexing;
- if caption/source URL changed only, re-run provenance/retrieval metadata as needed.

### MISSING
Previously known item is absent from current provider enumeration.

Action:
- never delete documentary history automatically;
- mark source status `UNAVAILABLE` only after the connector has completed a trustworthy full enumeration;
- retain provenance, evidence and relationships;
- exclude unavailable image access from generation unless a durable local/reference copy exists.

### RESTORED
A previously unavailable item reappears.

Action:
- mark `AVAILABLE`;
- preserve identity;
- classify again only if content changed.

## Enumeration completeness
A connector run must declare one of:
- `FULL`: complete board enumeration;
- `PARTIAL`: pagination interrupted, rate limited or otherwise incomplete;
- `DELTA`: provider supplied only explicit changes.

MISSING transitions are legal only after `FULL` enumeration.

## Idempotency
The same normalized snapshot may be replayed without creating duplicate SCA items, evidence units or classification jobs.

Idempotency keys:
- source: `provider + provider_item_id` when stable;
- fallback source: canonicalized `provider + pin_url`;
- job: `archive_id + job_type + input_fingerprint + classifier_version`.

## Failure boundaries
A failed item must not abort a successful board enumeration.

Use item-scoped statuses:
- `DISCOVERED`
- `ACQUIRE_FAILED`
- `FINGERPRINTED`
- `DUPLICATE_REVIEW`
- `CLASSIFICATION_PENDING`
- `CLASSIFICATION_FAILED`
- `VALIDATED`
- `INDEX_PENDING`
- `INDEXED`
- `QUARANTINED`

Retry transient failures with bounded exponential backoff. Permanent classification uncertainty is not a transport failure and should become UNKNOWN or QUARANTINED according to policy.

## Transaction rule
Classification output, Evidence Units and retrieval metadata for one archive item must be committed atomically. A partial classifier result must never become retrievable.

## Scheduling
The archive does not require continuous polling. Because the board grows manually and occasionally, a manual sync command or low-frequency scheduled sync is sufficient.

Recommended modes:
- `manual`: user/operator invokes sync after adding pins;
- `daily`: convenient default if automation is available;
- `on-demand-before-retrieval`: optional freshness check before a major Streetcraft session.

SVS execution must never block solely because the external board cannot be reached. It may continue using the last validated Archive state.
