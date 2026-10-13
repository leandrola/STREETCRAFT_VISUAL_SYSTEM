# Streetcraft · Reconstrucción trazable de procedencia hacia adelante

**ID:** SC-MULTIAGENT-06 · **Versión:** 1.1 · **Fecha:** 2026-10-13
**Estado:** SPEC_READY. Viabilidad técnica comprobada; reconstrucción y revisión no iniciadas.
**Origen:** decisión explícita de Lean para resolver `REVIEW_PROVENANCE_BLOCKED` sin excepción.
**Dependencias:** SC-MULTIAGENT-01 READY en modalidad `DELEGATED_ANALYSIS_CENTRALIZED_WRITES`; candidato 02/03 publicado pero no aprobado por el gate 04.
**Destino:** Codex CLI persistido sobre el repo vivo, con root como único escritor, registrador e integrador.

## 1. Problema y decisión

SC-MULTIAGENT-04 no puede demostrar que los revisores fueran distintos del implementador material porque el modelo efectivo de esa implementación quedó `UNKNOWN`. Una revisión adicional del mismo candidato no corrige esa ausencia y una excepción vaciaría el gate independiente.

SC-MULTIAGENT-06 rehace la procedencia hacia adelante. Un implementador iniciado con modelo fijado produce el candidato completo del supervisor desde una base anterior a esa implementación. Root registra el lanzamiento y vincula la ejecución a la metadata del runtime, al prompt y al diff. Después, uno o más revisores con otro modelo efectivo revisan exactamente el contenido que 04 integrará.

La metadata histórica puede conservarse como diagnóstico, pero no satisface 06 ni habilita 04. No hay ruta de cierre basada en aceptar `UNKNOWN`.

**Resultado visible:** candidato reconstruido, procedencia completa y revisión independiente; o bloqueo explícito sin integración ni piloto 05.

## 2. Viabilidad previa a la ejecución

La ejecución solo puede comenzar si root confirma estas capacidades sin consumir el turno del implementador:

1. El cliente permite fijar el modelo en el lanzamiento.
2. La ejecución usa una sesión persistida e identificable; no `--ephemeral` ni `--last`.
3. El runtime deja metadata posterior con el modelo efectivo ligado al turno, por ejemplo `turn_context.model`.
4. Existe un segundo modelo efectivo distinto para revisión.
5. Root puede congelar prompt, base y diff con SHA-256.

El preflight local de 2026-10-13 establece:

- Agent Host permite solicitar un modelo, pero `get_current_session`/`list_sessions` no exponen el modelo efectivo; esa vía sola es insuficiente.
- Codex CLI 0.153.0 acepta `-m` en invocaciones persistidas y devuelve un ID de sesión.
- rollouts persistidos anteriores exponen `turn_context.model` para `gpt-5.6-sol` y `gpt-6-astra`.
- la pareja viable actual es implementador `gpt-5.6-sol` y revisor `gpt-6-astra`, sujeta a disponibilidad y cuota al iniciar.

Resultado de preflight: `PASS_CLI_PERSISTED_RUNTIME_METADATA`. Esto prueba viabilidad, no ejecuta 06 ni acredita la futura corrida.

Si al comenzar cambian cliente, catálogo, cuenta o formato de metadata, repetir solo este preflight. Si el modelo efectivo no aparece, parar con `EFFECTIVE_MODEL_UNAVAILABLE`; no reemplazarlo por el modelo solicitado.

## 3. Base y alcance de la reconstrucción

La reconstrucción parte de `d946f1b5d0d6dad53f080540ae9634bdf360d440`, último commit publicado anterior a la implementación material del supervisor. Root comprueba que esa base y el contenido actual siguen disponibles y registra cualquier cambio posterior.

El implementador produce un patch completo para:

- `scripts/sc_supervisor.py`;
- `tests/test_sc_supervisor.py`;
- `tests/fixtures/sc_fake_executor.py`;
- `docs/SC_CONTINUITY_QUICKSTART.md`;
- cambios estrictamente necesarios en documentación o evidencia para describir el comportamiento implementado.

El patch debe reconstruir el comportamiento requerido por las specs 03–06: sobre acotado, lock, procesos, timeout/stop, sesión persistida, resume exacto, reconciliación sin relanzamiento, separación entre estado de proceso y estado de negocio y digest reproducible.

