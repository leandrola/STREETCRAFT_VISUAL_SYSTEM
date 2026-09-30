# VSG-2B / N1 · Viabilidad de un backend estructurado

**N1_NO_COMPATIBLE_BACKEND_VERIFIED** · 2026-09-30.

El cierre de evidencia consolida **cinco candidatos ya examinados**: sg2im,
GLIGEN, ComfyUI, SIMSG y SGDiff. Ninguno quedó verificado para el contrato completo
del A/B original. Las fuentes respaldan descartes limitados a las interfaces y
rutas inspeccionadas; esto no demuestra inexistencia universal de otro backend.
No se amplió la búsqueda, construyó sonda ni ejecutó ningún modelo.

Queda **pendiente una decisión arquitectónica explícita**: buscar/desarrollar un
consumidor estructural que preserve el experimento original, o proponer otro
experimento con nuevo alcance y gate. Ninguna alternativa se
decide por defecto, se implementa ni se autoriza mediante este cierre.

## Entrada, alcance y presupuesto

HEAD inicial/final: `42cfa61a480b6fe73e7e965993bd1f6327e28f05`.
La evaluación N1 anterior comenzó con árbol limpio y recomendación Alta. Este
**cierre de evidencia** comenzó con sus dos entregables locales sin seguimiento
(`??`), aún sin commit. HEAD y `main` coinciden en la base indicada. No se encontraron
AGENTS.md aplicables ni otros cambios locales. El usuario dio `go` después de la
recomendación Media para este cierre; no se afirma haber cambiado el selector de
razonamiento de la aplicación.

Se leyeron la spec N1 adjunta, P1R_SCOPE_DECISION, NATIVE_INTERFACE_REVIEW, el dry run
D persistido, el renderer, el protocolo CommandGenerator y la política 1.0.0.
El protocolo está en `pilot/README.md` y `pilot/harness.py`; no existe el archivo
`pilot/adapters/README.md` inicialmente consultado. Los 741 archivos previamente
versionados se conservaron byte por byte; solo se añaden este runbook y N1_RESULT.

| Etapa | 5-hour inicial/final | Weekly inicial/final | Consumo porcentual |
| --- | --- | --- | --- |
| Inicio / Gate A | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN | UNKNOWN |
| Gate B, dos candidatos | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN | UNKNOWN |
| Gate C, omitido por falta de candidato completo | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN | UNKNOWN |
| Cierre N1 anterior | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN | UNKNOWN |
| Cierre de evidencia actual | UNKNOWN / UNKNOWN | UNKNOWN / UNKNOWN | UNKNOWN |

No hay telemetría de Plan Limits accesible en esta ejecución. Se conserva el límite
solicitado de 40 puntos porcentuales como restricción, pero **no se certifica su
cumplimiento numérico**. La investigación termina al resolver los dos candidatos;
no se usa una supuesta cuota restante para ampliar la búsqueda. El objetivo de este
cierre es ≤10 puntos, con techo del proyecto de 40; consumo real UNKNOWN, sin
certificación numérica. Ocho llamadas de
campaña sin consumir por N1. Predicciones / imágenes / pares nuevos: **0 / 0 / 0**.

## Gate A · criterios fijados antes de la inspección de candidatos

Se descarta una ruta que convierta B a prompt, ignore registros, normalice A y B al
mismo input antes de la frontera experimental, use modelos diferentes, no preserve
la imagen fuente como entrada visual, no controle seed o trunque sin detectar.
Un puerto tipado, un parser, una promesa comercial o un mock no prueban consumo
estructural. Los campos de provenance pueden tener una función de validación y
auditoría: no deben inventarse efectos generativos para ellos ni para VALIDATE_ONLY.
La búsqueda inicial eligió repositorios; estos criterios quedaron registrados antes
de descargar e inspeccionar su código. Timestamp en N1_RESULT.

