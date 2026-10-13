# Streetcraft · Plan maestro para Codex

**ID:** SC-MULTIAGENT-PLAN · **Versión:** 1.0  
**Fecha local de Lean:** 2026-10-12  
**Destino:** Codex en el checkout vivo de STREETCRAFT_VISUAL_SYSTEM en la Mac.  
**Estado del documento:** PLAN_READY. La implementación de los hitos se verifica en el repo; no se presume por la existencia de una spec.

## 1. Objetivo y lectura

Implementar el equipo, ponerlo a trabajar sobre evidencia visual y habilitar continuidad acotada durante la ausencia de Lean. Después, incorporar specs sucesoras según las necesidades demostradas, conservando un único estado y un único orquestador.

Las “dos primeras” de este plan son las specs entregadas de operación visual (02) y continuidad (03). La configuración del equipo (01) es requisito previo y debe reconciliarse antes de ejecutarlas.

Este archivo define secuencia y admisión de trabajo. No sustituye las specs detalladas ni CHECKPOINT.json. No es una instrucción para ejecutar indefinidamente.

## 2. Documentos de entrada

Codex debe localizar y leer:

1. STREETCRAFT_v12.md: decisiones del proyecto.
2. STREETCRAFT_SUBAGENTS_SPEC_v1.md: SC-MULTIAGENT-01.
3. STREETCRAFT_MULTIAGENT_02_VISUAL_SPEC_v1.md: SC-MULTIAGENT-02.
4. STREETCRAFT_MULTIAGENT_03_CONTINUITY_SPEC_v1.md: SC-MULTIAGENT-03.
5. AGENTS.md y CHECKPOINT.json del checkout vivo.
6. README, contratos y validadores pertinentes.

Incorporar las specs y este plan en specs/ usando las convenciones reales del repo. Preservar ID, versión y contenido de cada spec; documentar cualquier adaptación técnica. Reutilizar archivos ya incorporados, sin crear copias de estado ni sobrescribir modificaciones de Lean.

Si falta un documento indispensable, identificarlo y continuar solo las tareas independientes cuyos inputs estén completos. No reconstruir una spec ausente de memoria.

## 3. Mapa de hitos

| Hito | Situación de diseño | Dependencia real | Resultado esperado |
| --- | --- | --- | --- |
| 01 · Equipo y orquestador | Spec disponible; ejecución no verificada en este plan | Compatibilidad del cliente y modelos | SC_MULTIAGENT_READY con piloto real |
| 02 · Operación visual | Spec disponible | 01 verificado y fuentes/payloads por carril | Pares, evaluación y decisión; corrección acotada si procede |
| 03 · Continuidad acotada | Spec disponible | 01 verificado y ruta CLI disponible | Supervisor probado y tanda real acotada |
| 04 · Uso diario y runtime estable | Sucesora propuesta; spec aún no creada | 01; runtime identificado; resultados técnicos pertinentes de 02/03 | Paquete chico, estado legible y verificación unificada |
| 05 · Mejora dirigida por evidencia | Sucesora condicionada; spec aún no creada | Evidencia de 02; candidato concreto y runtime verificable de 04 | Una mejora prioritaria comprobada |
| 06 y siguientes | Sin alcance asignado | Necesidad demostrada y tareas admitidas | Se define después; no abrir por numeración |

Los estados de la tabla describen documentos y dependencias, no el estado vigente de implementación. Los estados operativos se consultan exclusivamente en CHECKPOINT.json y su evidencia.

No hay una fecha de calendario prometida para cada hito. Los límites por sesión/tanda son los de cada spec y del sobre vigente. El reloj de VSG conserva su definición independiente.

## 4. Fase de entrada: reconciliar antes de construir

El orquestador registra HEAD, rama, cambios locales, checkpoint y configuración efectiva. Contrasta evidencia con cada criterio de cierre de 01.

- Si 01 está listo, reutilizarlo y pasar a 02/03.
- Si solo hay archivos de configuración, terminar el piloto pendiente.
- Si figura listo pero falta evidencia, registrar discrepancia y verificar el criterio afectado.
- Si hay un bloqueo del cliente o de modelos, resolver adaptaciones reversibles dentro del alcance; no cambiar proveedor ni gastar para aparentar cierre.
- Si el checkout tiene cambios de Lean, preservarlos y asignar tareas sin mezclarlos.

No rehacer pasos ya probados. No cerrar un hito porque otra conversación lo haya dado por terminado.

## 5. Primera ejecución: dos carriles independientes

Una vez verificado 01, el mismo orquestador puede coordinar trabajo de 02 y 03. Máximo tres subagentes simultáneos y dos tareas de implementación abiertas, sin delegación recursiva.

### Carril 02: evidencia visual

