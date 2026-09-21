# Reference Reasoning 2.0 · Archive integration · dev2

> Historical development integration record; its pending status and synthetic-only results are superseded by [the stable Archive integration](../../REFERENCE_REASONING_ARCHIVE_INTEGRATION.md). SVS 1.10.0 STABLE is the sole current client. The executable examples below use the current runner name; they do not introduce another runtime.

12/12 comprobaciones contra módulos reales de STREETCRAFT_ARCHIVE_V1_FINAL.
Evidence Units sintéticos, identificados como TEST / SYNTHETIC-TEST-ONLY: no equivale a recuperación sobre la colección real.
16 tests RR2, 89 existentes y 1 comprobación de entrada por archivos: PASS.

## Cambios
Se conservan los IDs de Evidence Bundles y la evidencia negativa en la traza.
Se admite task_context omitido como contexto vacío, sin inferirlo.
Entrada ejecutable: reference_runtime/run_reference_archive.py.
Archive continúa separado de SVS.

## Límite
Archive V1 Final entrega software y fixtures de prueba, pero no un catálogo clasificado de Evidence Units. Los snapshots de adquisición no sustituyen ese catálogo.
El motor Archive marca hechos distintos de un dominio como posibles conflictos; se mantiene esa regla conservadora, aunque puede requerir revisión de hechos compatibles.

## Ejecución
python3 reference_runtime/run_reference_archive.py --archive-root /ruta/STREETCRAFT_ARCHIVE_V1_FINAL --evidence /ruta/evidence_units.json --request /ruta/request.json --output /ruta/result.json

Evidence: array JSON de unidades clasificadas con evidence_unit_id, domain, visible_fact, permitted_learning, provenance_level, transfer_risk y status; procedentes de datos documentales existentes.
Request: objeto con needs, profile, mode, camera y controles RR2 opcionales. Necesidades compatibles con classify_reference_need.
Salida: SHA-256 de entradas y módulos Archive. Exit 2 si quedan requisitos sin resolver o revisión pendiente. No existe fallback de evidencia inventada.

## Estado
1.9.1 Stable por decisión del usuario; R2b incompleto, sin PASS visual.
1.10.0-dev2 sigue en desarrollo. Catálogo real y validación visual pendientes.
Entrada necesaria: export clasificado de Evidence Units o ubicación de ese catálogo.
No se hizo push. Formatos de exportación se mantienen en ROADMAP.md.
