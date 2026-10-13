# SC · Spec de implementación de subagentes y orquestador

**ID:** SC-MULTIAGENT-01 · **Versión:** 1.1 · **Fecha:** 2026-10-13
**Destino:** Codex local en VS Code, checkout de STREETCRAFT_VISUAL_SYSTEM en la Mac.  
**Estado:** SPEC_READY — configuración y ejecución aún no verificadas en la Mac.  
**Base de decisiones:** STREETCRAFT_v12.md, leído completo. El repo vivo no fue inspeccionado para elaborar esta spec.

## 1. Resultado esperado

Lean trabaja con un único chat principal. Ese agente coordina especialistas que analizan SC en paralelo, asigna implementaciones aisladas, recibe una revisión independiente e integra resultados con evidencia. Solo el orquestador actualiza CHECKPOINT.json.

El primer cierre debe mostrar agentes reales trabajando y devolviendo resultados: crear archivos TOML por sí solo no acredita que el equipo funcione.

Este hito implementa la capacidad de colaboración. No autoriza nuevos hitos de producto, gasto adicional, ejecución de GLIGEN ni cambios en D3/D4. Tampoco implementa un servicio permanente para continuar después de terminar la sesión.

## 2. Plataforma y comprobación previa

Usar la versión instalada de Codex en VS Code. Antes de editar:

1. Registrar versión de la extensión y del CLI si está instalado; no asumir que coinciden.
2. Registrar HEAD, rama, git status y ubicación real del checkpoint.
3. Leer instrucciones aplicables, checkpoint, README y contratos pertinentes.
4. Inspeccionar configuración efectiva: comprobar soporte de subagentes, agentes personalizados, límites, modelos y confianza del proyecto.
5. Identificar cambios de Lean y preservarlos. No limpiar ni resetear el árbol.
6. Localizar validadores y pruebas existentes; no inventar comandos o campos del checkpoint.

**Base oficial de configuración, consultada el 12-oct-2026:** los agentes personalizados actuales se definen mediante TOML en .codex/agents/, con name, description y developer_instructions; los controles globales de subagentes viven en [agents]. La configuración de proyecto .codex/config.toml requiere proyecto confiable. Revalidar el formato contra la versión instalada. [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic).

Si el cliente no soporta el formato, registrar CLIENT_CAPABILITY_BLOCKED y la adaptación necesaria. No simular subagentes con secciones de una sola respuesta ni cambiar silenciosamente a una API.

## 3. Equipo y responsabilidades

| Rol / identificador | Especialidad y entregable | Escritura permitida |
| --- | --- | --- |
| Orquestador / sesión principal | Define tareas, consolida evidencia, arbitra contradicciones técnicas, integra y explica el cierre a Lean | Archivos asignados a integración; único escritor del checkpoint |
| sc_architecture | Arquitectura urbana norteamericana 1960–1985: tipologías, ritmo de fachada, materiales, medianeras y rooftop; observaciones e inferencias separadas | Ninguna en el checkout principal |
| sc_camera | Cámara, composición y backdrop: CG-F, elevación, puntos de fuga, verticales, encuadre y oclusión; conflictos con los contratos citados | Ninguna en el checkout principal |
| sc_history | Fotografía histórica urbana estadounidense: procedencia, fecha, geografía, señalética y anacronismos; referencias y grado de certeza | Ninguna en el checkout principal |
| sc_implementer | Traduce decisiones consolidadas en cambios mínimos de contratos, runtime o validación; entrega patch y evidencia | Solo copia aislada y archivos asignados |
| sc_verifier | Revisa diff, contratos, pruebas y evidencia visual de forma independiente; devuelve PASS, FAIL o BLOCKED | Ninguna en el checkout principal |

Los perfiles son especializaciones de agentes IA, no credenciales profesionales acreditadas.

El experto histórico no debe atribuir fechas, ciudades, autorías o licencias por apariencia. Las hipótesis se marcan como inferencias; lo desconocido queda UNKNOWN. El implementador no transforma una sugerencia del experto en permiso para alterar un lock.

## 4. Archivos a implementar

Reutilizar ubicaciones existentes cuando cumplan la misma función. No duplicar documentación operativa.

| Archivo relativo propuesto | Contenido |
| --- | --- |
| AGENTS.md | Política común, delegación, sobre de trabajo, responsabilidades y condiciones de parada |
| .codex/config.toml | Activación y límite de concurrencia; conservar configuración previa |
| .codex/agents/sc_architecture.toml | Perfil arquitectónico |
| .codex/agents/sc_camera.toml | Perfil de cámara y composición |
| .codex/agents/sc_history.toml | Perfil de fotografía histórica |
| .codex/agents/sc_implementer.toml | Perfil implementador |
| .codex/agents/sc_verifier.toml | Perfil verificador |
| docs/SC_MULTIAGENT_QUICKSTART.md | Inicio, ejemplo de tarea, inspección de agentes, parada y recuperación |
| validation/sc_multiagent/PILOT_REPORT.md | Evidencia del piloto, sin convertirse en fuente paralela de estado |

