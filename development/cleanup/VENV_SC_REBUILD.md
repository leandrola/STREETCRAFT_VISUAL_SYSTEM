# Reconstrucción de `.venv-sc`

Estado: **CERRADO**. Este registro se toma antes de proponer eliminar el entorno local regenerable.

## Base observada

| Elemento | Valor |
| --- | --- |
| Python | 3.14.5 |
| Base del intérprete | `/usr/local/opt/python@3.14/bin/python3.14` |
| `Pillow` | 12.3.0 |
| `jsonschema` | 4.26.0 |
| Paquetes del sistema | deshabilitados |

## Receta de reconstrucción

Desde la raíz del checkout, con Python 3.14.5 disponible:

```sh
/usr/local/opt/python@3.14/bin/python3.14 -m venv .venv-sc
.venv-sc/bin/python -m pip install --upgrade pip
.venv-sc/bin/python -m pip install Pillow==12.3.0 jsonschema==4.26.0
PYTHONDONTWRITEBYTECODE=1 .venv-sc/bin/python benchmark/run_regression_suite.py
```

La última orden es una comprobación posterior de la reconstrucción; sus runners escriben bajo `validation/`, por lo que debe ejecutarse en una copia temporal del checkout como indica [VERIFICATION.md](../../docs/repository/VERIFICATION.md), no sobre evidencia congelada.

No hay un lockfile de dependencias en el repo. Esta receta fija las dependencias directas observadas; `pip` resolverá sus transitivas compatibles. Si una futura ejecución necesita repetibilidad de dependencias transitivas, debe generar un lockfile en un hito autorizado antes de retirar el entorno actual.
