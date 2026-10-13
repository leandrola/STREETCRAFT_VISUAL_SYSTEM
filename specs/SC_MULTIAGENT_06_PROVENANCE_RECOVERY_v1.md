# Streetcraft · Recuperación verificable de procedencia de implementación

**ID:** SC-MULTIAGENT-06 · **Versión:** 1.0 · **Fecha:** 2026-10-13  
**Estado:** SPEC_READY. No acredita recuperación, reconstrucción, revisión ni integración realizadas.  
**Origen:** decisión explícita de Lean para resolver el bloqueo vigente de SC-MULTIAGENT-04.  
**Dependencias:** SC-MULTIAGENT-01 READY en modalidad `DELEGATED_ANALYSIS_CENTRALIZED_WRITES`; candidato local 02/03; diagnóstico `REVIEW_PROVENANCE_BLOCKED` de 04.  
**Destino:** Codex sobre el repo vivo, con root como único escritor e integrador.

## 1. Problema y resultado visible

SC-MULTIAGENT-04 no puede acreditar que el revisor sea distinto del implementador porque el modelo efectivo de la implementación material del supervisor quedó `UNKNOWN`. Los modelos configurados, los nombres de perfiles y la identidad de revisores anteriores no resuelven esa atribución.

Esta spec define una recuperación única y verificable. El resultado para Lean será uno de estos:

- procedencia histórica recuperada y revisión independiente del candidato exacto;
- reconstrucción material trazable, seguida de revisión independiente del candidato exacto;
- bloqueo concreto y conservado, sin integrar ni iniciar el piloto 05.

La salvaguarda de modelos distintos se mantiene. No se acepta copiar o reemitir los mismos bytes para asignarles otra autoría.

**Tarjeta Go:** resolver la procedencia que bloquea 04 con metadata local o con una reconstrucción material acotada; gasto adicional cero, imágenes cero, una ronda de corrección y escritura centralizada.

## 2. Estado de entrada y preservación

Antes de cualquier ejecución:

1. Leer AGENTS.md, checkpoint, plan maestro y specs 01, 03, 04 y 05.
2. Registrar HEAD, upstream, cambios locales y hash del checkpoint con el Git funcional disponible.
3. Preservar el candidato local y la evidencia histórica. No reaplicar patches ni importar nuevamente specs ya presentes.
4. Comprobar el manifiesto congelado de 04. La admisión de esta spec lo convierte en evidencia histórica del candidato anterior; debe congelarse un manifiesto nuevo antes de una revisión.
5. Confirmar que no existe otro orquestador activo y que root conserva la única escritura del checkpoint.
6. Verificar cuota y modelos disponibles justo antes de invocar. Si el entorno no expone cuota, registrar `UNKNOWN`; no inventar porcentaje.

La inspección de metadata extrae solo identificadores de sesión/turno, modelo, timestamps y vínculo al candidato. No copia prompts, credenciales, rollouts completos ni datos personales no necesarios.

## 3. Ruta A · Recuperar procedencia histórica

La ruta preferida no modifica código:

1. Localizar la sesión Agent Host asociada a la implementación material y sus turnos pertinentes.
2. Consultar metadata local o del proveedor ya disponible para esos turnos.
3. Exigir un identificador de modelo registrado por el runtime y ligado al turno material; el autoinforme del modelo y el TOML no bastan.
4. Registrar fuente, sesión, turno, timestamp, componente y modelo efectivo, con cualquier límite de atribución.
5. Comparar ese identificador con el del revisor propuesto.

Si la metadata recuperada cubre la implementación material del supervisor, congelar el candidato actual y pasar a la revisión de la sección 5. Si la metadata sigue ausente o no liga modelo y turno material, registrar `HISTORICAL_PROVENANCE_UNAVAILABLE` y pasar una sola vez a la ruta B.

No repetir búsquedas equivalentes ni gastar llamadas de modelo para consultar metadata que puede leerse localmente.

