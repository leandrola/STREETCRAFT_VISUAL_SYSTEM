# Streetcraft · Análisis y plan (versión personal)

**Fecha:** 3 de octubre de 2026 · **Base analizada:** SVS 1.10.0 STABLE (README + zip del repo, ver límites en la sección 4) · **Revisión externa:** Claude · **Versión 8:** incorpora las decisiones de Lean (tope de 7 días para VSG, delegación de los "cómo" técnicos), la lectura de `ROADMAP.md`, `CHECKPOINT.json` y los documentos N2/N4/P1R, las objeciones de GPT a las versiones 4 y 5 (sección 11), la verificación sobre el repo vivo del 3 de octubre de 2026 y la estimación de la ruta estructural entregada por GPT/Codex (sección 8.4) y el registro de la pausa en el checkpoint (commit `33b6581`, informado por GPT/Codex) · **Versión 9 (9-oct-2026):** retira la regla de "un hito abierto a la vez" por decisión de Lean (hitos en paralelo con agentes coordinados por un orquestador) y fija que `CHECKPOINT.json` lo escribe un solo agente (secciones 3, 5, 6, 9, 10 y 11) · **Versión 10 (11-oct-2026):** por decisión de Lean, reinicia el reloj de VSG, retira las expectativas de fechas de calendario y todo contenido que no provenga de documentación oficial o del propio repo, y elimina la aprobación previa de Lean para generar imágenes (secciones 1, 5, 8, 9, 10 y 11) · **Versión 11 (11-oct-2026):** incorpora el dictamen de GPT sobre la v10 (APROBADO CON CAMBIOS): separa las autorizaciones, define el reloj, corrige qué compara el A/B, completa las reglas de paralelismo y corrige evidencia y procedencia (secciones 1, 5, 6, 8, 9, 10 y 11) · **Versión 12 (11-oct-2026):** corrige dos inconsistencias señaladas por GPT y registra las confirmaciones de Lean (reloj de 168 horas y continuidad)

---

## 1. Resumen ejecutivo

- Streetcraft (SC) es un **proyecto personal** cuyo output de reinterpretación ya le sirve a Lean. El problema no está en el output: está en **cómo se desarrolla**.
- Las tres fallas (sección 3): specs interminables hacia VSG, hitos y pruebas que ya no se entienden, y un workflow manual que obliga a Lean a decidir arquitectura sin ser arquitecto de sistemas visuales.
- **Principio central:** *Lean decide qué quiere ver; el agente decide cómo construirlo.* Lo único que Lean puede juzgar sin ser arquitecto es **la imagen**, así que toda decisión de arquitectura debe presentarse con su efecto visible (o con "no cambia el output").
- **VSG, tope de 7 días con el reloj reiniciado (decisión de Lean):** según los documentos del repo, la **ruta estructural** (consumidor aprendido sobre GLIGEN) requiere desarrollo de modelo, por lo que no se puede prometer su cierre dentro de ese tope (hay una estimación registrada, cuyo informe no fue auditado). La vía práctica identificada para obtener imágenes dentro de ese tope con tu flujo actual es una **exploración visual de instrucciones derivadas de VSG**, que no cierra VSG-2B ni juzga la arquitectura. GPT/Codex entregó la estimación de la ruta estructural, Claude coincidió en pausarla y la pausa quedó registrada en el checkpoint (commit `33b6581`, informado por GPT/Codex; sección 8.4). El reloj (168 horas desde la primera imagen válida) arranca con la primera imagen de la exploración y no tiene fecha de calendario; la generación de imágenes ya no requiere aprobación previa de Lean.
- **Primer paso:** reencuadre y marco de decisión, apoyándose en el `CHECKPOINT.json` existente en lugar de crear estructuras paralelas (sección 6).
- **Cambio de la v9 (decisión de Lean):** se retira la regla de un hito abierto a la vez para ir más rápido, con varios agentes coordinados por un orquestador. Para que el paralelismo no rompa el estado se fijan dos reglas: `CHECKPOINT.json` lo escribe un solo agente y cada agente tiene archivos propios (sección 9.1).
- **Continuidad sin Lean:** posible, pero con un sobre de autorización acotado y topes duros (sección 9).
- **Test liviano de 12 imágenes** (SC vs. prompt directo) para saber si SC aporta frente a un prompt simple (sección 7).

---

## 2. Contexto (confirmado por Lean)

| Tema | Estado |
| --- | --- |
| Naturaleza | Proyecto personal, no producto. Lean paga ChatGPT Plus. |
| Uso | Sesión de chat nueva en la app de ChatGPT; adjunta el repo de GitHub una vez, la imagen fuente y corre el CLI (ver `CHEAT_SHEET.md`). GPT es el motor de imagen que mejor le resultó; no probó otros. |
| Runtime real | ChatGPT leyendo las specs del repo. El orquestador Python es una formalización/verificador, no lo que corre en cada uso. |
| Archive | Un tablero de Pinterest: fuente de consulta, no Canon. |
| VSG | Replanteo de arquitectura inspirado en grafos (ej: el modelo del conectoma de la mosca). Hoy en modo sombra. |
| Desarrollo | App de ChatGPT + VS Code/Codex; Lean es el orquestador humano entre ambos. |
| Agentes | GPT (ChatGPT/Codex) construye; Claude actúa como revisor externo. Lean contrasta ambas posturas (sección 11). |

---

## 3. Las tres fallas de desarrollo

