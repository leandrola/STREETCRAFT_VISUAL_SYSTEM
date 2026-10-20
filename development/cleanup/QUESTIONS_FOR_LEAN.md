# Registro formal de preguntas y decisiones de Lean

Estado del paso 7: **CERRADO**. Las cinco preguntas iniciales ya tienen decisión vinculante; no requieren una nueva respuesta de Lean para preparar el candidato.

| ID | Pregunta original | Decisión/hipótesis registrada | Estado |
| --- | --- | --- | --- |
| Q1 | ¿Qué hacer con `reference/assets/`, fuentes R2b y `outputs/`? | Conservar rutas leídas por runtime o atadas a hash/procedencia. Clasificar el resto como `ARCHIVE`. El único grupo actualmente apto es `outputs/vsg-2b-campaign/`; el detalle está en `ARCHIVE_EXIT_CANDIDATES.csv`. | RESUELTA_POR_LEAN |
| Q2 | ¿Build Kit 1:64 se archiva? | No. Es el próximo hito y se clasifica `KEEP_NEXT_MILESTONE`. La documentación dedicada encontrada es `ROADMAP.md` (3966 bytes); no se observó lectura runtime. Las menciones 1:64 de BD01/BD02 son parte del runtime estable. | RESUELTA_POR_LEAN |
| Q3 | ¿BD01/BD02 se preservan? | Sí, como `KEEP_RUNTIME`: catálogo de comandos/presets, especificación, implementación, pruebas, esquema y benchmark visual. | RESUELTA_POR_LEAN |
| Q4 | ¿Archive/Pinterest y mapas pueden archivarse? | No todavía. Permanecen conservados hasta completar procedencia; el nombre o antigüedad no basta para archivarlos. | RESUELTA_POR_LEAN |
| Q5 | ¿Qué hacer con `.browser-profile/`? | Eliminar únicamente del disco local después de confirmar que no es versionado ni referenciado. La comprobación Git ya confirma que no está versionado ni tiene historial y que `.gitignore` lo cubre. Esta fase no lo elimina. | RESUELTA_POR_LEAN |

## Preguntas abiertas

Ninguna para cerrar este inventario. La futura spec de ejecución debe elegir el mecanismo de archivo para la agrupación apta y registrar la reconstrucción del entorno antes de retirar artefactos locales regenerables.
