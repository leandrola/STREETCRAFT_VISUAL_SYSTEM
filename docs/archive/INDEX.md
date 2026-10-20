# Archive index

## `outputs/vsg-2b-campaign/` — NO APLICA: conservado localmente

Esta carpeta contiene 28 salidas locales de la campaña VSG-2B (dos corridas y
sus artefactos de contrato, grafo, contexto, request, runtime y reporte). No
forma parte de Git: `.gitignore` la excluye mediante `/outputs/`, `git ls-files`
no devuelve ninguna de sus rutas y tampoco existe en el tag
`pre-cleanup-2026-10-20`. Por lo tanto no se retira de `main`, no se mueve, no
se borra y no tiene respaldo en ese tag.

Resultados VSG congelados sí citan estas rutas locales, entre ellos
`validation/vsg_2b/N4S_RESULT.json` y `validation/vsg_2b/N5PV_RESULT.json`.
Esas citas documentan evidencia local; no convierten las salidas en contenido
versionado. Se conservan en disco como están.

## Corrección del inventario

`CLASSIFICATION_CANDIDATE.csv` de la rama `cleanup/inventory` tenía 28 filas
`ARCHIVE`, todas bajo `outputs/vsg-2b-campaign/`. La comprobación contra
`git ls-files` muestra que las 28 son ignoradas y ninguna está versionada.
No hay otra agrupación `ARCHIVE` en ese candidato: el inventario incluyó
archivos ignorados locales al medir el árbol y los presentó erróneamente como
candidatos para retirar de `main`.

## Excepción de runtime autorizada

`visual_scene_graph/vsg_observer.py` y
`visual_scene_graph/graph_locks.py` son **KEEP_RUNTIME**. El orquestador
estable importa el primero y éste importa el segundo; ambos forman parte del
paquete de generación. No son material archivable.