| Falla (según Lean) | Causa probable *(hipótesis a partir de lo visto en el repo)* | Remedio |
| --- | --- | --- |
| **1. Cada vez más tiempo entre specs infinitas para llegar a VSG** | La hoja de ruta de VSG tiene 8 etapas (0, 0.5, 1, 1.5, 2A, 2B, 3, 4) y la ruta estructural agrega N1–N5 y M1–M3; cada una produce su spec y su informe (`validation/` tiene 490 archivos). Los hitos se producen más rápido de lo que se usan: hoy hay 0 imágenes generadas y `model_tests: NOT_RUN`. | **Hitos en paralelo** (v9, sin el límite de un hito a la vez), con un tope de **7 días** para VSG y un entregable observable por hito; abrir hitos nuevos sigue requiriendo la tarjeta "Go". VSG-3A/3B, VSG-4 y VSG-5 en pausa (sección 8). |
| **2. Hitos y pruebas interminables; ya no sabe qué aprueba** | Los criterios de aceptación los escribe el mismo sistema que implementa, en lenguaje técnico (ej.: `K1_CORPUS_RECOVERY_DRY_RUN_PASS`, `N4_SCOPE_CHANGE_REQUIRED`, compuertas D1–D4). Aprobar eso exige entender el sistema por dentro. | **Tarjeta "Go" en lenguaje llano** con qué vas a ver distinto, costo y una opción recomendada por defecto. Regla: si el hito no se explica en 3 líneas sin siglas, no se aprueba. |
| **3. Workflow manual y dependiente de Lean; necesita que la arquitectura se construya con menos inferencia suya** | Lean transporta contexto entre chats y toma decisiones técnicas sin ser arquitecto. Hay fricción concreta: N2 informa que la spec se buscó en Downloads y estaba en `Documents/specs vsg`, fuera del repo; N2 y N4 informan que no hay `AGENTS.md`. | **Marco de decisión escrito una sola vez** (`AGENTS.md`): el agente decide los "cómo" técnicos reversibles; Lean aprueba cambios visibles, gasto de tiempo/alcance y lo irreversible. Specs dentro del repo. Verificación automática + revisión por un segundo modelo. |

**Por qué delegar el "cómo" es razonable acá (Lean aceptó este reparto):** Lean no puede juzgar arquitectura, pero sí puede juzgar imágenes. El control de calidad no depende de que entienda el diseño, sino de que cada hito traiga evidencia visible (antes/después) o declare que no cambia el output. La delegación necesita tres salvaguardas: checks determinísticos (tests, schemas, hashes), revisión por un modelo distinto del que implementó y registro de cada decisión en el estado del proyecto.

---

## 4. Valoración de SC (resumida)

**Fortalezas**
1. Principio rector claro y bajado a mecanismos: Identity Lock, Semantic Text Lock, `LOCKED_UNKNOWN`, Reference Isolation, distinción observado/inferido.
2. Código del orquestador de buena calidad: estados explícitos (`GENERATION_READY`, `BLOCKED_*`, `REVIEW_REQUIRED`), locks derivados de la configuración. Tests del orquestador: 12/12 OK al ejecutarlos.
3. Interfaz de comandos clara y componible (`/sc-2a`, `/sc-rdr2-elevation`, `/sc-preserve`…).
4. Honestidad del estado: "Visual PASS: 0, Pending: 10"; los documentos N2/N4/P1R declaran sus límites (`STATIC_ONLY`, `NO_COMPATIBLE_BACKEND_VERIFIED`).
5. Resultado visual convincente en el caso R2B-191-F: texto y layout se conservan; deriva menor en escalera de incendios, ventanas y techo.

**Riesgos que siguen vigentes**
- **Sin comparación contra un prompt directo:** no se sabe cuánto aporta SC sobre pedirle lo mismo al modelo (sección 7).
- **Validación circular:** los "19/19" y "25/25" son sobre corpus armados con las mismas herramientas que construyen el sistema. Sirven como regresión.
- **Adherencia entre sesiones no medida:** cada sesión nueva interpreta el repo adjunto (873 archivos, 52 MB) y no se sabe cuánto lee realmente.
- **Evidencia solo con un motor (GPT):** el Core se declara agnóstico del motor, pero no hay validación con otro.
- **VSG es una hipótesis, no una medición:** el grafo lo construye un modelo interpretando la imagen.
- **La ruta estructural es un proyecto de desarrollo de modelo,** no una integración: sin backend compatible, con pesos, corpus, derechos y presupuesto pendientes (sección 8).

**Alcance de la revisión (y límites)**
- **Revisado:** README, estructura del zip, orquestador completo, `CHEAT_SHEET.md`, `STREETCRAFT.md`, `agent/AGENT_PROTOCOL.md`, `ROADMAP.md`, `development/coordination/` (incluido `CHECKPOINT.json`), README del piloto VSG-2B, y el caso visual F. Ejecutados: tests del orquestador.
- **Leído solo parcialmente:** `N2_ARCHITECTURE_DECISION.md`, `N4_GLIGEN_FEASIBILITY_RUNBOOK.md` y `P1R_SCOPE_DECISION.md` (los primeros ~3 KB de cada uno).
- **No revisado:** N1, N3, N5PV, `reference_runtime/`, el resto de `visual_scene_graph/` y los 490 archivos de `validation/`. No se ejecutó el benchmark VSG (falta `jsonschema`; no hay `requirements.txt`). El Archive externo no está en el repo.
- **Versión del repo:** la revisión se basa en el zip subido. GPT/Codex confirmó sobre el repo vivo (3-oct-2026, commit `f7c594e`, árbol limpio) que el checkpoint coincide con el del zip en los campos verificados (sección 8.1, punto 4). Lo que no se verificó en vivo sigue dependiendo del zip.

