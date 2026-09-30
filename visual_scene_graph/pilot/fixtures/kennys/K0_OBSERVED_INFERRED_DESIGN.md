# K0 · Kenny · contrato de fachada observada y rooftop inferido

**Decisión: K0_DESIGN_CONTRACT_READY.** Contrato documental cerrado; la ruta K1
queda delimitada mediante sidecar y verificación específica del diseño. No es
admisión, implementación del verificador, comparación ejecutada ni dry run.
Kenny conserva **RECEIVED_UNBOUND**; VSG-2B, **BLOCKED / PENDING_VISUAL**.

## 1. Provenance y autoridad

- Anotación prospectiva: Codex, 2026-09-29, sobre HEAD
  `f6aa0699cc8c369eed83947e7f6b20f47c5f8788` (`main`).
- Fuente: `visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg`.
  SHA-256 `45b8bff5c33ea411ffef3c88db99d757ce462a7f13b56df3f2fbc62b994357b2`;
  JPEG 736 × 414, hash y dimensiones comprobados, abierto a resolución nativa.
  Fotógrafo y fecha de captura: `UNKNOWN`.
- `reception.json`, en este directorio: SHA-256
  `9ef38ea1a63d5d31f6542c888b336b4356dcdbf43822cfb5055b73d0604fb456`.
  Registra la decisión del usuario: techo plausible que preserve la fachada,
  sin otra vista disponible. La autorización es de diseño, no evidencia del techo.
- Spec ejecutada: `/Users/macbookpro/Documents/VSG_2B_K0_KENNYS_OBSERVED_INFERRED_DESIGN_SPEC.md`,
  SHA-256 `92cbf4b17fa298bc57b609adffb80f7b5a48c1c5a9b393c3a54b698d4da2fbe2`.
  El usuario autorizó su ejecución y respondió «go» después de la pausa inicial.
- Diseño seleccionado por esta anotación dentro de ese alcance:
  **KENNYS_ROOFTOP_DESIGN_V1**. Las piezas elegidas abajo son decisiones nuevas;
  no se atribuyen al usuario como una selección previa de componentes.
- El control `visual_scene_graph/fixtures/kennys_graph_locks_vsg1.json`, SHA-256
  `77e2e0d144f95de802cb0d943661d749c34084223a7eaaec9a30b7ec0f2f3ea7`, marca
  `roof_01`, `parapet_01`, `hvac_01` y sus relaciones como `OBSERVED`. Es sintético,
  no describe observaciones de este JPEG y permanece intacto. K1 usará IDs nuevos.

En las tablas, **S** significa `OBSERVED_SOURCE` + el SHA-256 de la fuente arriba;
**D** significa `AUTHORIZED_INFERENCE` + `KENNYS_ROOFTOP_DESIGN_V1`, autorizado
por el alcance de la spec y de recepción. Ningún componente o relación rooftop
tiene autoridad S. BK trata piezas físicas separadas; este piloto VSG trata
entidades y relaciones de escena. No se fijan medidas, espesores, encastres,
despiece, escala física ni piezas imprimibles de BK.

## 2. Tabla de observación

Regiones aproximadas `[x0,y0,x1,y1]`, normalizadas a 736 × 414, origen arriba a la
izquierda. Son localizadores de evidencia visible, no dimensiones arquitectónicas
ni máscaras de segmentación. Confidence expresa certeza de la afirmación acotada,
no de contenido fuera de la foto. Apóstrofo tipográfico en transcripción editorial;
no presupone un código Unicode presente en una imagen raster.

