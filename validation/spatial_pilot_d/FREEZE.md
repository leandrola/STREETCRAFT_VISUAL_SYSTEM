# SPATIAL-PILOT-D · protocolo previo a generación · v1

Autorización: instrucción de Lean del 2026-10-15. Piloto local independiente,
sin cambios a SVS 1.10.0 STABLE, VSG ni GLIGEN. Codex no genera imágenes.
Lean genera en ChatGPT y realiza la evaluación visual. Sin push autorizado.

Base de entrada: `e9cec79b38ba14171e6b89e036924caa69b4fddb`, árbol limpio.
Fuente: [R2B-191-D_source.jpg](../../benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg).
SHA-256: `282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc`.
Dimensiones observadas: 347 × 389, RGB. No usar el candidato histórico.

## Zonas

- PRESERVE: edificio principal, diner, billboard, señalética y escalera de
  incendios, sus relaciones y oclusiones. Implementación conservadora: todo el
  rectángulo de la fuente queda protegido, incluido su contexto observado.
- EDITABLE: contexto lateral, cielo, calle extendida y edificios vecinos,
  exclusivamente fuera de ese rectángulo. La autorización permite extender;
  no obliga a repintar contexto ya observado dentro del núcleo.
- UNKNOWN / NO REVELAR: superficies no observadas detrás de elementos,
  interiores no visibles y textos secundarios ilegibles. No reconstruirlos,
  revelarlos, corregirlos ni convertirlos en evidencia observada.
- INVENCIÓN PERMITIDA: arquitectura urbana norteamericana de 1960–1985,
  utilería no identitaria e infraestructura vial, sin texto legible. Es una
  elección de época para el entorno ficticio, no una datación de la fotografía.
  Sin nueva identidad geográfica, marcas o locales reconocibles.

## Geometría determinista fijada

Pillow 12.3.0, decodificación RGB sin corrección automática, resize LANCZOS
con factor exacto 2 en ambos ejes: 694 × 778. Guardar PNG RGB sin pérdidas.
Lienzo 1600 × 900, fondo neutro RGB(128,128,128). Núcleo en
`[453,61,1147,839)`: origen superior izquierdo, x/y, extremos derechos e
inferiores exclusivos. Sin recorte de fuente. La igualdad se mide respecto
del PNG reescalado persistido, no respecto de bytes JPEG ni de una nueva
decodificación en otra versión de biblioteca.

## Criterios eliminatorios

1. Núcleo final exactamente igual al PNG reescalado: todos los canales de
   todos sus píxeles, incluidos bordes, sin tolerancia. Verificación automática
   después de guardar y volver a abrir el compuesto. Guardar hashes de archivo
   y de píxeles RGB. Fallar si hay un solo canal distinto.
2. Cero texto legible inventado en el entorno, incluida duplicación de carteles
   de la fuente. Lean inspecciona salida GPT y compuesto a resolución completa.
   Ausencia de OCR o de hallazgos automáticos no certifica este criterio.
   Texto nuevo en la salida GPT elimina la corrida aunque el pegado lo tape.

El pegado puede reparar alteraciones de apariencia del núcleo de GPT, pero
debe registrarlas; no demuestra que GPT haya preservado la fuente. La igualdad
del núcleo se exige al compuesto final. La deriva geométrica tiene gate propio.

## Alineación: límites fijados antes de observar salidas

Aceptar únicamente PNG/JPEG RGB legibles, 1600 × 900. Otro tamaño se rechaza;
no normalizarlo silenciosamente. Modelo geométrico: traslación y escala uniforme
respecto del centro del núcleo, sin rotación, homografía ni deformación local.
Buscar centro hasta ±48 px por eje y escala 0.90–1.10. Fuera del rango o máximo
en su borde: rechazar, no ampliar la búsqueda a partir del resultado.

Aceptación: desplazamiento del centro euclídeo ≤16 px; |escala−1| ≤0.02;
correlación normalizada de luminancia global ≥0.92; correlación en cada uno de
cuatro cuadrantes ≥0.80; desviación estándar de cada parche ≥8/255. Comparar
con alternativas gruesas separadas >8 px o >0.02 de escala: margen de
correlación ≥0.03. Comprobar coherencia con búsquedas locales por cuadrante
de ±3 px: corrección residual euclídea ≤1.5 px en todos. Ausencia de textura,
ambigüedad, deformación o métricas insuficientes: ALINEACION_NO_CONFIABLE.
No forzar ni permitir override de los umbrales desde la línea de comandos.

Tras aceptar, alinear el entorno al sistema del lienzo y pegar el núcleo
original opaco. Transición exterior de 4 px, sin tocar ningún píxel protegido.
Registrar eventuales bordes exteriores sin cobertura tras transformar y
rellenarlos con el mismo neutro; nunca esconderlos del juicio de costuras.
El núcleo y su halo deben tener cobertura de la salida original.

## Evaluación visual y variación

Lean puntúa de 1 a 5 cada eje; no promediar un eliminatorio para compensarlo:

| Eje | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Costuras | Ruptura evidente | Unión visible pero utilizable | Unión imperceptible |
| Perspectiva | Incompatible | Desajustes menores | Continuidad coherente |
| Iluminación | Contradictoria | Diferencias visibles | Luz/color integrados |
| Época | Anacronismos claros | Coherencia parcial | Coherencia consistente |
| Calidad del núcleo frente al entorno | Desbalance severo | Desbalance perceptible | Calidad relativa equilibrada |

2 y 4 son niveles intermedios. Conservar cada salida, incluidos rechazos y
fallos, sin selección de la mejor como único resultado. Registrar por corrida
hashes, geometría, todas las métricas, eliminatorios, cinco puntajes, autor y
notas. Comparar rango, media y desviación estándar poblacional de cada eje y
de las derivas para todas las corridas evaluables; informar denominadores y
tasa de rechazo. Con menos de dos corridas: variación NO_EVALUABLE.
Este protocolo no autoriza una cantidad adicional de generaciones ni reintentos.

## Secuencia y trazabilidad

1. Commitear este protocolo y obtener su commit antes de crear el lienzo.
2. Crear núcleo/lienzo deterministas y registrar hashes y coordenadas.
3. Redactar prompt de solo contexto y commitearlo antes de cualquier generación.
4. Implementar y validar localmente el compositor; una prueba sintética de
   geometría no equivale a una salida GPT ni a aceptación visual. Ejecución con
   una salida real requiere que Lean entregue sus bytes; si faltan, paso bloqueado.
5. Consolidar registro real solo tras cerrar 4. Modelo/versión no expuestos
   por ChatGPT se registran UNKNOWN, con captura o declaración de procedencia;
   no inferir el modelo de imagen a partir del nombre del chat.

Ante bloqueo resolver dentro de alcance y, si persiste, registrar intentos y
detener ese paso y sus dependientes. No instalar ni modificar configuración
global para resolverlo. El checkpoint sigue siendo la única fuente operativa.
