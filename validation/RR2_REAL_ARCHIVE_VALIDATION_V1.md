# RR2 Real Archive Validation V1

Status: **PASS**

18/18 RR2 unit tests PASS. Real Archive cases: 8/8 PASS.

| Case | Engine | Queries | Bundle(s) | Validation |
|---|---|---:|---|---|
| RR2-REAL-01 | READY | 1 | EB-DC359DF66953C6 | PASS |
| RR2-REAL-02 | BLOCKED_REQUIRED | 1 | EB-C083A66826FE3E | PASS |
| RR2-REAL-03 | BLOCKED_REQUIRED | 1 | EB-9BA03D3143A615 | PASS |
| RR2-REAL-04 | READY | 1 | EB-F4E99D8A934174 | PASS |
| RR2-REAL-05 | BLOCKED_REQUIRED | 1 | EB-EBD0C9A0C73346 | PASS |
| RR2-REAL-06 | READY | 1 | EB-1270277FF04F5F | PASS |
| RR2-REAL-07 | READY | 0 | none (no query) | PASS |
| RR2-REAL-08 | READY | 1 | EB-6082F854D94C8D | PASS |

For every queried case, the persisted result includes `input_provenance.evidence_sha256`, `input_provenance.request_sha256`, the SHA-256 map of Archive runtime modules, the full RR2 trace and Evidence Bundle IDs.

The Archive runtime used here was recovered from the previously validated RR2 package and byte-verified against the module hashes recorded by `validation/REFERENCE_REASONING_ARCHIVE_INTEGRATION.json` for STREETCRAFT_ARCHIVE_V1_FINAL.
