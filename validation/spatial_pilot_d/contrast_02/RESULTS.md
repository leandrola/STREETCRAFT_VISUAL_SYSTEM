# Contraste 02 · resultado local y parada

## Hallazgo prioritario: detección eliminatoria incompleta

**MOVING se reconoce, pero NO se clasifica como VIOLACION:** confianza 0.50,
inferior a 0.60 congelado, aun siendo legible. Queda ADVERTENCIA; ver su
[recorte original](runs/contrast02_20261019/v1_D_2/crops/tile_003_line_003.png).
No se redujo el umbral para hacerlo pasar. Esto es un fallo de sensibilidad
eliminatoria, no ausencia total de reconocimiento de esa palabra.

**El criterio congelado de frases completas falla: 0/2.** JOHNSON, WAREHOUSE
y STORAGE sí se detectan individualmente como VIOLACION (confianza 1.00).
La imagen positiva, por lo tanto, SÍ queda eliminada por tres hallazgos reales.
Sin embargo, no hay coincidencias completas con JOHNSON WAREHOUSE ni STORAGE
MOVING bajo el criterio de similitud/grupos predefinido; no convertir detección
parcial en PASS de ese criterio. Las cajas axis-aligned de líneas inclinadas
se solapan verticalmente; la regla congelada exige gap no negativo y no las une.
No se agruparon manualmente para corregir el resultado ni se retocó el runner.

## Freeze anterior a OCR

Lean respondió «si» a la caja del overlay `[0.20,0.00,0.89,0.94]`.
Commit del freeze: `b971cf43997017fecc6059961cbcf6dfaa49417b`.
SHA-256 de [FREEZE.json](FREEZE.json):
`26302674549af7528e63948a6a76e7a6b4186ba0ea2098e70691e379330899c6`.
El CLI comprobó ese commit, todos sus hashes y el binario antes del OCR.
El candidato/informe de preparación permanecen como historia anterior a la aprobación.

Motor: Apple Vision VNRecognizeTextRequest revision 3, accurate, en-US,
language correction=false, automatic language detection=false, CPU solicitado,
minimumTextHeight=0, customWords=[], topCandidates=1. Sin red ni instalación.
macOS 15.7.9 build 24G830, Swift 6.1.2, Python 3.14.5, Pillow 12.3.0.
El compilador advierte que usesCPUOnly está deprecated; compilación exitosa,
sin afirmar una versión de pesos no expuesta. El hash del binario está congelado.

Se pasaron 22 [tests de lógica/coordenadas](RUNNER_CHECKS.json) y un lote vacío
antes del freeze; no son pruebas de sensibilidad OCR con imágenes.
Se conservan thresholds, whitelist y reglas después de ver resultados.

## Entradas y ejecución

[Inventario y hashes](PREPARATION.json). Dos salidas v1 disponibles fuera del
workspace, en Escritorio; fuente y candidato 1.9.1 dentro del repo. Ninguna se
modificó: hash previo/posterior coincidente. Las tres descargas espaciales no
están identificadas. Nueva búsqueda acotada repo/Escritorio no las encontró;
Downloads sigue denegado por macOS. Se pidió específicamente la buena D3.
Esto no impidió ejecutar las entradas disponibles.

| Entrada | Tiles OCR | Hallazgos crudos / únicos | Resultado |
| --- | --- | --- | --- |
| D v1 corrida 2 | 6 | 45 / 23 | 3 VIOLACIONES, 1 ADVERTENCIA, 19 IGNORADOS POR SOLAPE |
| D v1 corrida 1 | 9 | 26 / 14 | Sólo RAW_UNREVIEWED; ZONA NO DEFINIDA |
| Fuente D | 0 | 0 / 0 | Núcleo ocupa toda la imagen; zona libre vacía |
| Candidato D 1.9.1 | 12 | 24 / 19 | Sólo RAW_UNREVIEWED, sin veredicto por distinto encuadre |
| Piloto espacial D1/D2/D3 | — | — | Ausentes; no sustituidos |

