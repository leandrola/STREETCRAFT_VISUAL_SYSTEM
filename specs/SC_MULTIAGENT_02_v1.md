# SC · Equipo en operación: evidencia visual y mejora acotada

**ID:** SC-MULTIAGENT-02 · **Versión:** 1.0 · **Fecha:** 2026-10-12  
**Estado:** SPEC_READY. No acredita implementación ni campañas ejecutadas.  
**Predecesora:** SC-MULTIAGENT-01 / STREETCRAFT_SUBAGENTS_SPEC_v1.md.  
**Decisiones de base:** STREETCRAFT_v12.md, secciones 6–10.  
**Destino:** Codex local en VS Code + generación en ChatGPT conforme al entorno autorizado.

## 1. Qué obtiene Lean

Un equipo que trabaja sobre imágenes reales y devuelve una decisión comprensible: qué aporta SC, dónde falla y si las instrucciones derivadas de VSG merecen más inversión.

El entregable visible es un paquete de pares comparables, evaluaciones y una recomendación respaldada por evidencia. Si hay una falla reproducible corregible dentro del alcance, se permite una corrección acotada; su integración exige revisión y comprobaciones. No es obligatorio inventar una mejora para cerrar el diagnóstico.

**Tarjeta Go**

- Hito: poner al equipo a trabajar con evidencia visual real.
- Qué vas a ver: pares sin etiquetas, fallas señaladas y una recomendación breve.
- Qué cambia: paquetes de evaluación y, solo con evidencia, una corrección reversible.
- Cómo se revierte: revert del commit de la corrección; la evidencia histórica se conserva.
- Costo: cero gasto adicional; topes de imágenes separados en la sección 4.
- Recomendación: ejecutar primero el carril VSG disponible; preparar el de SC sin retrasarlo.

Esta spec no cierra VSG-2B, no reabre GLIGEN, no autoriza forwards ni entrenamiento y no modifica D3/D4.

## 2. Dependencias y entrada

La implementación comienza después de comprobar SC_MULTIAGENT_READY en el checkpoint vivo y su evidencia, incluida la modalidad de integración habilitada por 01. No basta con que existan TOML. Si 01 cerró con escritura centralizada, los subagentes de 02 analizan en lectura y el orquestador conserva la única escritura e integración.

Verificar:

1. HEAD, checkpoint, instrucciones aplicables y estado de cambios locales.
2. Modelos efectivos: implementador y verificador distintos.
3. Capacidad real de inspeccionar imágenes de cada agente que participe en revisión visual.
4. Contratos de cámara, identidad, texto y oclusión relevantes.
5. Estado de campañas previas: reutilizar resultados válidos, no duplicar por cambio de sesión.
6. Autorización específica para imágenes, separada de GLIGEN. Preservar el registro histórico.

Las dos campañas son independientes. Un bloqueo de fuentes de SC no impide preparar VSG si sus fuentes y payloads están correctamente ligados. No usar el caso C para reemplazar otro caso ni levantar su bloqueo histórico.

Si un agente no puede acceder a los píxeles, su revisión es documental. Nunca convertirla en PASS visual.

## 3. Organización del equipo

| Rol | Trabajo en esta spec |
| --- | --- |
| Orquestador | Congela inputs y reglas, distribuye tareas, reúne evidencia y escribe checkpoint |
| sc_architecture | Marca rasgos observados, identidad y partes desconocidas; revisa coherencia edilicia |
| sc_camera | Revisa horizonte, verticales, encuadre, perspectiva y oclusiones contra el comando elegido |
| sc_history | Revisa rasgos de época con evidencia; no inventa datación ni ubicación |
| sc_implementer | Prepara paquetes exactos y, si corresponde, una corrección en copia aislada |
| sc_verifier | Comprueba integridad, presupuestos, diff y resultados; modelo distinto del implementador |
| Lean | Juzga preferencia visual y decide inversión o alcance que siga pendiente |

Máximo tres subagentes simultáneos. El juicio de Lean no se sustituye por mayoría de agentes. La segunda opinión técnica se registra aparte.

## 4. Dos carriles, dos presupuestos

| Carril | Fuentes y condiciones | Techo |
| --- | --- | --- |
| VSG textual | D, E y Kenny; dos representaciones textuales con igual contenido de restricciones | 3 pares / 6 salidas |
| Aporte de SC | 6 fuentes representativas; prompt directo vs. comando SC con mismo resultado solicitado | 6 pares / 12 salidas |

No compartir ni transferir presupuestos. Los techos son totales por campaña, incluyendo salidas válidas ya realizadas. Registrar intentos fallidos, salidas y cualquier resultado ambiguo.

