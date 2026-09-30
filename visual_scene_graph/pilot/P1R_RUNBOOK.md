# VSG-2B / P1R · Replicate FLUX.1 Kontext [pro]

**P1R_SCOPE_DECISION_REQUIRED** · 2026-09-30.
Representación: **TEXT_SERIALIZED_AB**. No bridge implementado ni proveedor declarado
READY. VSG-2B permanece **BLOCKED / PENDING_VISUAL**, `production_authorized=false`.

HEAD inicial/final: `7545774349d078b0c1dc36c5d9a54d1059456165`.
Árbol inicial limpio; sin AGENTS.md aplicable encontrado. Los **734 archivos
versionados** permanecen intactos. P1/G0 locales son la evidencia de entrada;
no se cambian sus resultados, manifests, deltas, política, allowlist ni preconditions.
El usuario eligió Replicate, `black-forest-labs/flux-kontext-pro`, y autenticación
local `REPLICATE_API_TOKEN`; respondió `go` para esta evaluación, sin autorizar
predicciones ni aprobar todavía un cambio de alcance.

## Decisión y versión

La [página oficial de la versión concreta](https://replicate.com/black-forest-labs/flux-kontext-pro/versions/569705b35f79b1160d51de1d0e3955626af86c77a034a16e89010dbdde5ad312/api)
publica `prompt` string, `input_image` string, seed entero, aspect_ratio,
output_format, safety_tolerance y prompt_upsampling. No publica un campo de relaciones
como array tipado. El [schema actual](https://replicate.com/black-forest-labs/flux-kontext-pro/api/schema)
también describe un prompt textual. Por ello, introducir el JSON B dentro de prompt
conserva datos pero cambia el experimento: ambas entradas son texto para el proveedor.
**No es NATIVE_STRUCTURED_AB.**

Versión elegida exclusivamente para los cuerpos offline/documentación:
`569705b35f79b1160d51de1d0e3955626af86c77a034a16e89010dbdde5ad312`.
No se seleccionó `latest` ni se creó un manifest operacional. La página de esta
versión se pudo leer mediante navegación documental después de fallos de acceso
iniciales; los GET públicos directos desde shell devolvieron HTTP 403. No se usó
ningún token para eludirlo. Se distingue existencia documental de disponibilidad
actual para la cuenta y fijación efectiva del backend, aún no demostradas.

La [API HTTP](https://replicate.com/docs/reference/http/) permite identificar una
versión en el cuerpo de predictions.create y describe receipts con ID, modelo,
versión, input y estado. La guía de [modelos oficiales](https://replicate.com/docs/topics/models/official-models)
presenta normalmente la ruta por nombre, mantenida por Replicate sin exigir versión.
No se infiere que esa ruta fije pesos/backend, ni que una página histórica garantice
una versión ejecutable. Antes del bridge operacional hay que resolver esta diferencia
con schema/config oficiales de la versión exacta; nunca sustituirla silenciosamente
por la ruta sin versión. No se envió ningún POST.

## Matriz de mapeo y solicitudes no enviadas

Se inspeccionó D real en
`validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f/payloads.json`.
Las ramas originales comparten todo `common`; A contiene diez líneas JSON en string,
B contiene los mismos diez registros en array. Se verificaron orden, IDs, prioridades,
valores, tres locks, identidad, preservación, prohibiciones e incertidumbre.

| Campo del harness | Propuesta de request proveedor | Evidencia/límite |
| --- | --- | --- |
| `source_base64` | `input.input_image` como data URI JPEG | Mismos 33.183 bytes fuente; sin recorte, reencode ni URL pública |
| `payload.common` | Incluido íntegro dentro de `input.prompt` | Round trip JSON exacto en A/B; no resumen ni prompt agregado |
| A `relations_and_locks` string | String JSON escapado dentro del prompt textual | Se conservan las diez líneas y su orden |
| B `relations_and_locks` array | Array JSON serializado dentro del prompt textual | No llega como campo nativo del API |
| `provider` | Selección local de transporte Replicate | No se manda como una instrucción al modelo |
| `model` | `version` concreto en cuerpo candidato de `/v1/predictions` | Versión documental; invocabilidad/pin efectivos pendientes |
| `seed` | `input.seed=20260930`, idéntico A/B | Valor propuesto solo para factibilidad; no seed operacional aprobado |
| `parameters` | `aspect_ratio=match_input_image`, `output_format=png`, `prompt_upsampling=false`, `safety_tolerance=2` | Iguales A/B; no quality ni tamaño WxH anunciados por esta interfaz |

La serialización exacta es:

```python
json.dumps(payload, sort_keys=True, separators=(',', ':'),
           ensure_ascii=False, allow_nan=False)
```

Se usa UTF-8 sin prefijo, sufijo o salto final. Las listas mantienen el orden.
Los cuerpos completos se construyeron y hashearon **en memoria**, incluida la fuente,
y nunca se enviaron ni guardaron con base64. Los cuerpos redactados con prompts
completos están en [UNSENT_REQUESTS.json](../../validation/vsg_2b/p1r/UNSENT_REQUESTS.json).
Reemplazan input_image por descriptor y hash local: esos JSON redactados no son
requests válidos para enviar y su hash de archivo no es el hash del cuerpo completo.

| Medida | A | B |
| --- | --- | --- |
| Tipo que recibe el proveedor | prompt string | prompt string |
| Bytes UTF-8 del prompt | 16.999 | 16.582 |
| Tokens léxicos JSON, no del modelo | 2.254 | 2.818 |
| Backslashes del prompt | 417 | 0 |
| Bytes del cuerpo completo no enviado | 63.798 | 62.962 |
| SHA-256 cuerpo completo | `d50dbc1123bdedf230e03e3840451a6ba5266b9b61ffc460c04eb1517de6c790` | `17fdd303ebe349ebf151abe3ba8e8f52835892fc7474df0ef465ba20f5ecb844` |

Tokens del modelo: **UNKNOWN**. No se usó otro tokenizer como sustituto. El límite
real del prompt y el truncado no quedaron establecidos para esta versión. La
serialización es reversible localmente, pero eso no demuestra que el backend procese
todos los registros. Verificar aceptación íntegra sin truncado es un requisito
pendiente; no se permite acortar, resumir, eliminar campos o rellenar una rama para
igualar longitudes. Las diferencias de escape/longitud forman parte del tratamiento
textual y limitan la atribución causal.

Fuente D SHA-256:
`282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
Delta histórico intacto:
`6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`.
Los hashes nuevos son de **requests de factibilidad no enviados**; no constituyen
nuevo delta aprobado, manifest admitido ni autorización de generación.

## Capacidades anunciadas y límites de lo comprobado

Los [archivos de entrada](https://replicate.com/docs/topics/predictions/input-files)
admiten data URI; la recomendación de tamaño de esa guía es inferior a 1 MB, mientras
la referencia HTTP recomienda hasta 256 KB. D cumple ambas. Este mecanismo evita
publicar la foto en una URL propia; una predicción futura sí transmitiría la imagen
al proveedor. En esta ejecución la imagen nunca salió de la máquina.

Se documenta seed reproducible, formato PNG y matching del aspecto de la fuente;
se propone desactivar explícitamente upsampling y mantener safety_tolerance=2.
No se supone salida 347×389: la interfaz consultada no ofrece dimensiones exactas
ni el quality genérico del manifest actual. No se afirma la lista completa de enums
que la tabla renderizada no expone. El schema actual del repo necesitaría una versión
que represente estos settings sin ignorar size/quality silenciosamente.

Un futuro bridge deberá guardar el request exacto y receipt oficial, enlazar el
prediction ID con sus outputs y comparar el input devuelto con seed/settings enviados.
Eso acredita solicitud y recibo, no obediencia visual ni garantía de determinismo.
Si faltan campos o el proveedor altera/reduce el prompt, deberá bloquear; nunca
fabricar metadata haciendo pasar un eco local por confirmación remota. Polling y
descarga deben preservar recibos y bytes, sin reintentos de creación automáticos.
No hay receipts reales, prueba de acceso/facturación ni output en P1R.

## Propuesta exacta y decisión requerida

[PROPOSED_SCOPE.diff](../../validation/vsg_2b/p1r/PROPOSED_SCOPE.diff) es una propuesta
**no aplicada**. Añade el contrato `VSG-2B-TEXT-SERIALIZED-AB-1`, versiona la política
como 1.1.0 con `native_structured_evidence=false`, y propone schema de manifest 1.1.0
para settings del candidato, conservando manifests 1.0.0. Incluye la rúbrica de
interpretación: cualquier mejora se limita a dos serializaciones textuales; jamás
prueba array nativo. Los criterios visuales de D y la review ciega permanecen iguales.

La propuesta conserva todos los fenómenos, C obligatorio, cuatro representantes,
ocho intentos, S3/UNKNOWN/seed/STOP/no regresión y producción no autorizada. No incluye
admisión ni hashes operacionales. Tampoco basta aplicarla: la siguiente implementación
debe vincular experimento, versión de bridge/serializador y hashes de requests al
nuevo delta, validar reports y resolver los requisitos pendientes antes de admisión.

Decisión que se solicita al operador: **aceptar expresamente TEXT_SERIALIZED_AB**
con estos límites, o **mantener el experimento de array nativo** y evaluar otra
interfaz. Elegir Replicate y decir `go` para P1R no aprueba automáticamente ese cambio.
La pausa procede del gate 1.3 de la spec P1R: pide decisión explícita antes de admitir
manifest o generar cuando ambas ramas terminan en prompt string.

Si se acepta el cambio, el trabajo siguiente todavía exige: versión/pin disponible,
capacidad íntegra para ambos prompts, autenticación nueva local, bridge aislado
propuesto en `visual_scene_graph/pilot/adapters/replicate_kontext_bridge.py`, mocks de
HTTP/asíncrono/timeout/formato/recibos, y D operacional coherente. Para preservar K1,
el diseño P1 propone `R2B-191-D-P1` como único representante D operacional y conserva
D original histórico; no deben contarse ambos ni habilitar dos pares D cambiando ID.
Actualizar de forma versionada selección, schema, replay, admisión y evidencia;
luego nuevo dry run y revisión concreta de delta. Ninguna aprobación de alcance
autoriza el primer POST de predicción, que queda para otra spec.

## Autenticación local

Estado: **NOT_CHECKED_SCOPE_GATE / ROTATION_REQUIRED**. El token enviado al chat no
se ejecutó, usó, guardó ni probó. No se comprobó presencia de la variable porque el
gate semántico requiere decisión primero. Su presencia tampoco demostraría validez.
Revocar el token expuesto y crear otro en [API tokens](https://replicate.com/account/api-tokens),
según la [guía oficial de seguridad](https://replicate.com/docs/topics/security/api-tokens).
Luego ejecutar en la terminal zsh local, nunca enviando el valor al chat:

```zsh
read -rs 'REPLICATE_API_TOKEN?Pegá el token nuevo y presioná Enter: '
printf '\n'
export REPLICATE_API_TOKEN
[[ -n "${REPLICATE_API_TOKEN:-}" ]] && printf 'CONFIGURADO\n' || printf 'FALTA\n'
```

La lectura oculta evita pegar el secreto como comando. Esto configura solo esa
terminal y sus procesos hijos; no modifica el entorno de procesos VS Code/Codex
que ya estaban abiertos. No escribir el secreto en archivos versionados ni ejecutar
un ejemplo de predicción como prueba de autenticación. No se instaló un SDK.

## Pruebas ejecutadas y entrega

```sh
.venv-sc/bin/python validation/vsg_2b/p1r/inspect_unsent_requests.py
.venv-sc/bin/python -m unittest visual_scene_graph.pilot.test_campaign.CommandBridgeTests -v
git apply --check validation/vsg_2b/p1r/PROPOSED_SCOPE.diff
git diff --check
```

**18/18 comprobaciones offline PASS**, incluyendo preconditions actuales, replay
D, revisión del paquete persistido, hashes y round trips; **3/3 tests existentes de
protocolo fake PASS**. El diff propuesto se comprueba aplicable pero no se aplica.
No hay transporte en el script offline, no lee autenticación y su stdout redacta
la fuente. La inspección preservó los **734 archivos originales**. La suite histórica
G0 de 100 controles/25 casos/24 checks no se reejecutó completa ni se anuncia como
nueva. No se modifican archivos controlados ni se refrescan preconditions.

Documentación consultada: URLs enlazadas arriba, 2026-09-30; detalles de método y
limitaciones, comandos, hashes y checkpoints en
[P1R_RESULT.json](../../validation/vsg_2b/P1R_RESULT.json).
Cuota 5-hour/Weekly inicial, por gate y final: **UNKNOWN**; consumo **UNKNOWN**,
techo 40 puntos sin certificación numérica.
Archive / predicciones / imágenes generadas / pares nuevos: **0/0/0/0**.
C conserva `NO_GO_C0_UNVERIFIED`: falta vínculo documental Fear City ↔ CG-FC;
F no sustituye Reference Isolation. No hay PASS visual ni avance a VSG-3A.