## 4. Ruta B · Reconstrucción material trazable

La ruta B está autorizada por esta spec únicamente cuando la ruta A no puede acreditar autoría. Debe producir una mejora material y necesaria del componente afectado, no un cambio cosmético.

### 4.1 Contrato del implementador

El implementador recibe task_id, objetivo, entregable observable, base, digest del checkpoint, contratos, archivos permitidos, dependencias, cierre, esfuerzo y parada. La ejecución debe persistir metadata con modelo efectivo observable.

Debido a `CHILD_SANDBOX_UNAVAILABLE`, el implementador trabaja en lectura y devuelve análisis, diseño y patch propuesto. Root aplica el patch de forma serial y mecánica, conserva cualquier adaptación y registra la correspondencia. No hay escritura delegada ni implementaciones paralelas.

Archivos permitidos para una reconstrucción necesaria:

- `scripts/sc_supervisor.py`;
- `tests/test_sc_supervisor.py` y fixtures estrictamente relacionados;
- `docs/SC_CONTINUITY_QUICKSTART.md` cuando cambie el comportamiento visible;
- evidencia de SC-MULTIAGENT-06 y delta del checkpoint por root.

### 4.2 Materialidad mínima

El cambio debe cerrar un hueco real hallado al revisar los contratos actuales. Son candidatos válidos, si la inspección demuestra que faltan:

- validación y versionado reproducible del digest del sobre;
- preservación de identidad de proceso y sesión durante start/resume/reconcile;
- rechazo seguro de estados o eventos desconocidos;
- recuperación sin relanzamiento tras caída entre invocaciones;
- pruebas de una falla contractual que el candidato anterior no cubría.

El recibo explica el requisito, el comportamiento anterior, el patch propuesto y la prueba que demuestra la diferencia. Un reformateo, renombre, comentario o reescritura byte-equivalente no cumple.

### 4.3 Atribución

La procedencia reconstruida se acredita solo si la metadata persistida liga el turno del implementador, su modelo efectivo y el patch material. Root puede resolver conflictos menores al aplicar, pero cualquier cambio material adicional de root queda `UNKNOWN` y exige nueva atribución o impide el cierre.

Si la invocación no expone el modelo efectivo, parar con `IMPLEMENTER_MODEL_UNAVAILABLE`; no probar perfiles sucesivos.

## 5. Congelamiento y revisión independiente

Antes de llamar al revisor, root crea un manifiesto por archivo con base, operación y SHA-256, más un hash combinado con receta explícita. Incluye código, tests, documentación y el checkpoint previsto para integración. Excluye el propio manifiesto y el recibo posterior para evitar autorreferencia.

El revisor:

- usa un modelo efectivo registrado por runtime y distinto del implementador;
- recibe el candidato congelado, specs y evidencia de procedencia;
- trabaja solo en lectura;
- revisa comportamiento del supervisor, lock, procesos, resume, reconcile, digest, separación de estado y límites;
- verifica que el patch material corresponda al implementador identificado;
- devuelve PASS, FAIL o BLOCKED con hallazgos y vínculo al hash combinado.

Un revisor previamente identificado puede reutilizarse solo si revisa el nuevo candidato exacto y su turno queda ligado al modelo efectivo. Una revisión de un hash anterior no se hereda.

Se permite una sola ronda de corrección. Si el candidato cambia materialmente, root vuelve a congelarlo y el revisor distinto verifica el hash final. Sin modelo distinto observable, el resultado es `REVIEW_MODEL_UNAVAILABLE`.

## 6. Evidencia mínima

Guardar en `validation/sc_multiagent/continuity/`:

- `SC06_PROVENANCE_RECEIPT.json`, con ruta A o B, sesiones, turnos, modelos efectivos, fuente de metadata y límites;
- `CANDIDATE_06_MANIFEST.json`, con base, archivos, operaciones, hashes y receta combinada;
- `REVIEW_06_RECEIPT.json`, con modelo del revisor, resultado, hallazgos y hash revisado;
- reporte breve solo si hace falta explicar un bloqueo que los JSON no expresen con claridad.

