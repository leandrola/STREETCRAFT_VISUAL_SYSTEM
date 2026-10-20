# Errata: `.DS_Store` en la lista intocable

El inventario de limpieza incluyó siete archivos locales `.DS_Store` ignorados
por Git dentro de `UNTOUCHABLE_HASH_PROVENANCE.csv`. Procedían exclusivamente
de `PACKAGE_MANIFEST.json`, que los enumeraba al capturar el árbol local; no
están versionados, no aparecen en el historial y el tag
`pre-cleanup-2026-10-20` no podía respaldarlos.

Lean autorizó su eliminación local el 2026-10-20 como parte del paso 8. No se
recrean ni se intenta recuperar su contenido: son metadatos del Finder y no
afectan el runtime, los contratos ni las pruebas estables de SVS 1.10.0.

Rutas eliminadas: `benchmark/.DS_Store`,
`benchmark/r2b_1_9_1/.DS_Store`, `validation/.DS_Store`,
`validation/camera_routing/.DS_Store`, `validation/cgc_e2e/.DS_Store`,
`validation/rr2_real_archive/.DS_Store` y
`visual_scene_graph/.DS_Store`.

Los hashes congelados y la lista original no se modifican. La verificación
final las registra como siete excepciones documentadas y exige coincidencia
estricta para las otras 1.058 rutas.