---

## 5. Plan priorizado

**Hacer ahora (en orden)**

1. **Reencuadre y marco de decisión** (sección 6).
2. **Carril de 7 días de VSG:** exploración visual de instrucciones derivadas de VSG, con decisión final (sección 8). No depende del reencuadre ni requiere aprobación previa de Lean; puede correr en paralelo con los pasos 1 y 3.
3. **Flujo mínimo apoyado en el estado existente:** `AGENTS.md`, specs dentro del repo, un comando único de verificación y la vista en llano del `CHECKPOINT.json`.
4. **Continuidad con sobre acotado** (sección 9): objetivo confirmado por Lean.
5. **Test liviano de 12 imágenes** (sección 7).
6. **Paquete de runtime chico + `/sc-status` + registro simple** por sesión (versión del repo, fecha, CLI usado).

*Nota (v9): la exploración visual y la continuidad del desarrollo avanzan por separado. La regla de "un hito abierto a la vez", acordada antes con GPT, queda retirada por decisión de Lean (9-oct-2026): los hitos pueden avanzar en paralelo bajo las reglas de la sección 9.1.*

**Se baja de prioridad o se pausa (por ser un proyecto personal)**

- Ruta estructural de VSG (desarrollo de modelo): **pausada** y registrada en el checkpoint (commit `33b6581`) tras la estimación de la sección 8.4 (25–59 días-persona de referencia y un escenario de infraestructura de USD 113,19, que no es un mínimo ni el costo total); sin ampliar implementación ni pruebas hasta que Lean decida el esfuerzo (D3/D4).
- Runner automático por API de imágenes (trabajo de construcción; el costo no está verificado en documentación oficial).
- Experimento grande de 48–72 imágenes con segunda persona y umbrales estadísticos.
- Compuertas formales G1–G3, VSG-3A/3B, VSG-4, VSG-5, el cierre formal de VSG-2B y la validación formal de BD01/BD02.
- Limpieza del README pensada para extraños y el tema de derechos de las referencias de Pinterest.
- Probar otro motor (Gemini): no urgente.

---

## 6. Primer paso: reencuadre y marco de decisión

**Objetivo:** que Lean vuelva a entender qué está aprobando y que el agente construya con menos inferencia suya, **sin crear estructuras documentales paralelas**.

**Qué incluye (una sesión):**
- Una **vista en llano generada desde `CHECKPOINT.json`** (no una fuente de verdad nueva): cada hito abierto clasificado en **cerrar / pausar / mantener**, con la recomendación del agente y 2 líneas de justificación, sin siglas sin definir.
- Un **`AGENTS.md`** con el marco de decisión (qué decide el agente, qué decide Lean), las reglas de paralelismo de la sección 9.1 (escritor único del checkpoint y archivos propios por agente), el tope de sesiones por hito y el sobre de autorización de la sección 9. Se mantiene como archivo separado porque no existe (lo informan N2 y N4 y se confirmó en el repo vivo) y es el archivo de instrucciones para agentes de código (su lectura automática por cada herramienta no está verificada en documentación oficial).
- Las **decisiones se registran en el campo `decisions`/`events` del checkpoint**, no en un `DECISIONS.md` aparte.
- **Specs dentro del repo** (`specs/`), no en carpetas locales.
- La definición de "terminado" para VSG (sección 8) y el tope de **7 días**, ya decidido por Lean.

**Recomendación:** que la vista generada la revise también un segundo modelo antes de que Lean la apruebe.

**Plantilla de tarjeta "Go" (para todos los hitos):**

```
HITO: <nombre en lenguaje llano>
Qué vas a ver distinto: <cambio visible en el output, o "nada visible">
Qué cambia / qué no cambia: <2 líneas>
Cómo se revierte: <rama/commit>
Evidencia que te voy a mostrar: <imágenes, resultado de verificación>
Costo: <sesiones/tiempo>
Mi recomendación (por defecto): <opción>   ← respondé "default" para aceptarla
```

**Tarjeta "Go" de este primer paso (lista para pegar a GPT / Codex):**

```
HITO: Reencuadre y marco de decisión (v0)
Qué vas a ver distinto: nada visible en el output; vas a tener el estado del proyecto en llano y reglas escritas de quién decide qué.
Qué cambia: se agregan AGENTS.md (confirmado que no existe), una vista en llano generada desde CHECKPOINT.json y la carpeta specs/.
Qué no cambia: core/, schemas/, hardening/, visual_scene_graph/ y validation/ (solo lectura). No se crea ninguna fuente de verdad paralela al checkpoint.
Cómo se revierte: un solo commit; se revierte con `git revert`.
Evidencia: diff con solo archivos nuevos (nada borrado); la vista con cada hito clasificado.
Costo: una sesión.
Mi recomendación (por defecto): aprobar la clasificación propuesta; el tope de VSG ya está fijado en 7 días.
Decisión de Lean: corregir o aprobar la clasificación de hitos y el marco.
Próxima acción: la exploración de la sección 8, que no requiere aprobación previa.
```

---

## 7. Test liviano de 12 imágenes

*Se puede hacer en paralelo con el carril de VSG de la sección 8: ambos usan la app de ChatGPT.*

