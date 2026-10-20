# Estado del inventario después de la interrupción

**Auditoría:** 2026-10-19 (solo lectura de los artefactos existentes)

**Rama auditada:** `cleanup/inventory`
**Base contra la que se comparó:** `main` = `241366d08558c0f9240a895a3801bb21748023fc`

## 1. Rama y último commit

| Campo | Valor |
| --- | --- |
| Rama local | `cleanup/inventory` |
| Remota observada | `origin/cleanup/inventory`, mismo hash |
| Último commit | `291e2c24776a9758466421314b02f88e3ec80c92` |
| Fecha del autor | `2026-10-19T21:24:11-03:00` |
| Mensaje | `Refactor code structure for improved readability and maintainability` |

No se hizo push durante esta auditoría.

## 2. Alcance real del diff

`git diff --stat main...cleanup/inventory` informa **19 archivos añadidos, 300456 inserciones**. Todos pertenecen a `development/cleanup/`; no hay modificación, movimiento ni borrado fuera de ese directorio. Los 19 archivos son los anexos de inventario y sus dos scripts de producción/verificación.

El commit de inventario ya estaba presente antes de esta auditoría y aparece también en la referencia remota. Esta auditoría no lo reescribió ni lo publicó.

## 3. Estado por paso de la spec

| Paso | Estado | Evidencia | Motivo |
| --- | --- | --- | --- |
| 1. Medición de tamaños, conteos, líneas, binarios y regenerables | **CERRADO** | [directory_metrics.csv](directory_metrics.csv), [largest_50.csv](largest_50.csv), [binary_files.csv](binary_files.csv), [local_generated.csv](local_generated.csv), [inventory_summary.json](inventory_summary.json) | Cubre primer/segundo nivel, top 50, líneas de texto/MD/JSON, imágenes/binarios y directorios locales. El perfil de navegador se midió sin leer contenido de sesión. |
| 2. Alcanzables desde SVS 1.10.0 | **CERRADO** | [reachability.json](reachability.json), [references.csv](references.csv), [inventory_audit.py](inventory_audit.py) | Parte de CLI/orquestador/RR2, AST de imports y lecturas explícitas. Identifica 15 archivos ejecutables y declara entradas dinámicas/external Archive y límites del análisis estático. |
| 3. Multiagente, CHECKPOINT y manifiestos/procedencia | **PARCIAL** | [protected_references.json](protected_references.json), [protected_paths.csv](protected_paths.csv), [hash_bindings.csv](hash_bindings.csv) | Se procesaron 377 fuentes de manifiesto/procedencia, incluido `CHECKPOINT.json`; hay 91 referencias desde él (70 resueltas) y protección de paths. Quedan 3483 referencias sin resolver de forma estática: rutas externas, históricas, dinámicas o no normalizadas requieren triage explícito antes de afirmar que la lista sea exhaustiva. |
| 4. Clasificación completa | **CERRADO** | [classification.csv](classification.csv) | Los 5654 archivos inventariados tienen una categoría y una razón. Las seis categorías solicitadas aparecen y cada fila conserva estado Git, hash cuando fue leído y fuente de protección. |
| 5. Riesgos de retirar ARCHIVE | **CERRADO** | [archive_risks.json](archive_risks.json), [references.csv](references.csv) | Hay una entrada por cada uno de 86 agrupamientos de ARCHIVE, con referencias entrantes desde KEEP, archivos protegidos y advertencia sobre dependencias dinámicas. Se detectaron 5571 aristas entrantes desde KEEP en total. |
| 6. Línea base de tests | **CERRADO** | [baseline_results.json](baseline_results.json), [baseline_result_hash.json](baseline_result_hash.json), [runtime_dry_run.json](runtime_dry_run.json) | 13 verificaciones locales existentes y los tests SC03 pasaron en copia temporal aislada. El informe tiene hash `527eb6c916bbe35c92d531bbd4ab71f0e5389aeb16a964a909130abf59c7bd18`; el dry run repetible tiene hash `0cee4e3f842c76d478c9be89034eaeae8c34b815f0202701c20a30f49498cee6`. No hubo generación ni modificaciones al runtime. La reejecución real del Archive externo quedó explícitamente fuera de alcance por ausencia de sus bytes. |
| 7. Lista de preguntas | **NO INICIADO** | — | Los límites y entradas dinámicas quedaron anotados como datos de método, pero no se sintetizó una lista de preguntas con hipótesis para decisión de Lean. |

