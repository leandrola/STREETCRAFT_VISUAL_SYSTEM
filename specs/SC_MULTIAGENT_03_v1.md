# SC · Continuidad acotada en la Mac

**ID:** SC-MULTIAGENT-03 · **Versión:** 1.0 · **Fecha:** 2026-10-12  
**Estado:** SPEC_READY. Supervisor aún no construido ni validado.  
**Dependencia obligatoria:** SC-MULTIAGENT-01 cerrado con evidencia.  
**Complementaria:** SC-MULTIAGENT-02; su cierre visual no es requisito para construir este supervisor.  
**Destino:** Mac de Lean, Codex CLI local, mismo repo y cuenta autorizados.

## 1. Resultado esperado

Lean inicia una tanda con un objetivo y tareas concretas. Mientras está ausente, la Mac ejecuta ese alcance, coordina los subagentes disponibles, guarda evidencia y se detiene al cerrar, bloquearse o alcanzar un límite. Al volver, Lean ve qué cambió y qué queda pendiente.

El resultado observable es una tanda real sin intervención entre inicio y cierre, más pruebas de parada, exclusión mutua y recuperación. No basta con un script que lance Codex.

**Tarjeta Go**

- Hito: continuidad del equipo durante una ausencia.
- Qué vas a ver: un comando de inicio, estado legible, parada y resumen final.
- Qué cambia: supervisor local y reglas de recuperación, sin ampliar alcance de SC.
- Cómo se revierte: detener supervisor y revertir su commit; preservar trabajo no integrado.
- Costo: cero gasto adicional; dos turnos Codex como máximo en la primera tanda.
- Recomendación: probar una tarea local reversible antes de habilitar tandas con cambios de producto.

El sistema es acotado a la tanda iniciada. No es un daemon de 24/7, no se registra para arrancar con macOS y no crea cron ni launchd durante este hito. La Mac debe seguir encendida, con red y sin suspensión que impida trabajar.

## 2. Base oficial y verificación local

La documentación oficial permite invocar Codex desde scripts con codex exec; ofrece salida JSONL mediante --json y continuación de una sesión identificada. En ejecución no interactiva, una acción que requiera nueva aprobación puede fallar y volver al flujo principal. Esto no garantiza que un supervisor exista ni que la versión instalada soporte todos los eventos necesarios.

Fuentes consultadas el 12-oct-2026:
- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Antes de implementar, leer documentación oficial y ayuda de la versión instalada. Confirmar autenticación existente sin exponer credenciales, selección de modelos, configuración de proyecto y comportamiento real de subagentes en modo no interactivo.

No copiar auth.json al repo, no añadir API keys y no cambiar de proveedor. Si la autenticación disponible no permite esta ruta, registrar AUTH_BLOCKED; no resolverlo gastando ni alterando permisos globales.

## 3. Arquitectura elegida

Tres componentes pequeños:

| Componente | Responsabilidad |
| --- | --- |
| Supervisor determinista | Valida sobre, toma lock local, inicia proceso, mide plazo, observa salida y detiene |
| Orquestador Codex | Decide pasos dentro del sobre, delega, verifica e integra; único escritor del checkpoint |
| Subagentes de SC | Analizan o implementan las tareas asignadas bajo SC-MULTIAGENT-01 |

El supervisor no tiene razonamiento autónomo ni genera hitos. No abre un agente permanente por especialista.

Implementar con Python y biblioteca estándar si el entorno existente lo permite; reutilizar utilidades del repo. Evitar framework de agentes, base de datos, servicios remotos y dependencias nuevas sin necesidad.

El sobre aprobado se registra en CHECKPOINT.json usando el esquema real. El prompt de ejecución y los logs son proyecciones o evidencia, no fuentes alternativas de decisiones.

## 4. Sobre de la tanda

Reutilizar el sobre de AGENTS.md y ampliar solo lo necesario. Antes de arrancar debe constar:

