# Contraste 02 — ejecución local congelada

Lean aprobó con «si» el overlay de la corrida 2 y su caja
`[0.20,0.00,0.89,0.94]`. [PROTOCOL.json](PROTOCOL.json) conserva los umbrales
y la whitelist del candidato. La preparación histórica no se reescribe.

## Antes de OCR

El freeze vincula protocolo, código, inventario, overlay, comprobaciones de
metadatos y hash del binario local. No ejecutar hasta que ese manifiesto esté
commiteado; el runner verifica bytes y commit. Swift compila contra el SDK
local; la consulta de capacidades y el lote vacío no reconocen imágenes.

```sh
swiftc validation/spatial_pilot_d/contrast_02/vision_ocr.swift \
  -o /tmp/contrast02-ocr.5L2pPS/vision_ocr
.venv-sc/bin/python validation/spatial_pilot_d/contrast_02/check_runner.py
```

El directorio temporal indicado ya fue creado para esta ejecución. Una réplica
puede usar otro directorio nuevo y pasar su binario; el hash debe coincidir con
el freeze. Si no coincide, detenerse: no sustituir el hash de una evidencia
existente. No instalar bibliotecas ni descargar modelos.

## Ejecución posterior al commit del freeze

```sh
.venv-sc/bin/python validation/spatial_pilot_d/contrast_02/run_ocr.py \
  --binary /tmp/contrast02-ocr.5L2pPS/vision_ocr \
  --run-id contrast02_20261019
```

La corrida tiene directorio exclusivo y no sobrescribe. El inventario vincula
los originales disponibles por ruta/hash; no copiar overlays como entradas.
Los tiles son temporales: sus hashes y geometría se guardan, y pueden
reconstruirse de los originales. stdout del OCR, hallazgos, cajas normalizadas y
originales, confianza, clase, grupos, deduplicación y recortes se conservan.
La confianza de un grupo es el mínimo de sus líneas; las líneas crudas no se
eliminan. Un error de motor/tiles detiene la tanda conservando lo ya obtenido.

No hay OCR dedicado al núcleo. Tiles que intersecan zona libre pueden incluir
contexto del núcleo; solape >30% de la caja de texto se ignora antes de cualquier
otra clasificación. La fuente completa no tiene zona libre: cero tiles no
prueba sensibilidad ni filtrado de texto. Para corrida 1 con zona no definida
y candidato 1.9.1 se hace sólo diagnóstico OCR bruto, sin veredicto.

Se preserva el criterio explícito: whitelist en zona libre =
ADVERTENCIA_DUPLICADO. Su falta de detección se reporta como hallazgo prioritario,
no se reetiqueta silenciosamente como VIOLACION.

Las salidas espaciales originales siguen ausentes. No se sustituye la salida
buena D3 para el control negativo ni para inyecciones; el test completo no
puede aprobarse sin esas mediciones. OCR sobre entradas disponibles sí procede.

Revisión visual de recortes y falsos positivos se registra aparte de las
predicciones inmutables, sin modificar umbrales después de ver resultados.
Los checks de metadatos no equivalen a OCR sobre texto renderizado.
