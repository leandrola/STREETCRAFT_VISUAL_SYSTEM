# sc_history: informe devuelto por el agente

task_id: `SC-MULTIAGENT-01-P1-HISTORY`  
Rol: `sc_history`, instrucciones aplicadas manualmente; modelo efectivo: `UNKNOWN` — la interfaz de este hilo no expone un identificador verificable. El TOML solicita `gpt-6.1-sol`, sin demostrar su carga efectiva.  
Base: `33b6581353b18004a4818e8fc597b5455ba7ccf3`  
Resultado: **PASS documental**, sin evaluación visual.

1. **La fidelidad parte de la identidad documental o autoral de la fuente.** La intención explícita y los invariantes P0 preceden modo, perfil y restricciones de período/región (`STREETCRAFT.md:9–20`). Archive queda subordinado a los invariantes y locks (`reference_runtime/REFERENCE_AUTHORITY_MAP.md:2`). Inferencia: una referencia históricamente plausible no autoriza reemplazar la identidad de la fuente.

2. **Plausibilidad, observación e inferencia tienen categorías separadas.** El modelo distingue `OBSERVED / DERIVED / INFERRED / GENERATED / UNKNOWN`, registra confianza y declara que la plausibilidad no equivale a observación (`core/PRESERVATION_MODEL.md:25–30`). Las zonas P5 separan continuación, inferencia estructural, contextual y desconocimiento (`core/PRESERVATION_MODEL.md:11–16`). Una región oculta de una sola vista queda `LOCKED_UNKNOWN`; múltiples vistas pueden permitir reconstrucción acotada (`hardening/OCCLUSION_LOCKS.md:2`).

3. **La evidencia requiere procedencia y aprendizaje limitado.** RR2 exige ID y procedencia mínima, evita contar duplicados como evidencia independiente y excluye evidencia negativa o pendiente de revisión (`reference_runtime/REFERENCE_REASONING_2.md:16–22`). El catálogo separa `USER_SOURCE_FIXTURE` de `MODEL_CANDIDATE_OUTPUT`, registra hashes y declara aprendizajes permitidos y transferencias prohibidas (`reference_runtime/real_catalog/REAL_EVIDENCE_CATALOG_V1.json:3–18`, `:24–39`). La fecha `2026-09-21` se describe como origen de la entrega/candidato; no demuestra fecha de captura histórica, autoría ni licencia.

4. **La geografía no se deduce por parecido y el texto incierto no se completa.** En Fear City la identidad geográfica externa es NULL por defecto y el parecido visual no constituye evidencia (`patch/FEAR_CITY_GEOGRAPHIC_NULL_LOCK.md:3–18`). Los tokens legibles de identidad se congelan; los parciales conservan únicamente fragmentos conocidos y el microtexto ilegible mantiene comportamiento gráfico (`patch/SEMANTIC_TOKEN_FREEZE.md:7–25`). Direcciones, nombres de calles, precios y titulares inventados están prohibidos (`patch/LOW_CONFIDENCE_TEXT_MASK.md:12–22`).

5. **READY documental no acredita calidad visual ni autenticidad histórica.** RR2 READY significa satisfacción de necesidades documentales modeladas, sin certificar calidad visual (`reference_runtime/REFERENCE_REASONING_2.md:28`). El catálogo es metadata-only y su reejecución requiere el runtime externo identificado (`reference_runtime/real_catalog/README.md:11`, `:26–28`). Inferencia: los contratos permiten controlar anacronismos cuando existe evidencia explícita; este análisis no acredita fecha, ciudad, autoría, licencia ni ausencia visual de anacronismos en una imagen.

Validaciones: HEAD y digest del checkpoint coinciden al inicio y al cierre; digest `2c60a49a3d58581dc40602e9c9357ea4d8ca842a0520d18b1b0bbc8d96ea1cc0`. `git diff --name-only HEAD` no mostró cambios en los contratos leídos. Leídos AGENTS, perfil, checkpoint, README y protocolo.  
Patch/archivos modificados: ninguno. Herramientas permiten escritura compartida; lectura fue una restricción de autorización, no aislamiento técnico. Sin ejecución de runtime, tests, imágenes, GLIGEN ni fuentes externas.  
Recomendación: preservar fechas de entrega separadas de fechas históricas y mantener `UNKNOWN` cuando falte procedencia suficiente. Bloqueos: ninguno para el análisis.

Cierre: análisis documental completado sobre la base asignada.  
Evidencia: cinco hallazgos citados; contratos y checkpoint preservados.  
Mantener: límites operativos, locks y validación visual pendiente.

Nota del orquestador: metadata local del hilo 01a132fb-0cc0-7702-9a59-c28da9944ee9 registra modelo efectivo gpt-6.1-sol, esfuerzo medium. El UNKNOWN del informe indica lo que el agente pudo observar; no se reemplaza su respuesta original.
