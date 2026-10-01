# VSG-2B / N3 · base fijada y dependencia de modelo

**N3_MODEL_DEVELOPMENT_REQUIRED** · 2026-10-01.

Se fija una sola base: GLIGEN con Diffusers v0.29.0 y el checkpoint de inpainting
seleccionado en N2. Se verifican código, configuración y metadatos de pesos, no su
ejecución. Su ruta de cajas/frases necesita un canal relacional aprendido para el
contrato VSG. La sección 6 de N3 exige cerrar en este estado cuando falta ese canal;
por eso no se crea un adaptador aleatorio ni se ejecuta una sonda de juguete.

Avance respecto de N2: commit y revisión de checkpoint concretos, hashes LFS y tamaños
publicados, configuración de 77 posiciones de texto y UNet de 9 canales, ubicación
exacta del consumidor y presupuesto de desarrollo. No se acredita consumidor VSG,
PROVIDER_READY, mejora visual ni cierre de VSG-2B.

## Preflight y archivos permitidos

HEAD inicial/final: `8009b66700f9f125a5e9ad8992ffd074425aa500`; árbol inicial limpio.
Inventario medido: **745 archivos previos**, no la cifra histórica de N2. Sin
AGENTS.md aplicables ni colisiones N3 encontradas. Se verificaron N2, P1R, política,
schemas/harness y D real. No se repitió la investigación de N1.

Lista de creación permitida, fijada antes de escribir entregables:

- `visual_scene_graph/pilot/N3_STRUCTURAL_CONSUMER_RUNBOOK.md`
- `validation/vsg_2b/N3_RESULT.json`
- `validation/vsg_2b/n3/BASE_MANIFEST.json`
- `validation/vsg_2b/n3/INPUT_MANIFEST.json`
- `validation/vsg_2b/n3/RECORD_CONSUMPTION_MAP.json`

Todos son documentos/evidencia del hito, no manifests operacionales admitidos.
No se crea CAUSAL_TRACE.json porque no hubo sonda. No se modifican archivos previos,
schemas, allowlist, campaña, Archive, CGC, P1R, N2 ni PROPOSED_SCOPE.diff.
Sin branch, commit ni push. Recomendación Alta conservando modelo del usuario;
modelo/esfuerzo expuestos por el cliente no son verificables desde estas herramientas.

## Base y checkpoint verificables

Código: `huggingface/diffusers`, release v0.29.0, commit
`39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f`.
Checkpoint: `masterful/gligen-1-4-inpainting-text-box`, revisión
`d6d957f8d27c40889c0d570a616571a5645c8be3`, variante fp16.
Los hashes LFS publicados de sus cuatro archivos seleccionados están en BASE_MANIFEST.
**Son hashes declarados por el repositorio, no verificación local de bytes de pesos.**
No se descargaron pesos ni se importó código externo.