No crear un segundo checkpoint, tablero persistente o roadmap alternativo. Los reportes documentan evidencia; el estado operativo sigue en el checkpoint existente.

### Configuración de proyecto

Fusionar esta sección con la configuración existente; no sobrescribir el archivo:

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 3
```

Tres subagentes simultáneos, además del orquestador. El equipo tiene cinco perfiles disponibles; no deben estar todos activos todo el tiempo.

### Plantilla de perfil

```toml
name = "sc_architecture"
description = "Evalúa arquitectura urbana norteamericana para Streetcraft."

developer_instructions = """
Leé AGENTS.md y los contratos de SC pertinentes.
Trabajá únicamente en la tarea delegada.
Separá hechos observables, inferencias y recomendaciones.
Citá archivos, referencias o evidencia para cada hallazgo material.
Preservá los locks y distinguí áreas observadas de áreas desconocidas.
No escribas CHECKPOINT.json. No hagas commit ni push.
No delegues a otros agentes.
Devolvé un informe breve con versión base, evidencia, límites y resultado.
"""
```

El implementador adapta las instrucciones para admitir escritura exclusivamente en la copia asignada. Cada especialista incorpora sus criterios de la sección 3. No acumular prompts genéricos que se contradigan.

## 5. Modelos, razonamiento y permisos

- El orquestador y el implementador usan un modelo disponible en la cuenta; registrar el identificador efectivo.
- El verificador debe usar un modelo distinto del implementador, conforme a la v12. Otro hilo del mismo modelo no cumple ese requisito.
- Seleccionar y comprobar ambos modelos antes del piloto. No hardcodear identificadores supuestos ni iniciar llamadas facturadas para resolver disponibilidad.
- Si no hay segundo modelo disponible, completar preparación y diagnóstico; registrar REVIEW_MODEL_UNAVAILABLE. No declarar cierre independiente.
- Recomendación de esfuerzo: medium para especialistas e implementación rutinaria; high para conflictos de contratos y revisión. Ajustar a los niveles admitidos por el modelo y cliente.
- No modificar permisos globales, credenciales, proveedores ni políticas de aprobación.
- Los perfiles analíticos y el verificador deben trabajar en lectura. Comprobar permisos efectivos, pues las instrucciones de un perfil no son por sí mismas un aislamiento de filesystem.

Los TOML almacenan configuración reusable; no mantienen expertos permanentemente activos ni una memoria propia que sustituya el checkpoint.

## 6. Contrato de cada tarea delegada

El orquestador debe entregar antes de iniciar:

```text
task_id:
objetivo:
entregable_observable:
base_commit:
checkpoint_digest:
referencias_y_contratos:
checkout_asignado:
archivos_permitidos:
dependencias:
criterios_de_cierre:
limite_de_esfuerzo:
gasto_adicional:
condiciones_de_parada:
```

Cada subagente devuelve:

```text
task_id / rol / modelo efectivo:
base_commit:
resultado: PASS | FAIL | BLOCKED
hallazgos: observación / evidencia / inferencia / recomendación
archivos modificados o patch:
validaciones ejecutadas y resultados:
límites de la evaluación:
bloqueos:
cierre en tres líneas:
```

No inventar cuotas o porcentajes. Si la plataforma no expone uso suficiente, registrar UNKNOWN. Un límite escrito en el prompt es una regla operativa, no un medidor ni un corte automático garantizado.

## 7. Reglas del orquestador en AGENTS.md

1. Delegar solo subtareas independientes, con entregable y alcance acotados.
2. Mantener como máximo tres subagentes simultáneos y dos tareas de implementación abiertas. Estos son valores iniciales propuestos por esta spec, sin crecimiento automático.
3. Prohibir delegación recursiva de especialistas.
4. Ser el único escritor de CHECKPOINT.json y el único integrador.
5. Asignar archivos propios. Secuenciar tareas que necesiten el mismo archivo.
6. Impedir que implementadores hagan commit o push; centralizar esas acciones bajo la política vigente del repo.
7. Preservar pausa de GLIGEN, decisiones pendientes y autorizaciones separadas de generación.
8. No equiparar consenso entre agentes con evidencia ni pruebas deterministas con validación visual.
9. No abrir nuevos hitos por iniciativa de los subagentes.
10. Detener la tarea afectada ante bloqueo; detener también las tareas que dependan de ella. Una condición global de parada detiene toda la tanda.
11. Rechazar integración basada en un commit o checkpoint desactualizado; volver a validar.
12. Entregar a Lean: qué cambió, qué evidencia lo sostiene y cerrar / pausar / mantener.

El sobre de cada tanda incluye objetivo, tareas permitidas, límites de uso y gasto, evidencia de cierre y parada. Registrar usando la estructura real del checkpoint, sin asumir nuevas claves.

## 8. Aislamiento e integración sin ramas nuevas

### Enmienda 1.1: dos garantías separadas

El aislamiento operativo mediante worktree detached o copia independiente y la
restricción de filesystem impuesta por el sandbox del subagente son evidencias
distintas. Una ruta separada permite comprobar base, cambios y patch, pero no
demuestra por sí sola que el proceso no pueda alcanzar el checkout principal.
Un `sandbox_mode` declarado tampoco demuestra que el cliente lo haya aplicado.

Para cerrar este piloto se admite una de estas modalidades, declarada en la
evidencia:

1. **Escritura delegada aislada:** el implementador escribe en la copia asignada
   y se comprueban ruta efectiva, permisos y ausencia de cambios en el checkout
   principal.
2. **Análisis delegado y escritura centralizada:** el implementador inspecciona
   en lectura y entrega una propuesta o patch textual; el orquestador es el único
   que escribe e integra en serie. Esta modalidad puede verificar 01 si se prueba
   el despacho real del perfil, el modelo efectivo, la revisión independiente y
   la preservación del runtime. No acredita sandbox de escritura por subagente ni
   habilita implementaciones paralelas.

Si el cliente no ofrece una garantía de sandbox por hijo, registrarla como
`CHILD_SANDBOX_UNAVAILABLE` sin convertirla en bloqueo de la modalidad centralizada.
La escritura delegada sigue bloqueada hasta que su aislamiento se demuestre.

Para respetar la preferencia actual de Lean, usar copias de trabajo aisladas sin nuevas ramas de desarrollo. La elección inicial es un worktree detached desde el commit base; una copia independiente es alternativa si el cliente no permite trabajar allí.

El orquestador:

1. Crea la copia desde un commit conocido y entrega su ruta absoluta al implementador.
2. Verifica que las herramientas del subagente operen allí; indicar una ruta en el prompt no prueba aislamiento.
3. Recibe el patch y comprueba que afecta únicamente archivos asignados.
4. Incluye altas, bajas y archivos nuevos en el manifiesto; un diff de archivos tracked no cubre archivos nuevos.
5. Aplica el cambio en un espacio de integración y ejecuta las comprobaciones pertinentes.
6. Pide al verificador revisar el patch final contra el HEAD vigente.
7. Integra de a uno. Si cambia HEAD o el contenido revisado, invalida la revisión y la repite sobre el candidato actualizado.
8. Actualiza el checkpoint y realiza commit/push solo según la autorización vigente.

El worktree detached no impide modificar el checkout principal mediante rutas absolutas. Si no se puede comprobar aislamiento de escritura, limitar el piloto a análisis y secuenciar la implementación en la sesión principal; registrar ISOLATION_BLOCKED para la capacidad de escritura paralela.

Para el checkpoint: releer justo antes de escribir, comprobar digest y aplicar solamente el delta previsto. El escritor único exige una única sesión coordinadora autorizada; no ejecutar dos orquestadores activos sobre el mismo repo. Si la evidencia revela otro escritor, parar. No atribuir garantías transaccionales a una simple comparación de hash.

## 9. Piloto mínimo

**Alcance inicial:** implementar configuración y demostrar coordinación. Gasto adicional: cero. Sin imágenes nuevas ni cambios de producto durante este piloto. Esto acota esta corrida; no revoca la autorización general de generar imágenes de la v12.

**Límite propuesto:** una sesión activa de hasta 60 minutos, una ronda de corrección y sin reinicios automáticos. El orquestador controla el tiempo entre operaciones; no se promete un corte duro mientras una llamada siga ejecutándose.

### P0 — Preparación

Inspeccionar el repo, completar configuración y seleccionar modelos. Validar TOML y comprobar carga real en una sesión nueva cuando sea necesario.

### P1 — Tres especialistas reales

Asignar al mismo commit base tres análisis independientes:

- Arquitectura: identificar restricciones existentes de identidad y coherencia edilicia.
- Cámara: identificar contratos CG-F y backdrop, y sus precedencias.
- Historia: identificar cómo SC distingue fidelidad histórica, inferencia y evidencia.

Usar una referencia existente solo si está disponible y cada agente puede inspeccionarla. Si no hay imagen, reportar análisis documental; no simular evaluación visual.

Esperar los tres resultados. Consolidar una conclusión breve con evidencia y discrepancias.

### P2 — Implementación aislada o propuesta en lectura

Asignar al implementador un cambio acotado del propio hito: completar el quickstart con un ejemplo basado en los contratos encontrados. Usar copia aislada y entregar patch, sin modificar contratos del runtime.

Si no hay sandbox por hijo comprobable, ejecutar el perfil en lectura sobre la
copia, recibir la propuesta y aplicar el cambio únicamente desde el orquestador.

### P3 — Verificación e integración

El verificador, con modelo distinto, revisa configuración, quickstart, cumplimiento de reglas y diff final. El orquestador aplica correcciones dentro de la ronda permitida y registra el resultado.

No usar este piloto para iniciar el reloj visual de VSG: ese reloj comienza con la primera imagen válida de su exploración específica.

## 10. Evidencia y criterios de aceptación

| Criterio | Evidencia requerida |
| --- | --- |
| Perfiles cargados | Registro del cliente y agentes personalizados seleccionados efectivamente |
| Paralelismo real | Identificadores de hilos, tareas y tiempos que muestran ejecución superpuesta |
| Especialización | Tres informes distintos, con referencias concretas al mismo commit base |
| Concurrencia acotada | Registro de máximo de agentes activos y configuración efectiva |
| Modalidad de integración | Escritura delegada: rutas/permisos y comparación de cambios; escritura centralizada: perfil real en lectura, propuesta trazable y root como único escritor |
| Escritor único | Diff del checkpoint producido exclusivamente por el orquestador |
| Revisión independiente | Identificador de modelo distinto, base y hash del patch revisado |
| Integración vigente | Correspondencia entre diff revisado y contenido integrado |
| Compatibilidad SC | Comprobaciones existentes pertinentes; sin cambio del runtime ni de GLIGEN |
| Lectura para Lean | Cierre en tres líneas y enlaces a evidencia suficiente |

No escribir tests que repitan las instrucciones. Usar una corrida real para comprobar delegación y rutas; validar sintaxis y ejecutar solo las comprobaciones del repo afectadas.

**Estados de salida propuestos, a adaptar al esquema vigente:**

- SC_MULTIAGENT_READY: configuración, delegación, aislamiento e independencia demostrados.
- SC_MULTIAGENT_CONFIGURED_PENDING_PILOT: archivos listos, prueba real pendiente.
- SC_MULTIAGENT_BLOCKED: falta una capacidad requerida; describir cuál y cómo resolverla.

El reporte debe declarar qué fue probado y qué sigue sin probar. No declarar mejoras de calidad visual a partir de un piloto documental.

## 11. Recuperación y límites de continuidad

Si la sesión se interrumpe, el siguiente orquestador lee checkpoint, HEAD y reporte antes de reanudar. No supone que los subagentes anteriores siguen activos ni relanza automáticamente una tarea completada.

Preservar copias y patches útiles hasta confirmar integración. No limpiar worktrees con cambios sin conservar.

Una ejecución durante la ausencia de Lean requiere un hito aparte para launcher, límites observables, manejo de permisos, prevención de doble orquestador y recuperación. AGENTS.md y los TOML no sustituyen ese supervisor. Esta separación no debe retrasar la exploración visual ya autorizada.

## 12. Orden de implementación y esfuerzo recomendado

| Paso | Entregable | Razonamiento recomendado |
| --- | --- | --- |
| 1. Inspección y compatibilidad | Base y capacidades verificadas | Medium |
| 2. Reglas y perfiles | AGENTS.md y cinco TOML | Medium |
| 3. Aislamiento y contrato de tarea | Ruta demostrada y asignaciones claras | High si hay conflictos; medium en el resto |
| 4. Piloto y revisión | Evidencia real y quickstart integrado | High para verificador |
| 5. Cierre | Checkpoint y resumen para Lean | Medium |

No convertir estos pasos en una cadena de nuevas specs. Resolver ajustes reversibles durante la implementación. Ante una limitación real, entregar lo completado y la causa concreta del bloqueo.

**Instrucción de arranque para Codex:** implementar SC-MULTIAGENT-01 en el repo vivo; comenzar por inspección, preservar cambios existentes y usar esta spec como contrato de alcance. Delegar el piloto únicamente después de comprobar configuración efectiva. No reabrir GLIGEN ni declarar cierre sin la evidencia de la sección 10.
