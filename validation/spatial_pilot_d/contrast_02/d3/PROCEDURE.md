# D3 · vinculación y ejecución de inyecciones congeladas

Suplemento de ejecución, no revisión de criterios. Se preservan intactos
[PROTOCOL.json](../PROTOCOL.json), [FREEZE.json](../FREEZE.json) y todas las
predicciones anteriores. Base observada `978e9f275cc027e555f8195f95bb9673347b78f8`.

## Entrada y procedencia

Lean identifica expresamente el adjunto como original de la salida buena del
piloto espacial D, corrida 3, y pide continuar. [INPUT.json](INPUT.json) vincula
su ruta/hash. Tiene los mismos bytes que el adjunto anterior: PNG RGBA 1365×768,
alpha opaco; no se afirma 1672×941 ni se fabrica un receipt de generación.
Originalidad e identidad de corrida: declaración del operador, no prueba
independiente. Se conserva la discrepancia observada con el tamaño reportado
anteriormente. El OCR permite este tamaño/modo mediante su preprocesado fijo;
eso no admite la entrada al compositor ni demuestra preservación pixel-exacta.

## Orden de ejecución

1. Commitear este suplemento, input binding, código y checks antes de OCR D3.
2. Verificar freeze original y suplemento, binario y fuentes; conservar copia
   exacta del input, sin alterar el archivo adjunto.
3. Ejecutar el control negativo D3 con la caja normalizada espacial original
   `[453/1600,61/900,1147/1600,839/900]`. No ajustar geometría al ver OCR.
4. Tras terminar ese OCR, aplanar alpha sobre blanco y normalizar ancho 1600
   con Pillow/LANCZOS, como ya define el protocolo. Esta entrada da 1600×900
   por redondeo; registrar factores, no cambiar los bytes originales.
5. Renderizar y reconocer 20 casos planificados (5 alturas × 2 fuentes ×
   sharp/blur), más duplicado y control interior. Una falla de sensibilidad
   no detiene ni borra los otros casos. Un error de motor sí detiene la tanda.

## Detalles de render, fijados antes de OCR D3/inyecciones

Texto NOVA DEPOT en una línea, negro sobre backing blanco, una inyección por
imagen, centrada en la franja libre izquierda `[0,0,453,900)`. No se reubica,
rota, parte en líneas ni encoge para entrar. El programa elige el menor tamaño
de fuente cuyo alto de tinta alcanza el objetivo; recorta al ink bbox y, si es
necesario, remuestrea la máscara con LANCZOS al alto exacto, preservando aspecto.
Esto define el tamaño solicitado, no un ajuste a la franja. Registra tamaño de
fuente, tinta antes/después y método. Padding blanco de 4 px por lado.
Blur: GaussianBlur(0.6) sólo en máscara del texto, no en imagen/base/núcleo.

Fuentes: Arial Regular y Times New Roman Regular, hashes ya congelados.
Los casos de 80 px necesitan más de 453 px de ancho: el protocolo original
ordena SKIP y reporte cuando no caben. Se anticipan **cuatro casos sin cobertura**;
no presentarlos como falsos negativos OCR ni como 100% de recall >=20.
No se altera texto/zona para completar artificialmente esos casos.

Los controles usan TERMINAL DINER, Arial, 20 px, sharp: uno en la franja libre
(ADVERTENCIA_DUPLICADO), otro centrado dentro del núcleo
(IGNORADO_POR_SOLAPE, nunca VIOLACION). Este último modifica intencionalmente
una copia sintética del núcleo; no es un compuesto productivo y no altera
la entrada. Las otras inyecciones verifican núcleo idéntico a su base.

Cada imagen tiene truth JSON y hash ANTES de su OCR. Matching con verdad:
IoU >=0.30 y similitud >=0.80, tal como ya estaba congelado. Se separan
reconocimiento, clase esperada, omisiones y skips, con denominadores explícitos.
El campo annotation del runner genérico se conserva; la verdad de esta tanda
es INPUT.json y los truth JSON de cada inyección, no una anotación visual nueva.

## Comando

```sh
.venv-sc/bin/python validation/spatial_pilot_d/contrast_02/d3/run_injections.py \
  --binary /tmp/contrast02-ocr.5L2pPS/vision_ocr
```

Directorio exclusivo execution/: nunca sobrescribe. No hay cambios de umbrales,
whitelist, agrupación, motor, tamaños de tiles ni deduplicación. Cero imágenes IA,
cero red, cero cambios a SVS/VSG/GLIGEN. La admisión del compositor sigue separada.
