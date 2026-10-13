# Streetcraft · Revisión trazable e integración del candidato 02/03

**ID:** SC-MULTIAGENT-04 · **Versión:** 1.0 · **Fecha:** 2026-10-13  
**Estado:** SPEC_READY. No acredita revisión ni integración realizadas.  
**Fuente:** output adjunto Pasted text(4).txt, leído completo; no se inspeccionó el checkout de la Mac para elaborar esta spec.  
**Dependencias:** SC-MULTIAGENT-01 READY en modalidad DELEGATED_ANALYSIS_CENTRALIZED_WRITES; candidato vigente de 02/03.  
**Destino:** Codex sobre el repo vivo.

## 1. Objetivo y entregable

Resolver una revisión independiente verificable del candidato existente y dejarlo integrado si cumple los criterios. El entregable es un recibo asociado al contenido exacto revisado, a los modelos observados y al resultado técnico; seguido de commit/publicación bajo la autorización vigente.

No rehacer el supervisor ni añadir infraestructura para reemplazar una comprobación de modelos. No marcar SC-MULTIAGENT-03 READY: seis pruebas locales y una tanda simulada no acreditan una tanda real.

**Tarjeta Go:** revisar e integrar lo construido; Lean verá un resultado PASS/FAIL/BLOCKED explicable, evidencia asociada al candidato y, si pasa, un commit identificable. Gasto adicional cero. Revertir solo commits propios; conservar evidencia histórica.

## 2. Qué dice el output y qué no prueba

| Observación reportada | Tratamiento |
| --- | --- |
| scripts/sc_supervisor.py, quickstart y tests implementados | Recuperar archivos reales y diff completo; no reconstruir del transcript |
| 6/6 pruebas locales PASS y corrida simulada COMPLETED | Reutilizar evidencia y revalidar si cambia candidato o entorno |
| PAIR_SHEET.json y CONDITION_KEY.json preparados | Revisar integridad, neutralidad y ligadura al manifiesto VSG |
| REVIEW_MODEL_UNAVAILABLE y un intento agotó cuota | Respetar bloqueo; diagnosticar identidad/uso antes de otra llamada |
| Candidato local sin commit/push | Observación del reporte, no estado actual: comprobar si Lean publicó después |
| Sin imágenes, forwards ni inicio del reloj VSG | Preservar; comprobar checkpoint vigente |

La salida adjunta no incluye los bytes completos del código ni las revisiones. No puede sustituir una revisión del repo.

## 3. Entrada y preservación

El orquestador:

1. Lee AGENTS.md, specs 01–03 en sus versiones enmendadas, plan y checkpoint real en development/coordination/CHECKPOINT.json.
2. Registra HEAD, upstream, git status y hash del checkpoint. Usa el Git funcional existente; no reinstala herramientas por defecto.
3. Inspecciona MODEL_REVIEW_ATTEMPTS_20261013.json y los hallazgos de revisiones previas, conservando los originales.
4. Identifica el candidato completo: tracked modificados, nuevos archivos, altas, bajas y archivos binarios.
5. Comprueba si el trabajo ya está en HEAD o remoto. Si está publicado, revisa ese commit/contenido; no vuelve a aplicar un patch.
6. Preserva cambios ajenos y no usa reset, limpieza masiva ni force push.

Congelar un manifiesto por archivo con path, operación y hash, más base y diff. Los archivos de evidencia no son otro checkpoint.

## 4. Identidad de modelos: resolver una vez, sin inventar

El bloqueo exige distinguir tres cosas:

| Nivel | Ejemplo | ¿Acredita modelo del turno? |
| --- | --- | --- |
| Solicitado/configurado | model en TOML o argumento -m | No, por sí solo |
| Etiqueta genérica | “GPT-6” en una interfaz | No distingue modelos |
| Resuelto y registrado por el runtime | Identificador ligado a sesión/turno en metadata observable | Sí, como identidad operativa del runtime |

No exigir un hash de pesos ni identidad interna del servidor. “Efectivo” significa el identificador que el runtime registra para esa ejecución, con su procedencia; no el nombre que el modelo declara en su respuesta.

### Diagnóstico mínimo

