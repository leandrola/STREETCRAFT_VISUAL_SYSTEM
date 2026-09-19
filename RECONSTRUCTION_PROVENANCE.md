# Reconstruction Provenance

This SVS 1.9.1 package was reconstructed from the public Streetcraft repository and the locally built 1.9.1 patch.

- Repository: `https://github.com/leandrola/STREETCRAFT_VISUAL_SYSTEM`
- Base commit: `04c070d2043295bb802ce3381b7c78faa26ee991`
- Base tree: `c9b52237e1cdfeb799d0c6f729114721858517b4`
- Base version: SVS 1.9.0 Candidate
- Integrated version: SVS 1.9.1 Candidate

## Exact embedded visual assets

The current reference assets and four Fear City validation views were matched against their Git blob identities before packaging.

## Historical L2 binary fixtures

Seven historical camera-validation PNGs are indexed in `benchmark/fixtures/REMOTE_BINARY_FIXTURES.json` with their Git blob IDs but are not embedded. The connected repository interface returned their base64 payloads truncated, so this reconstruction does **not** claim to be a byte-for-byte GitHub archive.

This limitation does not remove runtime code or the current 1.9.1 hardening logic. It means historical L2 visual fixture integrity should be rehydrated from GitHub when a raw clone/archive is available.
