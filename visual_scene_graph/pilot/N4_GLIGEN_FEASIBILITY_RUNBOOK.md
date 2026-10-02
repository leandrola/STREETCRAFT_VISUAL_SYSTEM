# VSG-2B / N4 · Cierre completado mediante N4R

**Viabilidad: `N4_SCOPE_CHANGE_REQUIRED`. Confianza: `STATIC_ONLY`.**

N4R completa los seis documentos que faltaban; no acredita un N4 exitoso anterior.
El auditor ya estaba publicado en HEAD `1ef2e344c71d446a508d94e2813b4f4bdb30ee90`.
El checkout estaba limpio y tenía 751 archivos previos, incluido ese auditor, que
se conserva intacto. El estado N3 continúa `N3_MODEL_DEVELOPMENT_REQUIRED`.

1. **Texto decidido:** bloques CLIP de 75 tokens y resampler aprendido compartido
   de 128 slots. Conteos acreditados para el dominio ASCII observado; semántica
   del condicionador sin validar.
2. **Fuente/máscara:** padding sin recorte de contenido y asociación observada de
   cinco IDs definidos. La máscara de reinyección total con schedule por defecto
   queda descartada para medir el aporte visual del canal B.
3. **A/B decidido como diseño:** mismo modelo compuesto, transformaciones visuales
   compartidas, canal relacional ausente en A y presente en B; cambios externos
   de código y settings pendientes, sin aplicar.
4. **Observable:** la variante por defecto borra el efecto estructural temprano.
   Mantener el canal hasta el final tiene una ruta estática no anulada, pero exige
   decidir expresamente la enmienda de settings. No hay observación con pesos.
5. **Antes de desarrollar:** resolver esa enmienda, fijar patch/entorno, corpus y
   derechos, pesos nuevos, protocolo de forwards y presupuesto. No hay GO a
   entrenamiento, generación ni admisión.

## Evidencia recuperada y límites

Se leyeron N4, N4R, los cinco artefactos N3, contrato vigente N2/P1R, D real y
política/harness. No se encontraron AGENTS.md aplicables ni documentos N4 de cierre
previos. Se conservó el progreso local: activos pequeños, ledger de descargas y
output de tokenización, seguido de una ejecución fresca y focalizada de controles.

La ejecución inicial N4 partió de HEAD `911b406db32f909ae57f1f01b5211b0366d8b07b`
y 750 archivos. El usuario publicó el auditor durante el trabajo; N4R vuelve a
congelar el estado actual. No se atribuye ese commit al agente ni se fuerza HEAD
al valor histórico. No se hace commit, push, branch ni ZIP.

Payload D SHA-256:
`7b995c02541b831524236cf36c9e8e834a8ddbcaea43da6a1f6669918f8a586d`.
Fuente SHA-256:
`282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
Se verificaron bytes y registros: dos edges, tres locks VALIDATE_ONLY y cinco
topology; A JSONL equivale a B y common es idéntico. N3 y su mapa coinciden.

El [manifest de entrada](../../validation/vsg_2b/n4/INPUT_MANIFEST.json) fija todos
los archivos previos, fuentes primarias, licencias, tamaños, hashes, specs y lista
de creación. Los hashes de pesos de N3 siguen siendo declaraciones remotas.

## Texto completo: mecanismo elegido

El harness conserva `common` como objeto, A como JSONL y B como array; todavía no
existe un bridge GLIGEN. Se mide este ensamblado **propuesto**, sin cambiar payloads:

```text
C = json.dumps(common, sort_keys=True, separators=(',', ':'),
               ensure_ascii=False, allow_nan=False)
