# Reference Reasoning 2.0 · Integración Archive de SVS 1.10.0

## Estado actual

**PASS real V1 · 21/09/2026**

- 18/18 tests de Reference Reasoning 2.0 PASS.
- 8/8 casos reales PASS.
- Catálogo real clasificado V1: 10 Evidence Units.
- Runtime Archive usado: software byte-verificado contra los SHA-256 registrados para `STREETCRAFT_ARCHIVE_V1_FINAL`.
- Bundles, trazas, `evidence_sha256`, `request_sha256` y hashes de módulos Archive preservados.

## Cobertura real

- needs REQUIRED / SUPPORT / BLOCKED
- query budget
- cache reuse
- provenance floor
- dedupe cross-ID por fingerprint de contenido
- contradicciones estructuradas por `claim_key` / `claim_value`
- Semantic Text Lock
- Fear City Geographic Null Lock
- Occlusion / locked unknown

## Resultado

El hito **RR2 / Archive sintético → real** queda cerrado. La integración **CGC end-to-end** también quedó cerrada con 8/8 casos PASS.

Evidencia principal:
- `validation/RR2_REAL_ARCHIVE_VALIDATION_V1.json`
- `validation/rr2_real_archive/results/`
- `validation/rr2_real_archive/ARCHIVE_RUNTIME_IDENTITY.json`

Archive continúa separado de Canon y la evidencia admitida sigue siendo scoped. El handoff al adapter solo ocurre con `GENERATION_READY`.