| Dato | Regla |
| --- | --- |
| envelope_id y run_id | Identidades distintas: autorización vs. intento de ejecución |
| Objetivo | Resultado observable, sin descripción abierta como “mejorar SC” |
| Lista de tareas | IDs fijos, dependencias, archivos permitidos y criterio de cierre |
| Base | Commit y digest del checkpoint esperados |
| Modelos | Orquestador e implementador; verificador distinto |
| max_codex_turns | Máximo de invocaciones permitidas, incluyendo reconciliación |
| max_wall_seconds | Plazo total de la tanda; no se renueva por reanudación |
| max_subagents | Tres simultáneos, sin delegación recursiva |
| max_open_implementations | Dos; archivos propios y aislamiento |
| max_commits | Techo de commits locales según alcance |
| Push | Política vigente explícita, con referencia remota objetivo |
| Gasto / imágenes | Gasto adicional cero; imágenes cero en el piloto del supervisor |
| Uso desconocido | Acción ante UNKNOWN: no certificar porcentaje ni relanzar automáticamente |
| Parada | Bloqueo, nueva decisión, auth, permiso, cuota, plazo, conflicto o cierre |
| Reanudación | IDs y tareas retomables; máximo de un relanzamiento controlado |

**Defaults propuestos para el primer piloto:** máximo 2 invocaciones Codex, 30 minutos totales, 3 subagentes, 1 commit local y 0 imágenes. Configurar push conforme al permiso vigente; este documento no lo amplía ni lo revoca.

Un sobre vencido no se renueva. Cambiar scope, topes o política crea una decisión nueva en el checkpoint; un subagente no puede cambiarla.

La lectura de un sobre no equivale a ejecutarlo. Esta entrega prepara la implementación; no inicia una tanda en la Mac.

## 5. Exclusión mutua y único escritor

Crear un lock de sistema operativo exclusivo y no bloqueante por ruta canónica del repo, mantenido por el proceso supervisor. Incluir todas las rutas equivalentes que apuntan al mismo repositorio para evitar locks distintos por symlink.

La segunda ejecución termina con ALREADY_RUNNING antes de iniciar Codex. PID, run_id y timestamps son metadata diagnóstica; la ausencia o antigüedad de un archivo no prueba que el lock esté libre.

El lock es coordinación local efímera, no un segundo checkpoint.

Todos los modos de integración deben respetar el mismo lock: supervisor y sesión interactiva coordinadora. El quickstart establece cerrar o detener el orquestador activo antes de iniciar otro. No afirmar protección contra procesos que ignoran el lock: si HEAD o checkpoint cambian fuera de la tanda, parar y reconciliar.

**Checkpoint:** solo el orquestador Codex lo modifica. El supervisor nunca escribe estado de negocio ni marca tareas cerradas. Si el proceso muere, el supervisor guarda un registro de interrupción; el siguiente orquestador autorizado lo incorpora al checkpoint después de verificarlo.

Aplicar escritura segura del checkpoint, conservar campos históricos y validar su esquema. No inventar rutas o campos antes de inspección.

## 6. Ejecución y alcance de comandos

Interfaz propuesta, a adaptar al estilo del repo:

- start: inicia una tanda desde un envelope_id registrado.
- status: muestra checkpoint vigente y observaciones del proceso, claramente diferenciadas.
- stop: pide parada cooperativa y escala si es necesario.
- reconcile: inspecciona una corrida interrumpida y propone acciones; no relanza tareas por defecto.

El supervisor invoca Codex con argumentos estructurados, directorio explícito y prompt enviado por stdin cuando la versión lo admita. No construir comandos concatenando textos del checkpoint ni ejecutar el contenido del sobre como shell.

Guardar eventos JSONL, salida final y errores bajo un run_id. No tratar una frase como “terminado” como cierre: validar evidencia de tarea y checkpoint.

La escritura se hace en copias aisladas. El orquestador integra de a uno contra HEAD vigente y recibe revisión del modelo independiente. La integración técnica y el juicio visual son gates distintos.

No usar --yolo ni acceso total para evitar bloqueos. La automatización opera con permisos efectivos ya autorizados. Un permiso nuevo requerido produce parada explicada.

## 7. Límites observables y parada real

