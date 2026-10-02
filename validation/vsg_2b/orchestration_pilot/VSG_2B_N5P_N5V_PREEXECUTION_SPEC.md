# Streetcraft · VSG-2B · N5P + N5V · Plan y validación antes de autorizar ejecución

Versión 1.0 · 2026-10-02 · Base: N4S_SETTINGS_DECISION_READY.

**Esta entrega crea la spec conjunta. No ejecuta N5P/N5V ni implementación, pesos, entrenamiento o pruebas.** La solicitud del usuario autoriza preparar el plan y el prerregistro sobre el diseño propuesto. No registrar automáticamente aceptación/aplicación de la enmienda ni permisos de cómputo.

## 1. Objetivo y salida revisable

Preparar juntos:

- **N5P:** implementación mínima viable, dependencias, entorno, datos, recursos, costo y secuencia de gates.
- **N5V:** protocolo preregistrado que permita distinguir consumo causal, preservación visual y aporte incremental, con controles, métricas, resultados posibles y presupuesto de pruebas.

El plan debe dimensionarse según el protocolo. Una lista de módulos sin pruebas o un protocolo sin recursos no cierra el hito conjunto. El resultado será un paquete concreto para decidir qué etapa autorizar después, con alcance/caps y dependencias explícitos. No prometer desbloqueo de VSG-2B por completar documentación.

Diseño de referencia: `VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0`, aún `PROPOSED_NOT_APPROVED` y `applied=false` según los artefactos revisados. N5 puede planificarlo condicionalmente bajo esta solicitud; no necesita detener la preparación para pedir una aceptación rutinaria. Toda implementación/activación sigue pendiente de decisión explícita.

## 2. Insumos y contrato que se conserva

Leer los documentos reales N4S: decisión, resultado, INPUT_MANIFEST y SETTINGS_AMENDMENT_PROPOSAL. Verificar sus hashes y el estado final. El resultado revisado acredita los inventarios históricos de 751 archivos y nuevos de 760; esos conteos no sustituyen medir el checkout actual.

Recuperar N3/N4 y política/harness para resolver una discrepancia concreta; no repetir N1–N4. Fijar HEAD y versiones de código/checkpoint/Transformers. Conservar cambios previos y evidencia congelada, D/E/Kenny/C, CGC, schemas, allowlists y `PROPOSED_SCOPE.diff` sin aplicar.

Invariantes del diseño leído:

- A: `common` + JSONL exacto por texto, canal R ausente. B: `common` textual + diez registros por puerto tipado aprendido. No B serializado al prompt ni A parseada para alimentar R.
- Mismo checkpoint compuesto, patch, fuente, asociaciones compartidas S, preprocesamiento, ruido, scheduler y settings dentro de cada comparación A/B.
- Bloques de 75 tokens y resampler compartido de 128 slots. A: 7.305 tokens de contenido/7.307 con especiales; B: 5.686/5.688. Son conteos del ensamblado propuesto, no receipts de un bridge.
- Candidato beta1.0 y control diagnóstico beta0.3; las dos configuraciones comparten el patch futuro y difieren solo en beta. El control no representa un backend upstream histórico ejecutado.
- Fuente D de 347×389 con padding de borde a 512; M_KEEP1 y reinyección de latentes. No prometer conservación exacta de píxeles ni autorizar edición por evidence.region.
- La ruta neutral conserva atención/FF/S; retirar R no equivale a introducir keys cero ni a desactivar todo el fusionador.
- Con el schedule propuesto, 50 pasos implican 51 llamadas UNet según la configuración fijada. Revalidar el resolver y PNDM; no convertir esa cifra en una constante para cualquier scheduler/settings.

`common` ya contiene relaciones protegidas: el ensayo mide **aporte incremental de la representación/canal**, no acceso exclusivo de B a hechos ausentes en A.

## 3. Alcance de preparar N5P/N5V

