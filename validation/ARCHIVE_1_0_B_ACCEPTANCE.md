# Archive 1.0-B Acceptance Criteria

The ingestion/classification layer is ready for implementation when all criteria below are true.

## Architecture
- [x] incremental single-item analysis contract
- [x] duplicate / near-duplicate policy
- [x] fact vs inference separation
- [x] Evidence Unit extraction contract
- [x] temporal confidence contract
- [x] regional confidence contract
- [x] provenance handoff
- [x] transfer-risk review
- [x] retrieval descriptors
- [x] quarantine/reject behavior

## GPT behavior
- [x] primary classifier runtime declared
- [x] UNKNOWN explicitly permitted
- [x] illegible text protection
- [x] Canon-geography contamination forbidden
- [x] no automatic Canon promotion
- [x] machine-valid JSON output required

## Implementation not yet included
- [ ] Pinterest connector authentication/discovery runtime
- [ ] image downloading/cache policy
- [ ] perceptual hashing implementation
- [ ] persistent database
- [ ] vector/semantic index
- [ ] scheduled sync job
- [ ] batch classifier runner
- [ ] automatic provenance URL resolution
- [ ] SVS live retrieval adapter

Archive 1.0-B therefore completes the behavioral specification of ingestion and classification but not the production connector/runtime.