prompt_A = C + '\n' + A.relations_and_locks  # JSONL exacto, sin recodificar
prompt_B = C                               # B entra por puerto tipado separado
negative_prompt = ''                       # misma propuesta en ambas ramas
```

| String | Tokens de contenido | Con BOS/EOS | Bloques de 75 |
| --- | ---: | ---: | ---: |
| common / prompt B | 5.686 | 5.688 | 76 |
| JSONL A completo | 1.619 | 1.621 | 22 |
| prompt A ensamblado | 7.305 | 7.307 | 98 |
| negativo vacío | 0 | 2 | 1 |

Se miden también ambos componentes de common y las cinco etiquetas observadas;
los componentes son diagnósticos y no se codifican dos veces. Las etiquetas
compartidas tienen entre 6 y 13 tokens contando especiales. Bytes, caracteres,
strings completos, SHA-256, hash de secuencia de IDs, overflow y controles están en
[TEXT_CAPACITY_AUDIT](../../validation/vsg_2b/n4/TEXT_CAPACITY_AUDIT.json).

Tokenizer: activos del checkpoint fijado; implementación de Transformers v4.41.2,
commit `573565e35a5cc68f6cfb6337f5a93753ab16c65b`. Se selecciona explícitamente el
camino lento `fix_text=None`, BasicTokenizer sin separación de puntuación ni
eliminación de acentos. Instalar ftfy o elegir un tokenizer fast no conserva por sí
solo esa elección: la implementación futura debe fijarla y verificarla.

El auditor extrae funciones de tokenización por AST, sin importar modelos. Para
ASCII, `\p{L}` equivale a A–Z/a–z y `\p{N}` a 0–9; se comprueba ese dominio en
todos los strings. Una segunda ruta de scanner/BPE concuerda en todas las secuencias
y ocho controles. Hay rechazos explícitos de Unicode, NUL y especiales embebidos,
y una comprobación conocida de IDs para `hello world!`. Esto acredita estos inputs,
no cualquier CLIPTokenizer/configuración. Los bytes congelados no se normalizaron
para superar las guardas. El tokenizer sí aplica su lowercasing normal.

**Diseño seleccionado:** tokenizar íntegramente; dividir IDs en bloques contiguos
de hasta 75; añadir BOS/EOS, pad EOS hasta77, mask de padding y posiciones locales
0..76. Codificar cada bloque con CLIP congelado; retener cada posición de contenido
una vez. Para texto vacío usar el estado EOS. Añadir embedding aprendido del índice
de bloque y consultar todos los estados válidos con un resampler de cuatro bloques,
ocho heads, dimensión768, FF3072 y 128 queries aprendidas. La misma ruta/pesos procesa
A, B y negativo. Salida `[batch,128,768]`, referencia float32; fp16 sujeto a réplica.

Techo propuesto: 128 bloques, 9.600 tokens de contenido. Exceso o dominio no soportado
se rechaza **antes** del encoder. Nunca truncar, resumir campos ni serializar B.
El orden de chunks es explícito; su comprensión sigue siendo una propiedad a probar.

La salida va a `attn2` de los bloques down/mid/up del UNet, cuya longitud de keys es
dinámica. No se envía al `position_net` de cajas. Las etiquetas comunes siguen una
ruta compartida CLIP pooled para asociar nodos. No se activa ningún condicionador
opcional que el checkpoint no configure. El patch futuro usa embeddings positivos
y negativos de igual shape y evita el truncado de `encode_prompt`.

Alternativa descartada en este hito: concatenar todos los embeddings directamente
en la atención variable del UNet. Necesita resolver orden global, también requiere
validación semántica y aumenta memoria en cada bloque. El resampler acota el contexto
del UNet; **no es semánticamente sin pérdida**. Conservar IDs o hashes solo demuestra
cobertura de entrada. El entrenamiento y las pruebas de semántica quedan NOT_RUN.

Memoria calculada, no medida: para CFG batch2, ocho heads, queries espaciales4096,
fp16, un score denso de cross-attention cuesta `2*8*4096*L*2` bytes: aproximadamente
913 MiB con L7305 y 16 MiB con L128. El resampler con queries128 y L7305 requiere
unos28,5 MiB de scores por capa. SDPA puede evitar materializarlos; no se estima el
pico del modelo, entrenamiento ni fuser visual a partir de estas cifras. Fórmulas
y supuestos exactos están en el JSON.

Prerregistro semántico propuesto: corpus independiente por escena, excluyendo
D/E/Kenny/C de entrenamiento/tuning; relaciones y campos en chunks iniciales,
centrales y finales; controles de negación, literal, endpoints y orden. Readout
diagnóstico separado con objetivos propuestos de QA relacional ≥95%, recall de
campos ≥99% y literal protegido100% en ≥1.000 ejemplos. No son resultados ni
sustituyen la rúbrica visual congelada. La suficiencia del corpus está por validar.

## Fuente, máscara y dependencia temporal

D es JPEG RGB de 347×389, sin orientación EXIF. Se elige preservar sus píxeles en
el canvas mediante padding por replicación de borde a512×512: izquierda82/derecha83,
arriba61/abajo62. Sin resize ni interpolación. Normalización propuesta `pixel/127.5-1`.
Al terminar se elimina **solo** el padding, recuperando347×389; no se copia la fuente
sobre el resultado. La identidad después de VAE/difusión está NOT_RUN.

Los cinco IDs se vinculan por etiquetas, `evidence.region`, evidence_id y source
reference_id ya presentes en common. La tabla completa y coordenadas transformadas
están en [SOURCE_CONDITIONING_DECISION](../../validation/vsg_2b/n4/SOURCE_CONDITIONING_DECISION.json).
La asociación propuesta combina ROI pooling del latente fuente común, etiqueta
CLIP y coordenadas en un proyector compartido. No se obtienen etiquetas del nombre
del ID, no se inventan boxes y las regiones aproximadas no se vuelven segmentación.
`x'=(347*x+82)/512`, `y'=(389*y+61)/512`; se verificó inversa racional de cada región.

La autoridad vigente es de preservación: `/sc-core /sc-lock`, transform/remove/infer
vacíos, fuente y literal protegidos. Permite diseñar asociación/reconstrucción
conservadora, no autoriza nuevas ediciones ni generación ahora. Locks VALIDATE_ONLY
y estados textuales MASK_GRAPHIC_ONLY no son máscaras de edición.

La máscara evaluada es `M_KEEP=1` en64×64 posiciones latentes, igual en A/B, sin
derivarla del grafo. Convención real: 1 reinyecta fuente con ruido y conserva latente
fuente en los canales auxiliares; 0 permite continuar el latente generado y anula
ese condicionamiento fuente. Son nueve canales: cuatro de estado ruidoso, cuatro
de `z_source*M`, uno de M. No son nueve canales de píxeles protegidos.

```text
s_i = add_noise(z_source, epsilon_source[i], t_i)
l_i = M*s_i + (1-M)*z_i
e_i = UNet(concat(l_i, z_source*M, M), t_i, text, shared_objs, R_i)
z_(i+1) = PNDM.step(e_i, t_i, l_i; ets, counter, cur_sample)
final = unpad(postprocess(safety_check(VAE.decode(z_final))))
```

Con M1, `l_i=s_i`: cada paso borra la recurrencia espacial del latente anterior.
**No basta mirar un paso**, porque PNDM conserva hasta cuatro predicciones y usa
`cur_sample` en su arranque especial. Config fijada: skip_prk_steps=true, offset1,
leading spacing. Los defaults upstream de50 pasos y beta0.3 producen51 llamadas;
el canal está activo en índices0–14. La memoria PLMS aún puede transmitir influencia
en15–17; desde18 se vació. El índice final50 no depende del canal B temprano, bajo
los supuestos de igualdad y modelo sin estado declarados.

Esto se comprobó con propagación simbólica de conjuntos, **sin UNet ni pesos**.
Se contemplan la excepción counter1, memoria PLMS y barridos de10/20/30/50/100 pasos.
El control con beta1 conserva una ruta final posible; el control M0 también, pero
M0 abre toda la imagen y carece de autoridad. Dependencia posible no es efecto medido.

La conclusión es B versus su ablación/mutación con texto B fijo. A puede diferir
de B por su texto durante todo el loop: esa diferencia no acredita aporte del canal
estructural. Decode, safety y postprocess no reciben R y no pueden recuperar una
dependencia ya borrada. Tampoco M1 garantiza que la reconstrucción sea idéntica a
la fotografía. Copiar píxeles finales de fuente haría el ensayo degenerado.

**Decisión:** descartar M1+beta0.3 para el observable original del canal B. Proponer
M1+beta1, igual en A/B, requiere una decisión explícita de settings. El manifest
actual no tiene un schedule operativo: beta0.3 es un default del código analizado,
no un valor congelado de campaña. No se adopta silenciosamente ninguno de los dos.
La [enmienda separada](N4R_SETTINGS_AMENDMENT_PROPOSAL.md) no está aprobada ni aplicada.

Con beta1 existe una arista computacional hasta la última predicción y PNDM final,
pero puede ser débil, cancelarse, quedar fuera de lo perceptible o ser semánticamente
incorrecta. Safety puede bloquear resultados y la cuantización puede borrar cambios
pequeños; ambas situaciones impiden acreditar una comparación útil. Se debe observar
el operador real, latente final, píxeles decodificados y criterios visuales
independientes. Un residuo del decode no es ventaja relacional.

## Control A/B y RNG

Sea S el conjunto común de cinco tokens fuente y R los siete tokens relacionales
aprendidos de B. Para A y ablación usar ausencia de R, no vectores cero con keys
todavía presentes. Mantener la transformación compartida:

```text
F(x,O):
  u = x + tanh(alpha_attn)*Attn(LN1(concat(x,Linear(O))))[:n_visual]
  return u + tanh(alpha_dense)*FF(LN2(u))