- **Fuentes:** 6 representativas de tu uso real (como mínimo las de R2b A–F si cubren lo que más usás).
- **Condiciones:** (A) prompt directo de una o dos frases pidiendo el mismo resultado; (B) la misma fuente con el comando SC correspondiente. Una corrida por condición, y se evalúa la **primera** salida (sin rerun selectivo).
- **Evaluación:** pares mezclados y sin etiquetas, juzgados por Lean. Por par: cuál prefiere y qué fallas críticas ve (identidad cambiada, texto alterado o inventado, deriva de cámara, detalle oculto "resuelto" como si fuera observado).
- **Regla de decisión (escribirla antes de ver resultados):** propuesta de partida, SC se considera aporte si gana en **≥ 4 de 6 pares** y no tiene más fallas críticas que el control. Son umbrales míos para que Lean los ajuste.
- **Alcance de la conclusión:** con 6 pares es **indicativo, no estadístico**.
- **Registro mínimo por imagen:** hash de la fuente, comando o prompt exacto, modelo que muestra la app, fecha, versión del repo adjunto.
- **Qué decide:** si SC gana, se sigue; si el margen es chico, se simplifica y se conservan los comandos que sí aportan; si pierde en algún tipo de escena, queda acotada la zona de trabajo.

---

## 8. VSG: tope de 7 días para ver resultados

**Tope decidido por Lean, con el reloj reiniciado:** 7 días para ver resultados, medidos como **168 horas transcurridas desde la primera imagen válida de la exploración** (definición propuesta por GPT para que el tope sea medible). Si al cumplirse no hay resultados, la inversión en VSG se pausa. El checkpoint registra solo el **evento de inicio** (marca temporal, identificador y hash de la imagen), que es evidencia y no una fecha de vencimiento escrita; ningún documento fija una fecha de calendario. Reiniciar la exploración no reactiva GLIGEN ni habilita reinicios sucesivos automáticos: cada reinicio requiere una decisión explícita de Lean. Antes del reinicio llevaba más de 12 días en specs.

### 8.1 Lo que dicen los documentos del repo

1. **El piloto formal textual (VSG-2B)** genera por un "bridge" externo hacia una API de proveedor que no está configurado (`BLOCKED: NO_GENERATOR`). Lean genera en la app de ChatGPT, así que no se ejecuta como está diseñado. Su cierre exige al menos 4 pares válidos que incluyan el caso C (hoy `NO_GO_C0_UNVERIFIED`), semillas controladas y revisión con esquema propio.
2. **En ese piloto las dos ramas llevan las mismas restricciones;** solo cambia cómo se expresan (JSONL dentro de un texto vs. arreglo tipado). Los dry runs de D, E y Kenny ya guardaron ambos payloads (`validation/vsg_2b/dry_runs/`).
3. **La ruta estructural** (N2 → N4 → N5, base GLIGEN en Diffusers v0.29.0) no tiene backend compatible verificado (P1R: `NO_COMPATIBLE_BACKEND_VERIFIED`; N3: `N3_MODEL_DEVELOPMENT_REQUIRED`; N4: `N4_SCOPE_CHANGE_REQUIRED`, confianza `STATIC_ONLY`). Requiere un consumidor aprendido con pesos nuevos, corpus y derechos, protocolo de forwards, presupuesto y una enmienda de settings. N2 la describe como un hito de investigación "sujeto a decisión explícita sobre su esfuerzo".
4. **Estado del checkpoint (zip subido; confirmado en el repo vivo el 3-oct-2026: commit `f7c594e`, árbol limpio, `main` al día con `origin/main`; no existe `AGENTS.md`):** `current_milestone: POST_M3_DECISION_GATE`; M1, M2 y M3 en `CLOSED`; D1 y D2 aprobados con alcance acotado (solo diseño y andamiaje aislado); **D3 y D4 pendientes**; `execution_authorized: false`, `model_tests: NOT_RUN`, `generated_images: 0`. La autorización de Lean dice expresamente que no autoriza ejecución del modelo ni generación de imágenes. **Actualización (11-oct-2026, decisión de Lean):** la generación de imágenes ya no requiere su aprobación previa. El checkpoint publicado todavía dice, según la cita de GPT, que la ejecución de modelos y las imágenes siguen sin autorizar hasta una aprobación explícita. Corresponde registrar una **autorización específica para la exploración textual** (seis salidas, tres pares, con la app de ChatGPT), conservando la autorización histórica, manteniendo GLIGEN desautorizado y D3/D4 pendientes. GPT coincide: generar queda autorizado y evaluar los resultados sigue siendo responsabilidad de Lean.
5. **VSG-3A/3B** dependen de salidas reales y anotaciones de 2B (según el ROADMAP); VSG-4 y VSG-5 están diferidos.

### 8.2 Dos rutas y qué demuestra cada una

| Ruta | Qué es | Qué demuestra | Qué **no** demuestra | ¿Cabe en el tope de 7 días? |
| --- | --- | --- | --- | --- |
| **Exploración textual** (nombre: "exploración visual de instrucciones derivadas de VSG") | Pegar en la app dos versiones de instrucciones textuales (payload A y B de D, E y Kenny) junto con la imagen fuente | Cómo responde el generador a dos instrucciones textuales con el mismo contenido | Que un consumidor estructural use el grafo; no cierra VSG-2B; no juzga la arquitectura | **Sí** |
| **Estructural** (GLIGEN + consumidor aprendido) | Un modelo que consuma el grafo como estructura, en lugar de texto | (Si se hiciera) si el grafo es útil usado como estaba previsto | — | **No prometible:** hay trabajo de modelo pendiente, pero no existe una estimación definitiva; requiere decisión de esfuerzo de Lean (D3/D4) |

### 8.3 Exploración textual: pasos

*La exploración no depende de la continuidad (sección 9) ni del reencuadre (sección 6): puede arrancar sin supervisor y sin aprobación previa de Lean.*

