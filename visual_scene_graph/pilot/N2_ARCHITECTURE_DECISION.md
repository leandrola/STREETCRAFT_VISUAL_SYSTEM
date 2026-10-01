# VSG-2B / N2 · decisión arquitectónica

**N2_ARCHITECTURE_DECISION_READY** · 2026-10-01.

Se completan el diseño de la ruta A y una propuesta independiente B. La única base
elegida para A es **GLIGEN en Diffusers v0.29.0**. Reúne texto, grounding y contenido
visual fuente, pero no acredita el consumidor de relaciones VSG, la capacidad para
todo el texto ni la preservación de la fuente que exige el contrato. Construir una
sonda causal honesta requiere trabajo de modelo/integración previo. No se implementa
un generador, sonda ni mock; tampoco se ejecuta generación.

**Recomendación técnica:** si la prioridad sigue siendo cerrar VSG-2B original,
mantener la ruta A como siguiente hito de investigación/desarrollo, sujeto a decisión
explícita sobre su esfuerzo. La ruta B es una opción más corta para estudiar
serialización textual, pero nunca cierra ese gate. Este documento deja ambas
alternativas concretas para decidir; no aprueba automáticamente ninguna.

## Entrada y contrato congelado

HEAD inicial/final y base de main: `4cac756d00d4ee1e3df7768ce38703c0c8605618`.
Árbol inicial limpio; N1 ya está versionado. Sin AGENTS.md aplicables encontrados.
Se conservan los **743 archivos de entrada**. Se leyeron N1_RUNBOOK/N1_RESULT,
P1R_SCOPE_DECISION, renderer/protocolo del harness, política, schemas y D persistido.
La spec se encontró en `Documents/specs vsg`, tras no encontrarse en Downloads.
El usuario dio `go` tras recomendar Alta; el selector de la aplicación no se verifica.

Dry run D: `validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f`.
JPEG SHA-256 `282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`;
33.183 bytes, dimensiones históricas 347×389. Delta
`6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`.
El JSON de resultado congela los diez registros completos y los hashes de entrada.
A es string JSONL, B array tipado; los registros y common son semánticamente iguales.
Fuente, common, modelo compuesto, pesos, seed y settings deben ser idénticos entre
ramas. El seed actual permanece null/DRY_RUN_ONLY; N2 no lo operacionaliza.

| Registro D | Tratamiento propuesto, sin cambiar sus valores |
| --- | --- |
| edge:rel_facade_left_of_diner | Señal relacional facade_01 LEFT_OF diner_01; conservar PR1, evidence y lock_ids. Consumidor aprendido pendiente. |
| edge:rel_sign_above_diner | Señal relacional sign_01 ABOVE diner_01; conservar PR0 y provenance. Consumidor pendiente. |
| lock:GL-GEO-DINER_01 | VALIDATE_ONLY: target, storefront y topología protegida; validar antes/después, nunca convertir a máscara. |
| lock:GL-GEO-FACADE_01 | VALIDATE_ONLY: target, facade y relación protegida; sin edición geométrica forzada. |
| lock:GL-SEM-SIGN_01 | VALIDATE_ONLY: sign_01 y literal TERMINAL DINER; fallo/UNKNOWN en revisión impide concluir preservación. |
| topology:billboard_01 | Nodo y lista vacía conservados; presencia explícita en índice/máscara de nodos, sin inventar aristas. |
| topology:diner_01 | Incidencia de las dos relaciones protegidas; referencias exactas, sin contar dos veces cada edge. |
| topology:facade_01 | Incidencia de rel_facade_left_of_diner; conservar prioridad y lock FACADE. |
| topology:fascia_01 | Nodo y lista vacía conservados, sin eliminarlo ni crear geometría. |
| topology:sign_01 | Incidencia de rel_sign_above_diner; conservar lock SEM-SIGN y prioridad. |

Priority, authority, confidence y provenance conservan su función de validación y
alcance. No se reinterpretan como pesos de atención. Conservarlos para auditoría
no se presenta como condicionamiento generativo. VALIDATE_ONLY sigue siendo tal;
una validación de bytes anterior no acredita obediencia visual posterior.

## Ruta A · una base y sus límites verificables

