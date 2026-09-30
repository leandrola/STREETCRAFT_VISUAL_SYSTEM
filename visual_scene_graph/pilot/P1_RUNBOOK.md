# VSG-2B / P1 · inventario y diseño del bridge

Estado: **P1_NEEDS_PROVIDER_SELECTION**. VSG-2B sigue **BLOCKED / PENDING_VISUAL**;
`production_authorized=false`. Fecha: 2026-09-30.
HEAD inicial/final: `beecfc9a71f6efa9ccd4e125d4eae1de143d93b3`, coincidente con la spec.
Árbol inicial limpio; no AGENTS.md aplicable encontrado. Entrega local sin commit.

## Bloqueo concreto

No se proporcionó proveedor/modelo ni una vía autorizada de autenticación local.
El CLI solo construye `CommandGenerator` con `--adapter-command` explícito; no
resuelve configuración del proveedor por variables de entorno. No hay implementación
ni configuración de bridge de imágenes en el checkout. D/E/Kenny siguen con
`DRY_RUN_ONLY`, quality provisional y seed null. La conclusión se limita a la
configuración invocable de este proyecto; no afirma que no existan servicios externos.
No se inspeccionaron secretos, archivos de credenciales ni valores de entorno.

Entradas necesarias del operador, sin secretos:

- Proveedor y modelo/versión exactos autorizados.
- Mecanismo local de autenticación: nombre de variable, perfil o ruta de configuración
  autorizada; nunca el token o contraseña. Indicar si ya está configurado.
- Ruta/argv del bridge si existe; en su defecto, indicar que requiere implementación.
- Parámetros/restricciones conocidos: tamaño/aspecto, formato, quality y seed.

La fuente oficial de capacidades queda **PENDING_PROVIDER_SELECTION**. No hay
proveedor elegido al que atribuir soporte. Tras la elección se verificarán docs
oficiales vigentes y código/config local sin llamadas live. Si ese modelo no permite
seed controlado en la ruta de edición con imagen fuente, el cierre correspondiente
será `P1_NO_GO_UNCONTROLLED_SEED`; nunca se inventará seed en metadata.

## Diseño revisable del bridge (propuesta, no implementada)

Ubicación propuesta: `adapters/vsg_pilot_provider_bridge.py`; argv local confiable,
fuera del manifest. La implementación concreta depende del proveedor seleccionado.

| Etapa | Contrato y rechazo |
| --- | --- |
| Entrada | Un JSON por stdin con exactamente `source_base64`, `payload`, `provider`, `model`, `seed`, `parameters`; validar antes de cualquier transporte |
| Fuente | Decodificar JPEG original sin recorte, redimensionado local ni postprocesamiento; usar el mecanismo de imagen fuente documentado por el proveedor |
| Payload | Transportar `payload.common` entero sin agregar instrucciones; preservar `relations_and_locks` como string en A y array en B. Si la API solo admite texto, proponer una serialización JSON determinista del payload completo, idéntica para ambos brazos, conservando esos tipos; documentar y revisar el cuerpo exacto antes de admitirlo |
| Configuración | Mismo provider/model/versión, seed y parámetros para A/B; validar valores soportados y rechazar extras. Ningún prompt oculto, negativo implícito ni mejora automática no declarada |
| Autenticación | Resolver solo el mecanismo local autorizado; no incluir credenciales en manifest, stdout, logs, receipts ni errores |
| Transporte | Cliente oficial o HTTP con destino verificado; sin shell ni interpolación de payload. Una invocación representa como máximo una solicitud de generación; sin retries automáticos. Polling solo si es necesario y documentado, sin crear otro trabajo |
| Respuesta | Exactamente `image_base64` y `metadata`. Metadata real: provider, model, seed, parameters y generation ID fresco del proveedor; conservar receipt verificable sin secretos. No fabricar IDs locales ni presentar un eco de la solicitud como confirmación del proveedor |
| Verificación | Decodificar salida, comprobar formato y dimensiones reales contra settings, validar metadata y respuestas incompletas; error acotado sin base64 de fuente ni credenciales |
| Preflight | Comando separado sin generación: tabla campo→documentación oficial→código/config. No invocar la API de imágenes para averiguar soporte ni inferir acceso/facturación a partir de una interfaz de ChatGPT |

El schema actual admite solamente `size`, `quality` y `output_format` en parameters.
Si el proveedor necesita strength, steps u otros ajustes que afecten A/B, deberán
quedar explícitos y congelados mediante una extensión mínima versionada del contrato,
con tests y nuevo delta. No esconderlos en defaults del bridge. Si no se puede
establecer el soporte sin una llamada facturable, registrar NO-GO sin hacerla.

Pruebas futuras del bridge concreto: mock local del transporte; inspección exacta
de los cuerpos A/B y bytes fuente; mismo seed/model/settings; rechazo de parámetros
ignorados, seed no soportado, metadata ausente, tamaño/formato incorrecto, respuesta
vacía y errores; no reintento ni logs sensibles. El mock no prueba capacidad real.