El reloj de 7 días arranca con la primera imagen generada. Los pasos van en orden, sin fechas de calendario:

| Paso | Qué pasa | Quién |
| --- | --- | --- |
| 1 | Se congela el cierre formal de VSG-2B (no se cierra en esta exploración). | Agente |
| 2 | Se arma un paquete manual por caso (D, E, Kenny): imagen fuente, texto del payload A, texto del payload B y el orden de pares mezclado, con la clave guardada aparte. | Agente |
| 3 | En la app de ChatGPT, una sesión nueva por imagen (6 imágenes): adjuntar la fuente, pegar el payload y generar. Anotar el modelo que muestra la app y la fecha de la corrida. Sin reintentos. | Lean (sin aprobación previa) |
| 4 | Mirar los 3 pares sin etiquetas: cuál preferís y qué fallas críticas ves (identidad, texto, oclusor o zona desconocida, deriva de cámara). Opcional: adjuntar los pares a un chat con Claude como segunda opinión, sin reemplazar tu juicio. | Lean |
| 5 | Decisión según la regla de abajo. | Lean decide |

**Terminado para este carril (una frase):** "Dentro del tope de 7 días veo 3 pares de imágenes, cada uno con dos representaciones textuales del mismo contenido de restricciones (A: las restricciones del CGC como texto; B: las mismas restricciones desde el contrato compilado por VSG-2A, como arreglo tipado), para D, E y Kenny, y decido si vale la pena invertir más."

*Ambos payloads contienen restricciones: no es una comparación entre presencia y ausencia del grafo (verificado por GPT en N2 y P1R).*

**Regla de decisión (propuesta; fijarla antes de ver las imágenes):**
- **Se observó una ventaja** (≥ 2 de 3 pares prefieren la versión B, sin más fallas críticas): se considera invertir en la ruta estructural. Esa inversión es una decisión de esfuerzo de Lean (D3/D4), no automática.
- **No se observó ventaja** (cualquier otro resultado, incluidos empates): significa que *en estas tres comparaciones no se vio una ventaja*. Alcanza para **pausar la inversión en VSG por decisión personal**. No permite concluir que el grafo carezca de utilidad ni descartar la ruta estructural. Lo construido queda en modo sombra.
- En ambos casos el reporte debe decir: 3 pares son anecdóticos, las semillas no están controladas y el nombre del ensayo es "exploración visual de instrucciones derivadas de VSG", no "cierre de VSG-2B".

**Límites de la exploración (propuestos por GPT, aceptados por Claude):**
- Seis salidas (3 pares), sin reintentos selectivos.
- Gasto adicional autorizado: cero; sin cambio automático a una API ni a otro proveedor.
- Se registran intentos, salidas, fallas y el uso disponible; si la cuota se desconoce, se registra `UNKNOWN`.
- El test separado de 12 imágenes (sección 7) no consume este mismo presupuesto.

### 8.4 Ruta estructural: estimación y pausa

**Entregado por GPT/Codex:** una recomendación de **pausar la ejecución** de la ruta estructural, en un informe con fundamentos y cálculos (`GLIGEN_RECOMENDACION_2026-10-03.md`, **fuera del repo**; Claude no lo leyó, solo vio el resumen).

| Concepto | Resumen entregado |
| --- | --- |
| Qué falta | Pesos entrenados, datos y licencias, entorno verificado, criterios congelados y presupuesto completo |
| Trabajo | Referencia conservadora de **25–59 días-persona**, basada en N2/N3. Excluye datos, esperas y revisión externa. M3 no demuestra cuánto puede descontarse. |
| Gasto | Escenario de **USD 113,19** de infraestructura, calculado con un techo propuesto de 34 GPU-h, cuatro núcleos, 64 GiB de RAM y almacenamiento (tarifas de Modal). **No es un mínimo ni el costo total:** ingeniería, datos y revisión siguen sin cotizar. Los cálculos y las tarifas no fueron verificados: el informe está fuera del repo y el hash registrado no acredita su contenido. |

**Valoración de Claude:**
- **Coincide con pausar.** Es mucho esfuerzo para un proyecto personal cuyo output ya sirve, y deja la ruta fuera de los 7 días.
- **Orden de magnitud, no cifra firme:** el rango es amplio y la estima viene del mismo agente que diseñó la ruta.
- **Faltan dos cosas que se pidieron:** un entregable concreto que Lean pueda ver y las unidades que le importan (sus horas, los días de calendario y el gasto total). "Días-persona" no decide su caso.

**Estado:** pausa **registrada** en `CHECKPOINT.json` (commit `33b6581`, informado por GPT/Codex). Claude no lo verificó: `git show 33b6581 --stat` debería mostrar cambios solo en ese archivo. El registro incluye la razón, la estimación de 25–59 días-persona y el hash del informe; D3/D4 siguen `PENDING`, lo construido se preserva, VSG continúa en modo sombra y no se ejecutaron pruebas ni se amplió la implementación. Tarjeta "Go" usada, para referencia:

```
HITO: Pausar la ruta estructural de VSG (GLIGEN)
Qué vas a ver distinto: nada en el output.
Qué cambia: el checkpoint registra la pausa, la razón y la estimación (con el hash del informe). D3/D4 siguen PENDING. No se hacen más pruebas ni implementación.
Qué no cambia: lo ya construido queda; VSG sigue en modo sombra.
Cómo se revierte: con una decisión explícita de esfuerzo (D3/D4).
Costo: una sesión corta.
Mi recomendación (por defecto): pausar.
Reabrir si: la exploración textual muestra ventaja (≥ 2 de 3 pares) y Lean decide asignar el esfuerzo estimado.
```

