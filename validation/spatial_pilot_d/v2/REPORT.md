# Evidencia de continuación · 2026-10-17

Este informe conserva evidencia; el estado operativo está en
[CHECKPOINT.json](../../../development/coordination/CHECKPOINT.json).

## Decisión y freeze previo a reales

Fase 1 completada con normalización determinista explícita 1672×941 -> 1600×900
LANCZOS/Pillow 12.3.0, o identidad si ya es 1600×900. Entorno observado:
Python 3.14.5, macOS 15.7.9 x86_64. No hay prueba de estabilidad de tamaño
entrada/salida nativa del generador. Se preparó la variante 1672×941 como
artefacto geométrico no habilitado para corridas; no se generó ninguna imagen GPT.

Freeze local: `7f0b4989e7c91d113f2a34bfc110a6ce26cba9e7`.
SHA-256 de [FREEZE.json](FREEZE.json):
`ecb4be11ce70a3088edcc3372a81ddfcffe7e9a800459bd9c433e216f79fe4a8`.
El CLI verificó ese commit, todos los hashes del freeze y los baselines v1.
Originales reales procesados antes/después de este freeze en esta sesión: cero.

La corrección de aspecto es explícita: x=1600/1672, y=900/941. La escala residual
se mide después; no se compara 1672/1600 contra el límite de 0.02.

## Tests observados

28 comprobaciones finales PASS: nueve históricas y diecinueve adicionales,
agrupadas en veinte entradas de [CHECKS.json](CHECKS.json). No son imágenes reales.

| Requisito | Resultado |
| --- | --- |
| Identidad canónica / núcleo de variante nativa | PASS |
| 1672×941 -> normalización determinista | PASS, factores e interpolación explícitos |
| Normalización + dx=0 | PASS, alineación aceptada |
| Normalización + dx=8 | PASS, corregida |
| Normalización + dx=24 | PASS del test, corrida sintética REJECTED/POSITION_DRIFT |
| Escala residual dentro del límite | 1.02 PASS; 1.01 y 1.002 REJECTED por ambigüedad |
| Escala residual 1.03 | PASS del test, REJECTED/SCALE_DRIFT |
| Deformación no uniforme | PASS del test, REJECTED/LOCAL_DEFORMATION |
| SEAM GOOD / BAD +8 | NOT_RUN; dependencia Fase 2 |
| Núcleo guardado: 0 canales distintos | PASS en las tres composiciones sintéticas aceptadas |
| Corrupción de 1 canal | REJECTED en las tres; PASS de los tests |
| Tamaño no autorizado / RGBA | REJECTED; PASS de los tests |

El primer intento esperaba aceptar 1.01 y falló. Se conserva íntegro en
[CHECKS_INITIAL.json](CHECKS_INITIAL.json), no se reemplaza por el resultado final.
Las pruebas finales retienen los controles ambiguos como rechazos. El control
1.02 comprueba el límite inclusivo. Ningún umbral ni código v1 fue cambiado.
Por cuantización/margen, no se promete corrección de toda escala dentro del límite.

## Fase 2: búsqueda y bloqueo de procedencia

Después del commit de Fase 1 se inventariaron imágenes del repositorio y del
Escritorio. La lectura de `/Users/macbookpro/Downloads` devolvió
`Operation not permitted` incluso con ejecución autorizada fuera del sandbox;
no se modificaron permisos de macOS ni se intentó eludirlos.

Hallazgos, sólo metadatos/hash, sin alineación ni juicio visual:

- `Desktop/untitled folder/R2B-191-D_source_corrida_1.png`: RGB 1254×1254,
  SHA-256 `0f3a7fd2da3d24f5794265893b01e5b06fcd645d5068ce62280b174b199fb8c4`.
  Coincide con una salida VSG histórica. No es sustituto de la corrida espacial 1.
- `Desktop/untitled folder/R2B-191-D_source_corrida_2.png`: RGB 1672×941,
  SHA-256 `e6353e48ec334a1d44be0e7f48d098dab0125b060f0e2f5a53bd03c304799799`.
  Tamaño compatible, pero sin vinculación comprobada con canvas/prompt v1 ni
  número de corrida espacial. No se procesó ni se atribuyó por su nombre.
- `Desktop/untitled folder/R2B-191-D.jpg`: RGB 1086×1448,
  SHA-256 `7018985acddcf21f843ee04e5104f2044fe415c7423fa4deb2fe5532eced855a`;
  no es el formato requerido ni tiene binding de descarga espacial original.

Se solicitaron rutas e identificación al operador. Siguen sin identificar:

1. Descarga original de D / corrida espacial 1: nombre/ruta/hash/procedencia pendientes.
2. Descarga original de D / corrida espacial 2: nombre/ruta/hash/procedencia pendientes;
   el archivo del mismo nombre en Escritorio no acredita esa identidad.
3. Descarga original de D / corrida espacial 3: nombre/ruta/hash/procedencia pendientes.

La ingesta está preparada en [compose.py](compose.py), con comandos exactos y
placeholders declarados en [README.md](README.md). No se inventan nombres de
descarga, hashes, métricas ni ACCEPTED/REJECTED para inputs no identificados.

## Estado de fases al detener la tanda

- Fase 1: CERRADA, freeze commiteado y tests sintéticos PASS.
- Fase 2: BLOQUEADA por bytes originales identificados/procedencia; ninguna corrida real procesada.
- Fase 3: NO INICIADA, dependencia Fase 2. SEAM_GATE no implementado ni calibrado.
  La costura +8 es una limitación real informada por Lean. Falta además una
  referencia GOOD identificada y la vinculación del BAD; no se inventa calibración.
- Fase 4: NO INICIADA, dependencias 2/3. COMPOSITE_PIPELINE_VISUAL_EVALUATION
  permanece NOT_YET_EVALUATED. Sólo se transcriben las puntuaciones aportadas
  como [RAW_GENERATOR_VISUAL_EVALUATION](RAW_GENERATOR_SCORES.json), sin nuevo juicio.

v1 original PRESERVED, supuesto de tamaño de salida INVALIDATED_BY_OBSERVATION
(declaración de Lean). Alineación sintética VALIDATED únicamente para los casos
registrados. Alineación real NOT_VALIDATED. Preservación visual de GPT y garantía
pixel-exacta del pipeline son afirmaciones diferentes. No se declara éxito visual.

SVS 1.10.0, VSG y GLIGEN permanecen intactos y no se reabren. Sin generación por
modelos, instalaciones o cambios globales. Sin push; el pedido lo condiciona a
autorización explícita adicional. Se conservan los commits locales.
