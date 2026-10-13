# Streetcraft · Piloto Codex real y cierre de continuidad

**ID:** SC-MULTIAGENT-05 · **Versión:** 1.0 · **Fecha:** 2026-10-13  
**Estado:** SPEC_READY. No acredita una corrida real del supervisor.  
**Base:** Pasted text(4).txt; supervisor implementado, seis pruebas locales reportadas PASS, tanda simulada completada y revisión independiente pendiente.  
**Dependencia de ejecución real:** candidato de 03 revisado e integrado mediante 04, o evidencia equivalente verificable del mismo contenido.  
**Destino:** Mac de Lean, Codex CLI disponible y cuenta existente.

## 1. Resultado visible

Demostrar que sc_supervisor.py puede iniciar y observar una tanda real de Codex, con una tarea delegada, límites de proceso y reanudación por ID. Entregar a Lean un comando de inicio probado, estado, parada y recuperación que correspondan al comportamiento real.

El piloto es de lectura y no cambia runtime ni produce imágenes. El supervisor puede escribir sus logs locales; el agente ejecutor no modifica archivos del proyecto. El orquestador escribe el checkpoint después de finalizar y reconciliar.

**Tarjeta Go:** probar la continuidad real con dos invocaciones como máximo; Lean verá evidencia del ejecutor Codex, hilo delegado y sesión reanudada. Gasto adicional cero. Parar ante cuota, permisos, conflicto o procesos desconocidos. No instalar servicio permanente.

Un piloto de lectura no demuestra desarrollo autónomo con escritura ni publicación durante la ausencia. Ese alcance queda explícitamente fuera de esta tanda.

## 2. Reconciliar lo ya construido

Antes de añadir código:

1. Leer versiones vigentes de specs 01–04, AGENTS.md, checkpoint y quickstart.
2. Comprobar HEAD/upstream y preservar cambios ajenos.
3. Verificar que el supervisor y tests coinciden con el contenido revisado por 04.
4. Reutilizar pruebas locales y corrida simulada. Reejecutar solo si cambió código, entorno o hay una preocupación no resuelta.
5. Leer evidencia de delegación persistida anterior. No volver a probar --ephemeral como alternativa.
6. Identificar implementación real de start/status/stop/reconcile; no asumir flags ausentes.
7. Confirmar ejecutor Codex, autenticación, modelo, permisos y cuota. No suponer disponibilidad por un catálogo viejo.

Si 04 sigue bloqueado, preparar prompt, sobre y verificaciones offline sin iniciar modelo. El código nuevo material del piloto debe recibir revisión distinta antes de usarlo; no cambiar la máquina revisada inmediatamente antes de lanzarla.

## 3. Sobre acotado del piloto

Reutilizar SC03-PILOT-READONLY-01 si todavía representa el alcance y sus límites; si fue consumido o venció, no reciclarlo. Registrar un nuevo sobre explícito con la relación al anterior.

| Campo | Límite |
| --- | --- |
| Objetivo | Probar supervisor con Codex real y continuidad por ID |
| Invocaciones del ejecutor Codex | Máximo 2 en toda la tanda |
| Plazo total | Máximo 30 minutos desde primer inicio, incluyendo espera/reanudación |
| Delegación | Un único subagente en la primera invocación; ninguno nuevo en la segunda |
| Escrituras del ejecutor | Cero archivos del proyecto |
| Imágenes / GLIGEN | Cero |
| Gasto adicional | Cero; usar cuenta y proveedor existentes |
| Modelo | Disponible y trazable; nivel admitido por cliente |
| Base | HEAD y checkpoint congelados antes del inicio |
| Reinicio | Ninguno automático; la segunda invocación es continuación controlada |
| Publicación | No forma parte de la tarea ejecutora de lectura |

Estas dos invocaciones limitan procesos Codex padre; el hijo consume trabajo del modelo adicional. No afirmar que el presupuesto equivale a dos llamadas de inferencia.

No prometer ≤40% de ventana si la telemetría no permite acreditarlo. Registrar usage disponible o UNKNOWN. El plazo y el número de invocaciones son controles distintos de cuotas de la plataforma.

## 4. Ejecutor real y simulación claramente separados

El script existente admite --executor-json para un ejecutor alternativo según el reporte. Revisar la implementación y distinguir:

- SIMULATED: fixture/fake, no cuenta como piloto real.
- CODEX_REAL: binario real, versión y autenticación vigente, eventos ligados a sesión/turno.
- UNKNOWN_EXECUTOR: identidad no comprobada, sin cierre real.

El manifiesto de la tanda incluye tipo de ejecutor, argumentos estructurados, cwd, binario y versión, sobre, base, run_id e IDs de sesiones. No registrar secretos del entorno.