---

## 9. Continuidad del desarrollo con autonomía acotada

**Objetivo (confirmado por Lean el 11-oct-2026):** que la Mac siga desarrollando SC mientras Lean está ausente.

**Estado actual (verificado en el repo vivo: no existe `AGENTS.md`):** `CHECKPOINT.json` ya tiene `resume`, `events` y `next_milestone`, así que permite **retomar**. En el zip no encontré mención de un supervisor ni de una continuación persistente (buscar una palabra no prueba su ausencia funcional), que es lo que permitiría **avanzar sin Lean**.

**Riesgo:** un agente sin supervisión y sin topes reproduce justo las fallas 1 y 2 (más hitos, más specs), pero sin nadie presente. Con varios agentes en paralelo el riesgo crece: más hitos a la vez y más posibilidades de que dos agentes se pisen el estado; por eso valen las reglas de la sección 9.1.

**Sobre de autorización (versión simplificada, acordada entre Claude y GPT; vive en `AGENTS.md`).** Antes de cada tanda de trabajo Lean fija cinco cosas:

1. **Objetivo.**
2. **Tareas permitidas.**
3. **Límites de gasto y de uso** (incluida la cuota).
4. **Evidencia de cierre** de cada tarea.
5. **Condiciones de parada** (bloqueo, decisión pendiente, límite agotado).

El agente ejecuta solo ese alcance, guarda el progreso en el checkpoint y se detiene ante cualquier condición de parada. Siguen requiriendo a Lean: D3/D4 y cualquier otra autorización de alcance, el gasto fuera de los límites, ejecutar modelos (hoy no autorizado) y abrir hitos nuevos. **La generación de imágenes ya no requiere aprobación previa de Lean** (decisión del 11-oct-2026); sigue sujeta a los límites de gasto y de uso del sobre.

**Commits y push:** Lean ya los autorizó y viene trabajando sin ramas, así que esa política no cambia sin una razón concreta. Razón a considerar: en cada sesión Lean adjunta el repo desde GitHub, de modo que lo que esté en `main` es lo que ChatGPT lee como SC; un push sin supervisión que rompa algo contaminaría el uso diario. Alternativa sin ramas: fijar el runtime a una versión estable (un tag, o el paquete de runtime chico, si la app no permite elegir versión) y registrar en el checkpoint el último commit verificado para poder revertir con un comando. **Con agentes en paralelo (v9)** aparece una razón concreta para reabrir el punto: si todos escriben sobre `main` sin ramas ni copias separadas, se pisan entre sí; hace falta aislar a cada agente en su rama o copia de trabajo. **Decisión de Lean.**

**Topes duros:** máximo de sesiones/horas/commits por tanda de trabajo; tope de hitos abiertos en paralelo, fijado por Lean en el sobre de autorización (un número fijo; no crece automáticamente al agregar agentes); parada automática ante cualquier bloqueo.

### 9.1 Orquestación multiagente (v9)

**Roles propuestos** (ajustables por Lean): un **orquestador** (líder, es con quien habla Lean), uno o más **implementadores** y un **verificador** de un modelo distinto del que implementó (salvaguarda de la sección 3).

**Reglas que reemplazan al límite de un hito a la vez:**
1. **Escritor único del checkpoint:** solo el orquestador escribe `CHECKPOINT.json` (`events`, `decisions`, pausas, último commit verificado). Los demás agentes le reportan sus resultados y no editan ese archivo. Sigue siendo la única fuente de verdad, sin estructuras paralelas.
2. **Archivos propios:** cada implementador trabaja solo sobre los archivos o carpetas que la tarjeta "Go" de su hito le asigna. Si dos hitos necesitan tocar lo mismo, el orquestador los secuencia.
3. **Aislamiento:** cada implementador trabaja en su propia rama o copia de trabajo (ver "Commits y push"). Cómo se logra eso en cada entorno de orquestación es una pregunta abierta que debe resolverse con la documentación oficial de cada herramienta; este documento no afirma nada al respecto.
4. **Revisión antes de integrar:** el verificador revisa el diff de cada hito antes de que se integre a `main`.
5. **Lectura para Lean:** el orquestador entrega cada cierre en la vista en llano (cerrar / pausar / mantener) y con la tarjeta "Go"; lo que Lean decide sigue siendo lo del sobre de autorización.
6. **Integración serial:** los hitos se integran de a uno, y el verificador revisa contra el commit que realmente se integra.
7. **Checkpoint sin versiones viejas:** el orquestador rechaza actualizaciones del checkpoint basadas en una versión antigua.
8. **Tarea acotada:** cada tarea tiene un entregable observable, un límite de esfuerzo y un cierre explicable en tres líneas.

*Reglas 6 a 8 y el tope numérico: propuestas por GPT, aceptadas por Claude.*

**Prueba corta:** una corrida de prueba bajo el sobre, midiendo si el resumen de cierre le permite a Lean decidir en menos de 5 minutos.

---

## 10. Decisiones de Lean y pendientes