## 4. Qué falta y orden recomendado

| Orden | Trabajo pendiente | Estimación | Resultado necesario |
| --- | --- | ---: | --- |
| 1 | Triage de las 3483 referencias no resueltas: separar externas, históricas, enlaces rotos y rutas dinámicas; resolver las que afecten a `CHECKPOINT.json` o manifiestos hash/provenance. | 12k–18k tokens | Paso 3 cerrado con una lista explícita de preservación intocable. |
| 2 | Revisar la clasificación de `ARCHIVE` frente a esas referencias resueltas; dividir los agrupamientos que mezclen evidencia congelada con material archivables. | 6k–10k tokens | Lista ejecutable de ARCHIVE sin romper hashes, tests ni enlaces KEEP. |
| 3 | Redactar preguntas con hipótesis para `DECISION_USER`, incluyendo Build Kit 1:64, BD01/BD02, fuentes visuales, Archive/Pinterest, mapas y perfil del navegador. | 3k–5k tokens | Paso 7 cerrado y decisiones de Lean aisladas. |
| 4 | Recalcular anexos y revisar consistencia final de categorías, riesgos, rutas protegidas y baseline antes de aceptar una spec de ejecución. | 4k–7k tokens | Candidato de limpieza verificable; todavía sin borrar ni mover. |

Estas estimaciones son para completar el informe y no incluyen ejecutar la limpieza posterior. Si se suministra el runtime externo `STREETCRAFT_ARCHIVE_V1_FINAL`, su validación de identidad y la reejecución de casos reales requerirían una tarea independiente (estimación adicional: 5k–8k tokens, sin generación de imágenes).

## 5. Preguntas pendientes de elaborar

El paso 7 no produjo una lista formal. Las preguntas que deben convertirse en decisiones, con hipótesis inicial, son:

1. ¿`reference/assets/`, fuentes R2b y `outputs/` son insumos activos del chat de generación o solo evidencia histórica? **Hipótesis:** `DECISION_USER`; hay rutas y hashes, pero no importación runtime directa.
2. ¿Build Kit y la escala 1:64 permanecen como documentación/decisión futura? **Hipótesis:** `DECISION_USER`; aparecen en documentación y no en el cierre de runtime ejecutable.
3. ¿BD01/BD02 deben preservarse para generación? **Hipótesis:** sí; CIL los carga desde `COMMANDS.json` y `BACKDROP_PRESETS.json`, y las pruebas pasan por esa ruta.
4. ¿Las referencias Archive/Pinterest y mapas pueden salir de `main` sin quebrar trazabilidad? **Hipótesis:** no hasta resolver cada entrada de procedencia y sus derechos/ubicación de archivo.
5. ¿El perfil `.browser-profile/` se conserva localmente, se elimina localmente o se migra? **Hipótesis:** `DECISION_USER`; mide 98.8 MB y no se inspeccionó por contener sesión persistente.

## 6. Límites confirmados

- La clasificación no autoriza borrar: incluso `ARCHIVE` puede estar protegido por hashes o por referencias entrantes.
- Los entornos `.venv`/`.venv-sc` y cachés se clasifican como regenerables, pero el entorno usado para la línea base fue `.venv-sc` con Python 3.14.5, Pillow 12.3.0 y jsonschema 4.26.0. La spec de ejecución debe registrar cómo reconstruirlo antes de eliminarlo.
- La línea base local comprueba el runtime estable y el supervisor simulado; no certifica Archive real externo, ejecución SC05/SC06 ni calidad visual.