Fuente D: `validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f`.
JPEG SHA-256: `282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
Delta: `6159ef5f5666afb9037f5ba9512cf6a3d3c89a778f376961c9c570391ce59282`.
A es string JSONL; B es array; su igualdad semántica y el common idéntico se
recomprobaron. Los parámetros siguen DRY_RUN_ONLY, seed null; no se seleccionó seed
operacional. El replay local no prueba disponibilidad de ningún proveedor.

### Matriz de los diez registros

`E1=rel_facade_left_of_diner`; `E2=rel_sign_above_diner`.
En todos los registros: `id:string`, `priority:string`, `lock_ids:array<string>`;
los tipos y valores anidados completos están inventariados en N1_RESULT.

| Registro | Prioridad; tipo de value | Validación y efecto esperado según contrato | Consumidor efectivo verificado en candidatos |
| --- | --- | --- | --- |
| edge:rel_facade_left_of_diner | PR1; objeto | facade_01 LEFT_OF diner_01; extremos existentes, evidence, protection y dos locks intactos | Consumo de triples documentado; mapeo íntegro de este registro NOT_VERIFIED |
| edge:rel_sign_above_diner | PR0; objeto | sign_01 ABOVE diner_01; extremos existentes, evidence, protection y lock DINER intactos | Consumo de triples documentado; mapeo íntegro de este registro NOT_VERIFIED |
| lock:GL-GEO-DINER_01 | LOCK; objeto | Target diner_01, storefront, topología E1/E2; VALIDATE_ONLY | NOT_VERIFIED; los controles de máscara/keep no implementan esta semántica |
| lock:GL-GEO-FACADE_01 | LOCK; objeto | Target facade_01, facade, topología E1; VALIDATE_ONLY | NOT_VERIFIED |
| lock:GL-SEM-SIGN_01 | LOCK; objeto | Target sign_01, sign, texto exacto TERMINAL DINER; VALIDATE_ONLY | NOT_VERIFIED; no se infiere obediencia literal |
| topology:billboard_01 | P2; array<string> vacío | Lista vacía conservada y nodo existente; no equivale a borrar el nodo | NOT_VERIFIED |
| topology:diner_01 | P0; array<string> | E1/E2 en orden y lock DINER; consistencia con extremos | NOT_VERIFIED como registro íntegro, aunque los triples codifican adyacencia |
| topology:facade_01 | P0; array<string> | E1 y lock FACADE; consistencia con extremos | NOT_VERIFIED |
| topology:fascia_01 | P2; array<string> vacío | Lista vacía conservada y nodo existente | NOT_VERIFIED |
| topology:sign_01 | P0; array<string> | E2 y lock SEM-SIGN; consistencia con extremos | NOT_VERIFIED |

### Matriz por campo y frontera de consumo

| Campos | Tipo / validación requerida | Uso y límite |
| --- | --- | --- |
| id, priority, lock_ids | string, string, array<string>; igualdad congelada, unicidad y referencias válidas | Identidad, protección y asociación; no equivalen a índices de categoría del modelo |
| edge.value.from/to/type | string; nodos existentes y relación exacta | Candidatos consumen índices s/p/o; correspondencia con D y vocabulario NOT_VERIFIED |
| edge.value.protection, confidence, epistemic_class | string, number, string; PR0/PR1, confianza en [0,1], OBSERVED según snapshot | Restricciones y autoridad de evidencia; consumidor completo NOT_VERIFIED |
| evidence y provenance.evidence | objeto con evidence_id/reference_id strings y region array<number>[4] | Provenance ligada a fuente; región no autoriza máscara/caja de intervención |
| lock.value.target, type, strength, enforcement | objeto {id,kind}, strings; NODE existente, tipo exacto, ABSOLUTE, VALIDATE_ONLY | Obligación de validar preservación; no orden de imponer geometría generativa |
| lock.value.expected.node_type/text | string; valores exactos del contrato | Validación de identidad/tipo/texto; sin sustitución por categoría aproximada |
| lock.value.expected.protected_topology | array de objetos {id,from,to,type}, strings | Referencias y correspondencia exacta con edges; sin duplicar/añadir constraints |
| lock.value.provenance.source | string VSG_NODE_LOCK | Autoridad de origen, sin efecto generativo inventado |
| topology.value | array<string>; IDs de edges incidentes, orden y listas vacías intactos | Representación explícita de adyacencia protegida; no omitir el registro tras derivar triples |

N1_RESULT contiene por registro cada ruta JSON, incluidos contenedores y listas
vacías, su tipo observado, regla de validación, papel semántico y referencia al
hallazgo de consumo de cada candidato. Los tipos observados no sustituyen un schema
operacional. La revisión local valida preservación del contrato; no ejecuta
validadores de los candidatos ni acredita efectos sobre imágenes.

## Gate B · dos candidatos adicionales

Se reutilizó el resultado anterior de sg2im, GLIGEN y ComfyUI sin repetir su revisión.
Solo se inspeccionaron los siguientes dos candidatos. Se descargaron archivos de
código/configuración públicos a un directorio temporal, sin ejecutarlos, instalar
dependencias ni obtener pesos. N1_RESULT registra URLs inmutables y SHA-256 por archivo.
Este párrafo describe la evaluación anterior; el cierre actual verifica sus fuentes
y consolida los cinco descartes en la tabla siguiente.

### Matriz consolidada del cierre

Las líneas son líneas reales del código recuperado, no numeración del HTML de GitHub.
Para documentación sin código fijado se cita la sección, sin inventar SHA o línea.
`UNPINNED` limita el hallazgo al contenido consultado; no identifica una versión
operacional. Los dos commits fijan código, no los pesos del modelo.

| Candidato; pin | Archivo / función o sección primaria | Evidencia positiva y fuente visual | Requisito exacto no demostrado |
| --- | --- | --- | --- |
| sg2im; **UNPINNED** (`master`) | [sg2im/model.py, Sg2ImModel.forward L108; encode_scene_graphs L173](https://github.com/google/sg2im/blob/master/sg2im/model.py#L108) | objetos y triples LongTensor; GCN consume extremos/predicados. La firma inspeccionada no recibe JPEG/píxeles fuente | A textual en ese backend, fuente visual y diez registros VSG íntegros; conclusión limitada a este archivo mutable |
| GLIGEN; Diffusers **v0.29.0** | [pipeline_stable_diffusion_gligen.py, StableDiffusionGLIGENPipeline.__call__ L530](https://github.com/huggingface/diffusers/blob/v0.29.0/src/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py#L530) | phrases/boxes tipados; L741 los pasa en conditioning; L744–761 codifica píxeles para inpainting | B como EdgeRecord/LockRecord/TopologyRecord; prompt y cajas en la misma API no equivalen al A/B original |
| ComfyUI; **UNPINNED** | [Custom datatypes, INPUT_TYPES / RETURN_TYPES](https://docs.comfy.org/custom-nodes/backend/more_on_inputs#custom-datatypes) | transporte de objetos Python entre puertos; ningún consumidor generativo concreto seleccionado | Validación y uso estructural de B, flujo de fuente y A/B en un mismo modelo; no extrapolar el descarte a todos los workflows posibles |
| SIMSG; **a1decd989a53a329c82eacf8124c597f8f2bc308** | [simsg/model.py, SIMSGModel.forward L191](https://github.com/he-dhamo/simsg/blob/a1decd989a53a329c82eacf8124c597f8f2bc308/simsg/model.py#L191); runner L362–364 | GCN sobre triples; sí usa contenido fuente para features y rama de imagen | A textual y contrato VSG completo, independientemente de que sí exista consumo visual |
| SGDiff; **953d14b8b815ee7d37505b1902608fd8c71f8738** | [testset_ddim_sampler.py, main L43 / llamada L81–90](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/testset_ddim_sampler.py#L81); CGIPModel.encode_graph_local_global L62 | GCN produce conditioning; el encoder usa image.shape. Ese sampler no proporciona fuente latente | A textual, registros VSG y preservación de píxeles fuente en **esa ruta**; no se extrapola a variantes del proyecto |

| Candidato | Cobertura de D: 2 edges / 3 locks / 5 topology | Seed y versionado |
| --- | --- | --- |
| sg2im | triples espaciales parciales / NOT_VERIFIED / NOT_VERIFIED | Sin seed de solicitud en forward; RNG/pesos NOT_VERIFIED; código UNPINNED |
| GLIGEN | cajas/frases, no edges VSG / NOT_VERIFIED / NOT_VERIFIED | Admite torch.Generator; control completo A/B y pesos NOT_VERIFIED; código v0.29.0 |
| ComfyUI | NOT_VERIFIED / NOT_VERIFIED / NOT_VERIFIED | Transporte sin modelo/workflow elegido; seed/pesos NOT_VERIFIED; docs UNPINNED |
| SIMSG | triples parciales / NOT_VERIFIED / NOT_VERIFIED | RNG y pesos NOT_VERIFIED; código fijado por commit |
| SGDiff | triples parciales / NOT_VERIFIED / NOT_VERIFIED | RNG y pesos NOT_VERIFIED; código fijado por commit |

Ninguna fila certifica cobertura efectiva de los diez registros de D. La matriz
individual y sus 163 rutas permanecen en el resultado; la tabla expresa capacidades
documentadas, no pruebas de modelo. No se combinan capacidades de varios candidatos
para declarar uno compatible. La posibilidad del **A textual + B array original**
en el mismo modelo sigue NOT_VERIFIED para los cinco.

### SIMSG

Repositorio `he-dhamo/simsg`, commit
`a1decd989a53a329c82eacf8124c597f8f2bc308`.

El [forward de SIMSGModel](https://github.com/he-dhamo/simsg/blob/a1decd989a53a329c82eacf8124c597f8f2bc308/simsg/model.py#L191)
recibe objetos, triples, imagen y controles de preservación/máscara. La ruta GCN
consume extremos y predicados antes del layout y decoder; la imagen aporta features.
No presenta una entrada A textual ni los registros VSG completos. Sus flags keep
no acreditan locks VALIDATE_ONLY. Hay ruido por `torch.randn`; no hay seed por
solicitud en esa firma. Control reproducible de todos los RNG: NOT_VERIFIED.

La [carga de imagen y grafo](https://github.com/he-dhamo/simsg/blob/a1decd989a53a329c82eacf8124c597f8f2bc308/simsg/data/vg.py)
decodifica y transforma la imagen, filtra objetos según límites y añade un canal de
máscara. Los nombres verificados son `SceneGraphNoPairsDataset.__getitem__` L81 y
`collate_fn_nopairs` L204; se corrigen los nombres VgSceneGraphDataset/vg_collate_fn
que figuraban en el resultado local anterior. El [runner](https://github.com/he-dhamo/simsg/blob/a1decd989a53a329c82eacf8124c597f8f2bc308/scripts/evaluate_changes_vg.py#L362)
pasa `imgs_in` a `src_image`. Esto documenta una ruta visual real, pero no vincula
el JPEG D a una ejecución ni autoriza transformar sus evidence regions en controles.
El loader puede recortar/seleccionar objetos según max_objects; no se afirma que
D haya sufrido truncado, porque no se ejecutó.

Campos desconocidos: no existe validador del envelope VSG inspeccionado. La firma
forward tiene parámetros definidos; los kwargs extra del constructor producen una
advertencia. Eso no demuestra rechazo estricto del contrato. Receipts de generación
con hashes/seed/settings requeridos por el harness: NOT_VERIFIED. Checkpoint,
vocabulario y soporte íntegro de D: NOT_VERIFIED; el commit fija código, no pesos.

**Descarte:** ausencia de A textual verificada y del consumidor/validador completo
de locks, topología, prioridades y provenance. Un adaptador que reduzca B a triples
perdería campos; parsear A a esos mismos triples eliminaría el tratamiento.

### SGDiff, generación desde scene graphs

Repositorio `YangLing0818/SGDiff`, commit
`953d14b8b815ee7d37505b1902608fd8c71f8738`. No se evalúan otros proyectos homónimos
ni se sigue el enlace del README a un modelo diferente.

[CGIPModel.encode_graph_local_global](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/ldm/modules/cgip/cgip.py#L62)
consume triples por convolución de grafo y produce features locales/globales.
`image` se consulta para su shape, sin usar sus píxeles en esa función. El
[sampler evaluado](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/testset_ddim_sampler.py#L76)
envía ese conditioning y empieza difusión sin fuente latente suministrada.
Por tanto, cargar una foto en el dataset no demuestra edición/preservación de D.

[get_learned_conditioning](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/ldm/models/diffusion/ddpm.py#L520)
usa el codificador de grafo; la [configuración inspeccionada](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/config_vg.yaml)
no aporta una rama A textual equivalente en ese modelo. No basta que el repositorio
contenga encoders textuales genéricos para acreditar una ruta compatible.

El [helper de features](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/ldm/modules/cgip/tools.py#L5)
recorta la secuencia local por encima del máximo (15 por defecto en CGIP); no se
afirma pérdida del grafo global ni que D exceda ese máximo. Su parser JSON consume
objects/relationships, agrega nodos/aristas auxiliares y rechaza nombres fuera del
vocabulario; no valida todos los campos VSG ni garantiza rechazo de extras.
El dataset también selecciona objetos según límite.

[DDIMSampler](https://github.com/YangLing0818/SGDiff/blob/953d14b8b815ee7d37505b1902608fd8c71f8738/ldm/models/diffusion/ddim.py#L107)
usa ruido aleatorio; permite x_T y mask/x0, pero el runner inspeccionado no establece
una ruta completa de edición con D. Añadirla sería otro trabajo. Seed controlado,
receipts, pesos fijados y validación de los diez registros: NOT_VERIFIED.

**Descarte:** faltan la rama A textual, el contrato VSG completo y la ruta de fuente
visual; además, no hay garantía de rechazo ante truncado en la ruta inspeccionada.

## Gate C y verificaciones realizadas ahora

Gate C: **NOT_RUN_NO_COMPLETE_CANDIDATE**. Cero sondas, mocks o trazas de ejecución
de candidatos; la trazabilidad anterior es lectura estática de código. Implementar
un consumidor o entrenar/adaptar un modelo queda fuera de N1.

Durante la evaluación N1 anterior se ejecutaron, sin generación:

- `harness.check_preconditions()`: PASS contra la evidencia y hashes vigentes.
- `review_dry_run.review(D)`: PASS en sus doce comprobaciones independientes.
- `harness.prepare(manifest_D, allowlist)`: PASS; payloads reproducidos idénticos
  a los persistidos, sin `execute()` ni CommandGenerator.
- Integridad de los diez registros, rutas de campos y referencias al grafo/locks:
  PASS; listas vacías y locks VALIDATE_ONLY conservados.
- Comparación SHA-256 de los 741 archivos previos, consistencia de N1_RESULT,
  enlaces locales y whitespace de los documentos nuevos: PASS.

### Verificaciones frescas del cierre de evidencia

Se ejecutaron nuevamente `harness.check_preconditions()` y
`review_dry_run.review(D)`: PASS. Se comprobaron tipos A/B, igualdad semántica,
common idéntico, fuente ligada al manifest, payload SHA-256 y delta persistido:
PASS; diez registros con distribución 2/3/5. No se repitió `prepare()` en este cierre.

Se recuperaron los diez archivos de SIMSG/SGDiff por commit: HTTP 200 y SHA-256
idénticos a los registrados. Se verificaron además las fuentes primarias de sg2im,
GLIGEN v0.29.0 y ComfyUI. Las funciones/líneas de código se comprobaron mediante
lectura y parsing AST, sin importar ni ejecutar código externo. Corrección de
nombres del loader SIMSG anotada arriba; no cambia el descarte.

`git diff --check`: PASS. Como los dos entregables siguen sin seguimiento, también
se aplicó `git diff --no-index --check /dev/null <archivo>` a cada uno: PASS.
Hashes de los 741 archivos versionados: intactos. Solo se actualizaron los dos
entregables N1 locales; sus hashes de entrada quedan registrados en N1_RESULT.
Los **100 controles, 25 casos VSG-2A y 24 checks de G0 son históricos**: se verifica
su evidencia vía preconditions, no se presentan como suites ejecutadas ahora.

No se vuelve a ejecutar la suite completa ni se refrescan reportes congelados:
los cambios son dos documentos de evaluación. No se llama a Archive ni a proveedores
de imagen; tampoco se inspeccionan credenciales. No hay manifests admitidos nuevos.
El README del piloto ya declara BLOCKED / PENDING_VISUAL y ausencia de bridge
operacional, por lo que no requiere actualización. Archive / predicciones /
imágenes / pares nuevos = **0 / 0 / 0 / 0**.

## Bloqueo independiente de C y cierre

C requiere una declaración o registro verificable que ligue su JPEG SHA-256
`2130500a09548d4f9c1991a210de3cfa13d8ef63406dd0c3a78c257c68858a09`
a la identidad authored Fear City y a la relación de cámara CG-FC. No se infiere
del PASS histórico. N1 no resuelve ese vínculo, no admite C ni sustituye Reference
Isolation con F.

`PROPOSED_SCOPE.diff` sigue sin aplicar, P1R sigue como factibilidad y Replicate
continúa fuera de esta campaña. Un experimento exploratorio futuro requeriría una
solicitud separada y no aportaría evidencia para cerrar el gate original.
VSG-2B permanece **BLOCKED / PENDING_VISUAL**, producción y predicciones sin
autorizar. El cierre técnico de N1 no es PASS de VSG-2B.

Resultado estructurado: [N1_RESULT.json](../../validation/vsg_2b/N1_RESULT.json).