1. Reconciliar campañas ya iniciadas y sus presupuestos.
2. Priorizar el paquete VSG de D, E y Kenny que tenga bindings completos.
3. Preparar en paralelo el test de SC con fuentes representativas.
4. Generar por la vía autorizada y conservar primeras salidas.
5. Presentar pares a Lean y registrar su evaluación o la espera.
6. Implementar como máximo la corrección prevista por la spec, si hay evidencia y alcance suficiente.

Preservar presupuestos separados: VSG 6 salidas; SC 12 salidas. Restar las salidas ya realizadas. Sin reruns selectivos, nueva API ni presupuesto adicional de imágenes para patches.

El reloj VSG de 168 horas empieza con su primera imagen válida y no se reinicia por activar el supervisor.

### Carril 03: supervisor local

1. Comprobar CLI, autenticación y permisos existentes.
2. Construir controles de inicio único, límites, parada y recuperación.
3. Probar casos críticos con ejecutor simulado.
4. Ejecutar el piloto real definido, con revisión independiente.
5. Registrar qué control fue demostrado y qué continúa pendiente.

El piloto del supervisor no genera imágenes. La campaña visual no espera al supervisor.

**Asignación inicial sugerida:** tres especialistas para diagnóstico de 02; luego implementador para paquetes y, en otra tarea/copia, construcción de 03. El verificador entra al recibir un candidato concreto. No mantener especialistas activos sin tarea.

## 6. Integración y continuidad

Todas las tareas tienen ID, commit base, inputs congelados, archivos asignados, entregable, evidencia y límites. Reutilizar el contrato de SC-MULTIAGENT-01.

Un único orquestador:
- Escribe CHECKPOINT.json.
- Integra un candidato por vez.
- Verifica que el diff revisado corresponde a la base vigente.
- Ejecuta checks pertinentes y conserva evidencia.
- Hace commit/push conforme a la autorización vigente, sin force push.
- Presenta cada cierre en tres líneas.

Usar copias aisladas sin ramas nuevas como define 01. Si dos tareas requieren el mismo archivo, secuenciarlas.

No lanzar una sesión interactiva coordinadora y un supervisor integrador simultáneos. El traspaso al supervisor exige detener la sesión anterior, tomar el lock, releer estado y asignar la tanda. Un lock no protege contra procesos que lo ignoren; cambios externos obligan a reconciliar.

Los locks, logs y manifiestos son controles o evidencia, no otra fuente de decisiones.

## 7. Próxima spec propuesta: 04 · Uso diario y runtime estable

**Necesidad:** que Lean pueda usar SC sin adjuntar documentación de desarrollo innecesaria, identificar la versión efectiva y consultar un estado claro.

Al redactar la spec 04, incluir:

- Selección determinista de archivos necesarios para el runtime según el repo real.
- Identidad verificable del paquete: versión/commit y hashes.
- Conservación de contratos y comandos incluidos.
- Vista /sc-status derivada del checkpoint y de la identidad del runtime, con alcance realista para cada entorno.
- Registro simple por sesión: fecha, versión y comandos usados.
- Entrada única de verificación que reutilice comprobaciones existentes.
- Exclusión de credenciales, logs operativos y material de entrenamiento o desarrollo no requerido.
- Prueba de uso con una invocación existente y evidencia de compatibilidad.

No asumir que escribir “/sc-status” crea un comando nativo de Codex o de ChatGPT. La spec debe definir si es una convención del runtime, un script o una instrucción y demostrar cómo se consume.

Puede prepararse con resultados técnicos disponibles sin esperar el juicio de Lean en 02. Si 03 sigue bloqueado, status muestra ese bloqueo; no presenta continuidad habilitada.

Cerrar con paquete utilizable y comprobaciones concretas, no con otra propuesta de empaquetado.

## 8. Siguiente spec condicionada: 05 · Una mejora visual demostrada

No redactar una spec genérica de “hacer SC mejor”. Elegir una falla observable de 02 y formular:

- Trigger y ejemplo de antes.
- Comportamiento esperado.
- Contratos y archivos afectados.
- Inputs y comparación que permitirán verificar la corrección.
- Presupuesto nuevo, solo si hace falta y está dentro de autorización existente.
- Revisión técnica y criterio visual separados.
- Reversión y límites de conclusión.

Si 02 ya corrigió y verificó esa falla, no abrir 05 para repetirla. Seleccionar otra necesidad real o terminar el ciclo.

Sin imágenes nuevas autorizadas y disponibles, un patch puede quedar técnicamente verificado y visualmente pendiente. No declararlo una mejora demostrada. El test prompt directo vs. SC tampoco demuestra el efecto causal de un patch frente a SC anterior.

GLIGEN, cierre formal VSG-2B, VSG-3A y validación formal BD01/BD02 no entran automáticamente en 05.

## 9. Cómo incorporar cualquier spec futura

Antes de admitirla, el orquestador comprueba:

| Dato | Requisito |
| --- | --- |
| ID y versión | Únicos y trazables |
| Problema | Evidencia o decisión concreta que lo justifica |
| Entregable | Observable para Lean |
| Dependencias | Estados y evidencia, no solo existencia de archivos |
| Alcance | Tareas y archivos definidos |
| Presupuesto | Tiempo, imágenes, uso/gasto y política de publicación |
| Cierre | Criterios técnicos y visuales, si aplican |
| Parada | Bloqueos y agotamiento de límites |
| Reversión | Pasos y commits propios |
| Autorización | Dentro del sobre vigente o identificada como decisión nueva |

Guardar la spec en specs/. Registrar su admisión o propuesta en el esquema vigente del checkpoint; el plan conserva solamente la descripción de dependencias. No crear SPEC_REGISTRY.json ni otro registro de estado si el checkpoint ya cumple esa función.

Detectar dependencias circulares y archivos compartidos. Una spec compatible con el alcance ya autorizado puede ejecutarse sin pedir de nuevo el mismo permiso. Una ampliación de producto, gasto o esfuerzo que siga reservada a Lean queda como propuesta concreta, con motivo y evidencia.

No generar automáticamente specs 06–10 para mantener una cola de agentes. Cuando no queden tareas autorizadas y útiles, terminar la tanda.

## 10. Resolución de conflictos y prioridades

Orden de decisión:
1. Instrucción vigente de Lean y autorizaciones aplicables.
2. Hechos del repo y restricciones verificadas.
3. Spec detallada admitida para la tarea.
4. Este plan como criterio de secuencia.

Un cambio explícito de Lean se registra y actualiza documentos afectados. No usar este orden para ignorar permisos efectivos del entorno.

Ante contradicción entre specs: documentar problema, resolver decisiones técnicas reversibles dentro del alcance y secuenciar si hace falta. Si implica cambiar alcance o juicio reservado, entregar opción concreta y continuar tareas independientes.

Priorizar output y evidencia sobre documentación adicional. Un bloqueo local no paraliza un carril independiente; uno global de permisos, presupuesto o integridad detiene la tanda.

## 11. Esfuerzo y límites

| Trabajo | Razonamiento recomendado |
| --- | --- |
| Reconciliación, paquetes y documentación operativa | Medium |
| Conflictos de contratos, watchdog, locks y recuperación | High |
| Verificación independiente | High |
| Estado y cierre para Lean | Medium |

Usar niveles y modelos realmente disponibles. No prometer porcentajes de ventana si la cuota es UNKNOWN.

Conservar topes de las specs: 01 una sesión; 02 dos sesiones de ingeniería/consolidación; 03 tres sesiones de construcción. No confundir estos límites con el plazo de 30 minutos y dos invocaciones de su piloto. Las esperas visuales no habilitan reinicios automáticos.

Los hitos 04/05 definen sus topes en sus futuras specs. No tienen presupuesto implícito por aparecer aquí.

## 12. Final de cada tanda y reanudación

Actualizar checkpoint con resultados verificados y tareas pendientes. Conservar patches y copias útiles. Diferenciar commit local, publicación remota, evidencia técnica y juicio visual.

Resumen:
1. Qué cambió o qué resultado ya puede ver Lean.
2. Evidencia y límites.
3. Próxima tarea permitida o causa concreta de parada.

La siguiente sesión relee checkpoint y HEAD; retoma únicamente lo pendiente. No duplica generación, commits, eventos o trabajo ya integrado.

**Criterio de éxito del plan:** 01 demuestra equipo; 02 produce evidencia o un bloqueo explícito; 03 demuestra continuidad o una preparación limitada claramente identificada; las siguientes specs se incorporan por necesidad, sin cambiar automáticamente decisiones reservadas.

## 13. Instrucción de arranque para Codex

Implementá este plan en el repo vivo de Streetcraft.

Comenzá por leer las specs y reconciliar SC-MULTIAGENT-01 contra CHECKPOINT.json y su evidencia. Si está listo, coordiná 02 y 03 como carriles independientes bajo un solo orquestador. Distribuí subtareas concretas entre los perfiles existentes, respetá aislamiento y modelos distintos para implementación y revisión, e integrá de a uno.

Continuá autónomamente las decisiones técnicas reversibles y tareas ya autorizadas. No reiteres permisos ya otorgados. Conservá pausa de GLIGEN, D3/D4 pendientes, presupuestos separados y el reloj original de VSG.

Incorporá las specs futuras mediante la sección 9. Prepará 04/05 solo cuando sus condiciones se cumplan; no interpretes su numeración como permiso para ejecutar alcance nuevo.

Si falta una capacidad o input, entregá lo completado y el bloqueo concreto; continuá trabajo independiente cuando corresponda. Terminá al agotar la tanda o cerrar su objetivo, con checkpoint actualizado y resumen de tres líneas.