**Decisiones tomadas**
1. **Tope para VSG:** 7 días para ver resultados (llevaba más de 12 días en specs); reloj reiniciado, ver decisión 6.
2. **Delegación:** el agente y sus skills deciden los "cómo" técnicos reversibles bajo el marco de decisión; Lean aprueba lo visible, el alcance y lo irreversible.
3. **Ruta estructural de VSG (GLIGEN):** pausada y registrada en el checkpoint (commit `33b6581`, informado por GPT/Codex), tras la estimación de la sección 8.4. Se reabre solo si la exploración textual muestra ventaja en ≥ 2 de 3 pares y Lean decide asignar el esfuerzo mediante D3/D4.
4. **Regla de un hito a la vez: retirada (9-oct-2026).** Lean prefiere ir más rápido; los hitos avanzan en paralelo con agentes coordinados por un orquestador (sección 9.1).
5. **Escritor único del checkpoint (9-oct-2026):** solo el orquestador escribe `CHECKPOINT.json`; los demás agentes le reportan (sección 9.1).
6. **Reloj de VSG reiniciado (11-oct-2026):** en lugar de parquear, se reinicia el tope de 7 días. Arranca con la primera imagen de la exploración y no tiene fecha de calendario.
7. **Imágenes sin aprobación previa de Lean (11-oct-2026):** la generación de imágenes ya no requiere su aprobación. Sigue valiendo su juicio sobre los resultados (acordado entre Claude y GPT; Lean puede delegarlo si lo decide) y los límites de gasto y de uso del sobre. El checkpoint debe registrar el cambio.
8. **Sin expectativas de fechas de calendario ni contenido de tutoriales (11-oct-2026):** el documento no fija fechas de vencimiento ni cronogramas por día, y no afirma nada sobre productos que no provenga de documentación oficial o del propio repo.
9. **Dictamen de GPT sobre la v10: APROBADO CON CAMBIOS (11-oct-2026).** Las cinco objeciones se incorporaron en esta versión.
10. **Confirmaciones de Lean (11-oct-2026):** el reloj de VSG se mide como 168 horas desde la primera imagen válida de la exploración, y la continuidad del desarrollo sin su presencia es un objetivo.

**Pendientes de Lean**
- **Adjuntar imágenes de uso real:** 4 a 6 fuentes que representen lo que más usás y, si podés, un resultado que te gustó y uno con una falla. Con eso se eligen las fuentes del test de 12 imágenes y los tipos de falla a mirar.
- **Aprobar la tarjeta "Go"** del primer paso (sección 6).
- **Decidir** la política de commits y push (sección 9), ahora con agentes en paralelo.
- **Elegir** el entorno del orquestador (decisión a tomar con la documentación oficial de cada opción) y confirmar los roles de la sección 9.1.
- **Pasar al agente con acceso al checkout de la Mac** el registro de la autorización específica de la exploración y de las reglas en `AGENTS.md` y el checkpoint, sin tocar la pausa de GLIGEN.

**Verificado en el repo vivo (3-oct-2026, por el agente con acceso al checkout de la Mac)**
- M3 cerrado (commit `f7c594e`); árbol limpio y `main` al día con `origin/main`.
- `D1` y `D2` aprobados con alcance acotado; `D3` y `D4` pendientes; `execution_authorized: false`; `generated_images: 0`.
- No existe `AGENTS.md`.
- Estimación de la ruta estructural entregada (sección 8.4); GPT no abrió hitos nuevos ni amplió implementación o pruebas.
- Pausa de la ruta estructural registrada en el checkpoint (commit `33b6581`): informada por el agente de la Mac y **verificada después por GPT en el remoto de GitHub** (`main` en `33b6581`, que modifica solo el checkpoint; el checkpoint publicado muestra la pausa y D3/D4 pendientes).
- GPT no tiene acceso al checkout de la Mac: inspeccionó un checkout propio en `2a489a6` y el remoto. El estado limpio de la Mac sigue sin verificación independiente.

---

## 11. Registro de desacuerdos Claude / GPT

**Qué vio cada agente:** el **repo vivo está en la Mac de Lean** y solo lo ve el agente con acceso a ese checkout; la instancia de GPT que dictaminó la v10 ve únicamente el remoto de GitHub (`main` en `33b6581`) y un checkout propio (`2a489a6`); Claude trabajó solo sobre el zip subido (snapshot) y con lecturas parciales de varios documentos. GPT reconoció que su recomendación sobre M3 se apoyaba en el último resultado compartido en la conversación y no en el checkpoint vivo. Ninguno ejecutó el benchmark VSG completo. La concesión de uno al otro **no cuenta como prueba**; lo que cuenta es la evidencia citada. El 3-oct-2026 GPT/Codex ejecutó `git status`, `git log -1` y la lectura de campos del checkpoint sobre el repo vivo; Claude no pudo leer el informe GLIGEN, que queda fuera del repo.