El plazo se mide desde el primer inicio de la tanda y con reloj monotónico durante un proceso vivo. Tras reinicio, conservar tiempo transcurrido a partir de metadata persistida; no conceder otros 30 minutos. Detectar reloj de pared incoherente y parar con TIME_UNCERTAIN.

El watchdog debe poder pedir interrupción cooperativa. Después de un margen breve fijo, terminar el grupo de procesos local y comprobar que no quedan implementadores escribiendo. Probar propagación real hacia hijos; no asumir que matar el proceso principal detiene toda actividad.

Si quedan procesos o trabajo remoto sin confirmación, registrar ORPHANED_OR_UNKNOWN; no iniciar otra tanda ni liberar la capacidad de integración hasta reconciliar. Terminar un proceso no garantiza cancelar una llamada remota ya enviada ni elimina el uso ya consumido.

Los límites de cuota/tokens solo son duros si existe telemetría fiable que incluya subagentes y mecanismo de corte verificable. Si no existe, usar plazo e invocaciones como límites observables; registrar uso UNKNOWN y no prometer un porcentaje de ventana.

Ante bloqueo global: pedir a subagentes detenerse, conservar patches y evidencia, dejar tareas no verificadas abiertas y finalizar. No autorreparar autenticación, aumentar cuotas o cambiar modelos para seguir.

## 8. Reanudación e idempotencia

Cada tarea tiene una clave estable derivada de envelope_id, task_id, base_commit e inputs congelados. El siguiente orquestador:

1. Lee checkpoint, HEAD, evidencia y registro de interrupción.
2. Comprueba si la tarea ya quedó integrada o si existe un patch verificable.
3. Revalida contra la base vigente antes de continuar.
4. Retoma únicamente tareas pendientes dentro de los límites originales.
5. No usa “última sesión” sin identificarla: puede pertenecer a otro trabajo.
6. No vuelve a generar imágenes con resultado desconocido.
7. No duplica commits, decisiones, eventos o tareas cerradas.

No prometer semántica “exactamente una vez” para llamadas externas. Un resultado ambiguo requiere reconciliación.

Si el proceso interrumpió la escritura del checkpoint, validar su integridad antes de operar. Recuperar desde evidencia/versión válida sin borrar decisiones posteriores. Un conflicto exige parada; no reset hard ni force push.

## 9. Commits, push y rollback

Mantener la política vigente de Lean; no introducir ramas nuevas como requisito. Solo el orquestador hace commit y push.

Si push está autorizado:

- Revisar diff final y ejecutar checks pertinentes.
- Incorporar registro de cierre del checkpoint dentro del cambio revisado.
- Verificar referencia remota antes de publicar; no sobrescribir trabajo ajeno.
- No usar force push.
- Registrar commit verificado y distinguir integración local de publicación remota.
- Si push falla o su resultado es incierto, preservar commit y reconciliar el remoto; no duplicarlo.

Si no está autorizado para la tanda, el cierre queda local con evidencia lista. Esto no requiere modificar la política general.

Rollback por revert de los commits propios identificados. No ejecutar rollback automático sobre trabajo posterior de Lean. Si se interrumpe una aplicación de patch, conservar estado y mostrar recuperación concreta.

## 10. Archivos propuestos

Adaptar a convenciones existentes y evitar utilidades duplicadas:

| Archivo / ubicación | Función |
| --- | --- |
| specs/SC_MULTIAGENT_03.md | Spec incorporada al repo |
| scripts/sc_supervisor.py | Supervisor pequeño, comandos y watchdog |
| scripts/sc_verify.py o comando equivalente existente | Única entrada de comprobación pertinente |
| docs/SC_CONTINUITY_QUICKSTART.md | Inicio, status, stop, bloqueo y recuperación |
| validation/sc_multiagent/continuity/ | Evidencia de pruebas, modelos y versiones |
| Carpeta local de runs fuera del runtime | Logs operativos e interrupciones, con exclusión del paquete de uso |

AGENTS.md incorpora reglas necesarias, sin convertirse en archivo de logs. CHECKPOINT.json conserva autoridad única. Logs no incluyen credenciales; paquetes de runtime no incluyen directorios de ejecución.

