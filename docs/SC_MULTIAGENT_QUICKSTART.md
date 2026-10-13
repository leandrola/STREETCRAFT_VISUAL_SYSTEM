# Colaboración Streetcraft: inicio y recuperación

## Estado y cliente

El piloto SC-MULTIAGENT-01 está configurado con tres subagentes como máximo.
El resultado y criterios comprobados están en [informe](../validation/sc_multiagent/PILOT_REPORT.md).
El estado operativo sigue en [checkpoint](../development/coordination/CHECKPOINT.json).

Cliente observado: extensión activa 26.930.61225, CLI 0.160.1; extensión
26.1007.21434 instalada pero no activa en el proceso observado. Proyecto trusted.
La configuración efectiva cargó agents.enabled=true y límite=3.
Los cinco TOML pasan sintaxis; este cliente no expone selección nominal de perfil
por la herramienta de delegación y su prompt diagnóstico no muestra estos perfiles.
Leerlos manualmente permite especialización por instrucciones, sin demostrar
carga nominal. Los agentes del piloto heredan filesystem unrestricted; sus
instrucciones de lectura no constituyen aislamiento. ISOLATION_BLOCKED impide
escritura delegada. El orquestador secuencia las ediciones en el checkout principal.
No declarar SC_MULTIAGENT_READY con estas capacidades pendientes.

## Una sesión principal

Abrí el repo en Codex, leé AGENTS.md, HEAD y checkpoint. Pedí al orquestador:

```text
Dentro del sobre autorizado de SC-MULTIAGENT-01, delegá tres análisis documentales:
identidad edilicia, cámara/backdrop y evidencia histórica. Usá el mismo HEAD y
digest del checkpoint, esperá los tres informes y consolidá citas y diferencias.
No generar imágenes ni cambiar contratos. Cada agente lee su perfil sc_*;
si no podés seleccionarlo nominalmente, registrá esa limitación.
```

No iniciar otro orquestador sobre este repo. La concurrencia no aumenta por
agregar perfiles. El verificador usa un modelo distinto del implementador;
si no está disponible, registrar REVIEW_MODEL_UNAVAILABLE y guardar preparación.
El tiempo/cuota se registra con evidencia disponible; cuota no expuesta: UNKNOWN.

## Ejemplo basado en contratos existentes

Este ejemplo audita documentación existente de Kenny y los contratos de cámara.
No solicita generación, ejecuta runtime ni evalúa imágenes. Kenny aporta un caso
con fachada observada, relaciones protegidas y rooftop de diseño inferido; no se
presupone su ciudad ni su fecha histórica. Comparar BD01/BD02 aquí no declara que
una fachada aislada sea una fuente adecuada para un backdrop panorámico.

### Tarjetas de los tres análisis

El orquestador entrega una tarjeta completa a cada especialista antes de iniciarlo.
Para reproducir una tarea, verificar primero HEAD y digest actuales; los siguientes
valores identifican la base usada en este piloto, no un estado futuro.

Campos comunes de las tres tarjetas:

```text
base_commit: 33b6581353b18004a4818e8fc597b5455ba7ccf3
checkpoint_digest: 2c60a49a3d58581dc40602e9c9357ea4d8ca842a0520d18b1b0bbc8d96ea1cc0
checkout_asignado: /Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2
archivos_permitidos: []
dependencias: ninguna entre los tres análisis; preparación del orquestador completada
entregable_observable: cinco hallazgos citados, con observación, inferencia y recomendación separadas; sin patch
limite_de_esfuerzo: 8 minutos por análisis, dentro del máximo de 60 minutos de la sesión
gasto_adicional: cero
condiciones_de_parada: base o digest distintos, necesidad de escritura, gasto, deriva de alcance o parada global
referencias_y_contratos: AGENTS.md, perfil propio .codex/agents/sc_*.toml, checkpoint, README.md, STREETCRAFT.md, agent/AGENT_PROTOCOL.md y contratos específicos indicados abajo
```

Completar los campos específicos de cada tarjeta:

| task_id / rol | objetivo | referencias_y_contratos adicionales | criterios_de_cierre |
| --- | --- | --- | --- |
| SC-MULTIAGENT-01-P1-ARCH / sc_architecture | Identificar invariantes edilicios y separar fuente de diseño inferido. | core/IDENTITY.md; core/PRESERVATION_MODEL.md; visual_scene_graph/pilot/fixtures/kennys/K0_OBSERVED_INFERRED_DESIGN.md; fixtures/kennys_new_01/observations.json y design.json bajo visual_scene_graph/pilot/. | Citar fachada, vanos, señalética y PR0/PR1; distinguir rooftop autorizado de P0 observado; conservar geometría oculta UNKNOWN. |
| SC-MULTIAGENT-01-P1-CAMERA / sc_camera | Comparar CG-F, modificador, macro y presets sin debilitar locks. | command_invocation/CG_F_FRONTAL_ELEVATION.md; command_invocation/BACKDROP_PRESETS.md; transform/VISUAL_PROFILES.md; transform/AUTO_ROUTING.md. | Explicar /sc-front frente a /sc-rdr2-elevation y BD01/BD02; indicar precedencias y conflictos; no promover validación visual. |
| SC-MULTIAGENT-01-P1-HISTORY / sc_history | Auditar procedencia, fecha, geografía y texto incierto. | core/PRESERVATION_MODEL.md; reference_runtime/REFERENCE_AUTHORITY_MAP.md; reference_runtime/REFERENCE_REASONING_2.md; reference_runtime/real_catalog/REAL_EVIDENCE_CATALOG_V1.json; patch/SEMANTIC_TOKEN_FREEZE.md; patch/LOW_CONFIDENCE_TEXT_MASK.md. | Separar fecha de entrega de fecha histórica; exigir procedencia; conservar ciudad, fecha y texto no acreditados como UNKNOWN; no completar señalética. |