Una primera salida mala es un resultado válido para evaluación. No regenerar selectivamente. Una llamada cuyo resultado se desconoce no se reenvía automáticamente: reconciliar antes de consumir otro intento.

Esta spec no agrega un tercer presupuesto de imágenes para validar patches. Si una corrección requiere imágenes nuevas después de agotar el carril, conservarla como candidata pendiente de evidencia; no afirmar mejora visual demostrada.

Usar la vía de generación ya autorizada, sin cambio automático a API o proveedor. La existencia de subagentes en Codex no acredita acceso al generador de ChatGPT desde el CLI.

## 5. Preparación y trazabilidad

Crear paquetes bajo la estructura existente del repo; ubicaciones propuestas si no hay equivalentes:

- specs/SC_MULTIAGENT_02.md: esta spec incorporada al repo.
- validation/sc_multiagent/visual_campaigns/<campaign_id>/: inputs, manifiesto y resultados.
- docs/SC_VISUAL_CAMPAIGN_QUICKSTART.md: pasos breves de generación y evaluación.
- Un solo informe de cierre por campaña.

El manifiesto es evidencia de una campaña congelada, no otro checkpoint. El estado y las decisiones viven en CHECKPOINT.json.

Registrar por fuente y condición:

| Campo | Requisito |
| --- | --- |
| Identidad | campaign_id, case_id, condition_id y output_id |
| Fuente | Ruta local real, hash SHA-256 y procedencia conocida |
| Instrucción | Texto exacto UTF-8, hash y comando SC cuando corresponda |
| Runtime | Commit/versión del paquete adjunto y contratos utilizados |
| Generación | Fecha con zona horaria, modelo mostrado por la app y versión si está disponible |
| Resultado | Archivo, hash, intento, estado y error o incertidumbre |
| Evaluación | Preferencia, fallas críticas, observaciones y juez |

No afirmar semilla controlada si el entorno no permite fijarla. Usar UNKNOWN para modelo, cuota u otro dato no observable; no deducirlo del nombre comercial de la app.

Los outputs, anotaciones y paquete enviado deben permitir reconstruir qué vio cada evaluador.

## 6. Carril VSG: preservar el experimento acordado

1. Recuperar las fuentes y payloads A/B congelados de D, E y Kenny.
2. Comprobar bindings, integridad y correspondencia del contenido de restricciones.
3. Detener un caso con fuente ausente o no ligada; no generar una sustituta.
4. A es texto derivado del CGC; B expresa el mismo contenido desde el contrato VSG-2A. No convertirlo en comparación con/sin grafo.
5. Preparar seis tareas de generación en sesiones separadas, con fuente correcta y payload exacto.
6. Conservar las primeras salidas y registrar fallas, sin reintentos selectivos.
7. Presentar tres pares sin revelar condiciones a Lean.

El orquestador registra el evento de inicio del reloj de 168 horas con la primera imagen válida: timestamp, ID y hash. Si ya empezó, conserva el evento original. No reinicia por pausa, cambio de sesión o supervisor.

**Regla antes de evaluar:** se observó ventaja de B si gana al menos 2 de 3 pares y no presenta más fallas críticas. Empates cuentan como no ventaja observada. Comparar también las fallas por tipo, sin esconder diferencias tras un promedio.

La conclusión es anecdótica: respuesta a representaciones textuales, sin semillas controladas. No demuestra consumo estructural y no cierra VSG-2B. Una ventaja permite recomendar inversión; D3/D4 siguen siendo decisión de Lean. Sin ventaja, recomendar pausar inversión, no declarar inutilidad del grafo.

## 7. Carril SC: primera salida y evaluación mezclada

Seleccionar seis fuentes de uso real. R2b A–F son candidatas únicamente si sus fuentes están disponibles y cubren el uso de Lean. Si faltan imágenes, preparar lo demás y registrar SOURCE_SET_INCOMPLETE con los casos faltantes; no llenar huecos con casos sintéticos para cerrar.

Antes de generar:

- Congelar el resultado solicitado para cada par.
- A: prompt directo de una o dos frases.
- B: comando SC correspondiente, con runtime adjunto y opciones exactas.
- Mantener fuente y objetivo comparables. No diseñar un control deliberadamente débil.
- Congelar regla y versión del runtime. Si cambia el runtime a mitad de campaña, no mezclar resultados como un único test de versión.

Usar el umbral indicativo de la v12 como propuesta inicial: SC aporta si gana al menos 4 de 6 pares y no presenta más fallas críticas. Registrar antes de generar si Lean había fijado otro umbral; no ajustar después de ver resultados.

