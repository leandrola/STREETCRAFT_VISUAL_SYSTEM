# Integración verificada · SVS 1.9.1 / CIL 1.1

- Master indicado por el usuario: STREETCRAFT_VISUAL_SYSTEM_V1_6_2.zip (copia de la carpeta Streetcraft, 12/09).
- Runtime y CIL conservados del paquete 1.9.1 / CIL 1.1 recuperado.
- 73 archivos faltantes restaurados desde master 1.6.2 y baseline 1.8.1.
- 7 PNG L2 recuperados: coincidencia exacta con los Git blob SHA previamente registrados.
- 25 golden fixtures íntegros. Baseline 1.8.1: 14 casos, 20 comprobaciones de fixtures, PASS.
- Tests existentes: CIL 19/19, Hardening 12/12, Archive-aware unit tests 10/10, Scene Intelligence 24/24, patch 24/24.
- Core, perfiles, Canon, comandos y patch preservados respecto del paquete 1.9.1 / CIL 1.1.
- Fuentes originales de CBGB, Fear City y oclusión recuperadas del audit histórico y comprobadas con SHA-256.
- Adaptador Archive V1 restaurado. Integración con un Archive externo real no ejecutada en esta corrida.
- No se recuperó ni se verificó el commit histórico 696afe5 en esta corrida; se conserva la reconstrucción semántica CIL 1.1 del paquete anterior.
- Los reportes anteriores describen sus builds históricos. El reporte vigente es validation/INTEGRATION_QA.json y el checksum vigente es INTEGRATED_SHA256SUMS.json.

## Estado y siguiente paso

Candidate; R2b pendiente; 0/6 candidatos frescos. La integridad del baseline no equivale a aprobación visual.
Siguiente ejecución: inspeccionar la fuente CBGB, fijar configuración y contrato de generación, generar un candidato individual y evaluarlo por separado. No agregar etiquetas ni dashboards.
Los goldens de cámara son salidas históricas: no son fotografías originales ni candidatos frescos. La fuente para los casos CG-A/B/F debe seleccionarse explícitamente antes de generarlos.
La integración no implica push a GitHub ni promoción a Stable.

## Exportación preservada en ROADMAP.md e IMAGE_EXPORT_FORMATS.md

A4 y A3 horizontales: 150/300 dpi. 90 × 45 cm: 150 dpi únicamente. Export runtime definido, aún no implementado.