Base: `StableDiffusionGLIGENPipeline`, código **v0.29.0**, con hash de cada archivo
consultado en N2_RESULT. La [documentación versionada](https://huggingface.co/docs/diffusers/v0.29.0/en/api/pipelines/stable_diffusion/gligen)
incluye texto, cajas/frases, imagen de inpainting y torch.Generator. Esa coexistencia
la hace base de diseño para un mismo modelo; no prueba soporte del B original.

Flujo inspeccionado en el
[pipeline](https://github.com/huggingface/diffusers/blob/v0.29.0/src/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py):
`__call__` L530 → prompt/grounding; L741 transmite boxes/embeddings/masks; L744–761
preprocesa y codifica píxeles fuente; L809 llama al UNet. La ruta textual activa
truncation en L276–291; las cajas excedentes se recortan con warning. La fuente puede
recortarse al centro. El muestreo VAE de L756 no recibe el generator explícito de
la solicitud. Son brechas a resolver antes de alegar paridad de seed, texto o fuente.

[GLIGENTextBoundingboxProjection](https://github.com/huggingface/diffusers/blob/v0.29.0/src/diffusers/models/embeddings.py#L910)
proyecta coordenadas y embeddings; no contiene la semántica de predicados VSG.
[GatedSelfAttentionDense.forward](https://github.com/huggingface/diffusers/blob/v0.29.0/src/diffusers/models/attention.py#L75)
fusiona features de objetos con features visuales. **Inferencia de diseño:** habría
que desarrollar y validar una representación relacional compatible con ese espacio,
posiblemente entrenar un adaptador y resolver texto largo/fuente. Tener tensores del
tamaño adecuado o activar un gate no demuestra esa compatibilidad semántica.

No se propone resolver LEFT_OF/ABOVE como cajas absolutas: dos relaciones no
determinan un layout único, y `evidence.region` no es una instrucción de inpainting.
Convertirlas automáticamente en cajas o usar los locks como máscaras cambiaría el
tratamiento aprobado. Tampoco se combinan capacidades de SIMSG y otro modelo.

Pesos candidatos: `masterful/gligen-1-4-inpainting-text-box`, variante fp16 citada en
la documentación. **Revisión inmutable y hashes de pesos: NOT_VERIFIED**; no se
descargaron. La [model card](https://huggingface.co/masterful/gligen-1-4-inpainting-text-box)
declara CreativeML OpenRAIL-M y limitaciones de texto legible/composicionalidad;
no garantiza el literal de D. Código Diffusers:
[Apache-2.0](https://github.com/huggingface/diffusers/blob/v0.29.0/LICENSE).
La licencia de código no sustituye la de pesos. La card mutable solo documenta el
candidato, no fija un checkpoint operacional ni acredita compatibilidad futura.

Entorno observado: Darwin x86_64, Python 3.14.5 en `.venv-sc`; torch, diffusers y
transformers ausentes allí. No se infiere ausencia en toda la máquina. Entorno
propuesto para otro hito: contenedor Linux con Python/PyTorch/CUDA fijados después
de comprobar compatibilidad con v0.29.0; GPU, memoria y coste **NOT_VERIFIED**.
No se instala nada. El hito de recursos debe medir memoria con pesos fijados antes
de comprometer entrenamiento; no se promete ejecución en este Mac.

## Módulos y frontera propuesta, no implementados

| Módulo | Contrato y salida | Falta para una sonda real |
| --- | --- | --- |
| N2EnvelopeValidator | JSON estricto sin duplicate keys/NaN; A string y B array, diez registros y referencias exactas; rechazar extras, coerción, pérdidas y parámetros no soportados | Implementación focalizada futura; parsing de A solo para validación, nunca para sustituir su entrada textual |
| FrozenInputBinder | Bytes JPEG, common, hashes de manifest/contrato, revisión de delta y settings iguales | Admisión operacional posterior; ningún rebind implícito de D |
| RecordLedger | Copia íntegra por ID y mapa reversible a índices; incluye listas vacías y validaciones de locks | Auditoría sin pérdida; separar campos generativos de validación |
| RelationalEncoder | Predicados/extremos y matriz de incidencia por nodo; mensaje tipado por edge y presencia de los cinco nodos | Representación y pesos entrenados/verificados; índices/shape no bastan |
| StructuralConditioner | Features relacionales conectados al fusionador/atención del UNet con trazas por ID | Adaptación de modelo no implementada; no reinterpretar cajas como edges |
| TextConditioner | common + A JSONL íntegro al encoder textual; en B mismo common y relaciones por puerto estructural | Capacidad completa sin truncar ni resumir; protocolo de texto largo no demostrado |
| SourceConditioner | Mismo JPEG y transformación registrada en ambas ramas; contenido visual en el modelo | Evitar recorte no aprobado y máscara derivada de locks; definir edición compatible |
| AuditReceipt | Hashes de request, fuente, common, código, pesos, vocabulario, tokenizer, scheduler, runtime, features por ID y respuesta | Instrumentación de módulos reales; receipt local no es confirmación remota |
| PreservationReview | Locks/rúbrica antes/después; observación visual independiente, S3/UNKNOWN/STOP | Solo tras una futura generación autorizada; nunca sustituir por distancia de features |

Modelo compuesto único: mismos pesos base **y del adaptador** cargados en A/B. La
diferencia prevista es el canal de relaciones: texto original en A, estructura en B.
El puerto estructural de A queda vacío mediante un estado nulo definido, no mediante
un segundo modelo; esa ausencia forma parte del tratamiento y debe revisarse en el
delta. Common no se resume ni se modifica para compensar información redundante.
Se fijan scheduler, precisión, hardware, RNG de CPU/GPU/VAE y política de máscaras;
un seed escalar por sí solo no acredita igualdad. No hay selección operacional ahora.

## Criterio causal previo y sonda omitida

Antes de implementar se fijó el criterio guardado en N2_RESULT: trazar D real desde
sus IDs hasta la entrada de un consumidor estructural con pesos fijados. Cambiar un
predicado válido debe cambiar las features efectivamente recibidas/usadas por ese
módulo, manteniendo fuente/common/settings/estado RNG. Comprobar solo el hash del
JSON o una lista serializada no prueba causalidad. Un gate apagado o una ruta que
ignora las features tampoco pasa. No se requiere ni se autoriza producir imágenes.

Pruebas futuras, **no ejecutadas**:

1. D intacto como baseline, texto A preservado y B completo en el puerto tipado.
2. Diagnóstico derivado de D: invertir `LEFT_OF` a `RIGHT_OF` conservando IDs y
   extremos, ambos enums del schema, y observar el cambio en el consumidor real.
   Es válido en tipos/referencias, **no** una nueva verdad autorizada de la fuente.
   Debe aislarse en la capa de consumidor: los locks congelados siguen esperando
   LEFT_OF y el gate de admisión debe rechazar cualquier request mutado. No se
   desactiva ese gate ni se presenta el diagnóstico como contrato D aprobado.
3. Referencia inexistente en topology: rechazo antes del consumidor.
4. Pérdida de GL-SEM-SIGN_01 o coerción de B a string: rechazo antes del consumidor.
5. A/B sin diferencias de pesos, fuente/common/RNG/settings; IDs/listas vacías
   íntegros; longitud excedida o campo no soportado: fallo explícito, sin fallback.

Sonda: **NOT_BUILT_NO_VERIFIED_STRUCTURAL_CONSUMER**. Ni los pesos relacionales ni
la ruta completa están disponibles/verificados. Un encoder ficticio podría producir
features diferentes, pero solo demostraría TRANSPORT_ONLY. N2 no lo construye.

## Ruta B · propuesta de experimento independiente

**ID propuesto: VSG-X1-TEXT-SERIALIZATION-D-01**, revisión de propuesta 0.1.
Estado `PROPOSED_NOT_APPROVED`; sin manifest, admisión ni implementación.

Hipótesis exploratoria: para una fuente y seed fijos, la serialización textual B
preserva más criterios de D que la textual A, sin pérdida protegida ni cambios no
autorizados. Compara **dos prompts textuales**; no mide consumo de arrays nativos.

Backend propuesto únicamente para X1: Replicate / FLUX.1 Kontext [pro]. Se reutiliza
la factibilidad documental P1R; no se contacta al proveedor. Su versión documental
`569705b35f79b1160d51de1d0e3955626af86c77a034a16e89010dbdde5ad312`
tiene invocabilidad/pin efectivos **NOT_VERIFIED**. Un alias latest no la sustituye.

| Elemento | Contrato propuesto X1 |
| --- | --- |
| Baseline A | `json.dumps(payload_A, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)` como prompt; relaciones JSONL quedan escapadas dentro del string |
| Comparador B | Misma serialización determinista de payload_B; su array queda dentro del prompt textual, nunca se declara entrada nativa |
| Fuente | Mismos bytes JPEG D y hash; snapshot nuevo bajo X1 con referencia a su procedencia, sin tocar evidencia original |
| Controles | Mismo modelo/pin efectivo, seed propuesto 20260930, common, aspect_ratio=match_input_image, output_format=png, prompt_upsampling=false, safety_tolerance=2; soporte y ausencia de truncado pendientes |
| Diferencia permitida | Solo representación/escapado de relaciones/locks; longitudes/tokens pueden diferir y se registran, sin padding ni resumen |
| Rúbrica | Copia versionada con hash de la rúbrica D: identidad, relaciones, geometría protegida, literal, topología y cambios no autorizados; observación ciega S0–S3/UNKNOWN por criterio |
| Presupuesto propio | Propuesta: un par, máximo dos intentos facturables, cero retries; techo USD 1.00 sujeto a verificar precio total antes de autorizar. Actualmente llamadas autorizadas: 0 |
| Ledger y evidencia | Nueva raíz `outputs/vsg-x1-text-serialization-d-01/`, manifest/schema/allowlist específicos de X1 y contador propio; rutas solo propuestas, no creadas |
| Gate | X1_OBSERVED_BETTER, X1_TIE, X1_WORSE, X1_INDETERMINATE o X1_TECHNICAL_BLOCK; jamás PASS de VSG-2B |

X1_OBSERVED_BETTER exige dos outputs válidos, settings/seed/receipts verificados,
mejora de al menos un criterio, ninguna regresión ni pérdida protegida, sin S3 ni
UNKNOWN. Es observación de un solo par, no evidencia estadística generalizable.
Empate devuelve TIE; pérdida/S3/regresión devuelve WORSE y STOP; UNKNOWN devuelve
INDETERMINATE. Error técnico, coste/pin no verificable, truncado, drift de parámetros,
recibo incompleto o revisión discrepante bloquea y detiene. No se consume otra
llamada para sustituir un fallo ni se cruza el máximo de intentos.

Los resultados X1 son **ineligibles** para pares, cobertura, mejora y cierre de
VSG-2B. No reutilizan su ID, manifests, allowlist ni ocho llamadas. El nuevo lector
de resultados deberá rechazar mezcla de IDs/ledgers; no basta cambiar de carpeta.
No se aplica el PROPOSED_SCOPE.diff histórico. X1 necesita aprobación explícita de
alcance antes de implementar o generar, más resolución de pin, coste, límites,
autenticación local y admisión propia. No se inspeccionó ni configuró ningún token.

## Tabla de decisión y siguientes hitos

Estimaciones de planificación en **días-persona de ingeniería**, no medidas de
consumo, garantías ni autorización. Excluyen espera, entrenamiento GPU, curación de
datos, licencias/costes y revisión visual humana; esas partidas siguen UNKNOWN.

| Ruta/hito | Esfuerzo estimado | Dependencia / riesgo / salida |
| --- | --- | --- |
| A0: viabilidad de pesos, texto y fuente | 2–4 días | Pin/licencia/entorno y estrategia sin recorte/truncado; puede descartar esta base |
| A1: validador, ledger y auditoría | 3–5 días | Contrato exacto; por sí solo es transporte y validación |
| A2: modelo relacional compatible | 15–40 días | Datos/entrenamiento o adaptación por demostrar; puede no lograr semántica útil |
| A3: sonda causal y reproducibilidad | 5–10 días | Pesos reales y módulos conectados; permite evaluar factibilidad offline, no PASS visual |
| A total indicativo | 25–59 días | Única ruta aquí que mantiene la posibilidad de cerrar VSG-2B original; éxito no garantizado |
| B1: bridge X1, límites y receipts | 1–3 días | Solo tras aprobar alcance; pin/invocabilidad/precio pendientes |
| B2: admisión/dry run propio | 1–2 días | Schema, contador y aislamiento de evidencia nuevos |
| B3: ejecución/revisión autorizada | 0.5–1 día | Más revisión humana/espera; un par textual, ninguna conclusión de estructura nativa |
| B total indicativo | 2.5–6 días | Experimento distinto; no resuelve VSG-2B ni el bloqueo C |

No se inicia A0 ni B1 en N2. La decisión queda lista para elegir si se financia la
ruta estructural o se aprueba por separado X1. Una recomendación no es aprobación.

## Verificación y estado final

Verificaciones frescas: `harness.check_preconditions()` PASS;
`review_dry_run.review(D)` PASS; igualdad de los diez registros con N1, A parseada/B,
common y tres VALIDATE_ONLY PASS. Inspección de cuatro archivos código/licencia de
la base sin ejecutarlos; hash del pipeline coincide con N1. `git diff --check` y
comprobación de whitespace de ambos entregables nuevos PASS. Los 743 archivos
previos siguen idénticos, incluidos D/E/Kenny/C y toda su evidencia. No se refresca
la suite: los 100/25/24 resultados G0 siguen siendo históricos.

| Tramo | Tope orientativo solicitado | 5-hour inicio/final | Weekly inicio/final |
| --- | --- | --- | --- |
| Lectura/criterios | ≤6 puntos | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN |
| Base/diseño | ≤12 puntos | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN |
| Sonda omitida | ≤12 puntos | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN |
| Verificación/cierre | ≤10 puntos | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN |

Techo global solicitado ≤40 puntos; sin telemetría no se certifica consumo ni
cumplimiento numérico. El tramo de sonda se omitió, pero su cuota no se reasigna a
otra búsqueda. No se reservó ni consumió una llamada de imagen mediante N2.

VSG-2B **BLOCKED / PENDING_VISUAL**, `production_authorized=false`. C sigue
NO_GO_C0_UNVERIFIED: falta autoridad verificable Fear City ↔ CG-FC ligada a su JPEG;
F no sustituye Reference Isolation. No se inicia VSG-3A. Archive / predicciones /
imágenes / pares nuevos = **0 / 0 / 0 / 0**.

[N2_RESULT.json](../../validation/vsg_2b/N2_RESULT.json) conserva el contrato, fuentes,
límites, hashes y verificaciones. No hay proveedor READY ni autorización visual.
