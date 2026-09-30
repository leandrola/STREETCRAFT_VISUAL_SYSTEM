# VSG-2B · decisión de alcance y evaluación de interfaz tipada

2026-09-30 · **ORIGINAL_SCOPE_RETAINED / NO_COMPATIBLE_BACKEND_VERIFIED**.

La instrucción posterior del usuario resuelve la decisión pendiente de P1R:
mantener el experimento original, conservar B como estructura tipada y no autorizar
predicciones. **No se aplica `PROPOSED_SCOPE.diff` ni se admite un manifest
operacional `TEXT_SERIALIZED_AB`.** El diff queda como propuesta histórica
descartada para esta campaña. P1R conserva su carácter de estudio de factibilidad.

Esta decisión prevalece sobre la pregunta pendiente y los pasos condicionales de
[P1R_RUNBOOK.md](P1R_RUNBOOK.md). Ese documento, su resultado y sus solicitudes no
enviadas se conservan sin reescribirlos. No constituyen autorización vigente para
implementar el bridge de Replicate, admitir D operacional ni generar imágenes.

## Alcance que continúa vigente

Se mantiene la política 1.0.0: selección D/E/Kenny/C, cuatro pares distintos como
mínimo, ocho intentos como máximo y los cinco fenómenos obligatorios. C sigue
bloqueado; F no lo sustituye. Continúan preconditions, admisión por hash, revisión
del delta, seed controlado, S3/UNKNOWN, no regresión y STOP. Los manifests existentes
siguen en DRY_RUN_ONLY. Estado: **BLOCKED / PENDING_VISUAL**;
`production_authorized=false`. Esta revisión no cambia código, schemas, allowlist,
política, manifests ni evidencia de G0/P1/P1R.

## Interfaz evaluada contra D real

Entrada: `validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f`.
B contiene diez registros, cada uno con `id`, `priority`, `value`, `lock_ids`:
dos relaciones (`LEFT_OF`, `ABOVE`), tres locks y cinco registros de topología.
A contiene exactamente los mismos registros y orden en un string JSONL;
`common` es idéntico. No alcanza con aceptar dos triples espaciales.

| Candidato inspeccionado | Interfaz comprobada documentalmente | Evaluación para VSG-2B |
| --- | --- | --- |
| sg2im, `Sg2ImModel` | `objs: LongTensor[O]`, `triples: LongTensor[T,3]`; con convolución de grafo habilitada, los extremos y predicados participan del cálculo de features y layout | Consume relaciones estructuradas, pero la interfaz inspeccionada no ofrece edición con el JPEG fuente, rama A textual ni el contrato completo de locks/prioridades/provenance. No es un backend admisible sin desarrollo y evaluación adicionales. |
| GLIGEN, Diffusers v0.29.0 | `gligen_phrases: List[str]`, `gligen_boxes: List[List[float]]`, `gligen_inpaint_image: PIL.Image.Image` | Ofrece controles espaciales tipados e imagen fuente, pero no recibe los registros de relaciones/locks de B. Convertir evidencia regional en cajas de intervención no demuestra equivalencia. |
| ComfyUI, nodos personalizados | Un puerto con un nombre de tipo propio puede transportar un objeto Python entre nodos | Es una opción de transporte para un futuro consumidor. La etiqueta de tipo no valida por sí sola los diez registros ni demuestra que el generador los use. No se identificó aquí un consumidor completo. |

