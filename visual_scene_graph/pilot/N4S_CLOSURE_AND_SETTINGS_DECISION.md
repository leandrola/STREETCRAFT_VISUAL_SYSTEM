# VSG-2B / N4S · Cierre consolidado y decisión concreta

**`N4S_SETTINGS_DECISION_READY` · confianza `STATIC_ONLY`.** La propuesta está lista
para aceptar, rechazar o pedir una corrección específica. No está aprobada ni aplicada.

Decisión identificable: **`VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0`**. Se conserva la
propuesta N4R existente; como no tenía un ID formal, N4S le asigna ese identificador
y versión, sin crear una enmienda competidora ni reutilizar X1.

Recomendación técnica: **aceptar el diseño únicamente para preparar un plan de
implementación y recursos**. Esa decisión no autoriza implementar, cargar pesos,
ejecutar forwards, entrenar, generar, contratar infraestructura ni admitir campaña.
La solicitud de ejecutar N4S tampoco constituye aceptación de la enmienda.

Documento exacto para decidir:
[SETTINGS_AMENDMENT_PROPOSAL.json](../../validation/vsg_2b/n4s/SETTINGS_AMENDMENT_PROPOSAL.json).
Opciones: `ACCEPT_DESIGN_FOR_PLANNING_ONLY`, `REJECT` o `REQUEST_SPECIFIC_CORRECTION`.
La decisión posterior debe identificar el ID/versionado y, preferentemente, el hash
registrado en [N4S_RESULT](../../validation/vsg_2b/N4S_RESULT.json). Ninguna opción se
adopta por defecto. N4 conserva `N4_SCOPE_CHANGE_REQUIRED`.

## Cierre local frente al snapshot publicado

HEAD de entrada: `6c238b24685117c1e9d6442e33a830fbe7606baf`. Se observaron cambios
previos: N4_RESULT modificado y tres documentos N4/N4R sin seguimiento. Se congeló
un inventario nuevo de **760 archivos**, 68.374.293 bytes, incluyendo esos avances.
No se encontraron AGENTS.md aplicables. Ningún archivo previo se reescribe.

El checkout contiene los seis documentos oficiales N4 y el resultado local declara
`N4R_CLOSEOUT_COMPLETE`, con HEAD final concreto. Sus ocho hashes de artefactos
coinciden. En cambio, `git show` del mismo HEAD conserva el resultado anterior con
`PENDING_FINAL_CHECK`; el runbook y la propuesta N4R todavía no pertenecen a ese
snapshot. Esto explica la discrepancia de la spec. Es una verificación de objetos
Git locales: **disponibilidad remota actual UNKNOWN**, sin consulta de main ni claim
de publicación del cierre. No se reconstruyó ningún documento faltante.

Preservación histórica y nueva se distinguen:

- Inventario auténtico N4/N4R de 751 archivos: comparación fresca de sus hashes
  contra los bytes actuales, todos coincidentes. No se inventa un scan pasado.
- Baseline N4S de 760 archivos: control antes/después de esta ejecución, incluyendo
  auditor, propuestas y N4_RESULT local. Resultado detallado en INPUT_MANIFEST/N4S_RESULT.
- `.git`, entornos y caches ignorados no forman parte del inventario de contenidos;
  outputs y validation sí se escanean por separado para counters.

Los 26 activos pequeños de código/config/tokenizer y `sources.json` se revalidaron
por SHA. Se conservan las revisiones de Diffusers
`39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f`, checkpoint
`d6d957f8d27c40889c0d570a616571a5645c8be3`, fp16, y Transformers
`573565e35a5cc68f6cfb6337f5a93753ab16c65b`. Cero descargas nuevas.

La salida textual acreditada distingue contenido de especiales: A tiene 7.305
tokens de contenido / **7.307 con BOS/EOS**; B, 5.686 / **5.688**. Son strings del
ensamblado propuesto, no receipts de un bridge. Se verificaron sus bytes, hashes,
guardas/documentación y las versiones del auditor/activos; no se repitió tokenización.
Se conserva BasicTokenizer lento, `fix_text=None`, dominio ASCII acotado y rechazo
de especiales embebidos. Resampler compartido de 128 slots tras bloques de 75:
cobertura acreditada, comprensión semántica **NOT_RUN**.

## Enmienda mínima y baseline real

La campaña actual sigue `DRY_RUN_ONLY_UNSELECTED_PROVIDER/MODEL`, seed null,
size347×389. No existe beta efectiva ni GLIGEN admitido. **0.3 es el default upstream,
no un setting operacional congelado.** No se fabrica un diff contra otra realidad.