| claim_id | entidad / región aproximada | hecho visible | literal si es legible | confidence | autoridad |
| --- | --- | --- | --- | --- | --- |
| KOBS-01 | `ks_facade`, [0.147,0,0.878,0.915] | Frente de tienda casi frontal; fábrica, montantes y ritmo de vanos visibles; su parte superior está cortada. | — | HIGH | S |
| KOBS-02 | `ks_upper_windows`, [0.295,0,0.798,0.166] | Grupo de vanos superiores y divisiones visibles; se corta su continuidad superior. | — | HIGH para lo visible | S |
| KOBS-03 | `ks_main_sign`, [0.149,0.174,0.861,0.355] | Letrero horizontal oscuro con letras claras y motivos musicales encima del banner. | Kenny’s Music Shop | HIGH | S |
| KOBS-04 | `ks_banner`, [0.174,0.357,0.849,0.483] | Banner claro, palabras grandes rojas y frase central manuscrita. | GOING out of BUSINESS | HIGH | S |
| KOBS-05 | `ks_left_display`, [0.160,0.493,0.423,0.824] | Vidriera izquierda con instrumentos y batería; conservar disposición visible sin completar objetos ocultos. | — | HIGH; detalles pequeños UNKNOWN | S |
| KOBS-06 | `ks_door`, [0.425,0.503,0.606,0.906] | Acceso central acristalado entre las dos vidrieras; divisiones y carteles pequeños visibles. | No congelado en K0 | HIGH para geometría | S |
| KOBS-07 | `ks_right_display`, [0.606,0.493,0.861,0.821] | Vidriera derecha con instrumentos colgados y carteles; preservar distribución visible. | No congelado en K0 | HIGH para conjunto | S |
| KOBS-08 | `ks_sale_strip`, [0.185,0.500,0.418,0.626] | Franja amarilla inclinada dentro de la vidriera izquierda. | EVERYTHING MUST GO!! | MEDIUM para puntuación; HIGH para palabras | S |
| KOBS-09 | `ks_lower_panels`, [0.156,0.807,0.868,0.915] | Zócalos/paneles oscuros bajo vidrieras; inscripción clara a la derecha. | No congelado en K0 | HIGH para forma; texto pendiente | S |
| KOBS-10 | `ks_context`, [0,0,0.147,0.915] y [0.878,0,1,0.915] | Fragmentos de frentes vecinos, carteles laterales y poste a la derecha; no son componentes de Kenny. | Fuera del inventario literal K0 | HIGH para presencia | S |
| KOBS-11 | `ks_sidewalk`, [0,0.906,1,1] | Acera, borde y franja de calzada delante del frente. | — | HIGH | S |
| KOBS-12 | límite de evidencia, y=0; laterales y profundidad no expuestos | El encuadre termina antes de mostrar techo; no hay observación de altura total, fondo, planta ni caras ocultas. | — | HIGH para el límite; geometría UNKNOWN | S, solo límite de captura |

KOBS-08 no habilita un lock literal exacto de puntuación: K1 debe comprobar los
signos regionalmente o conservarlos como ambiguos. Para carteles de puerta,
vidrieras, panel inferior y cartelería vecina no congelados aquí, no sustituir texto
por frases nuevas ni completar microtexto; K1 separará fragmentos legibles de
`PARTIAL_OR_UNKNOWN`. La falta de transcripción no autoriza borrar carteles.
KOBS-12 es un límite de evidencia, **no un nodo de techo observado**. Mantener
desconocida la forma del techo original incluso después de diseñar uno nuevo.

## 3. Diseño autorizado: KENNYS_ROOFTOP_DESIGN_V1

El resultado compuesto exige volumen legible y componentes distinguibles; una
superficie con textura de techo solamente no cumple este fixture. El techo de
solo textura es otra variante de producto, fuera de V1. No se heredan piezas del
control sintético: se selecciona aquí una propuesta compacta e independiente.

| design_id | componente propuesto | relación arquitectónica | autoridad de proyecto | regla visual / exigencia | prohibición |
| --- | --- | --- | --- | --- | --- |
| KDES-01 / `kd_roof` | Volumen de cubierta | Coronación prospectiva sobre `ks_facade`, sin alterar el frente observado | D | REQUIRED: cubierta con plano y borde volumétrico distinguibles; continuidad plausible con ancho del frente | No presentarlo como techo original; no añadir un piso habitable ni redimensionar fachada |
| KDES-02 / `kd_parapet` | Parapeto perimetral bajo | PART_OF `kd_roof`; borde frontal delante de equipo | D | REQUIRED: espesor aparente y silueta legible, lenguaje material compatible con fábrica del frente | No desplazar letrero, banner ni vanos; no reconstruir una cornisa histórica supuesta |
| KDES-03 / `kd_hvac` | Un equipo HVAC compacto | PART_OF `kd_roof`, BEHIND `kd_parapet`; apoyado en cubierta | D | REQUIRED: volumen parcialmente visible sobre/detrás del parapeto, subordinado al edificio; sin marca ni texto | No flotación, interpenetración ni ocultación total que impida evaluar su presencia |
| KDES-04 / `kd_skylight` | Un skylight bajo | PART_OF `kd_roof`, separado del HVAC | D | OPTIONAL, selección V1: EXCLUDED; solo incluir si se congela una revisión anterior a cualquier candidato | No activarlo después de mirar A/B ni computar su ausencia como fallo en V1 |

