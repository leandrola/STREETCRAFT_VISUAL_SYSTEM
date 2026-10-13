# SC-MULTIAGENT-01: evidencia de configuración y piloto

Resultado operativo: **SC_MULTIAGENT_BLOCKED**, adaptado a `milestones["SC-MULTIAGENT-01"].status=BLOCKED`
en el [checkpoint](../../development/coordination/CHECKPOINT.json). Se completó el
piloto documental permitido; no se cumple READY para perfiles seleccionados y
escritura paralela aislada. Este informe es evidencia, no fuente operativa de estado.

## Base y autorización

Lean pidió leer v12 y solo después ejecutar la spec. Se leyó v12 completo antes
de abrir la spec. Copias exactas: [v12](../../specs/STREETCRAFT_v12.md) y
[spec](../../specs/SC_MULTIAGENT_01_v1.md). Lectura de v12 no implica ejecutar todo
su plan. Base viva limpia en main: `33b6581353b18004a4818e8fc597b5455ba7ccf3`; checkpoint inicial
SHA-256 `2c60a49a3d58581dc40602e9c9357ea4d8ca842a0520d18b1b0bbc8d96ea1cc0`. Se inspeccionaron instrucciones de ancestros,
README, STREETCRAFT, protocolo, coordinación y contratos específicos.

Sobre: una sesión activa hasta 60 minutos, una ronda de corrección, tres subagentes
simultáneos, hasta dos implementaciones abiertas, un hito, un commit y un push
normal de archivos propios. Gasto adicional cero; cuota UNKNOWN. Ningún servicio
persistente, imágenes nuevas, cambios de producto ni ejecución GLIGEN.

## Cliente y capacidades comprobadas

Extensión activa **26.930.61225**, CLI **0.160.1**, observados por proceso activo
y `codex --version`; extensión 26.1007.21434 instalada, sin atribuirle ejecución.
El proyecto ya era trusted. Una instancia nueva de app-server, sin iniciar turnos
de modelo, cargó `.codex/config.toml`: enabled=true, máximo tres subagentes; strict
config sin errores. Seis TOML válidos con Python stdlib tomllib.

[CAPABILITY_CHECK](CAPABILITY_CHECK.json) separa configuración de evidencia real.
La herramienta expuesta `collaboration.spawn_agent` permite nombre de tarea,
modelo y esfuerzo, pero no seleccionar nombre/tipo de perfil ni permisos por hijo.
`codex debug prompt-input` tampoco muestra los cinco nombres custom. Por tanto,
**CLIENT_CAPABILITY_BLOCKED**: archivos preparados, carga/selección nominal no
acreditada. Los agentes reales recibieron tarjetas y leyeron perfiles manualmente;
no se presenta eso como prueba de selección de agentes personalizados.

Todos los hijos heredaron filesystem compartido sin sandbox, aprobación never.
Los TOML analíticos solicitan read-only y el implementador workspace-write, pero
la metadata efectiva dice disabled. **ISOLATION_BLOCKED**: no escritura delegada.
No se cambiaron permisos globales, confianza, credenciales ni proveedor.
Fuentes oficiales consultadas: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
y [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic).

## Agentes reales y especialización

Se eligió gpt-6.1-sol para especialistas/implementador y gpt-6-astra para revisar.
Ambos aparecen en catálogo local y en modelos admitidos por la herramienta.
La metadata de los hilos, obtenida en lectura de la base local Codex, acredita
modelo/esfuerzo efectivos; los informes originales conservan UNKNOWN donde
los hijos no pudieron observar su propia identidad.

| Hilo | UUID | Modelo / esfuerzo | Creado UTC | Última actualización observada UTC |
| --- | --- | --- | --- | --- |
| /root/sc_architecture | 01a132fa-abd9-7240-bb12-20ef93b7341c | gpt-6.1-sol / medium | 2026-10-13T01:57:31.225000+00:00 | 2026-10-13T01:58:37.863000+00:00 |
| /root/sc_camera | 01a132fa-db40-7f70-af47-adec2d11d90a | gpt-6.1-sol / medium | 2026-10-13T01:57:43.361000+00:00 | 2026-10-13T01:58:47.799000+00:00 |
| /root/sc_history | 01a132fb-0cc0-7702-9a59-c28da9944ee9 | gpt-6.1-sol / medium | 2026-10-13T01:57:56.032000+00:00 | 2026-10-13T01:58:45.859000+00:00 |
| /root/sc_implementer | 01a132fc-edfa-7a22-ab5f-6b4f08e0111b | gpt-6.1-sol / medium | 2026-10-13T01:59:59.226000+00:00 | 2026-10-13T02:01:22.525000+00:00 |

[ACTIVITY](ACTIVITY.json) conserva una muestra de los tres especialistas RUNNING
al mismo tiempo, más sus UUID y timestamps. Máximo observado: tres subagentes.
Los tiempos son marcas del runtime, no horas facturadas ni consumo de cuota.

