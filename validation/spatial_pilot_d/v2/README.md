# SPATIAL-PILOT-D v2 · tamaño y alineación residual

[Política versionada](PROTOCOL.md). Mantiene el núcleo y canvas canónicos v1.
[Variante nativa](NATIVE_CANVAS.json) sólo documental: no acredita estabilidad de
ChatGPT ni autoriza nuevas generaciones. [Tests](CHECKS.json) son sintéticos.
El estado operativo vive exclusivamente en el checkpoint del repositorio.

## Ingesta de originales (después del commit del freeze)

Desde la raíz del repo, para cada descarga auténtica, ejecutar el mismo comando
con los valores reales del operador. No sustituir la ruta por thumbnails,
capturas o material recomprimido. Estos placeholders no nombran archivos recibidos.

```sh
.venv-sc/bin/python validation/spatial_pilot_d/v2/compose.py \
  '/RUTA/ORIGINAL_D_CORRIDA_1.png' --run-id D-001 \
  --original-download-attested --expected-sha256 HASH_ORIGINAL_64_HEX \
  --metadata-evidence 'Descarga original ChatGPT; fuente de procedencia del operador' \
  --generation-id UNKNOWN --generated-at UNKNOWN \
  --generator-model UNKNOWN --generator-version UNKNOWN

.venv-sc/bin/python validation/spatial_pilot_d/v2/compose.py \
  '/RUTA/ORIGINAL_D_CORRIDA_2.png' --run-id D-002 \
  --original-download-attested --expected-sha256 HASH_ORIGINAL_64_HEX \
  --metadata-evidence 'Descarga original ChatGPT; fuente de procedencia del operador' \
  --generation-id UNKNOWN --generated-at UNKNOWN \
  --generator-model UNKNOWN --generator-version UNKNOWN

.venv-sc/bin/python validation/spatial_pilot_d/v2/compose.py \
  '/RUTA/ORIGINAL_D_CORRIDA_3.png' --run-id D-003 \
  --original-download-attested --expected-sha256 HASH_ORIGINAL_64_HEX \
  --metadata-evidence 'Descarga original ChatGPT; fuente de procedencia del operador' \
  --generation-id UNKNOWN --generated-at UNKNOWN \
  --generator-model UNKNOWN --generator-version UNKNOWN
```

Reemplazar UNKNOWN sólo con metadatos observados; el modelo del chat no acredita
el modelo de imagen. Un SHA calculado de una copia no prueba su procedencia:
la declaración y descarga original siguen siendo necesarias.

El CLI conserva input.original y result.json en `v2/runs/<run-id>/`, nunca
sobrescribe. Código 0: ACCEPTED_ALIGNMENT_ONLY, con compuesto DIAGNÓSTICO y
core_exact comprobado al reabrir PNG. Código 2: REJECTED con razones y métricas
disponibles, conservando bytes originales. Un rechazo no produce compuesto.
Un input ausente o un freeze no commiteado bloquea antes de abrir una corrida.
No hay overrides de umbrales. SEAM_GATE no implementado todavía: ninguna salida
es visual_evaluable por el mero éxito del alineador/pegado.

## Tests sin alterar evidencia v1

```sh
.venv-sc/bin/python validation/spatial_pilot_d/v2/checks.py
```

Ejecuta los nueve controles previos, capturando su reporte sin sobrescribir
LOCAL_CHECKS.json histórico, y los controles de normalización/residual/identidad.
Los tests de costura GOOD/BAD quedan NOT_RUN hasta cerrar Fase 2 e iniciar Fase 3.
No hay calibración visual implícita ni evaluación de modelos.
