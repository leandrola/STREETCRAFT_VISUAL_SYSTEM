# Entrada del plan maestro v1

Resultado: **preparación documental completada; ejecución bloqueada en 01**.
Este informe conserva evidencia. El estado operativo está únicamente en el
[checkpoint](../../../development/coordination/CHECKPOINT.json).

## Incorporación y base

Base observada: `577a538ddd2039193d24b71429faa0872a437fba`, rama `main`, árbol
inicial limpio. Git del sistema falla por `invalid active developer path`;
la instalación existente `/usr/local/bin/git` 2.51.2 funciona con acceso aprobado.
No se instaló software ni se cambiaron permisos globales.

Se incorporaron el [plan](../../../specs/STREETCRAFT_CODEX_MASTER_PLAN_v1.md),
la [spec 02](../../../specs/SC_MULTIAGENT_02_v1.md) y la
[spec 03](../../../specs/SC_MULTIAGENT_03_v1.md) con bytes idénticos al origen.
Solo se normalizaron los nombres de 02/03 a la convención existente `_v1.md`.
Las copias existentes de v12 y 01 coinciden exactamente con sus fuentes y se
reutilizaron. [ENTRY_EVIDENCE.json](ENTRY_EVIDENCE.json) conserva rutas, hashes,
base, digest inicial, error de despacho y hashes previos para comprobar preservación.

## Reconciliación de 01

| Criterio | Evidencia actual | Resultado |
| --- | --- | --- |
| Selección por nombre | La herramienta expone los cinco perfiles y aceptó una solicitud con `agent_type=sc_implementer`. | Capacidad de selección expuesta; ejecución no acreditada. |
| Modelo configurado | `/root/reconcile_capability` falló antes de trabajar: `The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.` | MODEL_DISPATCH_BLOCKED; modelo efectivo UNKNOWN. |
| Aislamiento de escritura | La herramienta comparte workspace y no ofrece raíces de escritura por hijo. El implementador falló antes de poder comprobar permisos efectivos. | ISOLATION_BLOCKED; aceptación pendiente, sin nuevas escrituras delegadas. |
| Tres análisis independientes | Evidencia histórica en el [informe del piloto](../PILOT_REPORT.md). | Reutilizada; no se repitieron tareas completadas. |
| Revisión final distinta | No hay candidato implementado por el hijo ni revisión nueva. | NOT_RUN; no se certifica cierre ni publicación. |

El perfil fue solicitado con tarjeta completa: tarea `PLAN-ENTRY-01-CAPABILITY`,
base y digest congelados, lectura del checkout principal, cero archivos escribibles,
entregable de diagnóstico y propuesta textual, sin dependencias para el diagnóstico,
8 minutos máximos, gasto adicional cero, sin delegación recursiva y parada ante
permisos, acceso, otro escritor o plazo. El orquestador continuó en paralelo con
la comparación documental. No llegó un informe del hijo; el error del cliente
es la evidencia del intento y no equivale a una revisión.

La [documentación oficial de subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents)
fue consultada durante esta entrada. Describe perfiles y controles, pero no prueba
disponibilidad de un modelo en esta cuenta ni aislamiento de esta sesión. No se
cambiaron modelos o proveedor para presentar un cierre aparente.

## Dependencias y límites

02 y 03 se incorporan como specs admitidas con ejecución bloqueada por 01
(sección 2 de 02 y dependencia obligatoria de 03). No se construyó supervisor
ni se iniciaron campañas. 04/05 siguen condicionados, sin spec nueva ni esfuerzo
implícito. Los presupuestos 6/12 son techos de campañas futuras, no salidas realizadas.

Se preservan GLIGEN PAUSED, D3/D4 PENDING, VSG SHADOW, la autorización histórica
y el reloj visual sin iniciar. Imágenes generadas, llamadas GLIGEN e invocaciones
de supervisor en esta entrada: cero. Uso/cuota: UNKNOWN. No hay validación visual.