Permitido: leer código/configs/documentos existentes, revisar fuentes primarias, calcular presupuestos y memoria teóricos, redactar módulos/patches propuestos como especificación, protocolos, manifests de planificación y solicitudes concretas de recursos. Revisar metadata de datos/proveedores si hace falta, sin contratar ni adquirir corpus.

Fuera de alcance: modificar modelo/cliente operativo, instalar pipelines, descargar pesos, generar tensores con modelos aprendidos, ejecutar forwards, entrenar, generar/decodificar imágenes, activar settings, admission, cambiar política de counters, X1, commit, push, branching o ZIP. Los ejemplos de código o diffs inertes se rotulan como diseño no aplicado.

Si datos, entorno o tarifas no pueden verificarse, registrar `UNKNOWN` con la forma de resolverlo. No inventar costos exactos ni extender el presupuesto para ejecutar una medición. Las versiones y capacidades citadas deben apoyarse en fuentes primarias fijadas.

## 4. N5V · Definir primero qué demostrar y qué no concluir

### 4.1 Tres preguntas separadas

| Pregunta | Evidencia futura necesaria | Conclusión máxima |
|---|---|---|
| ¿B se consume causalmente? | Mutación/ablación aislada, hooks reales, persistencia temporal y efecto final mayor al ruido de repetición | Consumo/dependencia computacional acreditados |
| ¿La salida conserva el contrato? | Revisión visual de relaciones, texto literal, identidad, geometría y P0/PR0/PR1 contra fuente/contrato | Preservación en casos efectivamente revisados |
| ¿B aporta frente a A? | Comparación emparejada con pesos/controles iguales y endpoint incremental preregistrado | Efecto incremental observado en la muestra; generalización solo si el diseño lo permite |

No derivar preservación ni utilidad semántica de hashes, cobertura de tokens o sensibilidad numérica. Una igualdad A/B puede ser evidencia válida: no forzar una ventaja de B para producir PASS. Tampoco cerrar el gate original si faltan sus requisitos de cobertura o evidencia.

### 4.2 Protocolo obligatorio

Fijar antes de observar outputs:

1. Hipótesis primaria, unidad de análisis, comparadores, endpoints primario/secundarios, rúbrica y reglas de empate/UNKNOWN/INCONCLUSIVE.
2. Casos y seeds permitidos por campaña; fuente/contrato/authority hashes. C sigue excluido. No ampliar E/Kenny automáticamente desde un canal cuyo vocabulario inicial es LEFT_OF/ABOVE/inversas; mapear compatibilidad de cada caso y rechazar lo no soportado.
3. Corpus de entrenamiento, validación y test separados por escena y provenance. D/E/Kenny/C no entran en entrenamiento ni tuning. Los casos diagnósticos derivados no son nuevas verdades del corpus congelado.
4. Lectura literal protegida, especialmente TERMINAL DINER en D; definir legibilidad/igualdad visual y registrar incertidumbre. OCR puede asistir, pero no reemplazar una revisión visual necesaria.
5. Definición observable de LEFT_OF/ABOVE y de preservación de identidad/geometry/layout, con anotaciones de referencia, tolerancias y tratamiento de oclusión. No inventar umbrales después de ver resultados ni usar solo centroides si no capturan el contrato.
6. Método de revisión: orden aleatorio, labels A/B ocultos al evaluador cuando sea viable, fuente disponible, roles y resolución de discrepancias. Definir el requisito de independencia; si no hay evaluador disponible, queda como prerrequisito, no como revisión ya satisfecha.
7. Umbral de efecto incremental útil y ausencia de regresión protegida. Justificar con la finalidad del piloto/criterios vigentes; diferenciar propuesta de umbral, calibración independiente y evaluación final.
8. Tamaño muestral y alcance de inferencia. Si la cuota vigente de ocho intentos solo permite una sonda diagnóstica, declararlo; no afirmar eficacia poblacional o cobertura general a partir de pocos pares.

Si hace falta calibrar la rúbrica, diseñar una calibración independiente del test principal y presupuestarla por separado. No ajustar el criterio sobre las mismas salidas que luego se usan para demostrar éxito.

