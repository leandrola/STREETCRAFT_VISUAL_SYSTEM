# VSG-2B · Dos recomendaciones para el siguiente trabajo en ChatGPT Work mode

Son propuestas de tareas, **no nuevas autorizaciones ni hitos ejecutados**.
Estado de partida: N4_SCOPE_CHANGE_REQUIRED, confianza STATIC_ONLY; cierre documental
N4R no equivale a arquitectura viable. N3_MODEL_DEVELOPMENT_REQUIRED permanece.

Contexto para adjuntar a cualquiera de los dos trabajos: los seis documentos N4,
`audit_static.py`, `closeout_checks.py`, esta propuesta de settings y N4/N4R specs.
Los documentos nuevos son locales; el commit citado en N4R solo contenía el auditor.
No asumir que un enlace a main incluye este cierre. Si Work no recibe un archivo,
pedir el insumo concreto; no inventar acceso al filesystem ni resultados de ejecución.

## 1. Revisión independiente de observabilidad — recomendada primero

Propósito: revisar la prueba temporal y los límites del diseño textual antes de
aceptar settings o comprometer desarrollo. Nombre propuesto: **VSG-2B / N4V**.
No necesita pesos ni generación. Resultado esperado: hallazgos y una decisión sobre
si la propuesta tiene fundamento suficiente para pasar a decisión de arquitectura.

Prompt listo para copiar en ChatGPT Work mode:

> Prepará la próxima spec «VSG-2B / N4V · Revisión independiente de observabilidad»
> usando exclusivamente el paquete N4/N4R adjunto y las fuentes primarias fijadas.
> Partí de N4_SCOPE_CHANGE_REQUIRED; no supongas N4 viable ni abras N5. La spec debe
> encargar una revisión adversarial y estática de: (1) equivalencia acotada del
> tokenizer BasicTokenizer y ensamblado A/B; (2) resampler compartido de128slots,
> orden y cobertura frente a semántica; (3) máscara M1, reinyección fuente, memoria
> PNDM/counter1, apagado del canal y decode/safety/postprocess; (4) neutralización
> de R conservando attention/FF/S compartidos. Exigí distinguir B contra ablación
> de una diferencia meramente textual A/B. Revisá si la conclusión de borrado con
> beta0.3 y la ruta posible con beta1 están respaldadas, incluyendo supuestos y
> casos que podrían refutarlas. No conviertas un cálculo simbólico en prueba causal.
> Definí entregables N4V_REVIEW.md y N4V_RESULT.json, criterios de aceptación/rechazo,
> evidencia mínima faltante y hashes/versiones a verificar. Preservá N4/N3 como
> evidencia previa; sin modelos, pesos, forwards, entrenamiento, imágenes, cambios
> de scope, admisión ni X1. Redactá la spec para revisión; no ejecutes ni apruebes
> su decisión arquitectónica. Si falta un adjunto indispensable, señalalo.

## 2. Decisión acotada de settings y frontera experimental

Propósito: convertir la enmienda en una decisión explícita y revisable. Nombre
propuesto: **VSG-2B / N4S**. Conviene usar también N4V si se realizó. Puede prepararse
sin aprobar el desarrollo: autorizar un diseño y autorizar recursos son decisiones
separadas.

Prompt listo para copiar en ChatGPT Work mode:

> Redactá la próxima spec «VSG-2B / N4S · Decisión de settings y frontera experimental»
> a partir de N4_RESULT y N4R_SETTINGS_AMENDMENT_PROPOSAL adjuntos; incorporá N4V si
> está disponible, sin fingir que ya se ejecutó. Objetivo: presentar para decisión
> explícita la variante M_KEEP1, schedule relacional beta1 hasta el final y patch
> simétrico que conserva attention/FF/S en A/B. Mostrá antes/después y separá los
> defaults upstream de settings operacionales: D sigue DRY_RUN_ONLY y seed null.
> Conservá fuente347×389, common, diez registros, A JSONL y B tipado, mismo artefacto
> compuesto y mismos RNG/settings. No cambies máscaras mediante locks ni regiones
> observadas. Exigí protocolo temporal, criterios de rechazo semántico y preservación,
> sin afirmar que sensibilidad numérica sea mejora visual. Ofrecé decisión aceptar,
> rechazar o pedir evidencia; ninguna se adopta por defecto. Si se acepta el diseño,
> la spec solo habilitará redactar un plan posterior de implementación/recursos con
> corpus/derechos, entorno fijado, descargas, cómputo/costo y clasificación de forwards
> pendientes de autorización. Entregables propuestos: N4S_DECISION.md, matriz de
> cambios y N4S_RESULT.json; sin editar manifests, schemas, allowlists, política de
> ocho intentos ni evidencia previa. No ejecutar modelos, entrenar, generar, abrir
> X1 o desbloquear VSG-2B. Prepará un documento autocontenido listo para revisar.