Chimenea, water tank y access bulkhead quedan **EXCLUDED** en V1; no son requisitos
implícitos ni opciones que el generador pueda añadir. Piezas mayores adicionales
requieren nueva versión. Detalle de apoyo mínimo del HVAC no crea una nueva
estructura, piso o conjunto de tuberías. No importar geografía, marcas, señalética
ni arquitectura de otra referencia.

Para mostrar el diseño se autoriza encuadre prospectivo ampliado hacia arriba y
una vista moderadamente elevada, manteniendo el frente reconocible y sus
proporciones/relaciones. Es una elección de presentación futura, no recuperación
de cámara original. K1 fijará modo/perfil/cámara compatibles antes del candidato;
si una configuración estrictamente frontal oculta cubierta o HVAC, debe resolver
esa incompatibilidad antes de congelar el request. Nunca deformar el frente o
inflar las piezas para forzar visibilidad. Esta autorización no alcanza laterales
detallados, interiores, edificio vecino completo ni extensión de ciudad.

## 4. Dos subgrafos conceptuales y ownership

**Observed Source Graph `KENNYS_SOURCE_OBS_V1`.** Owner: evidencia S; anotador
Codex. Nodos `ks_facade`, `ks_upper_windows`, `ks_main_sign`, `ks_banner`,
`ks_left_display`, `ks_door`, `ks_right_display`, `ks_sale_strip`, `ks_lower_panels`,
`ks_context`, `ks_sidewalk`, referidos a KOBS-01…11. Solo regiones visibles.
Exigencia P0 para geometría/ritmo de `ks_facade`, `ks_upper_windows`, `ks_door`,
ambas vidrieras y para identidad literal de `ks_main_sign` y `ks_banner`.
P1 para carácter/disposición visible de franja amarilla y paneles; P2 para contexto
y acera, sin autorizar eliminación, sustitución o reescritura de texto.
No promover `ks_sale_strip` a `SEMANTIC_TEXT_LOCK` con puntuación incierta: K1 debe
particionar el texto o desactivar ese lock implícito mediante una representación
de región visual hasta verificar el literal. Un signo P1 dispara lock por defecto.

Relaciones fuente propuestas (todas con epistemología `OBSERVED`, autoridad S,
regiones de ambos extremos como evidencia; PR expresa preservación de lo visible):

| ID | relación | protección |
| --- | --- | --- |
| KSR-01 | `ks_main_sign ABOVE ks_banner` | PR0 |
| KSR-02 | `ks_banner ABOVE ks_door` | PR0 |
| KSR-03 | `ks_left_display LEFT_OF ks_door` | PR0 |
| KSR-04 | `ks_right_display RIGHT_OF ks_door` | PR0 |
| KSR-05 | `ks_upper_windows ABOVE ks_main_sign` | PR0 |
| KSR-06 | `ks_main_sign PART_OF ks_facade` | PR0 |
| KSR-07 | `ks_door PART_OF ks_facade` | PR0 |
| KSR-08 | `ks_sale_strip INSIDE ks_left_display` | PR1 |
| KSR-09 | `ks_lower_panels BELOW ks_left_display` | PR1 |
| KSR-10 | `ks_lower_panels BELOW ks_right_display` | PR1 |

Estas relaciones describen disposición visible, no anclajes constructivos ocultos.
KOBS-12 pertenece al registro de límites; no inventar un polígono de techo fuera
del JPEG. Cualquier región oculta modelada en K1 se conserva UNKNOWN, con su propia
evidencia de límite y sin renombrarla como `kd_roof`.

**Authorized Design Graph `KENNYS_ROOFTOP_DESIGN_V1`.** Owner: contrato D.
Nodos activos `kd_roof`, `kd_parapet`, `kd_hvac`, todos
`epistemic_class=AUTHORIZED_INFERENCE`, `observed=false`, `requirement=REQUIRED`.
`kd_skylight` es opción inactiva, no nodo activo. No usar P0/P1/PR0 como sustitutos
de obligatoriedad de diseño ni dar confidence de observación a estos componentes.

