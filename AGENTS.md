# Streetcraft: reglas de trabajo para agentes

Lean decide qué quiere ver, alcance, esfuerzo e irreversibles. El agente decide
los cómo técnicos reversibles dentro del trabajo autorizado. Las especialidades
son perfiles de IA; no acreditan credenciales profesionales.

## Autoridad y estado

La instrucción actual de Lean remite al [plan maestro v1](specs/STREETCRAFT_CODEX_MASTER_PLAN_v1.md).
Primero reconciliar [SC-MULTIAGENT-01](specs/SC_MULTIAGENT_01_v1.md) contra su
evidencia; no repetir el piloto documental completado. [02](specs/SC_MULTIAGENT_02_v1.md)
y [03](specs/SC_MULTIAGENT_03_v1.md) requieren 01 verificado antes de implementar.
Leer [v12](specs/STREETCRAFT_v12.md) y el plan no permite omitir dependencias ni
ejecutar 04/05 sin sus condiciones y topes. Las decisiones históricas y sus límites
se conservan. CHECKPOINT.json en development/coordination/ es la única fuente
operativa de estado. Los informes guardan evidencia; no son otro checkpoint.
Leé el checkpoint, README.md, STREETCRAFT.md y los contratos de la tarea antes
de actuar; verificá HEAD y cambios locales, sin reset ni limpieza de Lean.

## Entrada del plan maestro

- Trabajo actual: incorporar specs exactas y reconciliar únicamente criterios
  pendientes de 01. Usar una sesión acotada a 60 minutos, sin reinicios automáticos.
- Conservar informes anteriores como evidencia histórica. Las capacidades
  expuestas por el cliente no demuestran ejecución; registrar errores reales.
- Hasta verificar 01, 02/03 quedan bloqueados por dependencia. No construir
  supervisor ni iniciar campañas como parte de esta reconciliación.
- No ampliar permisos globales, proveedor ni gasto para resolver un bloqueo.
  Si falla un modelo configurado, guardar la causa sin afirmar modelo efectivo.
- El plan permite incorporar sus tres documentos en specs/, evidencia de entrada
  en validation/sc_multiagent/ y el delta del checkpoint; raíz integra en serie.
  Conservar autorización de commit/push, condicionada a revisión del candidato.

## Sobre del piloto 01 (histórico; límites aplicables a su reconciliación)

- Objetivo: configurar colaboración y demostrar un piloto documental real.
- Tareas: configuración, tres análisis documentales independientes del mismo
  commit, ejemplo de quickstart y revisión por un modelo distinto.
- Archivos: AGENTS.md, .codex/config.toml, los cinco perfiles .codex/agents/sc_*.toml,
  docs/SC_MULTIAGENT_QUICKSTART.md, specs/SC_MULTIAGENT_01_v1.md,
  specs/STREETCRAFT_v12.md, validation/sc_multiagent/ y delta del checkpoint.
  Runtime, contratos de producto, GLIGEN y evidencias previas: lectura.
- Límites: una sesión activa de hasta 60 minutos, una ronda de corrección,
  cero gasto adicional, cero imágenes, cero llamadas a modelos de imagen o
  GLIGEN. Máximo tres subagentes simultáneos, dos implementaciones abiertas,
  un solo hito (este piloto), máximo un commit y un push normal de archivos
  propios, sin reinicios automáticos. Uso/cuota no expuestos:
  UNKNOWN. El límite temporal se controla entre operaciones; no garantiza
  interrumpir una llamada en curso.
- Evidencia: TOML válido, carga efectiva cuando el cliente la exponga, tareas,
  hilos y tiempos, informes citados, patch/manifiesto, revisión independiente
  del candidato final y preservación del runtime.
- Parada: 60 minutos, gasto requerido, otro escritor del checkpoint, deriva
  de alcance, modelo de revisión no disponible, bloqueo o corrección agotada.
  Parar la tarea afectada y dependientes; una causa global para toda la tanda.
  Guardar lo completado y la causa. No simular capacidades ni declarar READY
  con criterios pendientes.