### 4.3 Matriz de pruebas

Conservar las ocho pruebas N4S y mapearlas a acciones/receipts concretos: control negativo beta0.3, full schedule explícito, neutralización/ablación, mutación aislada, persistencia hasta decode, réplica numérica, revisión semántica/preservación y texto/input completo.

Definir qué resultado falsifica cada hipótesis, qué prerrequisito falta y qué acciones están prohibidas. Mutar LEFT_OF→RIGHT_OF en un diagnóstico no permite admitir el payload mutado como D original; los hashes de campaña deben seguir rechazándolo.

En el documento, todas las pruebas aprendidas/visuales siguen `NOT_RUN`. Ninguna cifra calculada o check simbólico es un receipt de modelo.

## 5. N5P · Plan de implementación mínimo y dependencias reales

Descomponer el desarrollo en entregas verificables, cada una con archivos/módulos futuros, input/output, dependencias, esfuerzo estimado, test de aceptación, rollback y acción que requerirá autorización:

| Etapa futura | Entrega a dimensionar |
|---|---|
| Contrato y entorno | Resolver estricto de settings, schemas/envelope, logs, versión/lock de entorno y control RNG |
| Patch compartido | Puerto tipado de UNet y fuser con S común/R opcional; misma arquitectura/pesos en A/B |
| Texto completo | Chunking exacto y resampler128 compartido; objetivo de aprendizaje y pruebas semánticas |
| Fuente y canal R | Asociación visual compartida, projector relacional, máscaras y fuente separadas de autoridad de edición |
| Datos/aprendizaje | Corpus licenciado, splits, módulos/pesos congelados y aprendidos, pérdidas y parámetros elegidos |
| Carga/sonda real | Verificación local de pesos, hooks, determinismo, controles temporales y sensibilidad |
| Campaña visual | Manifest/admisión posteriores según política vigente y protocolo N5V |

No presentar los pesos nuevos como existentes. Identificar cuánto trabajo corresponde a resampler, projector de fuente, projector relacional y deltas/LoRA; cerrar las elecciones que pueden cambiar sustancialmente recursos. Si persiste una elección esencial, usar estado condicional con esa dependencia precisa.

Fijar versiones compatibles de Python, PyTorch, Diffusers y Transformers como propuesta basada en sus requisitos. El entorno local Python3.14.5 sin esas dependencias no prueba incompatibilidad total ni capacidad operativa: planificar y verificar el runtime futuro, sin instalarlo en este hito.

Hardware y memoria: separar almacenamiento de pesos, parámetros entrenables, activaciones, gradientes, optimizer states, precisión, batch y acumulación. Proponer hardware solo con supuestos trazables; cualquier requisito medido permanece `NOT_MEASURED`. No reciclar 24–48 GiB, 50–200 GPU-h o 25–59 días-persona de N3 como mediciones nuevas.

Datos: requisitos de derechos para imagen, anotación y transformación; disponibilidad, volumen, roles de anotación, costo y adquisición pendientes. No asumir que el corpus de evaluación proporciona datos suficientes o permiso de entrenamiento.

## 6. Un presupuesto conjunto de llamadas, recursos y dinero

Construir un DAG de ejecución futuro y una tabla única de **receipts/ejecuciones**, enlazando cada prueba a receipts que puede compartir. No sumar otra vez un recorrido utilizado para réplica, persistencia y revisión semántica. Una referencia compartida conserva su ID; no se cuenta como un par adicional.

Para cada acción, registrar:

- Etapa, input/config/weights/RNG hash, módulos invocados, batch/CFG, cache y cantidad máxima de ejecuciones.
- Llamadas CLIP, resampler, projector S/R, VAE encode/decode, UNet y safety. Hooks internos se registran sin doble contabilización; un fuser llamado aisladamente sí tiene su unidad.
- Invocaciones y unidades aprendidas procesadas por batch, además de trayectorias/timesteps/outputs/attempts. Un batch CFG de dos no equivale a dos invocaciones del UNet, aunque consume cómputo para dos ramas internas.
- Tiempo, GPU-h, descarga, almacenamiento y costo, con fórmulas, tarifas/fuentes/fecha si disponibles, escenarios y techo solicitado.
- Reserva previa, cancelación, fallos, retry máximo explícito y condiciones STOP. No retries implícitos ni presupuesto aprobado por defecto.

Punto de control: la estimación N4S sin batching es98 bloques A + 76 B + 1 negativo + 5 labels = 180 llamadas CLIP, antes de resampler/VAE/projectors/UNet. Caching/batching puede reducir invocaciones si sus claves y dependencias lo permiten; no afirmar ahorro sin enumerarlo. Compartir una cache requiere identidad completa de inputs, pesos, dtype y posición/contexto relevantes.

Toda trayectoria completa es cómputo generativo aunque no se decodifique una imagen. No denominarla “simple forward offline” para eludir counters. Una salida decodificada requiere la clasificación/autorización correspondiente aunque se use solo para diagnóstico.

Respetar los ocho intentos de campaña, fallos incluidos. Resolver si controles/diagnósticos caben con los pares oficiales y cómo los clasifica la política. Si no caben, reducir honestamente el alcance o presentar una propuesta separada de presupuesto/política; no declarar exentos los diagnósticos ni ampliar la cuota automáticamente. Forwards aislados permanecen sin clasificación aprobada.

El presupuesto final debe tener caps numéricos de acciones aprendidas/attempts/outputs y una fórmula completa de costo. Si faltan tarifas, corpus, memoria o cómputo, se puede cerrar el plan como revisable condicionado, pero `execution_budget_complete=false`; esa etapa no queda lista para autorizar ejecución.

## 7. Gates y resultado conjunto

Cada fase futura debe tener entrada, éxito, rechazo, STOP y rollback. Priorizar: contrato/entorno → datos y pesos aprendidos → determinismo/causalidad → preservación/semántica → evaluación incremental. No iniciar la etapa siguiente si falla una precondición.

Registrar resultados futuros distinguibles: error técnico, canal sin sensibilidad final, incumplimiento protegido, efecto incremental no detectado, evidencia inconclusa por tamaño/cobertura y efecto observado. Mantener esos resultados bajo los gates originales del piloto; no inventar un PASS global nuevo que los sustituya.

Estados de **preparación**, propuestos:

- `N5P_PLAN_READY_FOR_REVIEW`: tareas/dependencias y recursos detallados, limitaciones identificadas.
- `N5V_PREREGISTRATION_READY_FOR_REVIEW`: protocolo completo, límites de conclusión y presupuesto enlazado; umbrales pendientes explícitos.
- `N5PV_JOINT_REVIEW_READY`: ambos coherentes, referencias/counters coincidentes y paquete de decisiones concreto.
- `N5PV_INCOMPLETE_<MOTIVO>`: falta una decisión o evidencia esencial para preparar el paquete.

Separar readiness para revisar de readiness para ejecutar. Campos obligatorios: `planning_requested=true`, estado real de aprobación de enmienda, `settings_applied=false`, `implementation_authorized=false`, `execution_authorized=false`, `execution_budget_complete`, `semantic_criteria_frozen` y lista de dependencias abiertas. Un umbral desconocido no puede coexistir con un prerregistro declarado congelado para ejecución.

VSG-2B sigue `BLOCKED / PENDING_VISUAL`; N3/N4/N4S históricos permanecen intactos; `production_authorized=false`, `provider_READY=false`; C bloqueado y X1 sin aprobar. La petición actual permite preparar este paquete sin conceder aprobación de los pasos posteriores.

## 8. Entregables propuestos en el repositorio

Verificar colisiones y conservar documentos anteriores. Crear:

- `visual_scene_graph/pilot/N5P_IMPLEMENTATION_AND_RESOURCES_PLAN.md`.
- `visual_scene_graph/pilot/N5V_SEMANTIC_VALIDATION_PREREGISTRATION.md`.
- `validation/vsg_2b/N5PV_RESULT.json`.
- `validation/vsg_2b/n5pv/EXECUTION_BUDGET_PROPOSAL.json`: DAG/receipts, conteos, caps/costos y clasificación propuesta.
- `validation/vsg_2b/n5pv/VALIDATION_MATRIX.json`: hipótesis, endpoints, controles, métricas, criterios y estados `NOT_RUN`.
- `validation/vsg_2b/n5pv/INPUT_MANIFEST.json`: baseline actual, hashes de propuesta N4S/inputs y lista permitida.

El resultado enlaza todos los documentos y registra HEAD, cambios previos, comandos de verificación, invariancia, límites, recursos desconocidos, decisions_needed y la primera etapa concreta solicitada. Presentar al usuario una tabla breve de cada decisión, alcance que habilitaría, caps propuestos y prerrequisitos; no pedir autorización para un paquete incompleto ni asumirla.

## 9. Operativa, verificación y prompt

Reasoning Alta para arquitectura, método experimental y presupuesto; Media opcional para tablas/checks mecánicos. Conservar el modelo del usuario. Techo heredado ≤40 puntos porcentuales de la ventana 5-hour desde saldo inicial observable: preflight 4, método 10, implementación 10, presupuesto 10, cierre 6. Plan Limits 5-hour/Weekly no visibles = `UNKNOWN`, sin certificación porcentual.

La ejecución documental N5P/N5V conserva Archive/predicciones/imágenes/pares nuevos=0/0/0/0, forwards con pesos=0 y entrenamientos=0. Verificar invariancia y consistencia de los seis entregables; no añadir tests de implementación que aún no existe ni repetir suites globales sin motivo.

> Prepará N5P y N5V con esta spec, sobre los artefactos reales N4S y el diseño VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0. La solicitud autoriza planificación/prerregistro, no aceptación automática ni aplicación de la enmienda. Definí primero hipótesis, controles y criterios, y dimensioná después la implementación mínima y un presupuesto consolidado por receipts sin doble conteo. Cerrá versiones, datos/licencias, módulos aprendidos, entorno, riesgos y rollback; diferenciá estimaciones de mediciones. Conservá los ocho intentos y no declares exentos los diagnósticos. Si hay dependencias o umbrales/costos desconocidos, señalalos y no declares ejecución lista. Entregá N5P, N5V, matriz, presupuesto, inventario y resultado conjunto listos para revisión, con las decisiones futuras concretas. Reasoning Alta; Media opcional para tareas mecánicas. Sin código operativo modificado, pesos, forwards, entrenamiento, generación, settings aplicados, política modificada, admission, X1, commit, push, branching ni ZIP.

## Fuentes y alcance

Esta spec usa la decisión N4S y SETTINGS_AMENDMENT_PROPOSAL leídos en GitHub el 2026-10-02. El resultado N4S consultado declara scans finales PASS y preservación histórica 751 / nueva 760; esta preparación no repite esos scans completos. La enmienda consultada sigue propuesta y sin aplicar.

- [Decisión N4S](https://github.com/leandrola/STREETCRAFT_VISUAL_SYSTEM/blob/main/visual_scene_graph/pilot/N4S_CLOSURE_AND_SETTINGS_DECISION.md).
- [Resultado N4S](https://github.com/leandrola/STREETCRAFT_VISUAL_SYSTEM/blob/main/validation/vsg_2b/N4S_RESULT.json).
- [Enmienda versionada](https://github.com/leandrola/STREETCRAFT_VISUAL_SYSTEM/blob/main/validation/vsg_2b/n4s/SETTINGS_AMENDMENT_PROPOSAL.json).

Toda capacidad aprendida, costo y validación visual requieren evidencia posterior. El paquete prepara una decisión informada de ejecución y conserva el gate original de VSG-2B.
