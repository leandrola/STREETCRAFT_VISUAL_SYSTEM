# C0 · Reference Isolation · evidencia mínima

Fecha: 2026-09-29. Revisor: Codex, inspección local de solo lectura y anotación
prospectiva. Base: `2a5cd77b95566953a4e2a9d97eb87fe7f33fbff3` (`main`).
Gate: **C0_UNVERIFIED**; no satisface `C0_SCOPE_READY`.

## Fuente y observación

- Fuente: `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-C_source.jpg`.
- SHA-256 comprobado: `2130500a09548d4f9c1991a210de3cfa13d8ef63406dd0c3a78c257c68858a09`.
- JPEG de 1490 × 1490, inspeccionado a resolución nativa. Bytes sin modificar.
- Hechos visibles: escena de diorama, automóvil rojo en primer plano, tres
  figuras a la derecha, otros vehículos parcialmente visibles, fachadas al fondo
  y acera en primer plano. Esto describe la foto, no identifica el proyecto.
- Identidad authored Fear City: **UNVERIFIED**. Vínculo de esta captura con una
  vista authored `CG-FC`: **UNVERIFIED**. Fotógrafo y fecha original: **UNKNOWN**.
- No se transcriben carteles dudosos ni se atribuye una ciudad real. La candidata
  histórica no se utilizó como fuente ni como salida fresca.

## Autoridad revisada

Rutas relativas a la raíz del repositorio, en el commit base indicado:

| Evidencia | Alcance comprobado y límite |
| --- | --- |
| `benchmark/r2b_1_9_1/R2B_1_9_1_EXECUTION_PLAN.md`, bloque C | Objetivo histórico de preservar Fear City y CG-FC; no vincula una vista authored concreta al hash de C. |
| `validation/R2B_1_9_1_FINAL_2026_09_21.json`, caso C y `evidence_files` | Registra PASS histórico y el hash exacto de la fuente; no contiene confirmación authored/cámara específica de esa captura. |
| `validation/camera_routing/L3_FEAR_CITY_EVIDENCE_REGISTRY.json` | Confirma `FCV001-01` a `FCV001-04`; los cuatro hashes se comprobaron contra los JPEG locales. Ninguno coincide con C y no se documenta una derivación o correspondencia de C con esas vistas. La diferencia de hash por sí sola no descarta pertenencia al mismo proyecto. |
| `validation/camera_routing/L3_FEAR_CITY_ROUTING_REPORT.md` | Establece la ruta T06 → VP03 → CG-FC para Fear City confirmado; no confirma esta fuente. |
| `fear_city/VALIDATION_001.md` y `scene_intelligence/FEAR_CITY_SCENE_POLICY.md` | Anclas y política del mundo authored; no autorizan trasladar esas anclas a la fotografía C. |
| `validation/vsg_2b/corpus_audit.json`, entrada C | Fuente recibida con hash correcto, `RECEIVED_UNBOUND`; no aporta el vínculo faltante. |

La búsqueda local de C0, del ID `R2B-191-C`, del nombre de fuente y de su hash en
documentación y registros de evidencia no encontró un sidecar que establezca
imagen → identidad authored → vista. No se afirma que esa prueba no pueda existir
fuera del clon. No se inspeccionaron snapshots ni código para avanzar el binding.

## Límites y transferencias prohibidas

Preservar composición, relaciones visibles, vehículos y figuras; no eliminarlos
por preferencias generales. Mantener sin resolver texto dudoso, geometría oculta
y geografía. Prohibido importar de referencias geografía real, cámara, señalética
literal, props, humedad o arquitectura fuera de scope; también prohibido importar
las anclas de otras vistas Fear City sin evidencia de correspondencia. Estos son
límites de la spec y de la política, no observaciones adicionales de la foto.

Para habilitar `C0_SCOPE_READY` falta una autoridad identificable y verificable
(ruta/ID y hash) que vincule el SHA-256 exacto de C con el mundo authored Fear City
y establezca la relación de esta captura con CG-FC. Si deriva de una vista ya
confirmada, hace falta documentar esa derivación y la relación de cámara.

No se configura `fear_city_confirmed=true`. El gate de Archive/RR2 queda sin
evaluar: ninguna referencia admitida ni Reference Isolation Lock ejercitado.