Fuentes primarias consultadas el 2026-09-30:
[sg2im/model.py](https://github.com/google/sg2im/blob/master/sg2im/model.py),
[GLIGEN v0.29.0](https://huggingface.co/docs/diffusers/v0.29.0/en/api/pipelines/stable_diffusion/gligen),
[ComfyUI custom datatypes](https://docs.comfy.org/custom-nodes/backend/more_on_inputs#custom-datatypes).
Son inspecciones de documentación/código público, sin instalación, descarga de
pesos ni ejecución. La revisión de GLIGEN corresponde a esa versión específica;
el enlace de sg2im a master no constituye un pin operacional.

En sg2im la ruta JSON convierte categorías y predicados mediante vocabularios y
añade un nodo de imagen con relaciones auxiliares. Su modo sin convolución de grafo
no acredita consumo de aristas por esa convolución. Estas transformaciones y la
cobertura de vocabulario exigirían revisión explícita. El análisis de los candidatos
es acotado: no demuestra que no exista otro backend compatible.

## Contrato de interfaz recomendado para continuar la evaluación

Diseño de frontera, **no implementado ni admitido**. Mantener el envelope actual del
bridge (`source_base64`, `payload`, `provider`, `model`, `seed`, `parameters`). El
tipo se aplica a `payload.relations_and_locks`, conservando los nombres actuales:

```text
A.relations_and_locks: string
B.relations_and_locks: array<EdgeRecord | LockRecord | TopologyRecord>

Record = {id, priority, value, lock_ids: array<string>}
EdgeRecord.value = objeto de relación del contrato congelado
LockRecord.value = objeto de lock del contrato congelado
TopologyRecord.value = array<string> de IDs de relaciones
```

El discriminante puede validarse mediante el prefijo existente de `id`; no hace
falta agregar información a una rama. Los valores anidados deben validarse contra
los tipos, enums y referencias del contrato original, sin convertir objetos a
strings, aceptar un `Any` opaco como prueba de tipado, eliminar campos ni inventar
defaults. La igualdad con el contrato congelado sigue siendo obligatoria.

| Datos de D | Obligación del consumidor/adaptador evaluado |
| --- | --- |
| Dos `edge:*` | Preservar extremos, tipo, prioridad, protection, confidence, epistemic_class, evidence y referencias a locks. Identificar el código que consume extremos/predicados estructurados. |
| Tres `lock:*` | Conservar target, type, expected, provenance, strength y `enforcement=VALIDATE_ONLY`, incluido `TERMINAL DINER`. No transformar VALIDATE_ONLY en edición forzada, máscara ni garantía de obediencia visual. |
| Cinco `topology:*` | Mantener IDs, relaciones asociadas, orden, prioridades y listas vacías; no eliminar nodos por carecer de aristas. |
| `common` y fuente | Misma información íntegra y mismos bytes fuente para A/B. No agregar restricciones, extraer nueva geometría ni introducir instrucciones ocultas. |

JSON como transporte es compatible con un campo array: el servidor debe decodificar
ese campo a objetos tipados y mantenerlos hasta un consumidor estructural real.
Un nodo `VSG_CONSTRAINTS` sería una posible implementación futura de transporte;
si luego hace `json.dumps(records)` y envía todo a `prompt`, vuelve a ser
TEXT_SERIALIZED_AB y queda fuera del gate original. Guardar registros solo como
metadata tampoco acredita que condicionen la generación.

Antes de considerar un proveedor compatible deben quedar demostrados, sin generar:

1. Schema de entrada y validación en runtime de las dos ramas; rechazo de tipos
   incorrectos, referencias inválidas y campos no soportados, sin coerción silenciosa.
2. Trazabilidad por registro/campo hasta el consumidor: qué condiciona al modelo,
   qué se usa para validación y qué conserva provenance. No exigir que VALIDATE_ONLY
   se convierta en control generativo ni contabilizar metadata como condicionamiento.
3. Rama A textual y rama B estructurada dentro del mismo backend/modelo fijado,
   con common/fuente/settings iguales. Parsear A y normalizar ambas ramas al mismo
   input antes de la frontera experimental elimina el tratamiento; usar modelos
   diferentes introduce otro cambio y tampoco acredita el experimento original.
4. Capacidad íntegra sin truncado, fuente original, seed y parámetros soportados;
   versiones verificables del modelo, consumidor, vocabulario y transformaciones.
   Un recibo local o schema válido no prueba obediencia visual ni pin remoto.

Una sonda futura puede validar el envelope y registrar los objetos justo antes del
consumidor con la generación deshabilitada. Debe indicar consumo simulado cuando
corresponda; un mock no demuestra soporte del backend real. No se crea esa sonda ni
se cambia la frontera experimental en esta revisión documental.

## Replicate como eventual experimento separado

Si se solicita más adelante, definir otro ID de experimento, contrato textual,
presupuesto, manifiestos y carpeta de evidencia independientes. Sus resultados
serían exploratorios y **no elegibles** para pares, cobertura, mejoras ni cierre
de VSG-2B. No reutilizar el gate ni extender su presupuesto mediante otra carpeta.
La separación deberá constar también en la admisión y el consumo de resultados
antes de ejecutar. No se crea ni se autoriza ese experimento ahora.

## Verificación local

El [resultado de esta revisión](../../validation/vsg_2b/NATIVE_INTERFACE_REVIEW.json)
registra hashes de entrada, inventario completo de B, revisión independiente del
dry run persistido y verificación de preconditions. Se comprueba además que todos
los archivos previamente versionados siguen idénticos. No se refresca evidencia
histórica ni se afirma una nueva prueba visual. Cero predicciones, imágenes nuevas,
pares válidos nuevos o acceso autenticado; no se inspeccionó el token local.