- [Arquitectura](sc_architecture_REPORT.md): identidad fuente, relaciones de
  fachada/señalética y rooftop inferido separado de arquitectura observada.
- [Cámara](sc_camera_REPORT.md): modificador `/sc-front` frente a macro y
  presets CG-F/BD01/BD02, precedencias y conflictos con locks.
- [Historia](sc_history_REPORT.md): procedencia, fecha de entrega frente a fecha
  histórica, geografía y texto desconocidos; plausibilidad no es evidencia.

Cada informe comprobó el mismo HEAD/digest y no escribió archivos. Los hallazgos
son complementarios, sin discrepancia que requiera cambiar contratos. El ejemplo
retiene el conflicto potencial de rooftop elevado vs. CG-F y evita combinarlo
en una orden de generación. El acuerdo entre agentes no reemplaza las citas.

## Implementación y verificación

El worktree detached `/tmp/sc-multiagent-01-worktree` se creó desde la base,
sin rama nueva. El implementador leyó contratos allí, comprobó ruta/base/digest
y entregó [propuesta](sc_implementer_REPORT.md) sin escribir. El orquestador aplicó
el [patch documental](P2_QUICKSTART.patch) serialmente en la sesión principal,
alineando la tarjeta de ejemplo con la ruta usada realmente en P1.
[ISOLATION_CHECK](ISOLATION_CHECK.json) acredita igualdad de hashes antes/después
del worktree y diferencia entre ruta de lectura e aislamiento de escritura.
No se afirma que una ruta impida usar rutas absolutas al checkout principal.

[Quickstart](../../docs/SC_MULTIAGENT_QUICKSTART.md) contiene inicio, tarjetas,
ejemplo concreto, inspección, parada y recuperación. No es otro runtime ni supervisor.
[CHECKS](CHECKS.json): 27/27 pruebas existentes de backdrop y orquestador PASS en
worktree y entorno temporal. Primer intento: 25 PASS y dos errores de importación
por jsonschema ausente. Una corrección de entorno aislado y una repetición: PASS.
No se cambiaron dependencias globales ni se escribieron tests de instrucciones.

Todos los 786 archivos previos distintos del checkpoint permanecen idénticos.
El root fue el único escritor del checkpoint: digest releído inmediatamente antes
del delta; decisiones D1–D4, autorización histórica, GLIGEN, hitos previos y eventos
anteriores preservados. La comparación no se presenta como garantía transaccional.
La autorización textual de v12 se registra separada; generated_images=0 y el
reloj de 168 horas no inició. No hay mejora visual, cierre VSG-2B ni impresión validada.

El candidato final queda congelado como patch y manifiesto de altas/cambios, con
base y SHA-256. La [revisión independiente](sc_verifier_REPORT.md) y su recibo
registran el modelo efectivo, alcance y hashes; son recibos posteriores al candidato,
no modificaciones silenciosas de los archivos revisados. Si cambia un archivo del
candidato o HEAD antes de integrar, la revisión se invalida y debe repetirse.

## Criterios del hito

| Criterio | Resultado y evidencia |
| --- | --- |
| Perfiles cargados/seleccionados | BLOCKED: selección nominal no expuesta; TOML válido no la demuestra. |
| Paralelismo real | PASS documental: tres hilos RUNNING superpuestos, UUID/timestamps. |
| Especialización | PASS documental: tres informes distintos del mismo commit. |
| Concurrencia acotada | PASS observado: máximo tres, config nueva cargada con límite tres. No se ensayó una cuarta solicitud. |
| Aislamiento de escritura | BLOCKED: permissions disabled; fallback de análisis + escritura serial root. |
| Escritor único | PASS observado: solo root aplicó delta del checkpoint; sin garantía transaccional. |
| Revisión por modelo distinto | Resultado en recibo/REVIEW_METADATA posterior; requiere identidad efectiva distinta. |
| Integración vigente | Evidencia en recibo/DELIVERY posterior; requiere hashes/HEAD coincidentes. |
| Compatibilidad SC | PASS: runtime preservado y 27 pruebas existentes; GLIGEN intacto. |
| Lectura para Lean | Resumen de tres líneas y enlaces. Tiempo de decisión de Lean aún no medido. |

## Continuación necesaria

Activar una versión del cliente que exponga/seleccione los perfiles custom y
comprobarlo en una sesión nueva; la extensión nueva instalada no prueba esa
capacidad. Verificar permisos efectivos que impidan escribir fuera de la copia
asignada antes de repetir P2 con escritura. No cambiar automáticamente permisos
globales, proveedor ni gasto. No repetir P1 completado ni reiniciar el piloto
por iniciativa automática. Una futura tanda requiere sobre vigente.

Cierre en tres líneas:
Configurar y analizar: cinco perfiles preparados y tres especialistas reales con evidencia citada.
Pausar capacidad completa: faltan selección nominal de perfiles y aislamiento efectivo de escritura.
Mantener: runtime preservado, GLIGEN PAUSED, D3/D4 PENDING y reloj visual sin iniciar.