Puede reproducir comportamiento o bytes correctos del candidato anterior. El criterio no es novedad estética: el implementador trazable debe ser responsable del patch completo desde la base declarada. Un cambio pequeño aplicado encima del supervisor de procedencia desconocida no transfiere procedencia al componente completo.

La corrida simulada anterior de 03 sirve como antecedente técnico y regresión. No cuenta como evidencia de procedencia del nuevo implementador ni como piloto real.

## 4. Registro de procedencia propiedad de root

El agente no certifica su propia identidad. Root crea `SC06_IMPLEMENTATION_PROVENANCE.json` antes del lanzamiento y es el único que lo completa.

### 4.1 Campos congelados antes del lanzamiento

- `task_id` y timestamp UTC;
- host y versión del cliente;
- base commit y hash del checkpoint;
- modelo solicitado y nivel de razonamiento;
- comando estructurado y política de permisos;
- ID del perfil;
- archivos permitidos y criterios de cierre;
- prompt exacto o ruta inmutable, más `prompt_sha256`;
- presupuesto, condiciones de parada y ausencia de gasto adicional.

El campo `effective_model` se inicializa como `PENDING_RUNTIME_METADATA`, nunca con el valor solicitado.

### 4.2 Campos completados por root después del turno

- ID de sesión y turno;
- hash del rollout sanitizado;
- ruta y nombre del campo runtime que informa el modelo;
- `effective_model` leído por root desde esa metadata;
- patch exacto y `diff_sha256`;
- resultado y límites observados.

El autoinforme del agente se conserva, si existe, pero no alimenta `effective_model`. Si la metadata del runtime no coincide con el modelo solicitado, root registra ambos valores y detiene la tarea.

## 5. Ejecución del implementador

Root lanza una única sesión persistida del implementador, con modelo fijado y sin escritura directa en el checkout principal. Debido a `CHILD_SANDBOX_UNAVAILABLE`, el agente trabaja en lectura y entrega el patch completo como artefacto de salida; root lo aplica serialmente en una copia operacional desde la base.

Root no modifica materialmente el patch. Puede aplicar adaptaciones mecánicas registradas que no cambien bytes del contenido propuesto. Si hace falta una corrección material, debe pedirse dentro de la única ronda disponible y producir un nuevo patch atribuido al mismo implementador.

Criterios del turno:

- modelo efectivo observable y ligado al turno;
- prompt y diff con hashes registrados por root;
- patch completo del alcance, aplicable a la base;
- tests significativos para los contratos implementados;
- cero cambios de producto, imágenes o GLIGEN;
- salida PASS, FAIL o BLOCKED con límites reales.

Si el agente termina sin patch completo, si root debe completar lógica material o si la sesión no expone modelo efectivo, la reconstrucción queda `BLOCKED`.

## 6. Congelamiento del candidato reconstruido

Después de aplicar el patch, root ejecuta las comprobaciones pertinentes y crea `CANDIDATE_06_MANIFEST.json` con:

- base commit;
- cada archivo, operación y SHA-256;
- `prompt_sha256` y `diff_sha256` de la procedencia;
- receta de `combined_sha256`;
- hash del checkpoint previsto para integración;
- ID de sesión/turno y modelo efectivo del implementador;
- exclusión explícita del propio manifiesto y del recibo posterior.

El `combined_sha256` representa todos los bytes que serán revisados e integrados. Si cambia cualquier archivo material, el manifiesto y la revisión quedan invalidados.

## 7. Revisión independiente hacia adelante

Root crea un registro de lanzamiento equivalente para cada revisor. El revisor trabaja en lectura y no autodeclara la identidad usada para el gate.

Requisitos:

- modelo efectivo obtenido por root desde metadata runtime;
- modelo o familia distinta de la del implementador;
- sesión/turno, host, `prompt_sha256` y candidato `combined_sha256` registrados;
- revisión de código, tests, procesos, lock, resume, reconcile, digest, límites y procedencia;
- resultado PASS, FAIL o BLOCKED asociado al hash exacto.

El mínimo obligatorio es un revisor independiente. Revisores adicionales no compensan una identidad `UNKNOWN`. Se permite una sola ronda de corrección y una revisión final del candidato corregido.

La revisión previa, la corrida simulada y cualquier informe sobre otro hash no se heredan como aprobación.