## D operacional y selección (propuesta, no admitida)

`kenny_binding.verify_preserved()` exige que las entradas originales de admisión D/E
coincidan exactamente con el baseline K1 congelado. Por ello se propone conservar
`R2B-191-D` y `fixtures/r2b_d_new_01/` como evidencia histórica, y crear
`R2B-191-D-P1` en `fixtures/r2b_d_provider_v1/` únicamente después del gate A.

La política versionada siguiente reemplazaría D por D-P1 en `global_selection` y
`partial_selection`; **no agregaría un quinto fixture**. Ambos representan Semantic
Text Lock, nunca dos fenómenos. D original no sería seleccionable para cerrar la
campaña operacional. C seguiría obligatorio; mínimo cuatro pares, máximo ocho
intentos. Tests deberán rechazar original+nuevo como dos fixtures de cierre y
revalidar que F no reemplaza Reference Isolation. No se altera el baseline K1 para
permitir la nueva admisión: se agrega una entrada nueva conservando las anteriores.

Los snapshots/request/rúbrica de D se preservan en semántica y bytes; una nueva
versión de manifest puede referenciar esos artefactos inmutables. Fuente JPEG:
`282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
El tamaño 347×389 describe la fuente, no soporte de salida. Seed explícito y todos
los settings reales se fijarán solo después de verificar el modelo.

Se deberán adaptar selección/replay en `fixture_replay.py`, `audit_corpus.py` y
`run_validation.py`: preservar comprobaciones y dry runs históricos D/E/Kenny,
y registrar la nueva versión operacional por separado. Las aserciones actuales que
exigen el delta D histórico no deben aplicarse al delta operacional. El revisor de
dry run deberá distinguir settings provisionales de operacionales sin eliminar
ninguna comprobación de bytes, semántica común o equivalencia A string/B array.

Tras actualizar coherentemente admisión/política, refrescar preconditions y regresión,
y guardar nuevo dry run en `outputs/vsg-2b-g0-provider-v1`. Codex revisará el paquete
persistido y publicará manifest hash, delta nuevo, HEAD, fecha y rutas. El delta
histórico no autoriza otro provider, model, tamaño, seed o parámetro. En este cierre
no hay nuevo manifest, admisión, delta ni dry run operacional.

## Evidencia y límites

Resultados ejecutados ahora se registran en
[`P1_RESULT.json`](../../validation/vsg_2b/P1_RESULT.json). Los 100 controles, 25 casos
VSG-2A y 24 checks de regresión del QA de entrada son evidencia histórica; no se
anuncian como una suite nueva. Se verifica el estado actual de preconditions,
replay D/E/Kenny y reviews de los paquetes ya guardados, y se ejecutan los tres
tests existentes de protocolo fake. No se necesita regenerar preconditions porque
no cambia ningún archivo controlado de código/schema/fixture/admisión.

Resultado de esta ejecución: **preconditions PASS**, **3/3 tests de protocolo fake
PASS**, **3/3 replays/comparadores y revisiones de paquetes existentes PASS**.
Los **732 archivos versionados** permanecen byte por byte intactos. No se ejecutó
la regresión completa ni se generaron nuevos dry runs. El resultado JSON conserva
argv, salida y código de retorno de cada comprobación realizada. El protocolo fake
ejecutó seis subprocesos locales sobre bytes sintéticos, sin probar soporte real.

Reproducción de los controles independientes:

```sh
.venv-sc/bin/python -c 'from visual_scene_graph.pilot.harness import check_preconditions; check_preconditions()'
.venv-sc/bin/python -m unittest visual_scene_graph.pilot.test_campaign.CommandBridgeTests -v
```

La comprobación de replays y paquetes es el tercer comando Python, íntegro en
`P1_RESULT.json` → `executed_now`; utiliza los BINDERS existentes y el revisor
de bytes persistidos sin invocar `execute` ni transporte de proveedor.

D/E/Kenny conservan bindings prospectivos y dry runs técnicos. C permanece
`RECEIVED_UNBOUND / NO_GO_C0_UNVERIFIED`: falta una declaración/registro verificable
vinculado al hash `2130500a09548d4f9c1991a210de3cfa13d8ef63406dd0c3a78c257c68858a09`
que establezca identidad authored Fear City y relación CG-FC, luego binding y
Archive admisible. Un hash válido o PASS histórico no constituye ese vínculo.
F sigue condicional y no aporta Reference Isolation.

Plan Limits de cinco horas/semanal al inicio, inventario y cierre: **UNKNOWN**.
Consumo observado: **UNKNOWN**; techo de 40 puntos conservado, sin certificar
cumplimiento numérico. No se puede inferir saldo desde duración o número de tests.
Archive / generación live / imágenes generadas / pares visuales nuevos: **0/0/0/0**.
No se inicia VSG-3A ni se afirma PASS visual o promoción a producción.