La validación de esta entrada comprueba hashes, JSON/TOML, preservación de archivos
anteriores y alcance del diff. No requiere repetir tests de runtime intacto ni
ejecutar pruebas GLIGEN. El [manifiesto](MANIFEST.json) cubre altas y cambios;
el patch conservado es un candidato documental **sin revisión independiente**.
No se hizo commit ni push de esta entrada.

## Reanudación

Leer HEAD, checkpoint y este informe. Resolver disponibilidad de un modelo de
implementación y otro de revisión bajo la cuenta actual, sin gasto ni cambio de
proveedor; comprobar despacho real de perfiles y permisos de copia aislada.
Actualizar solo los criterios pendientes de 01. No repetir el piloto documental,
no iniciar 02/03 hasta satisfacer su dependencia y no relanzar automáticamente.

Incorporado: plan y specs 02/03 exactos, con procedencia y hashes.
Bloqueado: modelo del implementador rechazado; aislamiento efectivo pendiente.
Mantener: evidencia previa, runtime y pausas; 02/03 esperan 01 verificado.

## Reconciliación posterior sobre base integrada

Lean integró el candidato anterior como `055431555eea6873ff184aeb725789e7e5dc6f1c`;
el orquestador encontró `main` limpio y no reimportó specs ni aplicó el patch
conservado. La continuación corrigió los cuatro perfiles que fijaban el modelo
rechazado: especialistas e implementador usan `gpt-5.6-sol`; el verificador
conserva `gpt-6-astra`. El catálogo efectivo de Codex CLI 0.153.0 mostró ambos
modelos y sus niveles configurados. Los seis TOML volvieron a parsear.

La spec 01 pasa a versión 1.1. Se separan dos garantías: una copia detached
demuestra aislamiento operativo de cambios; una política efectiva del sandbox
debe probarse aparte. La modalidad habilitada para este cliente es
`DELEGATED_ANALYSIS_CENTRALIZED_WRITES`: los perfiles analizan en lectura por
contrato y root escribe e integra en serie. No se acredita escritura paralela.

La tarea real `/root/sc01_profile_smoke` seleccionó `sc_implementer` y terminó
PASS: leyó el título y versión 1.1 sobre la base vigente, devolvió el contrato
pedido y no modificó archivos. La definición activa del rol fija
`gpt-5.6-sol`; el hijo solo pudo autoidentificar la familia GPT-5, por lo que
esa diferencia de observabilidad queda explícita. El mismo proceso comprobó
que el archivo del checkout vivo era escribible. Resultado:
`CHILD_SANDBOX_UNAVAILABLE`; se prohíben escrituras delegadas.

Una copia detached en la ruta registrada en [RECONCILIATION_01.json](RECONCILIATION_01.json)
partió exactamente de `0554315`. Root agregó allí un probe documental; el probe
quedó como único cambio de la copia y no existe en el checkout vivo. Esto prueba
la separación operativa de la copia, no una barrera de filesystem para hijos.

Una prueba adicional mediante `codex exec --ephemeral` arrancó correctamente con
`gpt-5.6-sol`, pero su router no pudo crear el hilo hijo (`no thread with id`).
Fue detenida tras la única invocación corregida. La prueba del orquestador activo
es la evidencia positiva de despacho; el fallo CLI queda como límite del cliente
para futuras tareas del supervisor 03.

La revisión independiente de este candidato usa `sc_verifier` / `gpt-6-astra`,
contra el HEAD y hash de patch congelados. Su recibo se guarda después del
candidato y no se usa para cambiar silenciosamente los archivos revisados.

Corregido: perfiles compatibles y selección real del implementador comprobada.
Habilitado: análisis delegado y escritura centralizada; copia operativa comprobada.
Limitado: sandbox por hijo no disponible; escritura paralela continúa deshabilitada.