| ID | relación prospectiva | exigencia y ownership |
| --- | --- | --- |
| KDR-01 | `kd_roof ABOVE ks_facade` | REQUIRED, D; cruce explícito a anchor fuente de solo lectura |
| KDR-02 | `kd_parapet PART_OF kd_roof` | REQUIRED, D |
| KDR-03 | `kd_hvac PART_OF kd_roof` | REQUIRED, D |
| KDR-04 | `kd_hvac BEHIND kd_parapet` | REQUIRED, D; orientación definida por la vista frontal prospectiva |

Las cuatro relaciones son `AUTHORIZED_INFERENCE`; nunca `PR0 OBSERVED`.
KDR-01 no duplica `ks_facade` en el grafo de diseño ni permite modificar su owner.
El verificador de diseño debe aceptar ese anchor externo declarado y rechazar
cualquier otro extremo ajeno. El apoyo del equipo, su visibilidad y la separación
de volúmenes son reglas de diseño; no se deduce una oclusión fotográfica obligatoria.

Ejemplo conceptual de vínculo; no es un request SAR2 ni un archivo creado en K0:

```json
{
  "design_version": "KENNYS_ROOFTOP_DESIGN_V1",
  "authority": "AUTHORIZED_INFERENCE",
  "source_binding": {
    "path": "visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg",
    "sha256": "45b8bff5c33ea411ffef3c88db99d757ce462a7f13b56df3f2fbc62b994357b2",
    "purpose": "preserve_observed_facade; not_rooftop_observation"
  },
  "external_anchors": ["ks_facade"],
  "nodes": [
    {"id": "kd_roof", "epistemic_class": "AUTHORIZED_INFERENCE", "observed": false, "requirement": "REQUIRED"},
    {"id": "kd_parapet", "epistemic_class": "AUTHORIZED_INFERENCE", "observed": false, "requirement": "REQUIRED"},
    {"id": "kd_hvac", "epistemic_class": "AUTHORIZED_INFERENCE", "observed": false, "requirement": "REQUIRED"}
  ],
  "relationships": [
    {"id": "KDR-01", "subject": "kd_roof", "predicate": "ABOVE", "object": "ks_facade", "authority": "AUTHORIZED_INFERENCE", "requirement": "REQUIRED"},
    {"id": "KDR-02", "subject": "kd_parapet", "predicate": "PART_OF", "object": "kd_roof", "authority": "AUTHORIZED_INFERENCE", "requirement": "REQUIRED"},
    {"id": "KDR-03", "subject": "kd_hvac", "predicate": "PART_OF", "object": "kd_roof", "authority": "AUTHORIZED_INFERENCE", "requirement": "REQUIRED"},
    {"id": "KDR-04", "subject": "kd_hvac", "predicate": "BEHIND", "object": "kd_parapet", "authority": "AUTHORIZED_INFERENCE", "requirement": "REQUIRED"}
  ]
}
```

## 5. Encaje con runtime y ruta concreta K1

Referencias de código relativas a la raíz, inspeccionadas en el HEAD indicado.
Esta es una revisión estática; no se ejecutaron pruebas ni compilación de K1.