## Delegación e integración

1. La sesión principal es el orquestador, único escritor del checkpoint,
   único integrador y único responsable de commit/push bajo autorización vigente.
2. Delegá solo subtareas independientes, acotadas y explícitas. Especialistas
   y verificador no delegan a otros agentes ni escriben archivos ni hacen commit/push.
3. Antes de iniciar, entregá: task_id, objetivo, entregable_observable,
   base_commit, checkpoint_digest, referencias_y_contratos, checkout_asignado,
   archivos_permitidos, dependencias, criterios_de_cierre, limite_de_esfuerzo,
   gasto_adicional y condiciones_de_parada.
4. Cada respuesta indica rol/modelo efectivo, base, PASS/FAIL/BLOCKED, evidencia,
   inferencias, recomendaciones, patch, validaciones, límites/bloqueos y cierre
   en tres líneas. Nunca inventar cuota, procedencia o validación visual.
5. Implementadores solo escriben archivos asignados en worktree detached o copia
   aislada desde el commit base. No crear ramas nuevas. Comprobar herramientas,
   rutas y permisos efectivos; una ruta o sandbox_mode en un TOML no prueba
   aislamiento. Si no se puede comprobar, registrar CHILD_SANDBOX_UNAVAILABLE,
   limitar el perfil a lectura y secuenciar escritura en la sesión principal.
   Esta modalidad centralizada puede verificar 01 con despacho, modelo, revisión
   y preservación comprobados; no acredita escritura paralela aislada.
6. Asigná archivos propios; secuenciá colisiones. Incluí nuevos archivos y bajas
   en el manifiesto. Revisá y comprobá el candidato antes de integrar de a uno.
7. El verificador usa un modelo disponible distinto del implementador. Otro
   hilo del mismo modelo no cumple. Si falta: REVIEW_MODEL_UNAVAILABLE.
8. Revisión vinculada a HEAD y hash del patch final. Si cambian, revalidar.
   Releé y compará digest del checkpoint justo antes de aplicar solo el delta.
   Un hash no garantiza una transacción. No operar dos orquestadores activos.
9. No abrir hitos nuevos, modificar locks ni convertir consenso en evidencia.
   Entregá a Lean qué cambió, evidencia y cerrar / pausar / mantener.
10. Preservá copias y patches útiles. Retomar exige leer HEAD, checkpoint e informe;
    no asumir que los agentes previos siguen activos ni relanzar tareas completas.

## Autorizaciones separadas

GLIGEN permanece PAUSED, D3/D4 PENDING, execution_authorized=false. No desarrollar,
probar, descargar pesos ni ejecutar esa ruta. VSG continúa SHADOW y no gobierna
la generación. Se conserva la autorización histórica sin reinterpretarla.
La exploración textual de v12 autoriza seis salidas (D/E/Kenny, tres pares), en
la app de ChatGPT, cero gasto adicional y sin reintentos selectivos. Su reloj
es de 168 horas desde la primera imagen válida, con timestamp/id/hash de esa
imagen; sin vencimiento escrito ni reinicio automático. No se ejecuta en este
piloto. Generar y juzgar resultados son responsabilidades separadas; Lean evalúa.
El piloto no cierra VSG-2B ni demuestra calidad visual ni continuidad persistente.
Un launcher/supervisor de trabajo sin Lean requiere un hito aparte autorizado.

## Contratos del producto

Preservá la autoridad de STREETCRAFT.md: intención explícita, invariantes de
fuente, modo, perfil, cámara, gramática, período/región, preferencias.
Leé agent/AGENT_PROTOCOL.md y contratos pertinentes. Observación, inferencia,
generado y UNKNOWN permanecen distintos. No completar zonas LOCKED_UNKNOWN,
inventar texto ni importar identidad/geografía desde referencias.
Validá sintaxis y checks existentes afectados; no escribir tests que repitan
estas instrucciones. No ejecutar pruebas estructurales GLIGEN pausadas.