Licencia del código: Apache-2.0 en el commit fijado. La
[card fijada del checkpoint](https://huggingface.co/masterful/gligen-1-4-inpainting-text-box/blob/d6d957f8d27c40889c0d570a616571a5645c8be3/README.md)
declara CreativeML OpenRAIL-M; no se transfiere la licencia de código a pesos/datos.
Metadatos públicos: `private=false`, `gated=false`; esto acredita acceso anónimo
a la metadata consultada, no capacidad operacional ni descarga comprobada de pesos.

La card/documentación muestra la carga explícita de StableDiffusionGLIGENPipeline.
El `model_index.json` histórico declara StableDiffusionPipeline/versión antigua;
no usar autodetección como prueba de compatibilidad. La carga explícita con todos
los componentes y v0.29.0 sigue pendiente de prueba autorizada.

| Capacidad | Clase | Evidencia y límite |
| --- | --- | --- |
| Texto como conditioning | VERIFIED_EXISTING | Pipeline.__call__ L530 y encode_prompt; no acredita soporte íntegro del JSONL D |
| Píxeles fuente | VERIFIED_EXISTING | Pipeline L744–761: preprocess/VAE; posible crop, semántica de máscara a revisar |
| Grounding tipado cajas/frases | VERIFIED_EXISTING | Pipeline L741 → UNet.forward L1165–1168 → position_net |
| Consumidor de features | VERIFIED_EXISTING | GatedSelfAttentionDense.forward L75; recibe objs y modifica features visuales |
| Edges/topología VSG | ADAPTATION_REQUIRED | GLIGENTextBoundingboxProjection.forward exige cajas, no predicados ni incidencia |
| JSONL/common sin pérdida | ADAPTATION_REQUIRED | tokenizer y text encoder fijados limitan a 77 posiciones; pipeline trunca con warning |
| A/B original en mismo checkpoint | UNVERIFIED | Existen texto y grounding, no canal VSG aprendido ni sonda |
| Preprocesamiento idéntico y autorizado | ADAPTATION_REQUIRED | Prohibido usar regiones de evidencia/VALIDATE_ONLY como máscaras o crop autorizado |
| Reproducibilidad total | UNVERIFIED | generator controla latents, pero muestreo VAE no recibe ese argumento; controlar todos los RNG |
| Carga y capacidad con pesos | UNVERIFIED | Configs revisadas, pesos no descargados/cargados |

VERIFIED_EXISTING significa evidencia estática en código/configuración, **no forward
ejecutado**. Código primario fijado:
[pipeline](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py),
[UNet](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/models/unets/unet_2d_condition.py#L1165),
[proyección](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/models/embeddings.py#L953),
[fusionador](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/models/attention.py#L75).

La configuración fijada del UNet especifica attention_type=gated,
cross_attention_dim=768, in_channels=9, out_channels=4, sample_size=64.
Scheduler PNDM: configuración fijada, no scheduler sustituido. Esa información
permite diseñar la inserción; no demuestra que features arbitrarios de 768 valores
sean entendidos por los pesos existentes.

## Contrato real D y mapa de consumo

Dry run: `validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f`.
Fuente SHA-256 `282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
Delta `6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`.
Se cotejó el inventario con N2: 2 edges, 3 locks y 5 topology; common igual,
A JSONL/B array iguales en contenido. Sin reconstrucción de memoria.

| Registro | Destino propuesto | Consumo efectivo en esta ejecución |
| --- | --- | --- |
| edge:rel_facade_left_of_diner | Token relacional facade_01 LEFT_OF diner_01 y registro de origen PR1 | NOT_RUN |
| edge:rel_sign_above_diner | Token relacional sign_01 ABOVE diner_01 y registro PR0 | NOT_RUN |
| lock:GL-GEO-DINER_01 | Ledger/validación VALIDATE_ONLY de target y topología; sin token de fuerza geométrica | NOT_RUN |
| lock:GL-GEO-FACADE_01 | Ledger/validación VALIDATE_ONLY | NOT_RUN |
| lock:GL-SEM-SIGN_01 | Ledger/validación de TERMINAL DINER íntegro y revisión visual posterior | NOT_RUN |
| topology:billboard_01 | Slot del nodo y lista vacía explícita, sin inventar edge | NOT_RUN |
| topology:diner_01 | Slot del nodo, incidencia de ambas relaciones | NOT_RUN |
| topology:facade_01 | Slot del nodo, incidencia LEFT_OF | NOT_RUN |
| topology:fascia_01 | Slot del nodo y lista vacía explícita | NOT_RUN |
| topology:sign_01 | Slot del nodo, incidencia ABOVE | NOT_RUN |

RECORD_CONSUMPTION_MAP conserva cada objeto original completo, rol y slot propuesto.
IDs, listas vacías, prioridades, authority/provenance y lock_ids nunca se descartan.
VALIDATE_ONLY no impone píxeles; P0/PR0/PR1 son controles de protección, no pesos de
atención inventados. La validación local de hashes no reemplaza la visual.

## Desarrollo concreto que falta (propuesta, no ejecución)

**Módulo faltante:** RelationalConditionProjector + adaptación del fusionador para
tokens de relaciones, y solución de texto largo/fuente antes de aceptar D completo.
El cambio concreto respecto de N1/N2 es proponer un canal aprendido que entra al
operador identificado, sin reducir relaciones a cajas ni combinar modelos.

Entradas internas derivadas sin cambiar el schema: cinco IDs/nodos, dos triples
con predicado tipado y matriz de incidencia de topology. Dos slots de edge y cinco
de nodo: tensor propuesto `[batch,7,768]`, índices int64, máscaras booleanas;
features float32 durante validación, precisión de cómputo fijada tras prueba.
Dispositivo futuro CUDA, no empleado ahora. El ledger conserva los campos que no
son tensores de conditioning. Vocabulario inicial explícito: LEFT_OF/ABOVE y sus
inversas RIGHT_OF/BELOW para diagnóstico; otros tipos se rechazan hasta ampliación
versionada. Esto no habilita E/Kenny/C ni cobertura de OCCLUDES automáticamente.

Inserción propuesta: un puerto relacional distinto en UNet.forward, junto al
procesamiento de kwargs de L1165, que entregue `objs` al mismo fusionador L75.
No reinterpretar el campo boxes existente ni agregar atributos al payload D.
Modificar el UNet externo requiere un fork/patch versionado de modelo en otro hito;
no se aplica a archivos protegidos ni a la campaña bajo N3.

Congelar VAE, text encoder y pesos base del UNet. Entrenar el proyector relacional,
embeddings de predicados y, si la transferencia no basta, deltas/LoRA del fusionador;
fijar y versionar esa elección antes del entrenamiento. Cargar el mismo artefacto
compuesto completo en A/B. A consume su JSONL textual original, con canal gráfico
desactivado por mecanismo definido; B consume common textual y registros por canal
estructural. No parsear A para alimentar el grafo. Un parser de auditoría no cambia
la entrada efectiva del modelo. No añadir B a prompt ni alterar common.

Texto largo: diseñar un encoder por bloques sin pérdida con resampler aprendido
o un mecanismo equivalente verificable; nunca asumir que concatenar embeddings
conserva semántica. Debe probarse en ambas ramas y formar parte del mismo checkpoint.
Si exige sustituir arquitectura más allá del presupuesto, descartar esta base en
ese hito. Los 77 lugares del encoder actual no se amplían por cambiar un config.

Fuente: definir un preprocesamiento común sin recorte de contenido y una máscara
de edición con autoridad propia cuando haga falta. Ni evidence.region ni locks
VALIDATE_ONLY conceden esa autoridad. La fuente latente y máscara comunes deben
formar los canales de inpainting requeridos sin un segundo tratamiento oculto.
Hasta resolverlo, ni el D actual ni un tensor con la forma correcta son admitidos.

### Datos y aprendizaje

No se declara ningún dataset disponible para este trabajo. Propuesta de adquisición:
pares source/target con autorización de edición y grafos anotados por IDs; licencia
y procedencia verificables por imagen, anotación y transformación. Separación por
escena/fotógrafo entre train/val/test; excluir D/E/Kenny/C de entrenamiento y tuning.
El corpus de evaluación del proyecto no es permiso ni volumen suficiente de training.

Piloto orientativo: 5.000–20.000 pares, balanceados LEFT_OF/ABOVE y controles/inversas,
con ejemplos sin edición y relaciones contradictorias para rechazo. Es una hipótesis
de escala, no disponibilidad ni suficiencia demostradas. Objetivo propuesto: pérdida
de denoising contra targets autorizados + término relacional sobre anotación de
layout/identidad; regularización de preservación para no-edición. Los pesos de las
pérdidas y umbrales semánticos se fijan antes del piloto, no después de ver D.

Éxito previo a pares oficiales: mejora relacional en test independiente frente a
ablación del canal y controles de seed, sin degradación protegida predefinida;
traza causal real, réplica numérica dentro de tolerancia, ninguna pérdida de campo,
texto sin truncado y fuente común demostrados. Métricas/umbrales de rendimiento
semántico permanecen pendientes de corpus: el diagnóstico computacional no los sustituye.

### Recursos y autorización posterior necesaria

- Descarga de los cuatro pesos fp16: **3.159.269.896 bytes** (~3,16 GB decimales),
  tamaño publicado; tokenizer/configs y caches suman más. No es RAM/VRAM requerida.
- Entorno observado: Darwin x86_64, 16 GiB RAM; `.venv-sc` Python 3.14.5 sin
  torch/diffusers/transformers. GPU/VRAM compatible y carga exitosa: UNKNOWN.
- Estimación de planificación: Linux, 1 GPU CUDA de 24–48 GiB, 32–64 GiB RAM,
  100–250 GB de almacenamiento. No son mínimos medidos; validar compatibilidad de
  versiones y memoria antes de reservar equipo.
- Piloto propuesto: 50–200 GPU-h, techo adicional propuesto 200 GPU-h, sin autorización
  vigente. A 5k–20k pares y 1–2 MB por imagen, solo imágenes ocuparían 10–80 GB;
  reservar más para caches, snapshots y checkpoints. Supuestos, no mediciones.
- Precio por GPU-h, costes de datos/licencias y coste total: UNKNOWN. Presupuesto
  monetario = GPU-h aprobadas × tarifa cotizada + almacenamiento + datos; no contratar
  infraestructura sin propuesta de importe total. N3 gastó cero en cómputo externo.
- Ingeniería: reutilizar rango N2 **25–59 días-persona**, excluye datos/esperas/GPU:
  2–4 viabilidad, 3–5 validación/auditoría, 15–40 adaptación, 5–10 sonda/reproducibilidad.

Siguiente hito concreto: aprobar un piloto de desarrollo con corpus licenciado,
importe/cómputo y permisos de descarga/entrenamiento; resolver primero texto largo y
fuente para evitar entrenar una base que siga sin aceptar D. Entregar entorno
bloqueado, scripts/configs, split y hashes de datos, checkpoint base/deltas con
SHA-256 local, vocabulario, prueba de carga estricta y receipts de sonda. Rollback:
desactivar el módulo externo/descartar su checkpoint; piloto, N2 y evidencia original
siguen intactos. Ninguna selección ni admisión se cambia sin el gate posterior.

## Protocolo causal pendiente

Todas las ocho pruebas de la spec quedan **NOT_RUN**, con causa individual en
N3_RESULT: D real, repetición, mutación válida, topology inválida, lock perdido,
B coercionada a string, ruta A y ablación. Faltan pesos aprendidos compatibles,
entorno autorizado, integración y clasificación del forward en counters.

Propuesta de tolerancia inicial, **no calibrada ni ejecutada**: repetición fp32
atol=1e-6/rtol=1e-5; fp16 atol=1e-3/rtol=1e-3. Declarar dtype/dispositivo y fijarlas
antes del test; si la base no las cumple, investigar, no ensanchar después del fallo.
Mutación/ablación: cambio normalizado mayor a diez veces el ruido de repetición y
mayor a 1e-4 en features/salida del operador real. Es criterio computacional propuesto,
no preservación visual ni un objetivo de calidad entrenable por sí solo.

Mutación LEFT_OF→RIGHT_OF derivada de D: válida en enums/IDs, pero contradice la
verdad congelada. Diagnóstico aislado de la capa de consumidor; no request admitido.
Los hashes y locks de campaña deben rechazarla si se intenta enviar como D. No
eludir esa comprobación para conseguir una prueba positiva. Hooks previstos en
salida del proyector, entrada y salida del fusionador real, incluyendo repetición
y ablación; cero loop de difusión/decodificación. Si no existe dependencia observable,
no hay PASS. No se crea una traza ficticia para documentar este protocolo.

## Counters y verificaciones frescas

La política cuenta `*.attempt.json` por campaña; harness L245 escribe uno antes de
`generator.generate`, también si falla. El límite es ocho intentos, no ocho imágenes.
Un forward local de encoder fuera del harness **no está clasificado** por la política
actual. Se mantiene bloqueado hasta aclaración explícita; no se declara exento ni
se oculta como “offline”. En N3 `offline_forward_count=0`: no se ejecutó ningún modelo.

Medición antes/después en `outputs` y `validation/vsg_2b`: cero attempt files,
15 reportes persistidos sin imágenes y ninguna evaluación; por tanto cero pares
visuales en esos registros. No se consultó la cuenta de un proveedor: su historial
total es UNKNOWN. Archive/predicciones de esta ejecución son cero por las acciones
realizadas; las lecturas públicas de metadata no son llamadas de generación.

Fresco: preconditions PASS; review independiente de D PASS; igualdad de registros
con N2 PASS; configuración y símbolos de la base revisados sin importarlos. Metadata
y configs descargados por GET anónimo, no pesos. Git/whitespace y comprobación final
de los 745 hashes previos PASS. No se ejecutan suites globales, ni se refresca
evidencia congelada. N3_RESULT distingue esos checks de las ocho pruebas NOT_RUN.

Plan Limits por tramo (preflight/base/integración omitida/cierre): 5-hour y Weekly
**UNKNOWN**. Techo heredado ≤40 puntos, distribución orientativa 4/10/20/6; no se
certifica consumo porcentual ni se reasigna remanente a más candidatos.

VSG-2B **BLOCKED / PENDING_VISUAL**, producción false; C sigue NO_GO_C0_UNVERIFIED,
X1 sin aprobar, VSG-3A sin iniciar. Archive / predicciones / imágenes / pares nuevos:
**0 / 0 / 0 / 0**, forwards locales **0**.

Evidencia: [resultado](../../validation/vsg_2b/N3_RESULT.json),
[base](../../validation/vsg_2b/n3/BASE_MANIFEST.json),
[inputs](../../validation/vsg_2b/n3/INPUT_MANIFEST.json),
[mapa por registro](../../validation/vsg_2b/n3/RECORD_CONSUMPTION_MAP.json).