| Campo / frontera | Soporte actual comprobado | Límite semántico y decisión K1 |
| --- | --- | --- |
| `epistemic_class` | `schemas/scene-entity.schema.json` admite string; SAR2 conserva entidades. `vsg_observer.py::build_visual_scene_graph` copia la clase. Schemas VSG-0/VSG-1 no imponen autoridad source/design. | Aceptar `AUTHORIZED_INFERENCE` no valida su procedencia. Usar S→`OBSERVED` solo para hechos fuente; D permanece en sidecar separado. |
| `observed` | Observer copia booleano, default false; `scene_intelligence.py::resolve_entity_action` lo usa en reglas concretas de T01. SAR2 puede inferir default desde `epistemic_class`, a diferencia del observer. | Fijarlo explícitamente; false no impide acciones preserve ni verifica autoridad. |
| `preservation_level` | `resolve_entity_action` convierte P0 en `PRESERVE_EXACT` antes de considerar la epistemología; P1/P2 preservan carácter/contexto. P5 permite inferencia mínima solo con soporte, o bloquea UNKNOWN. | No introducir D como P0 ni fabricar `multi_view_support`/`continuity_support`; REQUIRED pertenece al contrato de diseño. No usar `INFER_MINIMAL` para simular autorización del rooftop compuesto. |
| Relaciones | `schemas/scene-relationship.schema.json` requiere PR0/PR1/PR2/PRX; observer conserva epistemología y tipos admitidos. SAR2 solo advierte PR0+UNKNOWN y extremos faltantes. | No existe ownership obligatorio; no detecta toda inferencia rotulada como evidencia. Mantener KSR en SAR2; KDR en sidecar con REQUIRED y anchor explícito. |
| Graph Locks | `vsg_observer.py::_locks` y `graph_locks.py::build_graph_locks` derivan locks de P0, flags, signos P0/P1 y relaciones protegidas; no comprueban autoridad fotográfica. Geometry lock verifica tipo/topología, no medidas de fachada. | Locks fuente solo sobre hechos verificados. No computar roof/parapet/HVAC como geometría observada. La rúbrica visual sigue siendo necesaria para proporciones, texto y apariencia. |
| Evidence / sidecar | Observer `_evidence` retiene solo `reference_id`, `region`, `evidence_id`, con fallback global; no arrastra automáticamente todos los campos de autoridad. Compiler preserva otros atributos SAR2 bajo `source_attributes`. | No pasar hash fotográfico como evidencia de nodo D; source binding y autoridad de diseño son vínculos distintos. Verificar sidecar y su hash fuera de la mera proyección. |
| CGC / directivas | `integration/streetcraft_orchestrator.py::_draft_cgc` recibe `request.infer` y `forbid`; `project_scene_to_cgc` conserva directivas iniciales. Compiler acepta seis listas explícitas, incluido `infer`. | Codificar determinísticamente requisitos D en directivas originales, antes de orquestar. No añadir un campo CGC arbitrario: compiler/comparador rechazan extensiones no soportadas. |
| Comparación VSG-2A | `generation_compiler.py` compila source graph, SAR2 y contexto; `generation_comparator.py::stable_constraints` exige P0 exacto y grafo completo de SAR2. Compara también directivas; campos desconocidos fallan. | PASS comprueba equivalencia, no veracidad de la anotación ni cumplimiento visual del diseño. Un baseline incorrecto puede ser equivalente. Separar gate fuente y gate de diseño. |
| Manifest / replay / harness | Schema de manifest v1 fija diez artefactos y provenance textual. `fixture_replay.py::FIXTURE_PATHS` solo enumera D/E. `harness.py::prepare` verifica los diez blobs y VSG-2A, sin verificador de sidecar de Kenny. | Un hash escrito en prose no basta. K1 necesita integración explícita, bloqueante, del verificador y congelación de bytes del sidecar; no hay soporte de Kenny ya implementado. |

**Ruta elegida: sidecar versionado + verificación del contrato**, sin extender
SAR2/VSG/Compiler centrales para fingir nodos observados. Alcance mínimo de K1:

1. Congelar un sidecar nuevo de diseño con los nodos/relaciones activos, opciones
   excluidas, autoridad, hash de foto, hash de este K0 y de recepción. Congelar
   también un registro separado de observaciones/incertidumbres y el encuadre.
2. Crear SAR2, expected VSG y candidate VSG solo con evidencia fuente e
   incertidumbres explícitas; KSR conserva prioridades fuente. No incluir nodos D
   para satisfacer cobertura P0 o locks. No resolver la identidad del techo original.
3. Convertir el sidecar D a strings canónicos identificados por versión e ID en
   `request.infer` y sus prohibiciones en `request.forbid`. Llevarlos como
   directivas originales a `generation_context`; comprobar igualdad con CGC final
   y contrato. Son instrucciones de creación autorizada, no observaciones ni
   salida de `INFER_MINIMAL`. Una descripción humana equivalente debe conservar
   los requisitos sin ambigüedad. No agregar D después de mirar payloads A/B.
4. Implementar un verificador K1 en la frontera del piloto: exige bytes/hash de
   sidecar y source, IDs disjuntos, autoridad D, `observed=false`, tres nodos y
   cuatro relaciones REQUIRED, exclusiones, anchor `ks_facade`, límites de cambio
   y correspondencia exacta entre sidecar y directivas. Rechaza falta o alteración
   del sidecar, relabeling a OBSERVED, componente extra, extremo cambiado, omisión
   de requisito o modificación de la fachada. Debe ejecutarse en replay **y** en
   prepare del harness antes de admitir/usar Kenny, sin vía alternativa que lo omita.
5. Vincular path/hash del sidecar dentro de un artefacto admitido (request y su
   provenance), guardar sus bytes junto al dry run y verificar nuevamente desde
   bytes persistidos. La lectura/congelación adicional requiere trabajo K1 en el
   piloto; no extender silenciosamente la lista de artefactos del manifest v1.
   Añadir selección/replay explícitos de Kenny y controles de separación, preservando D/E.
