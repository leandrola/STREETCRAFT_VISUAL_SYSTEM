# Cleanup 2026-10 verification

**PASS_LOCAL.** La verificación final comparó las 1.065 rutas intocables contra
los hashes congelados: 1.065 coincidencias y 0 diferencias. Las 12 pruebas
estables seleccionadas y las pruebas unitarias SC03 pasaron en una copia
temporal de los archivos versionados. El dry run aislado del paquete produjo
`0cee4e3f842c76d478c9be89034eaeae8c34b815f0202701c20a30f49498cee6`, igual a
la referencia congelada.

El paquete derivado `dist/streetcraft-generation/` contiene 34 archivos,
130.307 bytes y 2.959 líneas; el inventario pre-limpieza registró 5.654
archivos, 361.864.337 bytes y 1.384.234 líneas (sin `.git`, e incluyendo
archivos locales ignorados). Sus 19 inclusiones fuera de
`EXECUTION_READ_PATHS.csv` son contratos, documentación de generación y cinco
esquemas: `STREETCRAFT.md`, `CHEAT_SHEET.md`, protocolo de agente, contratos
CIL/CG-F/BD, RR2, SAR2/CGC, hardening/patch y los esquemas de contrato,
evidencia, referencia, SAR2 y backdrop. Están justificadas por la clausura de
documentación y contratos; no se incorporó evidencia congelada.

La única intersección con una carpeta excluida son
`visual_scene_graph/vsg_observer.py` (importación incondicional del
orquestador) y `visual_scene_graph/graph_locks.py` (dependencia transitiva).
Ambos son KEEP_RUNTIME autorizado. Las 28 rutas que el inventario había
clasificado ARCHIVE estaban bajo `outputs/vsg-2b-campaign/`, pero son locales,
ignoradas y no existen en `main` ni en el tag de respaldo; se conservan sin
cambio.

La evidencia detallada está en `CLEANUP_2026_10_FINAL_VERIFICATION.json`,
`GENERATION_BUNDLE_REPORT.json` y el manifiesto ignorado del paquete.
