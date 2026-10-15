# Piloto local de composición · R2B-191-D

Congelamiento: `ce681b0c6df133e2f9900583ce9370d819e77d28`.
Lienzo y prompt: `b62ad278d6bb09704b1358f316650b4dca5c0862`.
El [checkpoint](../../development/coordination/CHECKPOINT.json), clave
`spatial_pilot_d`, conserva el estado operativo. Este documento es evidencia
y guía de uso; no sustituye el checkpoint.

## Entrega y límites

| Paso | Estado al entregar | Evidencia / causa |
| --- | --- | --- |
| 1. Congelar | CERRADO | [FREEZE.md](FREEZE.md), commit anterior a todo procesamiento |
| 2. Lienzo | CERRADO | [CANVAS.json](CANVAS.json), coordenadas y hashes; núcleo exacto comprobado tras guardar |
| 3. Prompt | CERRADO | [PROMPT.md](PROMPT.md), commit anterior a toda generación |
| 4. Composición | BLOQUEADO | Script y pruebas locales disponibles; falta una salida original de ChatGPT para medir su deriva, alinear y verificar su compuesto |
| 5. Registro | BLOQUEADO | Dependencia del paso 4; no se abrió ni se inventaron registros de corridas reales |

No hay generaciones GPT del agente ni resultados visuales del piloto.
SVS 1.10.0, VSG y GLIGEN se preservan. Sin push. No se abrió la clave de
campañas anteriores ni se retomó ningún supervisor.

## Archivos

- [FREEZE.md](FREEZE.md): zonas, eliminatorios, puntuación, variación y umbrales.
- [prepare_canvas.py](prepare_canvas.py): reescalado determinista y manifiesto.
- [core.png](core.png): fuente completa ×2, 694 × 778, PNG RGB.
- [canvas.png](canvas.png): 1600 × 900, núcleo `[453,61,1147,839)`, borde gris.
- [CANVAS.json](CANVAS.json): parámetros y hashes de archivo/píxeles.
- [PROMPT.md](PROMPT.md): texto para copiar en ChatGPT junto al lienzo.
- [compose.py](compose.py): registro geométrico, rechazo, alineación, pegado
  con halo exterior de 4 px y verificación exacta del PNG persistido.
- [check_composition.py](check_composition.py) y [LOCAL_CHECKS.json](LOCAL_CHECKS.json):
  pruebas sintéticas de geometría; no representan corridas GPT.
- [REPORT.md](REPORT.md): evidencia, intentos, límites y causa de parada.

## Uso cuando se aporte la salida real

En ChatGPT, adjuntar **canvas.png** y copiar el bloque de **PROMPT.md**.
Descargar cada archivo original y conservar también resultados rechazados.
Anotar fecha/hora, identificador de generación y modelo/versión efectivamente
expuestos; usar UNKNOWN para lo que ChatGPT no muestre. El nombre del modelo
de conversación no acredita el modelo generador de imagen.

Desde la raíz del repositorio, con el entorno existente que contiene Pillow
12.3.0, ejecutar (reemplazar la ruta de ejemplo por la descarga real):

```sh
.venv-sc/bin/python validation/spatial_pilot_d/compose.py /ruta/a/salida.png \
  --run-id D-001 \
  --generator-model UNKNOWN \
  --generator-version UNKNOWN \
  --metadata-evidence 'Declaración del operador: ChatGPT no expone modelo ni versión de imagen' \
  --generation-id UNKNOWN \
  --generated-at UNKNOWN
```

Usar identificadores nuevos para cada corrida. El script nunca sobreescribe una
corrida. Guarda bytes originales, hashes, parámetros y diagnóstico por corrida
en un subdirectorio `runs` del piloto. Ante rechazo devuelve código 2 y no
produce compuesto. Ante éxito técnico devuelve 0 y guarda un PNG compuesto;
eso **no** cierra la evaluación de texto inventado ni los puntajes visuales.

Los umbrales están fijados en el protocolo y no tienen override CLI. Una
salida de dimensiones o modo distintos se rechaza sin ajuste silencioso.
La búsqueda usa pasos de 8 px/0.01, refinamiento 1 px/0.002 y final 0.001;
el recorte a píxeles introduce cuantización, no precisión subpíxel garantizada.
Se admite solamente escala uniforme y traslación. Rotación/perspectiva o
deformaciones no tienen reparación automática. Correlación alta no demuestra
identidad semántica del núcleo GPT; se informa también su error antes del pegado.

Si falla, conservar el diagnóstico y cerrar la corrida como rechazo; no
retocar umbrales ni ampliar búsqueda para conseguir un PASS. Tras procesar una
salida real, reconciliar el paso 4 antes de abrir el registro consolidado del 5.
Lean evalúa ambas imágenes a resolución completa; un cartel nuevo en la salida
GPT elimina la corrida aunque el núcleo restaurado lo tape. La variación requiere
al menos dos corridas, sin selección retrospectiva de resultados.

## Reproducibilidad local

```sh
.venv-sc/bin/python validation/spatial_pilot_d/check_composition.py
```

Solo crea transformaciones de control en memoria y archivos temporales locales;
no llama modelos ni red. La preparación del lienzo usa creación exclusiva para
proteger los PNG persistidos: no volver a ejecutarla sobre la entrega existente.
