# SPATIAL-PILOT-D v2 · amendment de tamaño

Base: `421627deb3aa9c2ffe4e349a1ef71273601619b1`. Autoridad: pedido de Lean
del 2026-10-17. v1 y toda su evidencia permanecen intactos. Esta enmienda
no cambia SVS, VSG, GLIGEN, el prompt histórico ni los umbrales de alineación.

## Fase 1: decisión única antes de procesar originales

La observación declarada por Lean de salidas 1672×941 invalida la suposición
de salida 1600×900 de v1. No hay evidencia de que una entrada 1672×941 produzca
siempre ese tamaño; la variante nativa es un artefacto determinista de estudio,
NO una nueva entrada autorizada ni prueba de estabilidad del generador.

El canvas canónico sigue siendo el v1 persistido, RGB 1600×900, núcleo
`[453,61,1147,839)` y PNG de núcleo original 694×778. No se recalcula ese núcleo.

```
original RGB -> normalización explícita -> RGB canónico 1600×900
-> alineación residual -> composición diagnóstica -> verificación guardada
```

Sólo se admiten PNG/JPEG RGB de un frame, sin orientación EXIF distinta de 1.
1600×900: identidad, sin resampling. 1672×941: Pillow 12.3.0
`resize((1600,900), Resampling.LANCZOS)`, sin crop, padding, autocontraste,
conversión ICC o rotación. Otro tamaño/modo se rechaza, sin fallback silencioso.
Los bytes originales se archivan intactos y se hashean antes de decodificar.

Transformación de límites de píxel RAW -> CANONICAL:
`x_c = (1600/1672)*x_r`, `y_c = (900/941)*y_r`.
Pillow usa centros: `x_r = (x_c+0.5)/scale_x-0.5`, análogo en y.
`scale_x=200/209`, `scale_y=900/941`; el cociente entre ambos es
`188200/188100`. Es una corrección anisotrópica de aspecto explícita (~0.0532%),
no una escala uniforme de cámara ni una detección del comportamiento de GPT.
Se registran ambas fracciones y decimales, tamaños, método, aspecto y affine.

La búsqueda v1 recibe exclusivamente la imagen normalizada. Su `scale` pasa a
llamarse también `residual_scale_after_normalization`; dx/dy están en píxeles
canónicos. Nunca se compara 1672/1600 con el umbral residual de 0.02.
La normalización puede remuestrear el núcleo GPT; sólo el pegado posterior
restaura el núcleo congelado. La identidad es respecto del PNG v1 persistido.

Se mantienen todos los límites NCC, cuadrantes, margen, residual local, escala
y posición de v1. Una escala dentro del límite NO garantiza aceptación si otro
gate falla; el rechazo conservador por ambigüedad de v1 debe seguir rechazado.
En el primer intento sintético se esperaba aceptación de 1.01; el gate recuperó
1.009 pero rechazó margen 0.0277104 < 0.03. El intento fallido se conserva en
CHECKS_INITIAL.json. La comprobación adicional 1.002 también se rechaza por
margen 0.0219662. Ambos quedan como controles de rechazo, no eliminados.
El límite inclusivo 1.02 pasa (margen 0.035992). No se cambió código ni umbrales
del alineador: la aceptación no es monótona con la escala por su búsqueda y
cuantización congeladas. No se afirma que toda escala permitida sea corregible.

## Variante nativa no seleccionada

Fuente completa 347×389, Pillow 12.3.0 RGB, resize directo LANCZOS a 725×813
(redondeo de 694*1672/1600 y 778*941/900). Canvas RGB neutro 1672×941;
núcleo `[473,64,1198,877)`, sin recorte, centrado con redondeo entero.
Relaciones equivalentes a v1 dentro de 1 px por borde (centro x desplazado
0.5 px por paridad de dimensiones); núcleo y canvas
tienen hashes de archivo y RGB en NATIVE_CANVAS.json. No se usa en registros v2.

## Freeze y reproducción

FREEZE.json vincula por SHA-256 el protocolo, código, tests y artefactos nativos,
además de todos los archivos históricos v1. Se crea después de los tests y se
commitea antes de ingerir reales; el CLI exige ese freeze commiteado e idéntico.
No cambiar umbrales después de observar reales. Una revisión nueva requiere
otro freeze identificado. Cada corrida tiene directorio exclusivo; no sobrescribir.

## Fases pendientes, sin adelanto

Fase 2 exige los originales descargados de las tres corridas D del piloto
espacial, no las antiguas dos salidas VSG. Se requiere declaración de procedencia,
hash del original aportado por el operador, id/fecha/modelo o UNKNOWN.
Faltando bytes originales no hay métricas reales ni aceptación/rechazo inventados.

Hasta cerrar Fase 2 no se implementa/calibra SEAM_GATE ni se abre evaluación de
compuestos. Los resultados geométricos ACCEPTED son diagnósticos, nunca aptitud
visual. Los rechazos se conservan y el núcleo final es NOT_APPLICABLE si no hubo
composición. SEAM_GATE y texto humano quedan NOT_RUN/PENDING, visual_evaluable=false.

La costura visible de la fixture +8 declarada por Lean prueba una limitación real
del alignment gate; no se inventará calibración GOOD/BAD ni thresholds para superarla.
La futura Fase 3 exige referencias visuales identificadas y un freeze separado.
No se retoca interior, no se confunde core_exact con continuidad visual.

Las notas de preservación/fidelidad comunicadas por Lean corresponden a
RAW_GENERATOR_VISUAL_EVALUATION, nunca a COMPOSITE_PIPELINE_VISUAL_EVALUATION.
Su clasificación se registra al cerrar el estado, sin abrir Fase 4 ni puntuar.