- Resolver ruta/version del CLI instalado. En el output previo hubo un binario en el cache de VS Code; localizarlo, no fijar permanentemente ese path versionado.
- Consultar catálogo de la cuenta/cliente actual y configuración efectiva.
- Inspeccionar únicamente metadata de sesiones pertinentes, extrayendo campos necesarios; no publicar rollouts completos, credenciales ni prompts personales.
- Reutilizar evidencia de IDs de sesión, turno y modelo cuando exista.
- Si hay una API local de thread metadata ya disponible, usarla conforme a su documentación. No construir un nuevo servicio ni migrar a API facturada.
- Comprobar niveles de razonamiento admitidos y cuota antes de la revisión.

La documentación oficial permite listar modelos e inspeccionar/controlar threads en App Server, y guardar eventos en ejecución no interactiva. No promete que cada versión exponga el modelo en cada evento JSONL. Comprobar el campo real. [App Server](https://learn.chatgpt.com/docs/app-server) · [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), consultados el 13-oct-2026.

## 5. Autoría del candidato y criterio independiente

La comparación requerida es entre implementador y revisor, no entre dos etiquetas del mismo producto.

Registrar por componente y cambios materiales:
- Modelo del implementador observado.
- Sesión/turno de implementación y fuente de metadata.
- Modelo del revisor observado y sesión/turno.
- Identidad del contenido revisado.
- Limitaciones y partes cuya autoría siga UNKNOWN.

El modelo con que pasó el smoke de 01 no demuestra quién escribió sc_supervisor.py después. No atribuir retroactivamente la implementación a gpt-5.6-sol.

**Ruta preferida:** recuperar metadata de la implementación existente y ejecutar la revisión con un modelo operativo distinto disponible.

**Si la autoría material no es recuperable:** no declarar el gate satisfecho. Entregar REVIEW_PROVENANCE_BLOCKED con lo conocido. Dentro del alcance original y de los límites, puede proponerse una reconstrucción real del componente afectado por un implementador trazable, seguida de revisión distinta; no copiar/reemitir bytes para cambiarles la autoría ni reconstruir automáticamente todo SC.

Dos revisores distintos con autor desconocido no cumplen silenciosamente “revisor distinto del implementador”. Una alternativa a ese criterio requiere una decisión explícita y registro; esta spec no cambia la salvaguarda de la v12.

No pedir de nuevo permisos para diagnósticos y correcciones reversibles ya autorizados.

## 6. Alcance de revisión

El revisor recibe el candidato congelado y las specs. Trabaja en lectura; root conserva escritura.

| Área | Preguntas obligatorias |
| --- | --- |
| Sobre | ¿Valida tareas, plazo, base y límites? ¿Rechaza desconocidos o inválidos? |
| Lock | ¿Impide dos corridas? ¿Usa identidad canónica del repo, incluidos worktrees? |
| Procesos | ¿Timeout y stop alcanzan hijos? ¿Cómo detecta actividad huérfana o desconocida? |
| Reconciliación | ¿Conserva evidencias y evita relanzar efectos ya completados? |
| Checkpoint | ¿El supervisor evita escribir estado de negocio? ¿Root es único escritor? |
| Digest | ¿La normalización SELF está definida y versionada, sin mutaciones en lectura? |
| Ejecutor simulado | ¿No puede tomarse su resultado como evidencia Codex real? |
| Sesiones persistidas | ¿Se conserva ID explícito? ¿No usa --last ni --ephemeral para la ruta probada? |
| Campaña VSG | ¿Pares y clave corresponden a fuentes/payloads congelados? ¿La hoja no revela condiciones? |
| Documentos | ¿Distinguen preparación, pruebas locales, revisión, piloto real y publicación? |

No basta con parsear JSON/TOML. Revisar comportamiento y comprobar que tests cubren fallas relevantes. La existencia de seis tests no obliga a mantener exactamente seis si aparecen huecos reales.

### Digest autocontenido

Revisar la implementación existente antes de tocarla. Documentar algoritmo, versión, codificación, orden de claves y campos sustituidos por SELF.

Probar: reproducibilidad sin editar checkpoint; alteración de una tarea o límite invalida digest; alteración del digest almacenado se rechaza; diferencias de formato JSON no cambian un digest semántico; decisiones ajenas no se excluyen arbitrariamente.

No confundir digest íntegro con firma de autorización: un proceso capaz de editar checkpoint y recalcular digest puede cambiar ambos. La autorización proviene de instrucciones y decisiones vigentes, no del hash.

## 7. Corrección y congelamiento final

Consolidar hallazgos por gravedad y evidencia. El orquestador aplica una ronda de correcciones dentro del alcance; no escribe el revisor.

Una modificación material invalida la revisión anterior. Congelar otra vez el contenido final y verificar ese contenido antes de integrar.

El checkpoint previsto para integración debe incluirse en la revisión. El recibo posterior puede añadirse como evidencia, sin alterar silenciosamente el código revisado. Evitar hashes autorreferentes: definir explícitamente exclusiones del recibo y su relación con el candidato.

No tratar un PASS de formato o una revisión sin modelo trazable como PASS independiente.

## 8. Integración y publicación

Solo después de satisfacer el gate:

1. Comprobar que base y archivos revisados siguen vigentes.
2. Ejecutar checks pertinentes sobre el candidato final.
3. Actualizar estado de integración y evidencia, sin declarar 03 READY.
4. Commit del alcance propio revisado, preservando cambios de Lean.
5. Push normal conforme a autorización vigente.
6. Comprobar commit remoto; diferenciar publicado de integrado localmente.

Si Lean ya publicó, conservar ese hecho y revisar el commit. Si hay problemas, producir corrección mínima posterior. No reescribir historia para simular que la revisión precedió al push.

Si falla publicación, conservar commit y registrar pendiente. Si el resultado es ambiguo, consultar el remoto antes de reintentar.

## 9. Archivos y estados

Reutilizar archivos de revisión existentes o añadir un recibo nuevo con referencias históricas:

- specs/SC_MULTIAGENT_04_v1.md.
- validation/sc_multiagent/continuity/REVIEW_04_RECEIPT.json.
- Reporte breve junto a evidencia existente.
- Delta pertinente del checkpoint.
- Correcciones estrictamente necesarias en scripts, tests y quickstarts.

No crear catálogo de modelos paralelo ni nueva fuente de decisiones.

Estados propuestos:
- SC04_REVIEW_VERIFIED: candidato exacto con revisión distinta acreditada.
- SC04_INTEGRATED: revisión satisfecha y contenido integrado, publicación diferenciada.
- SC04_BLOCKED: identidad, autoría, cuota o hallazgo impide cierre.

02 conserva el estado real de campañas; 03 sigue preparado/pending hasta su piloto real. GLIGEN PAUSED, D3/D4 PENDING y reloj VSG sin reinicios.

## 10. Presupuesto, parada y esfuerzo

**Topes propuestos:** una sesión de hasta 60 minutos para diagnóstico y revisión; máximo una revisión inicial y una revisión del candidato corregido. Correcciones dentro de una sola ronda. Gasto adicional cero; imágenes cero.

Consultar cuota antes de cada llamada. Si UNKNOWN, registrar sin certificar porcentaje. Ante cuota agotada, no ciclar revisores/modelos. Ante falta de metadata, producir bloqueo concreto después del diagnóstico; no dedicar nuevas sesiones a intentar etiquetas equivalentes.

Razonamiento: high para revisor y lógica de procesos/digest; medium para inventario e integración. Usar modelos de la cuenta actual, sin asumir el catálogo observado ayer.

## 11. Relación con el plan maestro

Este output cambia la prioridad inmediata. Los números 04/05 del plan eran propuestas sin specs: 04 pasa a revisión/integración y 05 a piloto real del supervisor. El empaquetado de runtime y la mejora visual quedan posteriores, sin abrirse automáticamente.

Al implementar, comprobar que no exista otro hito 04 real. Si hay colisión, preservar IDs existentes y registrar equivalencia con SC03-REVIEW; no sobrescribir otra spec.

Actualizar la descripción de secuencia en el plan del repo; las decisiones y estados permanecen en el checkpoint. No cerrar ni admitir futuros hitos por numeración.

**Arranque para Codex:** reconciliar el candidato 02/03 actual; resolver identidad operativa y autoría con evidencia mínima; revisar con modelo distinto; corregir una ronda e integrar solo el contenido final verificado. No rehacer pruebas ya válidas ni convertir preparación del supervisor en cierre real.