El checkout asignado identifica dónde leer; no impone aislamiento. En este cliente
los perfiles se leen manualmente y las herramientas permiten escritura compartida.
Registrar ISOLATION_BLOCKED y mantener estos análisis sin escritura. Solo el
orquestador guarda sus respuestas en validation/sc_multiagent/.

### Consolidación respaldada por el piloto

Los tres informes aportan evidencia documental complementaria:

- [Arquitectura](../validation/sc_multiagent/sc_architecture_REPORT.md):
  fachada, vanos, acceso, vidrieras y relaciones de señalética están protegidos.
  El rooftop pertenece al diseño inferido autorizado; no se convierte en fuente
  observada. Laterales, profundidad y coronación histórica siguen desconocidos.
- [Cámara](../validation/sc_multiagent/sc_camera_REPORT.md):
  `/sc-front` cambia únicamente cámara y frontalización STRICT.
  `/sc-rdr2-elevation` agrega VP02, T02, identidad STRICT, oclusión
  LOCKED_UNKNOWN, 16:9 y calle mínima. BD01 y BD02 son presets compuestos:
  BD01/T02 permite recomposición en regiones no protegidas; BD02/T08 preserva
  layout y prohíbe trasladar masas importantes o sustituir edificios.
- [Historia](../validation/sc_multiagent/sc_history_REPORT.md):
  apariencia plausible no acredita fecha, ciudad, autoría ni licencia.
  RR2 exige procedencia y aprendizaje limitado; referencias no pueden importar
  identidad ni completar texto ilegible.

La autoridad viene de los [invariantes de fuente](../STREETCRAFT.md),
las [clases epistemológicas](../core/PRESERVATION_MODEL.md),
[CG-F](../command_invocation/CG_F_FRONTAL_ELEVATION.md),
[BD01/BD02](../command_invocation/BACKDROP_PRESETS.md) y
[RR2](../reference_runtime/REFERENCE_REASONING_2.md), no del acuerdo entre agentes.
BD01 puede tener alcance de recomposición vacío si toda la composición está
protegida. Ni frontalización ni T08 autorizan rellenar LOCKED_UNKNOWN.

Una vista moderadamente elevada del diseño rooftop y CG-F, que prohíbe una vista
elevada de conjunto, requieren resolver la intención y compatibilidad antes de
una futura solicitud. Este ejemplo no los combina en una orden de generación.
Fear City confirmado conserva su routing T06/VP03/CG-FC salvo override explícito;
el parecido con una ciudad no establece geografía.

El orquestador recibe los tres informes, conserva discrepancias y citas, y encarga
al implementador solo la propuesta documental del quickstart. Ante
ISOLATION_BLOCKED, aplica la edición de forma secuencial en la sesión principal.
Después vincula el candidato final a HEAD y hash del patch y solicita revisión
por un modelo efectivo distinto. Sin ese modelo, registra
REVIEW_MODEL_UNAVAILABLE y conserva lo completado.

El cierre acredita colaboración y análisis documental. Calidad visual, aceptación
de BD01/BD02 e impresión permanecen pendientes; GLIGEN sigue PAUSED, D3/D4 PENDING
y VSG SHADOW. No se inicia el reloj visual de 168 horas con este ejemplo.

## Inspección, parada y recuperación

En la UI expandí la actividad de subagentes cuando esté disponible o pedí a la
sesión principal listar agentes/tareas y sus estados. En CLI, /agent permite
inspeccionar los hilos. Para parar, pedí al orquestador detener la tarea indicada
(y dependientes), o todos los agentes por una condición global. No suponer que
cerrar una vista detuvo trabajo; verificar los estados y preservar resultados.

Al retomar: leer checkpoint, git status, HEAD e informe. Verificar que no haya
otra sesión escritora. No asumir agentes activos ni relanzar automáticamente
trabajo completo. Preservar copies/patches; solo integrar archivos asignados y
un candidato cuyo HEAD y hash coincidan con la revisión.

Si el cliente permite implementar en aislamiento verificable, crear worktree
detached desde HEAD conocido, sin rama nueva, y comprobar permisos efectivos
antes de escribir. Una ruta o sandbox_mode=workspace-write no basta. Si no,
mantener ISOLATION_BLOCKED y secuenciar implementación en la sesión principal.

El piloto no inicia el reloj de VSG, genera imágenes ni cambia D3/D4 o GLIGEN.
La exploración textual conserva su autorización separada. Continuidad después
de terminar la sesión exige otro hito autorizado; estos archivos no son supervisor.

Referencias de producto: [jerarquía](../STREETCRAFT.md), [preservación](../core/PRESERVATION_MODEL.md),
[CG-F](../command_invocation/CG_F_FRONTAL_ELEVATION.md),
[backdrop](../command_invocation/BACKDROP_PRESETS.md) y
[RR2](../reference_runtime/REFERENCE_REASONING_2.md).
Fuentes de configuración: [OpenAI Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
y [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic).
