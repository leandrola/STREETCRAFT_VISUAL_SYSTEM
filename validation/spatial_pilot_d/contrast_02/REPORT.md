# Contraste 02 — preparación previa a OCR

Fecha de instrucción: 2026-10-19. Base:
`fc4936282aa0f17698b0d7f5bb2f37d2a2b83474`.
Había cambios locales anteriores en el checkpoint y el informe v2 de reanudación;
se preservan y no se incluyen en el commit del candidato de este contraste.

## Hallazgo prioritario y bloqueo

**Detección de violaciones eliminatorias y duplicados: NO EVALUADA.** No hay
falsos negativos ni aciertos medidos todavía. No declarar cero violaciones.
El paso 1 requiere aprobación humana del overlay de la corrida 2 antes de un
freeze válido. Se preparó y mostró el [overlay](v1_D_2_zone_review.png) y se
solicitó confirmación de `[0.20,0.00,0.89,0.94]`. Sin respuesta registrada,
se detiene aquí; no se ejecuta OCR ni se renderizan inyecciones.

El commit del candidato sólo preserva la propuesta, NO acredita aprobación ni
un freeze habilitado. Tras aprobar/corregir la caja se debe completar el runner
con estas reglas, verificarlo sin OCR de casos, fijar el manifiesto final,
commitearlo y registrar su hash antes de reconocer imágenes. No hay resultados
que puedan usarse para ajustar umbrales o whitelist.

## Entradas

| Entrada | Disponibilidad | Uso previsto / estado |
| --- | --- | --- |
| D v1 corrida 1 | Externa disponible, Escritorio, RGB 1254×1254 | Matching fallido: ZONA NO DEFINIDA, sin veredicto |
| D v1 corrida 2 | Externa disponible, Escritorio, RGB 1672×941 | Positivo conocido según Lean; caja pendiente de revisión |
| Fuente D | En workspace, RGB 347×389 | Referencia de matching y núcleo; zona libre vacía |
| D 1.9.1 candidato histórico | En workspace, RGBA 1086×1448 | Sólo OCR bruto, jamás veredicto espacial |
| Piloto espacial D corridas 1/2/3 | Originales identificados no disponibles | No bloquean OCR de otras entradas tras freeze; buena D3 e inyección quedan sin evaluar |

Rutas exactas, hashes y tamaños en [PREPARATION.json](PREPARATION.json).
Se buscaron imágenes en repo/Escritorio/Downloads con rg; Downloads devolvió
`Operation not permitted`. No se alteraron permisos ni entradas.
La denominación v1 del contraste no atribuye las dos salidas antiguas a las
tres corridas espaciales ni reabre VSG o revela su clave A/B.

Matching multiescala de la corrida 1: NCC=0.7898405072 <0.80;
peor cuadrante=0.3735046150 <0.50; margen=0.0936919672.
Los parámetros se fijaron en [prepare.py](prepare.py) antes de buscar;
no se relajaron tras el fallo. No son umbrales del alineador del piloto.
La mejor caja candidata NO se adopta como núcleo. No se emite veredicto.

## OCR local y reglas propuestas

Tesseract no encontrado en PATH; pytesseract, EasyOCR, PaddleOCR, cv2, numpy y
bindings Python Vision/Quartz/objc no instalados en el entorno del piloto.
Alternativa sin instalación: Apple Vision mediante Swift local.
Consulta de capacidades con [ocr_preflight.swift](ocr_preflight.swift) equivalente
al comando ejecutado: revisión 3 disponible, nivel accurate, en-US entre idiomas
soportados. Swift 6.1.2; macOS 15.7.9, build 24G830. La primera importación tardó
minutos compilando módulos, pero terminó con código 0; no hubo request de imagen.
No se usaron servicios OCR, descargas ni red. Capacidad consultable no equivale
a una medición de sensibilidad: la ejecución OCR de imágenes sigue NOT_RUN.

[PROTOCOL_CANDIDATE.json](PROTOCOL_CANDIDATE.json) fija la whitelist completa,
similitud 0.80, solape >30%, confianza 0.60, tres alfanuméricos, altura equivalente
10 px y tiles 800×800 con paso 640, ampliación x2. Define deduplicación, recortes,
anotaciones, excepciones sin veredicto y la futura matriz sintética de 20 casos.
Arial Regular y Times New Roman Regular se cargaron con Pillow 12.3.0 y tienen
hashes vinculados; no se renderizó la matriz sintética.

Conflicto textual de la spec preservado: 1c exige ADVERTENCIA para duplicados
de whitelist; la regla final los menciona junto a eliminatorios. Se mantiene
la clasificación explícita de 1c, ADVERTENCIA_DUPLICADO, y la omisión de un
duplicado seguirá siendo hallazgo prioritario. No se convierte silenciosamente
en VIOLACION. El criterio de placas no exime automáticamente una cadena que
cumpla los tres umbrales; se conserva una marca para revisión humana.

El recuento vacío sobre la fuente (núcleo completo) no prueba por sí solo que
se filtre bien texto legítimo. Hará falta el control de solape/inyección para
ese criterio. OCR no garantiza detectar glifos pseudo-legibles.

## Tabla de resultados (no ejecutados)

| Caso | Esperado | Obtenido | DETECTÓ / NO DETECTÓ |
| --- | --- | --- | --- |
| D v1 2: JOHNSON WAREHOUSE | VIOLACION | NOT_RUN, pendiente freeze | NO MEDIDO |
| D v1 2: STORAGE MOVING | VIOLACION | NOT_RUN, pendiente freeze | NO MEDIDO |
| Piloto D3 buena | Cero VIOLACIONES | MISSING_INPUT | NO MEDIDO |
| D v1 1 | Sin anotación; sin veredicto por zona no definida | Matching fallido; OCR NOT_RUN | NO MEDIDO |
| D histórico 1.9.1 | OCR bruto sin veredicto | NOT_RUN | NO MEDIDO |
| Inyecciones 8/12/20/40/80 px × dos fuentes × sharp/blur | 100% >=20 px | NOT_RUN, falta base buena y freeze | NO MEDIDO |
| Duplicado en zona libre | ADVERTENCIA_DUPLICADO | NOT_RUN | NO MEDIDO |
| Texto en núcleo | IGNORADO / excluido; nunca VIOLACION | NOT_RUN | NO MEDIDO |

Falsos positivos: **NOT_EVALUATED**, no lista vacía interpretada como cero.
Recortes de hallazgos: no existen sin OCR. El único archivo visual de esta
preparación es el overlay de geometría; no es un resultado OCR.

## Estado y límites

1. BLOQUEADO: aprobación humana del overlay; freeze válido todavía no existe.
2. BLOQUEADO por paso 1; entradas ausentes no bloquean futuras entradas disponibles.
3. BLOQUEADO por paso 1 y base buena no disponible; sin sustitución silenciosa.
4. BLOQUEADO para cierre integral; se registra únicamente preparación y parada.

No se modifican SVS 1.10.0 STABLE, umbrales congelados, v1/v2, VSG ni GLIGEN.
Cero imágenes IA; overlay determinista autorizado. Sin push. El estado operativo
permanece en [CHECKPOINT.json](../../../development/coordination/CHECKPOINT.json).