## 8. Correspondencia exacta con 04

Antes de integrar, SC-MULTIAGENT-04 debe comprobar:

1. `combined_sha256` del manifiesto revisado.
2. `combined_sha256` recalculado sobre el candidato de integración.
3. hashes de archivos en el árbol del commit resultante.
4. ausencia de cambios materiales posteriores a la revisión.

Los tres contenidos deben coincidir. El recibo 04 registra commit local, commit remoto y hash combinado. Si el commit incluye bytes materiales no revisados, 04 permanece bloqueado aunque Git acepte el push.

Publicar antes del gate no convierte el candidato en aprobado. Si el contenido ya está en `origin/main`, 04 debe integrar la reconstrucción como un commit posterior verificable y registrar la cronología real; no reescribe historia.

## 9. Estados de cierre

### `SC06_RECONSTRUCTION_VERIFIED`

- implementador con modelo efectivo, sesión/turno, host y prompt registrados por root;
- patch completo desde la base declarada y `diff_sha256` verificable;
- candidato congelado con `combined_sha256`;
- checks pertinentes PASS;
- revisión PASS por modelo efectivo distinto sobre ese hash.

### `SC06_BLOCKED`

Falta cualquier dato de procedencia, el implementador no produce el patch completo, el runtime no expone modelo efectivo, no hay revisor distinto, falla la cuota, cambia la base/checkpoint, aparece otro escritor o se agota la ronda.

No existe estado de excepción ni cierre por metadata histórica recuperada. 06 no declara SC-MULTIAGENT-03 READY ni ejecuta el piloto real. Su PASS permite que 04 integre; solo después comienza 05.

## 10. Evidencia

Guardar en `validation/sc_multiagent/continuity/`:

- `SC06_VIABILITY_PREFLIGHT.json`;
- `SC06_IMPLEMENTATION_PROVENANCE.json`;
- prompt congelado o referencia a sus bytes exactos;
- patch del implementador;
- `CANDIDATE_06_MANIFEST.json`;
- `REVIEW_06_PROVENANCE.json` y `REVIEW_06_RECEIPT.json`;
- recibo final 04 con correspondencia de hashes y commit.

Los registros distinguen solicitado, configurado, autoinformado y efectivo según runtime. Root es autor de la evidencia de procedencia.

## 11. Relación con otros hitos

Secuencia de continuidad: `06 → 04 → 05`.

SC-MULTIAGENT-02 continúa en paralelo. Esta spec no genera imágenes, no inicia ni reinicia el reloj VSG y no decide representatividad visual. GLIGEN permanece `PAUSED`, D3/D4 `PENDING`, VSG `SHADOW` y `execution_authorized=false`.

## 12. Presupuesto, razonamiento y parada

**Topes:** una sesión de hasta 60 minutos; una invocación de implementador; una revisión inicial y, solo si se usa la ronda de corrección, una revisión final. Cero imágenes, cero llamadas de imagen/GLIGEN, cero gasto adicional y cero reinicios automáticos.

Consultar cuota y catálogo antes de cada invocación. Una cuota `UNKNOWN` se registra; un rechazo por cuota no habilita otro perfil para eludir el límite.

Razonamiento recomendado:

- medium para preflight, registro y congelamiento;
- high para reconstrucción, procesos/digest y revisión.

El nivel high actual es suficiente para preparar y verificar la reconstrucción. Cambiarlo solo si el modelo elegido no lo admite; root registra el nivel solicitado y el observado.

Parar ante: modelo efectivo ausente, falta de dos modelos distintos, cuota/permisos, otro escritor, deriva de base/checkpoint, patch incompleto, cambios materiales de root, hallazgo crítico no corregible en una ronda, 60 minutos o necesidad de ampliar gasto/alcance.

## 13. Instrucción de arranque

Confirmar nuevamente el preflight. Root congela y registra el prompt antes de lanzar una única sesión persistida del implementador con modelo fijado. El implementador reconstruye el patch completo desde `d946f1b`; root obtiene el modelo efectivo desde runtime, registra sesión/host/prompt/diff y aplica el patch serialmente. Congelar el candidato, revisarlo con otro modelo efectivo y exigir igualdad del `combined_sha256` hasta el commit de 04. Sin esa cadena, mantener 04 y 05 bloqueados.
