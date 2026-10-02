# VSG-2B / N4R · Propuesta separada de settings y control

**PROPOSED_NOT_APPROVED · NOT_APPLIED.** No es manifest operacional ni autorización
de implementación, pesos, forwards, entrenamiento o generación.

Problema: máscara M_KEEP=1 + reinyección fuente en cada paso + schedule relacional
temprano beta0.3 deja de transmitir el canal B a la salida final cuando PNDM vacía
su memoria. Con defaults50 pasos/51 llamadas, la última influencia posible está
en índice17 y la salida es índice50. No usar diferencias textuales A/B como evidencia
del canal estructural. Véase [análisis N4](N4_GLIGEN_FEASIBILITY_RUNBOOK.md).

El manifest D actual conserva DRY_RUN_ONLY, seed null y size347x389. **No tiene beta
operacional congelada**;0.3 es el default upstream usado para el análisis. Esta
propuesta elige settings nuevos expresamente y debe pasar una decisión posterior.
No presenta beta1 como una corrección ya autorizada ni aplica PROPOSED_SCOPE.diff.

| Variable | Actual / referencia | Propuesta para decidir |
| --- | --- | --- |
| Schedule relacional | No seleccionado; upstream default0.3 | beta1.0: canal condicional B presente hasta última llamada |
| Transformaciones compartidas del fuser | Upstream enabled=false retira attention y FF | Patch externo simétrico mantiene attention/FF/S en A/B; solo R varía |
| Steps / CFG / eta | No seleccionados; defaults50/7.5/0 | Fijar50/7.5/0 conjuntamente para esta variante, no asumir defaults implícitos |
| Fuente / salida | D347×389 congelado | Igual fuente y salida; padding interno512 sin resize, sin composición de píxeles finales |
| Máscara | No máscara operacional | M_KEEP1 compartida; reinyección latente, ninguna región de edición autorizada nueva |
| Seed | null | Valor concreto pendiente en settings versionados; streams y estados completos además del seed |
| Modelo | Placeholder DRY_RUN_ONLY | Misma base fijada + módulos aprendidos compartidos, aún inexistentes |

Con beta1, el canal puede modificar la última predicción y PNDM final sin borrado
posterior por reinyección. Eso abre una ruta computacional; **no demuestra** efecto
útil, fidelidad del literal, calidad, conservación del source ni sensibilidad visible
tras safety/postprocess. Requiere pruebas futuras de réplica, hooks en pasos finales,
ablación, mutación aislada, latente final y juicio semántico visual independiente.

La enmienda no agrega campos a common, no cambia los diez registros, no interpreta
locks como órdenes de edición y no da información oculta distinta a A/B. Los datos
comunes de regiones/etiquetas solo asocian IDs observados a fuente. No aprobar M0,
boxes de edición o nuevos targets mediante esta propuesta.

Decisión posterior requerida: aceptar/rechazar este protocolo de inferencia y el
patch simétrico declarado como diseño, especificando su frontera experimental.
Si se acepta, redactar un plan de implementación y recursos separado; no ejecutarlo
por defecto. Antes de una campaña se requieren manifest nuevo/versionado, delta
review, seed real, presupuesto, validación de pesos y admisión expresa. No sustituir
ni actualizar silenciosamente el manifest congelado.

Criterios para descartar la variante aun si se acepta su estudio: efecto final
ausente o solo ruido/artefacto, pérdida protegida, dependencia de edit masks sin
autoridad, texto truncado o canal R sin significado aprendido. No abrir otro backend
ni X1 como fallback automático.

Rollback: rechazar o archivar esta propuesta, conservar N4_SCOPE_CHANGE_REQUIRED y
N3_MODEL_DEVELOPMENT_REQUIRED, sin ningún cambio a cliente, política, corpus o gate.
