# Campañas visuales SC: preparación operativa

## Carril VSG textual disponible

El manifiesto `validation/sc_multiagent/visual_campaigns/vsg_textual_20261013/MANIFEST.json` congela las fuentes, payloads y hashes de D, E y Kenny. La campaña consume seis salidas: una condición A y una B por caso.

Para cada salida, abrir una sesión nueva en la app de ChatGPT, adjuntar la fuente exacta y enviar la rama `.A` o `.B` del payload canónico sin cambios semánticos. Los hashes `condition_text_sha256` corresponden a la rama completa serializada como JSON compacto, conservando el orden original de claves, en UTF-8 y con un salto de línea final. Conservar la primera salida válida y registrar sesión, modelo, timestamp, ID y hash. No reintentar selectivamente. El reloj de 168 horas comienza con esos datos de la primera imagen válida; preparar archivos no lo inicia.

La comparación se presenta a Lean con códigos neutrales y la clave separada. Lean juzga preferencia, fallas críticas y casos no evaluables antes de revelar las condiciones. Generación y juicio visual son responsabilidades separadas.

## Carril de aporte de SC pendiente de fuente

`validation/sc_multiagent/visual_campaigns/sc_contribution_20261013/SOURCE_CANDIDATES.json` registra seis fuentes existentes y sus hashes. Son candidatas: su representatividad para la campaña actual permanece `UNKNOWN_PENDING_LEAN_CONFIRMATION`. No generar este carril hasta confirmar el conjunto o recibir reemplazos y congelar los payloads A/B.

## Límites vigentes

GLIGEN permanece pausado, D3/D4 siguen pendientes y VSG continúa en modo SHADOW. Esta preparación no autoriza forwards, entrenamiento, gasto adicional, reintentos selectivos ni evaluación visual por agentes. El checkpoint vivo conserva el estado operativo.
