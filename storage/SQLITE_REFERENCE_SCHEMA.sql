PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS archive_item (
  archive_id TEXT PRIMARY KEY,
  archive_class TEXT NOT NULL DEFAULT 'DOCUMENTARY_EVIDENCE',
  source_status TEXT NOT NULL DEFAULT 'AVAILABLE',
  first_ingested_at TEXT NOT NULL,
  last_seen_at TEXT,
  classifier_version TEXT,
  schema_version TEXT NOT NULL,
  content_fingerprint TEXT,
  perceptual_hash TEXT,
  notes TEXT,
  CHECK (archive_class IN ('DOCUMENTARY_EVIDENCE','INFLUENCE_REFERENCE','CANON_CANDIDATE','CANONICAL','REJECTED')),
  CHECK (source_status IN ('AVAILABLE','UNAVAILABLE','CHANGED','QUARANTINED'))
);

CREATE TABLE IF NOT EXISTS source_record (
  source_record_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  provider_item_id TEXT,
  source_url TEXT NOT NULL,
  original_source_url TEXT,
  board_url TEXT,
  caption TEXT,
  discovered_at TEXT NOT NULL,
  last_seen_at TEXT,
  source_fingerprint TEXT,
  UNIQUE(provider, provider_item_id),
  UNIQUE(provider, source_url)
);

CREATE TABLE IF NOT EXISTS evidence_unit (
  evidence_unit_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  domain TEXT NOT NULL,
  subject TEXT,
  observation TEXT NOT NULL,
  evidence_state TEXT NOT NULL,
  confidence REAL NOT NULL,
  transfer_risk TEXT NOT NULL DEFAULT 'MEDIUM',
  permitted_learning TEXT,
  forbidden_transfer TEXT,
  classifier_version TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT,
  CHECK (evidence_state IN ('DOCUMENTED','CORROBORATED','INFERRED_HIGH','INFERRED_LOW','UNKNOWN')),
  CHECK (confidence >= 0.0 AND confidence <= 1.0),
  CHECK (transfer_risk IN ('LOW','MEDIUM','HIGH','PROHIBITED'))
);

CREATE INDEX IF NOT EXISTS idx_evidence_domain ON evidence_unit(domain);
CREATE INDEX IF NOT EXISTS idx_evidence_archive ON evidence_unit(archive_id);
CREATE INDEX IF NOT EXISTS idx_evidence_confidence ON evidence_unit(confidence);

CREATE TABLE IF NOT EXISTS retrieval_tag (
  evidence_unit_id TEXT NOT NULL REFERENCES evidence_unit(evidence_unit_id) ON DELETE CASCADE,
  tag TEXT NOT NULL,
  PRIMARY KEY (evidence_unit_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_retrieval_tag ON retrieval_tag(tag);

CREATE TABLE IF NOT EXISTS period_assertion (
  assertion_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  value_from INTEGER,
  value_to INTEGER,
  label TEXT,
  evidence_state TEXT NOT NULL,
  confidence REAL NOT NULL,
  basis TEXT,
  CHECK (confidence >= 0.0 AND confidence <= 1.0)
);

CREATE TABLE IF NOT EXISTS region_assertion (
  assertion_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  country TEXT,
  region TEXT,
  city TEXT,
  neighborhood TEXT,
  evidence_state TEXT NOT NULL,
  confidence REAL NOT NULL,
  basis TEXT,
  CHECK (confidence >= 0.0 AND confidence <= 1.0)
);

CREATE TABLE IF NOT EXISTS provenance_assertion (
  assertion_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  provenance_level TEXT NOT NULL,
  source_name TEXT,
  source_url TEXT,
  confidence REAL NOT NULL,
  verified_at TEXT,
  basis TEXT,
  CHECK (provenance_level IN ('P0','P1','P2','P3','P4')),
  CHECK (confidence >= 0.0 AND confidence <= 1.0)
);

CREATE TABLE IF NOT EXISTS archive_relationship (
  relationship_id TEXT PRIMARY KEY,
  from_archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  to_archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  relationship_type TEXT NOT NULL,
  confidence REAL NOT NULL,
  created_at TEXT NOT NULL,
  CHECK (relationship_type IN ('SAME_SCENE','CROP_OF','ALTERNATE_SCAN','REPOST_OF','SEQUENCE_WITH','RELATED_SUBJECT')),
  CHECK (confidence >= 0.0 AND confidence <= 1.0),
  CHECK (from_archive_id <> to_archive_id)
);

CREATE TABLE IF NOT EXISTS semantic_document (
  semantic_document_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  evidence_unit_id TEXT REFERENCES evidence_unit(evidence_unit_id) ON DELETE CASCADE,
  document_text TEXT NOT NULL,
  index_version TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS embedding_locator (
  embedding_id TEXT PRIMARY KEY,
  semantic_document_id TEXT NOT NULL REFERENCES semantic_document(semantic_document_id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  dimensions INTEGER,
  external_key TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE(provider, model, external_key)
);

CREATE TABLE IF NOT EXISTS classification_event (
  event_id TEXT PRIMARY KEY,
  archive_id TEXT NOT NULL REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  actor TEXT NOT NULL,
  runtime_version TEXT,
  payload_json TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_migration (
  migration_id TEXT PRIMARY KEY,
  from_version TEXT,
  to_version TEXT NOT NULL,
  applied_at TEXT NOT NULL,
  checksum TEXT
);

-- Archive 1.0-D sync/runtime additions
CREATE TABLE IF NOT EXISTS sync_run (
  run_id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  board_url TEXT NOT NULL,
  enumeration_mode TEXT NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  status TEXT NOT NULL,
  seen_count INTEGER NOT NULL DEFAULT 0,
  new_count INTEGER NOT NULL DEFAULT 0,
  changed_count INTEGER NOT NULL DEFAULT 0,
  unchanged_count INTEGER NOT NULL DEFAULT 0,
  missing_count INTEGER NOT NULL DEFAULT 0,
  failed_count INTEGER NOT NULL DEFAULT 0,
  error_json TEXT,
  CHECK (enumeration_mode IN ('FULL','PARTIAL','DELTA')),
  CHECK (status IN ('RUNNING','SUCCESS','PARTIAL','FAILED'))
);

CREATE TABLE IF NOT EXISTS sync_item_state (
  provider TEXT NOT NULL,
  provider_item_key TEXT NOT NULL,
  archive_id TEXT REFERENCES archive_item(archive_id) ON DELETE SET NULL,
  source_fingerprint TEXT,
  content_fingerprint TEXT,
  provider_updated_at TEXT,
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  last_run_id TEXT REFERENCES sync_run(run_id) ON DELETE SET NULL,
  runtime_status TEXT NOT NULL DEFAULT 'DISCOVERED',
  PRIMARY KEY (provider, provider_item_key)
);

CREATE TABLE IF NOT EXISTS runtime_job (
  job_id TEXT PRIMARY KEY,
  archive_id TEXT REFERENCES archive_item(archive_id) ON DELETE CASCADE,
  job_type TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  input_fingerprint TEXT,
  runtime_version TEXT,
  status TEXT NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  available_after TEXT,
  last_error TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  CHECK (job_type IN ('ACQUIRE','FINGERPRINT','DUPLICATE_REVIEW','CLASSIFY','VALIDATE','INDEX')),
  CHECK (status IN ('PENDING','RUNNING','SUCCEEDED','FAILED','QUARANTINED'))
);

CREATE INDEX IF NOT EXISTS idx_runtime_job_status ON runtime_job(status, available_after);
CREATE INDEX IF NOT EXISTS idx_sync_item_archive ON sync_item_state(archive_id);