| Variable | Baseline real / referencia | Propuesta revisable |
| --- | --- | --- |
| Beta | Campaña sin valor; default upstream0.3 | 1.0 explícito en A/B candidato;0.3 en control diagnóstico emparejado |
| Fuser | Upstream `enabled=false` devuelve x, retirando attention/FF | Patch externo mantiene attention/FF/S compartidos; ausencia o presencia de R es el tratamiento |
| Steps / CFG / eta | No seleccionados; defaults50/7.5/0 | 50 /7.5 /0 explícitos, ambos configs y ambas ramas |
| Seed | null congelado | Root20261002; source20261003, initial20261004, reinject20261005, propuesta nueva |
| Fuente/máscara | JPEG D y diseño N4; ninguna máscara operacional | M_KEEP1 en64×64, padding512, ningún permiso nuevo de edición |
| Precisión | Pesos base almacenados fp16; ejecución no acreditada | float32 de referencia; fp16 de cómputo solo tras decisión y réplica posterior |
| Texto | JSONL A / array B y common congelados | Mismo mecanismo N4; negativo vacío compartido, sin B textual ni A parseada para generar R |
| Modelo | Placeholder operacional; base de diseño fijada | Mismo artefacto compuesto en A/B; módulos nuevos/pesos todavía inexistentes |

Se distinguen **dos cambios**: setting de inferencia y patch del modelo. Cambiar
beta no implementa neutralización, resampler, asociación visual ni aprendizaje de R.

El control `VSG-2B-GLIGEN-M1-B030-CONTROL@0.1.0` y el candidato
`VSG-2B-GLIGEN-M1-B100-CANDIDATE@0.1.0` usan exactamente el mismo patch futuro,
pesos, texto, fuente, RNG, scheduler y transformaciones compartidas. Solo cambia
beta entre esas dos configuraciones. El control no representa una ejecución histórica
del upstream sin patch y no sirve como evidencia positiva del piloto.

Dentro de cada configuración, A recibe common más JSONL exacto por texto y R vacío;
B recibe common por texto y sus diez registros por el puerto tipado aprendido.
S contiene las mismas cinco asociaciones fuente observadas. La ruta neutral es
`F(x,S)`; B activo usa `F(x,concat(S,R))`. R ausente no se representa con keys cero
que alteren el softmax. CFG negativo no recibe R en ninguna rama. Common conserva
sus relaciones redundantes: el ensayo mide el aporte incremental del canal.