La evidencia diferencia solicitado, configurado, autoinformado y registrado por runtime. Los valores desconocidos permanecen `UNKNOWN`.

## 7. Criterios de cierre

### `SC06_METADATA_RECOVERED`

- metadata histórica liga implementación material, sesión/turno y modelo efectivo;
- candidato exacto congelado;
- revisión PASS por modelo efectivo distinto;
- checks pertinentes PASS;
- no hay cambios materiales sin atribución.

### `SC06_RECONSTRUCTION_VERIFIED`

- ruta A documentada como insuficiente;
- reconstrucción material necesaria atribuida a un implementador con modelo efectivo observable;
- root aplicó el patch serialmente y registró correspondencia;
- candidato final congelado;
- revisión PASS por modelo efectivo distinto y checks pertinentes PASS.

### `SC06_BLOCKED`

Cualquier criterio imprescindible queda sin prueba por metadata ausente, cuota, catálogo sin dos modelos distintos, conflicto de base/checkpoint, permisos, patch no material, autoría mixta o revisión fallida fuera de la ronda disponible.

SC-MULTIAGENT-06 resuelve procedencia y revisión; no declara SC-MULTIAGENT-03 READY ni ejecuta el piloto real. Tras PASS, 04 puede integrar/publicar el candidato revisado conforme a su spec. Solo entonces se habilita la ejecución de 05.

## 8. Integración y relación con otros hitos

Secuencia de continuidad: `06 → 04 → 05`.

- 06 recupera o reconstruye procedencia y obtiene revisión del candidato exacto.
- 04 consume esa evidencia, comprueba vigencia, integra y publica bajo la autorización existente.
- 05 ejecuta el piloto real únicamente después de la integración verificada.

SC-MULTIAGENT-02 continúa en paralelo. Esta spec no genera imágenes, no inicia ni reinicia el reloj VSG y no modifica la selección representativa de fuentes. GLIGEN permanece `PAUSED`, D3/D4 `PENDING`, VSG `SHADOW` y `execution_authorized=false`.

## 9. Presupuesto, razonamiento y parada

**Topes:** una sesión de hasta 60 minutos; una auditoría local de metadata; como máximo una invocación de implementador para ruta B; una revisión inicial y, solo si se usa la ronda de corrección, una revisión final. Máximo una ronda de corrección. Cero imágenes, cero llamadas de imagen/GLIGEN, cero gasto adicional, cero reinicios automáticos.

Consultar cuota antes de cada invocación. Una cuota `UNKNOWN` se registra; si el cliente rechaza por cuota, no reintentar con otro perfil para evadir el límite.

Razonamiento recomendado:

- medium para inventario y recuperación de metadata;
- high para reconstrucción material, procesos/digest y revisión independiente.

El nivel high actual es suficiente para ejecutar esta spec. Solo modificarlo si el cliente rechaza ese nivel o el modelo efectivo elegido no lo admite; registrar entonces el nivel realmente usado.

Parar ante: falta de dos modelos efectivos distintos, modelo del implementador no observable, cuota o permisos insuficientes, otro escritor, deriva de HEAD/checkpoint, patch no material, hallazgo crítico no corregible en una ronda, 60 minutos o necesidad de ampliar gasto/alcance.

## 10. Instrucción de arranque

Preservar el candidato; intentar una vez la recuperación local de procedencia. Si no acredita el modelo del turno material, despachar una reconstrucción acotada y material a un implementador de lectura con metadata observable; root aplica serialmente. Congelar el candidato final, revisarlo con otro modelo efectivo y entregar PASS o bloqueo concreto. No integrar ni iniciar 05 hasta satisfacer la cadena completa.
