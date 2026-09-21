# Hito 4 · SVS 1.10.0 · PROMOCIÓN A STABLE

Fecha: 2026-09-21

## Dictamen

**PASS → SVS 1.10.0 STABLE**

La promoción se ejecuta por decisión explícita del usuario después de cerrar todos los gates técnicos del Roadmap 21/9.

## Evidencia del gate

- Regression unificada: **PASS**.
- R2b visual: **6/6 PASS · score 91.0 · S3=0**.
- Integridad de evidencia visual: **14/14 archivos con SHA-256 y tamaño coincidentes**.
- RR2 unit tests: **18/18 PASS**.
- Orchestrator: **10/10 PASS**.
- RR2 contra evidencia real: **8/8 PASS**.
- Bundles, traces, evidence SHA y request SHA: **preservados**.
- CGC end-to-end con Archive: **8/8 PASS**.
- Identidad del runtime Archive: **20/20 módulos SHA-256 MATCH** contra `STREETCRAFT_ARCHIVE_V1_FINAL`.

## Flujo estable

`CIL → SAR2 → CGC draft → Reference Needs → Archive → RR2 → CGC enriched → 1.9.1 hardening/preflight → GENERATION_READY / explicit block`

## Nota de procedencia Archive

El ZIP de Library `STREETCRAFT_ARCHIVE_V1_FINAL.zip` no pudo materializarse como bytes crudos en este entorno. Para Gate 4 se re-ejecutó el runtime contra una copia cuyos 20 módulos Python ejercitados coinciden byte-a-byte por SHA-256 con el manifest registrado de `STREETCRAFT_ARCHIVE_V1_FINAL`. El gate certifica el runtime y la ruta RR2/CGC usados por Streetcraft; no vuelve a certificar el packaging completo de adquisición/release del producto Archive.