Nunca aceptar la frase “turn.completed” de una fixture como prueba de que intervino Codex. El resultado se liga al proceso real y a su metadata. Un proceso puede terminar correctamente sin completar la tarea: comprobar también el entregable.

Resolver el binario local al iniciar. No depender de que codex esté en PATH ni fijar un cache de extensión versionado como ruta eterna. Si falla localización, parar con EXECUTOR_UNAVAILABLE.

## 5. Primer turno: delegación real de lectura

La invocación empieza desde el supervisor, no desde un terminal manual que deje al supervisor fuera del circuito.

Usar sesión persistida y argumentos admitidos por la versión instalada; respetar posición de flags globales comprobada por ayuda. No --ephemeral, --last, full access ni cambios de permisos para eludir fallos.

Tarea:
- Delegar al perfil sc_implementer una lectura acotada del checkpoint y de SC_MULTIAGENT_03_v1.md.
- Devolver estado real de 03, modalidad de escritura, título/versión de la spec y una condición de parada.
- Distinguir explícitamente supervisor simulado de piloto real pendiente.
- Esperar resultado del hijo y terminar el turno.
- No editar archivos, iniciar más tareas o inferir READY por el propio prompt.

Capturar:
- run_id del supervisor.
- ID de sesión/turno padre.
- ID y resultado del hilo hijo.
- Modelo registrado por runtime cuando esté disponible.
- Eventos de inicio/fin y salida final.
- Resultado, salida de proceso y duración.
- Hashes de archivos del proyecto antes/después.

Un evento de espera con receiver_thread_ids vacío no prueba delegación. Debe existir un hilo hijo identificable que produzca el resultado.

## 6. Segunda invocación: continuidad controlada

Solo si la primera terminó correctamente, no quedan procesos desconocidos y aún hay plazo:

1. Reanudar exactamente el ID capturado de la primera sesión.
2. Conservar run/envelope y plazo originales.
3. No crear sesión nueva ni usar la última sesión por conveniencia.
4. Pedir una recapitulación de la tarea previa y de sus restricciones sin suministrar todos los resultados esperados.
5. No delegar otra tarea, escribir, generar o implementar.
6. Verificar identidad de sesión y coherencia con el primer turno.

La identidad de sesión y metadata son la evidencia principal de continuidad. Una respuesta que repite un token incluido en el prompt no basta.

Si el supervisor existente no implementa esta segunda invocación con el mismo presupuesto, añadir el soporte mínimo, pruebas pertinentes y revisión. No usar un resume manual fuera de su contabilidad para cerrar el piloto.

Tras agotar dos invocaciones, no iniciar una tercera aunque la segunda haya fallado. Conservar evidencia y causa. Una tanda nueva requiere alcance/límite explícito, no reset del contador.

## 7. Lock, procesos y semántica de finalización

El lock debe mantenerse durante ambas invocaciones y entre ellas, o demostrar una reserva equivalente que impida otra tanda. Si queda una ventana entre turnos donde otro orquestador puede integrar, detectar conflicto y abortar la continuación.

Durante el piloto solo existe un orquestador activo. La sesión interactiva que prepara debe ceder ejecución e integración al flujo correspondiente; no lanzar dos escritores del checkpoint.

Estados de proceso y negocio no son iguales:
- El supervisor puede informar COMPLETED por finalización del proceso/tarea.
- SC-MULTIAGENT-03 solo cambia después de verificar evidencia de cierre.
- Si no hay entregable o hijo válido, una salida 0 no acredita éxito.
- Un error de permiso, auth, cuota o routing produce BLOCKED/FAILED según esquema real, no COMPLETED por ausencia de error de shell.

Al terminar:
- Comprobar hijos locales y actividad pendiente.
- Registrar si no puede confirmarse cancelación de una llamada remota.
- Liberar lock solo cuando corresponda.
- Preservar logs y patches; no ejecutar limpieza automática de worktrees ajenos.

No afirmar que terminar un grupo de procesos cancela consumo remoto ya iniciado.

## 8. Parada y recuperación

No añadir una tercera corrida de modelo para probar interrupción. Usar pruebas locales existentes y pruebas focalizadas con ejecutor simulado para:

- stop cooperativo y escalamiento.
- hijo que permanece activo.
- pérdida de JSONL o evento desconocido.
- caída entre primera invocación y resume.
- segundo supervisor.
- sobre vencido o checkpoint cambiado.
- reconciliación sin relanzar.

Agregar solo casos nuevos necesarios por cambios del código. No repetir toda la batería por cada archivo documental.

Antes/después del piloto real, ejecutar status y reconcile del supervisor. reconcile no lanza modelo ni modifica estado de negocio automáticamente.

Si hay divergencia de HEAD/checkpoint mientras el agente debe estar en lectura, identificar actor/causa y detener. Los cambios posteriores intencionales del orquestador al registrar cierre deben diferenciarse del estado congelado de la tanda.

