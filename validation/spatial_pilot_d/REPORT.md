# Evidencia de entrega local · 2026-10-15

Base: `e9cec79b38ba14171e6b89e036924caa69b4fddb`, árbol inicialmente limpio.
Congelamiento de zonas/criterios/umbrales:
`ce681b0c6df133e2f9900583ce9370d819e77d28`.
Commit posterior de lienzo y prompt:
`b62ad278d6bb09704b1358f316650b4dca5c0862`.
Modelo generador y versión: UNKNOWN / no ejecutado por el agente.
Salidas reales del piloto disponibles: 0. Juicio visual: no realizado.

## Secuencia ejecutada

1. Lectura de autoridad, checkpoint, protocolo y preservación. Fuente histórica
   inspeccionada y vinculada por SHA-256, sin reutilizar su candidato como fuente.
2. Zonas, geometría, evaluación y umbrales congelados en commit antes del lienzo.
3. LANCZOS ×2 con Pillow 12.3.0; PNG RGB persistidos. Igualdad del núcleo en el
   lienzo verificada tras reabrirlo. Hashes en [CANVAS.json](CANVAS.json).
4. Prompt de solo contexto commiteado antes de toda generación del piloto.
5. Compositor local implementado y probado exclusivamente con geometría sintética.
   Parada en paso 4: no hay bytes de salida GPT para ejecutar la composición real.
   El paso 5 no se abrió; no existe registro consolidado de corridas reales.

## Intentos y observaciones

- La primera invocación Git dentro del sandbox falló con `invalid active developer
  path /Library/Developer/CommandLineTools`. La comprobación de solo lectura con
  permisos por operación encontró Git 2.51.2 y Python 3.14.5 ya instalados.
  No se instaló software ni se alteró configuración global. El entorno existente
  del repositorio aporta Pillow 12.3.0; numpy y OpenCV no están disponibles y no
  fueron necesarios. Una invocación de shasum falló por biblioteca Perl bloqueada;
  los hashes efectivos se calcularon con hashlib.
- La primera prueba mostró un sesgo de −0.002 de escala por soporte del filtro
  de reducción fuera del rectángulo. Se corrigió recortando antes de reducir,
  sin cambiar el protocolo. El control identidad mide escala 1, traslación 0,
  correlación 1 y píxeles finales exactamente iguales al núcleo.
- La corrección reveló un rechazo conservador: control con dx=5, dy=−3 y escala
  1.012. La geometría se recupera correctamente, pero el margen entre alternativas
  es aproximadamente 0.0261, inferior al 0.03 congelado. Resultado del piloto:
  **ALINEACION_NO_CONFIABLE por ambigüedad**, sin compuesto forzado. El test inicial
  esperaba aceptación y falló; la prueba final conserva este caso y exige su
  rechazo. No se relajó el criterio para obtener aprobación.
- Las métricas y resultados finales de controles, incluidos rechazos, están en
  [LOCAL_CHECKS.json](LOCAL_CHECKS.json), vinculados a los hashes del compositor
  y del script de comprobación. PASS allí significa comportamiento técnico
  esperado, no aceptación de todos los controles ni aptitud visual.

## Límite y parada

Pasos 1, 2 y 3: CERRADO. Paso 4: BLOQUEADO por ausencia de salida original de
ChatGPT; el script está listo, pero ninguna composición real fue ejecutada.
Paso 5: BLOQUEADO por dependencia del 4. No se sustituyó esa evidencia por una
imagen histórica, una simulación ni un modelo de imagen ejecutado por el agente.

El desbloqueo requiere el archivo original que genere Lean con el lienzo y
prompt congelados. Su modelo/versión/id/fecha se consignarán según evidencia
del operador o UNKNOWN. La existencia del script no acredita alineación de una
salida futura. Si resulta incierta, se conservará el rechazo.

Solo se modificaron archivos del piloto y el delta de su clave en el checkpoint.
No se tocó SVS 1.10.0 STABLE ni se reabrieron VSG/GLIGEN. Cero llamadas a modelos
de imagen; ningún nuevo gasto de generación. Uso/cuota del agente: UNKNOWN.
