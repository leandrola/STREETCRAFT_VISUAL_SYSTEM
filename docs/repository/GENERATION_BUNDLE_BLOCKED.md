# Bloqueo del paquete de generación

**Paso:** 3 · **Estado:** BLOQUEADO

## Causa

El contenido exigido es contradictorio: debe contener todas las rutas de `EXECUTION_READ_PATHS.csv`, pero debe excluir `visual_scene_graph/` completo.

El runtime estable no permite esa exclusión. [streetcraft_orchestrator.py](../../integration/streetcraft_orchestrator.py) añade `visual_scene_graph/` a `sys.path` y realiza una importación incondicional de `vsg_observer`; este módulo importa `graph_locks`. Ambas rutas figuran en `EXECUTION_READ_PATHS.csv` y son necesarias incluso cuando la solicitud usa `vsg.mode=OFF`.

## Intento reproducible

Se creó una copia temporal que incluyó las demás dependencias ejecutables y excluyó `visual_scene_graph/`. La importación de `streetcraft_orchestrator` falló antes de ejecutar un dry run:

```text
ModuleNotFoundError: No module named 'vsg_observer'
```

No se modificó ningún archivo del repositorio durante la prueba. El directorio temporal se dejó fuera del checkout.

## Consecuencia

No se puede construir el paquete pedido ni demostrar que el dry run conserve el hash `0cee4e3f…` bajo las restricciones actuales. Por regla de parada, no se retiran `outputs/vsg-2b-campaign/`, no se actualiza documentación de estado, no se ejecuta verificación final y no se publica `cleanup/execute`.

## Decisión necesaria

Elegir una de estas opciones antes de reanudar:

1. Permitir que el paquete incluya únicamente `visual_scene_graph/vsg_observer.py` y `visual_scene_graph/graph_locks.py` como dependencias ejecutables no gobernantes.
2. Autorizar un cambio separado del runtime estable para importar VSG de manera diferida, con nueva línea base y revisión de la lista intocable.
3. Revisar el requisito de dry run para que no importe el orquestador estable.