## 11. Pruebas necesarias

El supervisor añade lógica de procesos y recuperación: aquí sí hacen falta pruebas de comportamiento. Usar fake ejecutor local para límites e interrupciones sin gastar cuotas.

| Caso | Resultado requerido |
| --- | --- |
| Segundo supervisor | Rechazado antes de lanzar Codex |
| Sobre inexistente, inválido o base vieja | No ejecuta ni escribe checkpoint |
| Dependencia incompleta | No inicia tarea dependiente |
| Plazo agotado | Interrupción, escalamiento y comprobación de hijos |
| Permiso, auth o cuota bloqueados | Parada sin elevar privilegios ni cambiar proveedor |
| Ejecutor colgado | Watchdog independiente produce salida acotada |
| Caída a mitad de tarea | Evidencia conservada; no marca cierre |
| Resume de tarea integrada | No repite patch, commit ni eventos |
| HEAD/checkpoint cambiado fuera de tanda | Conflicto explícito, sin sobreescritura |
| stdout parcial o evento desconocido | No lo confunde con éxito |
| Push fallido o ambiguo | Estado local/remoto diferenciado |
| Uso UNKNOWN | No certifica topes porcentuales ni reinicia automáticamente |

Después, una prueba real pequeña bajo autenticación vigente: delegar revisión de dos secciones del quickstart ya implementado, consolidar un ajuste documental si hay evidencia y verificarlo con otro modelo. Sin imágenes ni cambios al runtime.

No hace falta que el supervisor genere imágenes para acreditar continuidad. SC-MULTIAGENT-02 sigue su propio carril en ChatGPT.

## 12. Cierre

| Estado propuesto | Evidencia |
| --- | --- |
| SC_CONTINUITY_READY | Tanda real completada, subagentes reales, lock, stop y recuperación verificados |
| SC_CONTINUITY_PREPARED_PENDING_LIVE | Código/pruebas locales listos; auth o prueba real pendiente |
| SC_CONTINUITY_BLOCKED | Limitación concreta con evidencia y acción para resolverla |

Adaptar estados al esquema existente.

READY requiere distinguir con claridad:
- Qué tareas se ejecutaron y qué se integró.
- Qué corte fue técnicamente comprobado y qué depende de telemetría.
- Qué entorno estuvo activo y cómo terminó.
- Si el repo quedó publicado o solo integrado localmente.
- Que GLIGEN, D3/D4 y reloj de VSG no fueron alterados indebidamente.

El resumen de regreso tiene tres líneas: hecho / evidencia / pendiente. status no muestra un estado ficticio tomado de memoria; deriva del checkpoint y del proceso observado.

## 13. Orden, esfuerzo y relación con SC-MULTIAGENT-02

| Paso | Entregable | Razonamiento |
| --- | --- | --- |
| Compatibilidad y auth | Ruta CLI demostrada sin cambios de permisos | Medium |
| Supervisor y lock | Inicio único y watchdog | High |
| Reconciliación | Recuperación sin repetir efectos | High |
| Pruebas y revisión | Casos críticos + verificador distinto | High |
| Corrida real y cierre | Tanda acotada y quickstart | Medium |

**Tope de construcción propuesto:** tres sesiones activas de hasta 60 minutos y una ronda de correcciones. Si falta una capacidad del cliente, cerrar preparación y reportar bloqueo; no extender por una cadena de specs.

La ingeniería de SC-MULTIAGENT-03 puede avanzar en paralelo con generación/evaluación de SC-MULTIAGENT-02, siempre con un único orquestador y archivos asignados. No ejecutar dos sesiones integradoras simultáneas. No esperar a un juicio visual para construir y probar controles locales.

**Arranque:** comprobar SC-MULTIAGENT-01; inspeccionar ayuda y permisos efectivos; implementar supervisor mínimo y probar fallas con ejecutor simulado; demostrar una tanda real; no instalar servicio permanente ni ampliar tareas para mantener a los agentes ocupados.