| # | Tema | Claude | GPT | Estado | Qué lo resolvió o lo resolvería (y quién) |
| --- | --- | --- | --- | --- | --- |
| 1 | Qué prueba la exploración textual | Muestra la respuesta del generador a dos textos; la v4 concluyó de más | No prueba el consumo estructural; debe tener nombre y conclusión propios | **Resuelto (acuerdo)** | Aplicado en 8.2–8.3 |
| 2 | Interpretación de los empates | Tres empates = "no se observó ventaja"; se retiró "VSG no cambia el output" | Tres empates no demuestran que el grafo carezca de utilidad | **Resuelto (acuerdo)** | Aplicado en la regla de decisión (8.3) |
| 3 | Estado de M3 | El checkpoint del zip lo mostraba `CLOSED`, con D3/D4 pendientes | Su "cerrar M3" estaba desactualizado | **Resuelto (verificado en vivo)** | `git status`, `git log -1` y campos del checkpoint, ejecutados por GPT/Codex |
| 4 | Ruta estructural en 7 días | Lectura parcial: hay trabajo de modelo pendiente; la v5 sobreafirmó que "no cabe" | No está demostrado que quede fuera; el agente debe estimar y recomendar | **Resuelto:** GPT entregó la estimación, recomendó pausar y registró la pausa en el checkpoint (commit `33b6581`); Claude coincidió (orden de magnitud, no cifra firme) | Informe `GLIGEN_RECOMENDACION_2026-10-03.md` y registro en el checkpoint; reapertura solo con ventaja textual y decisión de Lean (D3/D4) |
| 5 | Orden: cerrar M3 antes o no | No debe retrasar la evidencia visual | Aplica "un hito activo" a la cadena de desarrollo; las imágenes se evalúan aparte | **Resuelto (acuerdo); reemplazado en v9** | Aplicado en la nota de la sección 5; la regla se retira en la v9 por decisión de Lean (9-oct-2026) |
| 6 | Estructuras documentales | La vista en llano se genera desde `CHECKPOINT.json`; las decisiones van al checkpoint; `AGENTS.md` aparte | Evitar otra estructura paralela | **Resuelto:** `AGENTS.md` no existe (verificado), se crea en el primer paso | Verificación en vivo |
| 7 | Continuidad sin Lean | Sí, con límites y condiciones de parada | Sí; sobre simplificado: objetivo, tareas, límites, evidencia de cierre y parada | **Resuelto (acuerdo)** | Corrida de prueba bajo el sobre (sección 9) |
| 8 | "Única vía" a imágenes | La v5 dijo "la única vía con la app" | Es la vía práctica identificada, no quedó acreditado que sea la única | **Resuelto (acuerdo)** | Redacción corregida |
| 9 | Ramas y prohibición de push a `main` | Propuso ramas; ahora la retira como regla | Lean ya autorizó commits y push y trabaja sin ramas; cambiarlo requiere una razón concreta | **Abierto: decide Lean** | Razón y alternativa en la sección 9 (`main` = lo que ChatGPT lee; fijar el runtime a un tag o paquete); v9: con agentes en paralelo hace falta aislar a cada uno en su rama o copia |
| 10 | Secuencia: exploración vs. supervisor | La exploración no debe esperar a la continuidad | Aceptó que depender del supervisor volvería a postergar las imágenes | **Resuelto (acuerdo)** | Aplicado en 8.3 |
| 11 | Contenido de la estimación | Faltan un entregable concreto que Lean pueda ver y las unidades que le importan (sus horas, días de calendario, gasto total) | Entregó trabajo en días-persona y gasto de infraestructura; reconoce que no es el costo total | **Abierto (menor)** | Revisar el informe completo (Claude no lo leyó) |
| 12 | Un hito a la vez vs. paralelismo | Recomendó el límite para frenar las fallas 1 y 2 (hitos que se producen más rápido de lo que se usan) | Dictaminó la v10 como APROBADO CON CAMBIOS; no objetó el retiro, pidió completar las reglas (filas 15 a 19) | **Retirado por decisión de Lean (9-oct-2026)** | Lean prioriza la velocidad; se mantienen el escritor único del checkpoint y los archivos propios por agente (sección 9.1) |
| 13 | Retiro de expectativas de fechas y de contenido de tutoriales (v10) | Aplicado por decisión de Lean | Revisó: quedan una afirmación de producto sin fuente (lectura automática de `AGENTS.md`) y un precio no comprobado | **Resuelto en la v11** | Correcciones aplicadas |
| 14 | Imágenes sin aprobación previa de Lean (v10) | Aplica a generar, no al juicio sobre los resultados | Coincide; exige una autorización específica en el checkpoint, separada de GLIGEN | **Resuelto en lo conceptual; falta registrarlo** | Lo registra el agente con acceso al checkout de la Mac |
| 15 | Qué compara el A/B | La v10 decía "con y sin instrucciones derivadas de VSG" | Ambos payloads contienen restricciones: son dos representaciones textuales del mismo contenido, no presencia vs. ausencia del grafo | **Resuelto (Claude corrige)** | Payloads y N2/P1R |
| 16 | Definición del reloj | Tope de 7 días sin fecha de calendario | 168 horas desde la primera imagen válida; evento de inicio registrado; sin reinicios automáticos | **Resuelto (acuerdo);** unidad confirmada por Lean | El orquestador registra el evento de inicio |
| 17 | Reglas de paralelismo | Escritor único y archivos propios | Agregar integración serial, revisión contra el commit integrado, rechazo de checkpoint viejo, tope numérico fijo y tareas acotadas | **Resuelto (acuerdo)** | Aplicado en 9 y 9.1 |
| 18 | Estimación de infraestructura | "Al menos USD 113,19" | El checkpoint lo describe como escenario, no como mínimo | **Resuelto (Claude corrige)** | Aplicado en 5 y 8.4; el informe sigue sin auditar |
| 19 | Supervisor, continuidad y productos | "0 coincidencias" probaba la ausencia; la continuidad estaba por confirmar | Buscar una palabra no prueba ausencia; hay afirmaciones de producto sin fuente | **Resuelto (acuerdo)** | Aplicado en 5, 9 y 10 |

**Reglas para que la interobjetividad sirva:**
1. Separar **hechos verificables** (archivo, comando, hash) de **interpretaciones**.
2. Cada agente declara **qué versión del repo vio**.
3. Todo desacuerdo se registra con **qué evidencia lo resolvería y quién puede obtenerla**.
4. Lean arbitra solo lo que puede juzgar: imágenes, alcance y tiempo.
5. Un acuerdo entre agentes **no es evidencia**; una citada, sí.
6. Un estado se verifica **ejecutando el comando sobre el repo vivo**; nadie lo da por vigente de memoria (ni GPT ni Claude).
