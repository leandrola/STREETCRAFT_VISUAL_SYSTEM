# Streetcraft SVS 1.10.0 · Stable

## Estado 21/09/2026

**SVS 1.10.0 está promovido a STABLE.** Streetcraft continúa como un único cliente.

Gate final de promoción:
- Regression unificada: **PASS**.
- R2b visual: **6/6 · S3=0 · 91.0 PASS**.
- Evidencia visual: **14/14 archivos verificados por SHA-256**.
- Reference Reasoning 2.0: **18/18 tests PASS**.
- Catálogo real V1: **10 Evidence Units**.
- RR2 / Archive real: **8/8 PASS**, con bundles, traces y provenance SHA preservados.
- CGC end-to-end: **8/8 PASS**.
- Orquestador: **10/10 PASS**.
- Runtime Archive: **20/20 módulos SHA-256 MATCH** contra la identidad registrada de `STREETCRAFT_ARCHIVE_V1_FINAL`.

Flujo estable:
`CIL → SAR2 → CGC draft → Reference Needs → Archive → RR2 → CGC enriched → hardening/preflight → GENERATION_READY / explicit block`

Entry point: `STREETCRAFT.md`  
Orquestación: `integration/streetcraft_orchestrator.py`  
Gate final: `validation/RELEASE_GATE_1_10_0_FINAL.json`
