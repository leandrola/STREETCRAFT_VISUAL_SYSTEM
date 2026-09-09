# Streetcraft Archive 1.0 Status

## Completed through 1.0-D
- Living Archive architecture
- documentary vs Canon governance
- stable SCA identity
- GPT ingestion/classification contract
- Evidence Unit extraction
- provenance/period/region confidence
- duplicate relationship model
- transfer-risk model
- durable SQLite architecture
- provider-independent semantic indexing architecture
- authority ranking policy
- SVS ↔ Archive runtime contract
- normalized connector snapshot contract
- FULL/PARTIAL/DELTA enumeration semantics
- NEW/CHANGED/UNCHANGED/MISSING/RESTORED sync state model
- idempotency and retry policy
- sync-run/job persistence schema
- provider-neutral Python reference diff runtime

## Still not live
- real Pinterest board adapter / MCP connection
- real image acquisition
- perceptual hashing implementation
- GPT classifier invocation
- production SQLite population from the actual board
- embedding/vector provider
- live SVS retrieval tool call
- operational deployment/hosting

## Next recommended milestone
Archive 1.0-E — Live Connector Integration: select the actual Pinterest access path (plugin/MCP/API or compatible provider), bind it to the normalized snapshot contract, and run the first real incremental ingest against the user's public board.

## 1.0-E
Public Pinterest Board Adapter contract and local normalization runtime complete. Live board acquisition still requires a browser/connector runtime capable of resolving and fully enumerating the public board.