6. Reportar por separado VSG-2A fuente, integridad/cumplimiento estructural del
   contrato D y rúbrica visual pendiente. En la ruta propuesta las directivas D
   viajan iguales en `common` de A/B; las relaciones/locks estructurados de VSG
   siguen siendo los de fuente. **No se afirmará que el experimento A/B ejercita
   Graph Locks de rooftop.** Eso requeriría otro alcance explícito para diseño.

La distinción es expresable con esta frontera separada; no queda una extensión
semántica central sin resolver. Su implementación y prueba pertenecen a K1 y
pueden bloquear ese hito. Si K1 exige que los nodos D entren en el VSG fuente o
midan cobertura de locks como observaciones, debe revisar el contrato: no se
habilita esa mezcla por el estado READY documental de K0.

## 6. Matriz de evaluación futura

No promediar fidelidad fotográfica y cumplimiento de diseño para ocultar fallos.
Un defecto S3 bloquea aunque los otros ejes pasen. Revisar cada requisito activo;
denominador cero significa no ejercitado. Evaluación humana de imágenes pendiente.

| Eje | Baseline / criterio | Fallo y gravedad |
| --- | --- | --- |
| Fachada y texto | KOBS y KSR: proporciones/ritmo, puerta entre vidrieras, letrero encima del banner; literales de KOBS-03/04; apariencia regional de textos no resueltos | S3: rediseño de fachada P0, desplazamiento de identidad, sustitución/invención de literal protegido, ruptura PR0. Cambio menor de acabado fuera de tolerancia: S2. |
| Diseño prospectivo | KDES-01…03 y KDR-01…04; tres componentes activos distinguibles, cuatro relaciones, apoyo/visibilidad/subordinación; opciones excluidas | S3: cubierta solo textura, componente REQUIRED ausente, relación REQUIRED rota o volumetría que modifica el frente. Defecto menor de acabado sin pérdida de componente/relación: S2. Evaluar «cumplimiento del diseño», jamás «fidelidad al techo original». |
| Cambios no autorizados | Prohibiciones D y preservación S; ninguna adición fuera de lista o scope | S3: nuevo piso, pieza mayor excluida, geografía o arquitectura importada, fachada reinterpretada para acomodar techo. |
| Incertidumbre y provenance | Límite KOBS-12, texto parcial, laterales/profundidad no visibles; separación de autoridades y hashes | S3: declarar observado un componente/relación inventado, completar microtexto sin prueba, presentar geometría oculta como recuperada o usar el control sintético como evidencia fotográfica. Incertidumbre conservada se informa, no es fallo automático. |

Las severidades de este contrato son criterios del piloto; no presuponen que el
ledger actual detecte automáticamente todas esas violaciones visuales. K1 debe
comprobar la compatibilidad del modo/cámara y bloquear si la expansión autorizada
contradice un lock de desconocidos. No quitar locks fuente para obtener READY.

## 7. Cierre y verificación K0

- Revisados región/límite de cada claim, IDs de las dos tablas y extremos de
  relaciones: ningún roof/parapet/HVAC ni KDR lleva autoridad `OBSERVED_SOURCE`.
- SHA del JPEG coincide antes y después; `git diff --check` sin errores. Los
  archivos versionados previos permanecen sin cambios y el único entregable nuevo
  es este documento. No se ejecuta regresión unificada por agregar un Markdown.
- D/E, allowlist, snapshots, CGC estable, QA, preconditions y recepción sin cambios.
  C permanece cerrado `NO_GO_C0_UNVERIFIED` y `RECEIVED_UNBOUND`.
- **0 llamadas Archive nuevas, 0 llamadas de imagen, 0 imágenes, 0 pares visuales.**
  No se declara `CORPUS_RECOVERY_DRY_RUN_PASS` de Kenny ni VSG-2B.
- Plan Limits: inicio, tramos y cierre de cinco horas/semanal **UNKNOWN**;
  consumo observado **UNKNOWN**. No se certifica numéricamente el tope de 40
  puntos ni se reutiliza el snapshot antiguo como saldo. Revisión documental
  acotada, sin instalación, ejecución del pipeline ni binding K1.

Siguiente hito posible: una spec K1 derivada de este contrato para binding ligado
a la fuente y dry run, con verificador D obligatorio, controles de separación y
gate técnico propio. K0 termina aquí, incluso si queda cuota.