A: F(x,S)
B: F(x,concat(S,R)) si el schedule relacional está activo; F(x,S) si no
```

Ambas ramas cargan el mismo checkpoint compuesto completo. El patch externo futuro
mantendrá visual attention, S y FF en ambas; no ejecutará `enabled=false` solo para
A. La presencia de R tiene un schedule explícito. Esto cambia simétricamente la
semántica upstream de apagado y queda declarado como adaptación versionada pendiente.
El CFG negativo no recibe R en ninguna rama; S es común. No hay baseline con otro
modelo, resampler exclusivo de A ni parsing generativo del JSONL.

El mismo seed nominal no basta. Propuesta: muestrear el posterior VAE una vez con
generator_source; generar ruido inicial de cuatro canales con generator_initial;
precomputar ruido fuente por **índice de loop**, incluyendo timestep repetido, con
generator_reinject. Reusar exactamente esos tensores en ambas ramas; restaurar
estados CPU/CUDA/Python y desactivar dropout. Reiniciar PNDM completo por rama.

El código upstream tiene draws sin generator en VAE, sustitución de latentes9→4 y
ruido de fuente por paso. Deben sustituirse explícitamente en el patch futuro,
igual para ambas ramas. El seed congelado sigue null y no se ejecuta ningún draw
de modelo aquí. La matriz completa y siete pruebas futuras NOT_RUN están en
[AB_CONTROL_MATRIX](../../validation/vsg_2b/n4/AB_CONTROL_MATRIX.json).

## Desarrollo, recursos y protocolo futuro

Módulos nuevos: resampler ordenado; proyector visual de nodos comunes; proyector
relacional/predicados; deltas versionadas del fuser; pipeline externo para texto,
fuente, RNG y schedule; ledger/validator y hooks. CLIP/VAE/UNet base congelados,
mismas deltas aprendidas en A/B. No se implementan ni entrenan en N4R.

| Módulo/etapa | Esfuerzo y evidencia |
| --- | --- |
| Decisión de settings/autoridad | Pendiente; no estimar duración de aprobación |
| Condicionador textual | Ingeniería y entrenamiento UNKNOWN;4 bloques/128slots es diseño, no benchmark |
| Fuente/ROI/RNG y control del fuser | Ingeniería UNKNOWN; cambios concretos arriba, sin entorno de ejecución |
| Proyector relacional y deltas | Ingeniería/volumen de datos/GPU-h UNKNOWN; sin corpus ni curva de aprendizaje |
| Validación de carga y temporal | Duración UNKNOWN; medir memoria/latencia antes de reservar entrenamiento |
| Datos/derechos | No adquiridos; permisos por imagen/anotación, split por escena, exclusión D/E/Kenny/C |

Los rangos N3 de5k–20k pares,50–200 GPU-h,25–59 días-persona y24–48 GiB GPU no son
requisitos medidos y no se revalidan aquí. Se retiran como estimación suficiente de
esta arquitectura: el resampler y proyector común amplían los módulos. Solo conserva
fundamento aritmético el cálculo de almacenamiento condicionado a cantidad/tamaño
de imágenes, sin certificar que ese corpus sea adecuado.

Descargas futuras: cuatro pesos fp16 fijados en BASE_MANIFEST N3,
3.159.269.896 bytes declarados remotamente; pesos nuevos de los módulos entrenados,
tamaño final UNKNOWN; entorno y sus wheels, tamaño UNKNOWN. Ningún peso descargado.
Verificar SHA locales, carga estricta, clases explícitas, configs y licencias antes
de cualquier forward. Apache-2.0 del código no sustituye CreativeML OpenRAIL-M del
checkpoint ni derechos de datos.

Entorno reproducible **propuesto como requisito, no lock validado**: Linux/CUDA
con digest inmutable, Python/PyTorch/CUDA/Pillow/libjpeg fijados en un lock futuro;
Diffusers commit fijado, Transformers4.41.2 commit fijado y tokenizer BasicTokenizer
explícito, sin ftfy implícito. Versiones/binarios compatibles de hardware y librerías
restantes UNKNOWN; deben resolverse en hito de recursos sin inventar compatibilidad.
Registrar deterministic flags, attention processor, dtype, GPU/driver y hashes.
Costo total UNKNOWN: horas medidas/aprobadas × tarifa cotizada + datos + storage.

Política vigente: ocho intentos de campaña; harness guarda attempt antes de llamar
al generador, incluso si falla. Forwards locales aislados con pesos siguen
**UNCLASSIFIED_NOT_EXEMPT**. Esta propuesta no los reclasifica.

Protocolo posterior para decisión, no aplicado: una unidad por llamada a módulo
aprendido (CLIP/VAE/proyectores/UNet/safety), con contador por clase y wall/GPU time;
una generación sigue consumiendo además un intento original antes de iniciarse.
No descontar forwards de los ocho intentos ni declararlos exentos por ser locales.
Entrenamiento se cuenta por pasos, muestras y GPU-h; se propone techo0 hasta permiso
separado. Primer preflight con pesos, si se autoriza: techo200 llamadas aprendidas,
10 minutos wall, sin train ni decode/generación; incluir chunks CLIP en el cómputo,
planificarlo antes de lanzar y parar si no cabe. Hoy techo autorizado0. No retries
automáticos; reservar unidades antes de cada llamada, log append-only de input,
pesos, RNG, módulo, tiempos, memoria, output/error. STOP al límite, fallo de hash,
input no admitido, no determinismo o cancelación del usuario. Importes/techo GPU-h
de entrenamiento y generación requieren propuesta posterior, no aprobados aquí.

## Reproducibilidad y comprobaciones

El manifest incorpora íntegramente `sources.json`, sus URLs inmutables y SHA.
Los activos pequeños ya existentes se verificaron. N4 descargó1.986.531 bytes nuevos;
N4R descargó0. Historial de adquisición N3 no reconstruido. Límite de nuevos activos
N4:10.000.000 bytes. No wheels, paquetes ni pesos instalados.

Para reejecutar con los caches verificados:

```sh
python3 validation/vsg_2b/n4/closeout_checks.py --repo . --assets /tmp/vsg_n4 --output /tmp/n4r-recheck.json
```

En otro entorno, reconstruir caches únicamente desde
`INPUT_MANIFEST.source_manifest.contents`: por cada entrada, GET de su URL fijada,
comprobar tamaño y SHA antes de guardar en `local_path`; si ya existe con otro hash,
parar. Sumar bytes nuevos y parar antes de10MB. Serializar esa lista con indent2 y
newline como `/tmp/vsg_n4/sources.json`; su SHA debe coincidir. No usar URLs latest
ni descargar componentes adicionales. El auditor y wrapper no hacen red.

`closeout_checks.py` reusa sin modificar el auditor publicado, incorpora controles
de dependencia PLMS y coordenadas, y corrige solo la contabilización descriptiva:
41 invocaciones exitosas entre ambas rutas y3 rechazos de guarda por ejecución
(el auditor anterior omitía su assert extra de IDs conocidos). No es consumidor
simulado ni sonda causal. Los resultados íntegros están en los tres JSON temáticos.

El resultado registra los exit codes, incluidos errores exploratorios corregidos;
no se repiten suites globales. Verificación final: hashes de todos los archivos
previos, única lista permitida de nuevos, JSON/referencias/consistencia, counters y
whitespace. El marcador `N4R_CLOSEOUT_COMPLETE` se fija solo al completar estos checks;
no significa `ARCHITECTURE_FEASIBLE`.

Plan Limits por tramo: 5-hour/Weekly UNKNOWN. Techo heredado40 puntos, reparto
N4R4/10/12/8/6; sin certificación porcentual ni cambio del modelo del usuario.
Archive / predicciones / imágenes / pares nuevos =0/0/0/0. Forwards y train=0.
Historial de cuenta de proveedor UNKNOWN, no consultado. VSG-2B sigue
BLOCKED / PENDING_VISUAL, producción/provider_READY=false; C y X1 intactos.

## Fuentes primarias y entregables

- [Pipeline fijado](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py): texto, máscara, source RNG, loop y salida.
- [PNDM fijado](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/schedulers/scheduling_pndm.py): timesteps, counter1, memoria PLMS y actualización final.
- [Attention/fuser](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/models/attention.py) y [processor](https://github.com/huggingface/diffusers/blob/39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f/src/diffusers/models/attention_processor.py): transformaciones compartidas y keys de longitud variable.
- [Tokenizer fijado](https://github.com/huggingface/transformers/blob/573565e35a5cc68f6cfb6337f5a93753ab16c65b/src/transformers/models/clip/tokenization_clip.py): reglas y fallback realmente seleccionado.
- [Resultado](../../validation/vsg_2b/N4_RESULT.json), [texto](../../validation/vsg_2b/n4/TEXT_CAPACITY_AUDIT.json), [fuente](../../validation/vsg_2b/n4/SOURCE_CONDITIONING_DECISION.json), [matriz](../../validation/vsg_2b/n4/AB_CONTROL_MATRIX.json), [inputs](../../validation/vsg_2b/n4/INPUT_MANIFEST.json).
- [Enmienda no aprobada](N4R_SETTINGS_AMENDMENT_PROPOSAL.md) y [dos recomendaciones para ChatGPT Work mode](N4R_WORK_MODE_NEXT_STEPS.md).