Evaluar identidad, texto, cámara y zonas ocultas presentadas como observadas. La preferencia estética no cancela una falla crítica. Reportar por caso y condición tanto incidencia como tipo de falla.

Seis pares no dan una conclusión estadística ni certifican BD01/BD02 formalmente.

## 8. Presentación de pares

Asignar códigos neutrales y mezclar lado y orden mediante un procedimiento reproducible. Guardar clave aparte; no exponerla en la hoja destinada a Lean.

Los archivos originales se conservan intactos. La vista comparativa puede escalar uniformemente para presentar, sin recortar áreas relevantes ni retocar el contenido. La hoja anota:

- Prefiero izquierda / derecha / empate.
- Falla crítica y dónde se observa.
- Motivo breve.
- No evaluable y causa, si corresponde.

Los especialistas pueden analizar antes o después, pero sus opiniones y la clave no deben contaminar el primer juicio de Lean. Luego revelar condiciones y consolidar. No prometer cegamiento del generador o del equipo que preparó los paquetes.

## 9. Primera corrección, si la evidencia la justifica

Máximo una falla prioritaria y una ronda de corrección técnica. Elegir por impacto visible y reproducibilidad.

El orquestador entrega una tarjeta de tarea con trigger concreto, comportamiento esperado, contratos afectados, archivos permitidos y modo de revertir. El implementador trabaja aislado.

Permitido: corregir contradicciones de precedencia, una compilación que pierde una restricción o instrucciones operativas confusas dentro del comportamiento existente.

Fuera de alcance: ampliar estilos, nuevos perfiles, rediseñar VSG, cambiar política de locks o reactivar modelos.

El verificador revisa el patch final contra el HEAD vigente y las comprobaciones pertinentes. Si no hay evidencia visual del candidato, el estado debe decir CANDIDATE_VISUAL_PENDING. La integración de un fix técnico probado no permite declarar mejora estética demostrada.

No atribuir al patch la diferencia prompt directo vs. SC: ese test mide el aporte de SC frente al control, no el efecto causal de la corrección frente a SC anterior.

## 10. Cierre y límites de trabajo

**Topes propuestos:** dos sesiones activas de hasta 60 minutos para ingeniería y consolidación, más las acciones de generación/evaluación dentro de los techos. Esperas por imágenes o juicio de Lean no consumen una sesión activa; tampoco reinician el reloj VSG.

Parar ante presupuesto agotado, binding ausente, cuota bloqueada, nueva decisión de alcance o incoherencia de runtime. No crear otra spec para postergar el cierre.

| Estado propuesto | Significado |
| --- | --- |
| SC_VISUAL_PACKAGES_READY | Paquetes completos; imágenes o juicio pendientes |
| SC_VISUAL_EVIDENCE_READY | Outputs íntegros y revisión técnica disponible; juicio de Lean pendiente |
| SC_VISUAL_DECISION_RECORDED | Juicio y recomendación registrados; ningún cierre formal de VSG implícito |
| SC_VISUAL_PARTIAL_BLOCKED | Un carril o parte de él sigue bloqueado; evidencias parciales conservadas |
| SC_FIX_VERIFIED / CANDIDATE_VISUAL_PENDING | Distingue corrección comprobada de candidata sin evidencia visual |

Adaptar nombres al esquema del checkpoint. Conservar estados separados por carril; no hacer depender uno del cierre del otro.

**Criterios:** primeras salidas conservadas; hashes y payloads verificables; presupuestos separados; juicio de Lean explícito o pendiente; modelos independientes registrados; cero ampliación de GLIGEN; reloj original preservado; límites de conclusión escritos.

Cierre para Lean en tres líneas: qué se vio / qué evidencia lo sostiene / qué conviene cerrar, pausar o mantener.

## 11. Ejecución y fuentes

Razonamiento recomendado: medium para paquetes y trazabilidad; high para revisión de conflictos y evaluación técnica de fallas. Las decisiones visuales pendientes siguen en Lean.

Esta spec usa decisiones del documento de SC, no presupone capacidades de generación en Codex. Para perfiles y delegación: [documentación oficial de subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), consultada el 12-oct-2026. Comprobar soporte real del cliente antes de ejecutar.

**Arranque:** verificar cierre de SC-MULTIAGENT-01; continuar campañas existentes o preparar las faltantes; ejecutar cada carril disponible con su presupuesto propio; no esperar a SC-MULTIAGENT-03 y no declarar cierre visual mediante pruebas documentales.
