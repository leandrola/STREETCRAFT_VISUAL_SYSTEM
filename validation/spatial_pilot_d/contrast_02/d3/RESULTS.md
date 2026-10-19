# CONTRASTE 02 · continuación con original D3

## Hallazgo prioritario: una violación conocida no es eliminada

`sans_12_blur`: NOVA DEPOT, Arial, tinta de 12 px, GaussianBlur(0.6),
fue reconocido pero **NO DETECTÓ la violación eliminatoria esperada**.
Confianza OCR 0.50: el clasificador congelado devuelve ADVERTENCIA, no VIOLACION.
Es un falso negativo del gate, no una ausencia de reconocimiento. Ver
[recorte](execution/sans_12_blur/crops/tile_000_line_000.png) y
[resultado íntegro](execution/sans_12_blur/result.json).
No se modificaron confianza, whitelist, agrupación, alturas ni geometría.

El [resultado histórico](../RESULTS.md) sigue vigente: MOVING tampoco alcanzó
confianza eliminatoria y las dos frases completas anotadas no cumplieron el
matching congelado. D v1 corrida 2 sí fue eliminada por JOHNSON, WAREHOUSE y
STORAGE. No reinterpretar esa detección parcial como éxito de las frases completas.

## Entrada y freeze

Lean confirmó el adjunto como original bueno del piloto espacial D, corrida 3.
La copia [D3_original.png](execution/D3_original.png) conserva exactamente los
bytes: SHA-256 `1e8a03659cc877da91b34fd8dae35cda2130929ffd1932abd7fdc4f57bc27603`.
Tamaño observado **1365×768**, RGBA, 2,495,549 bytes. Es la misma secuencia de
bytes que el adjunto previo, no una nueva versión 1672×941. Originalidad/corrida:
confirmación del operador, sin receipt independiente. La discrepancia queda
registrada y no se usa como bloqueo para este contraste OCR autorizado.
No es evidencia de admisión, alineación o preservación del compositor.

- Freeze original: commit `b971cf43997017fecc6059961cbcf6dfaa49417b`;
  SHA-256 `26302674549af7528e63948a6a76e7a6b4186ba0ea2098e70691e379330899c6`.
- Suplemento D3, commiteado antes de OCR D3 e inyecciones:
  `ad0a19750b71a7d7ac008ae33bb14ba959bc57e5`;
  [FREEZE.json](FREEZE.json) SHA-256
  `0890c7b0ce4bcff2b1f6086ede277ea82a2e3e43b95c8da9440e6e833bf1c428`.

Preprocesado fijo: alpha sobre blanco, ancho 1600, alto redondeado 900,
Pillow 12.3.0 LANCZOS; scale_x=1.1721611721611722,
scale_y=1.171875. La diferencia por redondeo se explicita, no se confunde con
deriva residual. RGB normalizado SHA-256
`762e01abda913086800ed4652759da0d0963988debde2bf4f0f58a89be24b92d`.
Tiles 800×800 superpuestos, stride 640 y último tile al borde; ampliación x2.
Apple Vision revision 3, accurate, en-US, corrección/autodetección desactivadas,
CPU local, sin red; macOS 15.7.9 (24G830), Python 3.14.5, Swift 6.1.2.
Binario SHA-256 `9e6441ab042ce165c43251078556ca14571d475fe6cff400d10529d8b4dfa4d0`.

## Resultados y sensibilidad

| Caso | Esperado | Obtenido | Resultado |
| --- | --- | --- | --- |
| D3 original bueno | 0 violaciones | 0 violaciones, 0 advertencias, 25 hallazgos ignorados por solape | PASS del control negativo disponible |
| 8 px, 2 fuentes × sharp/blur | advertencia | reconocimiento 4/4; al menos una VIOLACION en 4/4 | DETECTÓ texto; sobreclasificación respecto al alto real |
| 12 px, 2 fuentes × sharp/blur | violación | reconocimiento 4/4; violación 3/4 | NO DETECTÓ violación en Arial blur |
| 20 px, 2 fuentes × sharp/blur | violación | reconocimiento y violación 4/4 | DETECTÓ 4/4 |
| 40 px, 2 fuentes × sharp/blur | violación | reconocimiento y violación 4/4 | DETECTÓ 4/4 |
| 80 px, 2 fuentes × sharp/blur | violación | 4 SKIPPED; no imagen ni OCR | NO EVALUADO; no es falso negativo OCR |
| TERMINAL DINER en zona libre | ADVERTENCIA_DUPLICADO | ADVERTENCIA_DUPLICADO, confianza 1.00 | DETECTÓ |
| TERMINAL DINER dentro del núcleo | IGNORADO_POR_SOLAPE | IGNORADO_POR_SOLAPE, confianza 1.00 | DETECTÓ e ignoró; 0 violaciones |