## 9. Checkpoint, digest y reloj

Usar el algoritmo de digest revisado en 04. Si incorpora SELF, guardar su versión y receta. Recalcular una vez después de preparar el sobre, validando coherencia sin editarlo al leer.

Durante el piloto, congelar checkpoint y HEAD. Los logs del supervisor están fuera del paquete de runtime y no constituyen otra fuente de estado.

Después de cerrar procesos y verificar evidencia, solo root actualiza el checkpoint. El recibo registra las huellas de entrada y salida; no exige que el hash anterior siga igual después de un delta legítimo de cierre.

Preservar sin cambios de autorización:
- GLIGEN pausado y D3/D4 pendientes.
- Campañas visuales de 02 y sus presupuestos.
- Evento original del reloj VSG, si ya existe.
- Ausencia de inicio del reloj cuando no hubo primera imagen válida.

## 10. Evidencia y criterios de cierre

Crear, reutilizando la estructura existente:

- specs/SC_MULTIAGENT_05_v1.md.
- validation/sc_multiagent/continuity/REAL_SUPERVISOR_PILOT_<run_id>.json.
- Referencias a eventos/logs sanitizados y resultados locales.
- Delta del checkpoint.
- Quickstart actualizado con comandos que efectivamente funcionaron.

| Criterio | Evidencia mínima |
| --- | --- |
| Supervisor revisado | Candidato integrado y recibo 04 o equivalente |
| Ejecutor real | Binario/version, proceso y IDs ligados a metadata |
| Delegación | Hilo hijo identificable y resultado de lectura |
| Persistencia | Primera sesión retomada por ID en segunda invocación |
| Límites | ≤2 invocaciones, ≤30 minutos y ningún reinicio automático |
| Escritura | Sin cambios de archivos del proyecto por ejecutor |
| Lock | Exclusión comprobada y propiedad durante el ciclo |
| Procesos | Finalización y ausencia de hijos desconocidos o bloqueo explícito |
| Recuperación | reconcile coherente y sin relanzamiento |
| Revisión | Modelos operativos distintos para implementación/revisión material |
| Estado | Preparación, piloto y publicación claramente separados |

Estados propuestos:
- SC05_LIVE_PILOT_PASS: corrida real y continuidad verificadas.
- SC05_LIVE_PILOT_PARTIAL: algún criterio real no quedó acreditado.
- SC05_LIVE_PILOT_BLOCKED: permiso, modelo, cuota, routing o integridad impiden completar.

Si satisface todos los criterios de la spec 03 enmendada, root puede cerrarla como READY con capability_scope=READ_ONLY_DELEGATION_CONTINUITY. Si faltan criterios, registrar cuáles y mantenerla pendiente.

READY en este alcance no habilita automáticamente escritura autónoma, commits del ejecutor, push ni operación de 24/7. No borrar el alcance al resumir el estado.

## 11. Relación con 02 y con siguientes hitos

02 no espera a esta spec para generar por su vía autorizada. El supervisor no se convierte en bridge de imágenes.

Para VSG D/E/Kenny, conservar los paquetes ya preparados y presentar fuentes/instrucciones a Lean cuando corresponda. La representatividad de seis fuentes SC sigue siendo una decisión independiente. No confundir preparación de hoja neutral con evaluación visual.

Después de este piloto, el empaquetado de runtime y /sc-status puede retomarse como propuesta siguiente. La modalidad con escritura autónoma requiere una tarea acotada y revisión propias; no ampliar el piloto de lectura durante la ejecución.

Actualizar el plan maestro con la prioridad 04 revisión → 05 piloto real y 02 como carril paralelo. Si IDs 04/05 ya fueron usados en el repo, preservar los existentes y asignar alias SC03-LIVE-PILOT.

## 12. Esfuerzo, parada e instrucción de arranque

Razonamiento recomendado: high para watchdog, lock entre turnos y reconciliación; medium para preparación y documentación. No cambiar modelos o niveles fuera del alcance vigente; usar capacidades disponibles.

**Tope propuesto de preparación:** una sesión de hasta 60 minutos, una ronda de ajustes. **Piloto:** límite independiente de 30 minutos y 2 invocaciones. Revisión material necesaria no se disfraza de tercera invocación del piloto; usar el presupuesto de revisión aplicable y registrar por separado.

Parar ante gate 04 insatisfecho, cuota agotada, nuevo permiso, resultado ambiguo o presupuesto consumido. Entregar evidencia concreta y conservar lo completado; no crear otra spec para reemplazar el criterio que falló.

**Arranque para Codex:** comprobar contenido integrado/revisado del supervisor; preparar una tanda real de lectura con un hijo y resume por ID bajo el mismo supervisor y plazo; conservar trazabilidad y finalizar sin ampliar alcance. Cerrar 03 solo por criterios demostrados, nunca por resultado simulado.
