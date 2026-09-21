# Reference Reasoning 2.0 · Integración principal de SVS 1.10.0

Estado: EN DESARROLLO dentro del único cliente Streetcraft. Amplía la admisión Archive 1.7 como componente interno y constituye la interfaz principal de razonamiento de referencias.

## Flujo implementado
Validar necesidades → ordenar dependencias → priorizar requeridas → aplicar presupuesto → consultar Archive → filtrar procedencia y duplicados → aplicar admisión existente → resolver contradicciones → proyectar evidencia admitida al CGC.

`resolve_reference` recibe las necesidades existentes con `depends_on` opcional. Usa el callback Archive (`request` → `bundle`) de la capa interna de admisión. La solicitud agrega `specific_problem`. No requiere nuevos comandos CIL.

- RN_NONE evita consultas y registra que la fuente es suficiente.
- RN_BLOCKED conserva unknowns; no busca referencias para rellenarlos.
- Una necesidad requerida dependiente de un unknown bloqueado permanece sin resolver.
- RN_REQUIRED tiene prioridad sobre soporte opcional, respetando las dependencias.
- El presupuesto limita llamadas reales; errores consumen la llamada efectuada.
- Caché por solicitud completa y problema, dentro de una sola ejecución. No reutiliza evidencia entre escenas o ejecuciones.
- Se exige ID y procedencia mínima P0–P4 (orden ascendente heredado de los datos del proyecto).
- Duplicados del mismo Evidence Unit ID no cuentan como evidencia independiente; diferencias bajo el mismo ID requieren revisión.
- La admisión existente mantiene los locks de texto, oclusión, cámara y geografía Fear City.
- Evidencia negativa o pendiente de revisión no entra en la proyección.
- Si falta evidencia requerida, se bloquea la proyección completa; el soporte opcional ausente no bloquea.
- La salida incluye traza por necesidad, IDs de evidencia, razones, consultas y unknowns conservados.
- `enrich_cgc_v2` solo acepta READY y copia el contrato sin mutar sus locks.

## Uso

Desde Python, incluir `reference_runtime` en el import path, importar `resolve_reference` y `enrich_cgc` desde `reference_reasoning`. Pasar `needs`, `profile`, `mode`, `camera`, `archive_retriever`; opcionalmente `query_budget`, `allow_support`, `semantic_text_lock`, `occlusion_locked`, `fear_city_confirmed`.

READY significa que las necesidades documentales modeladas están satisfechas o son opcionales. No certifica calidad visual ni reemplaza el preflight 1.9.1 o el Critic.

## Límites y pendientes

- Saturación inicial: una consulta por necesidad; sin búsqueda iterativa adaptativa ni ranking nuevo.
- Conflictos detectados por IDs inconsistentes y conflictos estructurados del bundle. No se infieren contradicciones semánticas en lenguaje natural.
- No deduplica contenidos iguales con IDs distintos todavía.
- No analiza imágenes ni crea SAR2 automáticamente.
- No ejecuta por sí mismo generación ni preflight 1.9.1: deben permanecer en el flujo posterior.
- Validación con un catálogo Archive real y nueva validación visual pendientes. Los 16 casos automatizados usan callbacks controlados.
- Siguiente entrega: integrar y probar el adaptador Archive real; después ampliar deduplicación/contradicciones y evaluar cambios visuales.

La promoción excepcional de 1.9.1 no constituye aprobación final de SVS 1.10.0.

## Integración Archive
Integración de software Archive: 12 comprobaciones PASS con datos sintéticos. Catálogo real no disponible. Entrada ejecutable: `run_reference_archive.py`; las trazas retienen bundle IDs y `negative_evidence`.