Los 8 px producen cajas OCR de altura superior al umbral de 10 px. En tres
casos coexisten ADVERTENCIA y VIOLACION de tiles diferentes; en serif blur sólo
VIOLACION. La deduplicación congelada conserva clases diferentes. El campo
`expected_class_detected=true` significa que existe esa clase, **no** que no
haya una clase contradictoria. No son falsos positivos de objetos sin texto.

Reconocimiento: 16/16 inyecciones principales ejecutadas. Violaciones esperadas
para alturas 12–40: 11/12 detectadas. Para >=20: 8/8 ejecutadas detectadas,
pero sólo 8/12 casos planificados tienen evidencia; **100% de cobertura/recall
>=20 NO ESTABLECIDO**. La matriz completa y cada imagen/verdad están en
[FINDINGS.md](FINDINGS.md); OCR bruto, cajas, clases, confianza y recortes por
caso se conservan en [execution/](execution/).

## Bloqueo de cobertura, sin reajuste posterior

NOVA DEPOT de 80 px no cabe horizontalmente en la franja izquierda de 453 px.
Se comprobó antes del OCR y quedó explícito en el suplemento congelado.
El protocolo original ordena omitir/reportar si no cabe; se cumplió, sin
encoger, mover al núcleo, rotar o cambiar el texto para completar el denominador.
Los cuatro intentos conservan JSON con dimensiones requeridas y disponibles.
Cubrir 80 px requiere autorizar y congelar un protocolo adicional de ubicación
o texto **antes** de una nueva ejecución; no reescribir estos resultados.

## Revisión de falsos positivos y límites

Revisión visual por Codex, no anotación de Lean: 25 recortes únicos del baseline
y 20 hallazgos no ignorados de las inyecciones. **Lista de falsos positivos de
no-texto: vacía (0/45 revisados)**. Todos muestran texto real. Lecturas parciales
o incorrectas del cartel no se reclasifican como objetos sin texto. No se afirma
haber revisado manualmente los 504 hallazgos únicos de toda la tanda.
Ver [VISUAL_REVIEW.json](VISUAL_REVIEW.json),
[baseline 1](review/baseline_01.png), [baseline 2](review/baseline_02.png),
[hallazgos libres 1](review/noncore_detections_01.png),
[hallazgos libres 2](review/noncore_detections_02.png) y
[controles de duplicado/núcleo](review/injections_03.png).

Calibración limitada: un solo fondo D, misma posición por tamaño, negro sobre
blanco de alto contraste, dos fuentes y blur leve. No representa texto oblicuo,
integrado a materiales, bajo contraste ni pseudo-glifos. Cero detecciones en D3
no prueba ausencia universal de texto legible. Las zonas no se realinearon.

## Validaciones y estados

[VALIDATION.json](VALIDATION.json): 19 imágenes OCR / 114 tiles, 881 hallazgos
brutos con grupos / 504 únicos; cero errores de motor y cero violaciones de
núcleo. 961 hashes de salida verificados, entrada y freezes intactos.
22 checks del runner + 22 de render/geometría PASS, sin OCR nuevo ni reescritura
de checks congelados. Las 17 inyecciones exteriores guardadas conservan el
núcleo exacto respecto de su base normalizada; sólo el control interior modifica
intencionalmente una copia sintética. Esto no valida pixel identity del piloto.

| Paso | Estado real |
| --- | --- |
| 1 · Freeze | CERRADO: freeze original y suplemento D3 commiteados antes de sus respectivas ejecuciones |
| 2 · OCR disponible | CERRADO: histórico preservado + D3 procesada. D1/D2 espaciales aún ausentes; v1 corrida 1 sin zona, sólo OCR bruto |
| 3 · Inyección completa | BLOQUEADO: 16/20 principales + 2 controles ejecutados; cuatro casos 80 px no caben en diseño congelado; falla 12 px reportada |
| 4 · Registro completo del test | BLOQUEADO por cobertura del paso 3; evidencia parcial, fallas y checkpoint registrados, sin declarar aprobación |

Aceptación global: **NOT_PASSED**. La falla histórica de frases permanece;
esta continuación no la corrige ni demuestra cobertura de 80 px. No confundir
checks de integridad PASS con sensibilidad/aprobación PASS.

Sólo se agregan evidencias bajo este suplemento y el delta de CONTRASTE 02 en
el checkpoint. No se generaron imágenes IA, no se alteraron entradas, reglas,
umbrales de deriva, SVS 1.10.0 STABLE, VSG ni GLIGEN. Sin push.
Resultados y presentación quedan para commit; el freeze ya está commiteado.
