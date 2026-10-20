# Candidato verificable de limpieza

**Rama:** `cleanup/inventory` · **Estado:** candidato documental; sin movimientos, borrados ni merge a `main`.

## Estado

| Paso | Estado | Evidencia |
| --- | --- | --- |
| 1. Medición | CERRADO | `directory_metrics.csv`, `largest_50.csv`, `binary_files.csv` |
| 2. Alcanzabilidad SVS 1.10.0 | CERRADO | `reachability.json`, `EXECUTION_READ_PATHS.csv` |
| 3. Hashes, procedencia y multiagente | CERRADO | `STEP3_REFERENCE_TRIAGE.json`, `UNTOUCHABLE_HASH_PROVENANCE.csv` |
| 4. Clasificación | CERRADO | `CLASSIFICATION_CANDIDATE.csv` |
| 5. Riesgos ARCHIVE | CERRADO | `ARCHIVE_EXIT_CANDIDATES.csv` |
| 6. Línea base | CERRADO | `baseline_results.json` (`PASS_LOCAL`) |
| 7. Preguntas | CERRADO | `QUESTIONS_FOR_LEAN.md` |

## Lista intocable

La lista definitiva contiene **1.065 rutas** en `UNTOUCHABLE_HASH_PROVENANCE.csv`; cada una debe permanecer en su ruta actual hasta reemplazar las referencias y hashes que la fijan. Sus fuentes autoritativas son:

- `development/coordination/CHECKPOINT.json`
- `SVS_1_10_0_SHA256SUMS.json`
- `PACKAGE_MANIFEST.json`
- `RECONSTRUCTION_PROVENANCE.json`
- los manifiestos, recibos y procedencias de `validation/sc_multiagent/` enumerados en `STEP3_REFERENCE_TRIAGE.json`

Además, el runtime estable alcanza 15 rutas por importación/lectura explícita; se enumeran en `EXECUTION_READ_PATHS.csv`. BD01/BD02 se mantienen como `KEEP_RUNTIME` junto con su catálogo, implementación, esquema, pruebas y benchmark visual.

## ARCHIVE apto para salir de `main`

| Agrupación | Archivos | Tamaño | Estado |
| --- | ---: | ---: | --- |
| `outputs/vsg-2b-campaign/` | 28 | 666.708 bytes | APTA_CON_PLAN_DE_RETIRO |

No tiene referencia de hash/procedencia ni lectura runtime detectada. Es una autorización técnica para preparar un plan: no autoriza mover ni borrar todavía. Los restantes materiales cerrados siguen retenidos porque la lista intocable conserva sus rutas.

## Próximo hito y decisiones ya aplicadas

- Build Kit queda como `KEEP_NEXT_MILESTONE`: el único documento dedicado hallado es `ROADMAP.md` (3.966 bytes), sin lectura runtime observada. Las menciones 1:64 de BD01/BD02 permanecen `KEEP_RUNTIME`.
- Archive/Pinterest y mapas se retienen hasta cerrar procedencia.
- `.browser-profile/` no aparece en historial ni índice Git y está ignorado; [BROWSER_PROFILE_AUDIT.md](BROWSER_PROFILE_AUDIT.md) registra el resultado sin leer su contenido. Puede eliminarse solo del disco local en una acción posterior autorizada.
- [VENV_SC_REBUILD.md](VENV_SC_REBUILD.md) registra cómo reconstruir `.venv-sc` antes de retirar ese entorno regenerable.

## Riesgos y límites

- Los hashes/procedencia dominan la clasificación: `ARCHIVE` funcional no implica que pueda salir de `main`.
- La línea base local no sustituye el runtime Archive externo, SC05/SC06 ni evaluación visual.
- Los anexos de inventario son deliberadamente grandes y permanecen en esta rama; no deben incorporarse a `main` salvo decisión explícita.