27 tiles locales procesados, cero errores del motor. Preprocesado fijo:
ancho canónico 1600 preservando aspecto por redondeo, LANCZOS; tiles 800×800,
stride 640, bordes finales anclados, ampliación x2. Todas las transformaciones,
cajas, clases, confianza y hashes están en los [resultados persistidos](runs/contrast02_20261019/).
Los 95 hallazgos crudos/grupos tienen recorte individual; 56 representantes tras
deduplicación conservadora. La exportación completa está en [FINDINGS.md](FINDINGS.md).
El resumen original mantiene PENDING_VISUAL_REVIEW porque precede a la revisión;
ésta se añade separadamente en [VISUAL_REVIEW.json](VISUAL_REVIEW.json), sin reescribirlo.

## Tabla de aprobación y falsos negativos

| Caso | Esperado | Obtenido | Detección |
| --- | --- | --- | --- |
| Imagen v1 D2 positiva | Violación eliminatoria | Tres palabras eliminatorias | DETECTÓ a nivel imagen |
| JOHNSON WAREHOUSE, frase congelada | Coincidencia de frase VIOLACION | JOHNSON y WAREHOUSE separados, 1.00 cada uno; grupo ausente | NO DETECTÓ como frase; detección parcial |
| STORAGE MOVING, frase congelada | Coincidencia de frase VIOLACION | STORAGE=VIOLACION; MOVING=ADVERTENCIA 0.50; grupo ausente | NO DETECTÓ como frase; detección parcial |
| Texto del núcleo disponible D2 | Nunca VIOLACION | 19 únicos ignorados; cero violaciones de núcleo | IGNORÓ correctamente en este caso |
| Buena D3 | Cero violaciones | Entrada ausente | NO MEDIDO |
| Inyección 8/12/20/40/80 × 2 fuentes × sharp/blur | Recall 100% para >=20 | Base buena ausente | NO MEDIDO, no denominadores inventados |
| Whitelist duplicada en zona libre | ADVERTENCIA_DUPLICADO | Sin control de imagen | NO MEDIDO |
| Inyección sobre núcleo | IGNORADO/excluido | Sin control de imagen | NO MEDIDO |

No hay PASS global: falla un criterio congelado y faltan controles de sensibilidad
y especificidad. Cero tiles sobre la fuente no prueba filtrado de texto ni recall.
Los otros casos permanecen sin anotación de Lean y no cuentan para aprobar/fallar.

## Falsos positivos y recortes

Lista de falsos positivos «zona que a simple vista no es texto»: **ninguno
observado en los 56 recortes únicos revisados por Codex**. No es una tasa de
especificidad sobre un corpus completo ni la anotación final de Lean.
Hay errores de transcripción sobre texto real, registrados aparte (por ejemplo
NILLNOL en un recorte parcial del letrero histórico); no se cuentan como
detecciones de no-texto. Los duplicados de tiles no se inspeccionaron por separado.

Hojas para revisión de Lean:

- [D2, página 1](review_20261019/v1_D_2_page_01.png).
- [D2, página 2: advertencia MOVING](review_20261019/v1_D_2_page_02.png).
- [D1 sin zona definida](review_20261019/v1_D_1_page_01.png).
- [Histórico, página 1](review_20261019/legacy_191_D_page_01.png).
- [Histórico, página 2](review_20261019/legacy_191_D_page_02.png).

## Estado y parada

1. **CERRADO:** aprobación registrada, protocolo/ejecutor congelados en commit antes de OCR.
2. **CERRADO para entradas disponibles:** OCR y recortes persistidos, incluidos fallos;
   casos ausentes excluidos explícitamente, sin bloquear los disponibles.
3. **BLOQUEADO:** falta original de buena D3. Se buscó y pidió al operador; no se
   reemplaza por fixture, canvas, v1 o candidato histórico. Sin inyecciones renderizadas.
4. **BLOQUEADO para cierre integral:** registrado todo lo realizado y la causa
   de parada; sensibilidad y control negativo no completos.

No hay generación IA ni cambio de inputs, SVS 1.10.0 STABLE, umbrales de deriva,
VSG o GLIGEN. No se ejecutó composición ni se abrió un SEAM_GATE. Sin push por
este agente. Se observó el commit externo 01b42e3 integrando la documentación
pendiente anterior, sin colisión con este freeze; no se atribuye al agente.