Fuente intacta de entrada: SHA
`282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
Payloads: SHA
`7b995c02541b831524236cf36c9e8e834a8ddbcaea43da6a1f6669918f8a586d`.
Dos edges, tres locks VALIDATE_ONLY, cinco topology, mismo common A/B. Sin alterar
P0/PR0/PR1, D/E/Kenny/C, schemas, allowlists, CGC ni PROPOSED_SCOPE.diff.

Las regiones/etiquetas existentes sirven para asociación compartida; no son boxes
de edición. Padding de borde L82/T61/R83/B62 conserva el contenido347×389 sin resize;
normalizar a[-1,1], formar latente fuente con escala0.18215 y9 canales4+4+1. Al final
retirar solo padding, sin pegar píxeles fuente sobre el resultado. M1 reinyecta
latentes: **no promete preservación exacta de píxeles**.

El futuro adapter usará `latent_dist.sample(generator_source)`, ruido inicial de
cuatro canales con `generator_initial` y una cinta de ruido fuente por índice de
loop con `generator_reinject`, incluidos timesteps repetidos. Reusará los tensores
en A/B y restaurará estados globales CPU/CUDA/Python, eval/dropout0. PNDM fresco por
rama: timesteps, ets, counter, cur_sample y cur_model_output reiniciados. Es diseño;
no se generó ni muestreó ningún tensor de modelo en N4S.

## Fundamento temporal y límites

Se revisó código fijado y la evidencia simbólica persistida, sin ejecutar modelos.
Con M1, la mezcla antes del UNet reemplaza el latente espacial anterior por fuente
ruidosa común. PNDM aún transmite predicciones previas: conserva hasta cuatro valores
epsilon y usa cur_sample en counter1; esa excepción se limpia posteriormente.

Con50 pasos, skip_prk_steps=true y offset1 hay51 llamadas. Beta0.3 activa R en0–14;
la memoria puede conservar dependencia en15–17; desde18 hasta50 desaparece, bajo
RNG idéntico y eval sin estado oculto. Esto es B frente a ablación/mutación con texto
B fijo. Una diferencia textual A/B durante todo el loop no acredita el canal B.

Beta1 mantiene R hasta50. El último UNet/PNDM puede afectar el latente que se decodifica
sin reinyección posterior. Decode, safety y postprocess no resucitan una dependencia
anteriormente borrada. La ruta posible puede cancelarse o quedar por debajo de la
cuantización, ser semánticamente inútil o producir pérdidas protegidas. Un gate
aprendido nulo, copia final de fuente o salida bloqueada por safety no pasa el ensayo.

Fuentes revalidadas, hashes en INPUT_MANIFEST:
[pipeline](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py),
[PNDM](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/schedulers/scheduling_pndm.py),
[fuser](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/models/attention.py).
No se presenta esta revisión del mismo agente como una evaluación independiente.

## Pruebas posteriores, recursos y rechazo

Las ocho pruebas del JSON están **NOT_RUN**, cada una con prerrequisitos, observable,
éxito/fallo y presupuesto propuesto. Incluyen control negativo, beta explícito,
neutralización/ablación, mutación aislada, persistencia hasta decode, réplica,
evaluación semántica/preservación y validación de texto/input.

Cada test de trayectorias propone hasta dos, con51 llamadas UNet cada una; algunos
permitirían hasta dos decodes, sujetos a autorización separada. Son techos de diseño,
no cuota aprobada. Llamadas auxiliares, tiempo/costo total y consolidación de pruebas
con receipts compartidos deben presupuestarse antes de ejecutar. El preflight de200
llamadas sugerido en N4R no cubre automáticamente el conjunto: solo CLIP sin batching
para A/B/negativo/cinco etiquetas puede requerir180 llamadas, además de resampler,
VAE, proyectores y trayectorias. No se añade capacidad implícita.

Réplica propuesta: fp32 atol1e-6/rtol1e-5; fp16, si se selecciona después,
atol1e-3/rtol1e-3. No ensanchar tras resultados. Una mutación válida aislada sigue
siendo una contradicción de D congelado y debe ser rechazada por hashes de campaña.
Sensibilidad numérica no sustituye lectura literal, identidad y relaciones correctas.
Umbral de utilidad semántica a escala de corpus UNKNOWN: requiere corpus/licencias,
métrica, tamaño muestral y revisión independiente antes de mirar outputs.

Se separan cuatro decisiones: aceptar diseño; autorizar implementación; autorizar
carga/sonda con pesos; autorizar campaña visual. Datos, entrenamiento e infraestructura
requieren además presupuestos explícitos. Pesos base publicados:3.159.269.896 bytes;
no se descargaron ni verificaron sus bytes. Pesos nuevos, GPU-h, costo, ingeniería
y tamaño final de corpus UNKNOWN. No se convierten los rangos N3 en mediciones.

Política vigente: ocho intentos, incluidos fallos. Forwards aislados siguen
UNCLASSIFIED_NOT_EXEMPT. Propuesta posterior: contabilizar cada frontera aprendida
(CLIP, VAE, resampler, proyectores, UNet, safety), registrar hooks internos sin
doble contabilidad y contar un fuser directo como llamada si se ejecuta aisladamente.
Cada generación mantiene su attempt antes del despacho. El presupuesto y clasificación
de diagnósticos deben resolverse antes; no se inventa una campaña exenta alternativa.
Logs append-only, reserva previa, STOP por límite, mismatch, no determinismo o
cancelación; cero retry implícito. Todos los permisos/cupos actuales de N4S son0.

## Activación futura y rollback

Después de las autorizaciones separadas, el plan podrá definir configuración
inmutable por ID/version/hash, patch y pesos estrictamente verificados, delta review
y eventual manifest nuevo/admisión. Ningún archivo operativo cambia ahora.

Antes de aplicar nada, rechazo/retiro se registra en un nuevo documento y continúa
DRY_RUN_ONLY. Si en el futuro se activa el candidato, rollback desactiva su ID/version
y solo restablece una configuración anterior identificada y autorizada. Actualmente
no existe backend operacional anterior: volver significa **sin backend/BLOCKED**.
El beta0.3 diagnóstico no se vuelve READY. Nunca borrar intentos o resultados, resetear
counters ni contar receipts previos como nuevos pares positivos.

Verificaciones finales y hashes en [N4S_RESULT](../../validation/vsg_2b/N4S_RESULT.json)
y [INPUT_MANIFEST](../../validation/vsg_2b/n4s/INPUT_MANIFEST.json). Archive/predicciones/
imágenes/pares=0/0/0/0, forwards/train/tokenizaciones/descargas nuevas=0. Se observan
15 reportes sin imágenes y0 attempts/evaluaciones; cuenta remota UNKNOWN, no consultada.
Plan Limits5-hour/Weekly UNKNOWN, sin certificación porcentual del techo40 puntos.

N3_MODEL_DEVELOPMENT_REQUIRED; N4_SCOPE_CHANGE_REQUIRED; VSG-2B BLOCKED/PENDING_VISUAL;
producción/provider_READY=false. C permanece NO_GO_C0_UNVERIFIED y X1 sin aprobar.
Sin commit, push, branch ni ZIP. El siguiente paso concreto es decidir esta enmienda;
si se acepta, preparar el plan acotado, sin ejecutar su implementación por defecto.

[Dos recomendaciones con prompts para ChatGPT Work mode](N4S_WORK_MODE_NEXT_STEPS.md).
