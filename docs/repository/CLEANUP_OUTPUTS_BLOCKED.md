# Bloqueo del retiro de `outputs/vsg-2b-campaign/`

**Paso:** 4 · **Estado:** BLOQUEADO

## Hallazgos verificados

1. `git ls-tree -r pre-cleanup-2026-10-20 -- outputs/vsg-2b-campaign` no devolvió rutas: el directorio no forma parte del árbol de `main` ni del tag de respaldo.
2. `git ls-files --stage -- outputs/vsg-2b-campaign` no devolvió rutas: no hay archivos indexados que `git rm` pueda retirar.
3. `git check-ignore -v` confirmó que `/.gitignore` ignora `/outputs/`.
4. El directorio local contiene 28 archivos y ocupa 712 KiB, pero no tiene respaldo Git en el tag creado para este paso.
5. No está en las listas de rutas intocables ni de lecturas del runtime estable. Sin embargo, varios resultados y runbooks VSG congelados conservan referencias textuales a `outputs/vsg-2b-campaign/` como salida histórica o destino de reproducción.

## Consecuencia

La instrucción de retirarlo de `main` con `git rm` no es aplicable: no está en `main`. Borrar la copia local ahora tampoco cumpliría la condición de respaldo por tag y podría dejar rutas históricas sin su salida local. No se ejecutó `git rm`, no se borró ningún archivo y no se modificó evidencia VSG.

## Decisión necesaria

Indicar una política explícita para los 28 archivos locales ignorados:

1. conservarlos como salida local hasta una política de archivo externo; o
2. autorizar un respaldo fuera de Git y, después de verificarlo, una eliminación local.

Hasta esa decisión, los pasos 5–8 permanecen sin iniciar por la regla de parada.
