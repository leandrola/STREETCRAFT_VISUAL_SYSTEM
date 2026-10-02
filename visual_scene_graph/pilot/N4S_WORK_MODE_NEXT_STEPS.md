# VSG-2B · Dos recomendaciones después de N4S para ChatGPT Work mode

Estado: `N4S_SETTINGS_DECISION_READY`, no aprobación. La enmienda exacta es
`VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0`. Su aceptación solo habilitaría preparar
implementación/recursos; no ejecutarlos. N4 y VSG-2B siguen bloqueados.

Adjuntar a Work: N4S_CLOSURE_AND_SETTINGS_DECISION.md, N4S_RESULT.json,
n4s/SETTINGS_AMENDMENT_PROPOSAL.json, n4s/INPUT_MANIFEST.json y los tres documentos
temáticos N4 de texto/fuente/A-B. Incluir una decisión explícita posterior si existe.
No asumir que main contiene los cambios locales ni que Work accede a estas rutas.
Los siguientes nombres son propuestas; comprobar colisiones antes de adoptarlos.

## 1. Plan de implementación y recursos — recomendado tras decidir la enmienda

Próxima spec propuesta: **VSG-2B / N5P · Plan acotado del consumidor GLIGEN**.
Debe convertir módulos y dependencias en trabajo ejecutable con límites, sin iniciar
desarrollo ni comprar cómputo. Si la enmienda sigue sin decisión, puede redactarse
como borrador condicional, pero no declarar el hito habilitado.

Prompt para copiar:

> Redactá la spec «VSG-2B / N5P · Plan acotado del consumidor GLIGEN» con los adjuntos
> N4S. Verificá primero si existe aceptación explícita de la enmienda
> VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0 y registrá su evidencia; si no existe, mantené
> la spec como borrador condicional y no infieras permiso de esta solicitud.
> Desglosá el patch externo en resampler compartido128, asociación visual común,
> proyector relacional, fuser simétrico, source/RNG, settings resolver, validación
> y trazas. Fijá contratos, dependencias, entregables y criterios de rechazo por
> módulo, mismo checkpoint A/B y baseline diagnóstico que solo difiere en beta.
> Proponé un lock de entorno verificable, lista de descargas y derechos de datos,
> estrategia de entrenamiento y validación independiente; marcá costos/tiempos
> desconocidos sin convertir rangos N3 en mediciones. Separá permisos para código,
> pesos/carga, forwards, entrenamiento y campaña. Exigí un presupuesto completo
> de llamadas auxiliares y trayectorias;200 llamadas no son presupuesto universal.
> Entregá una spec autocontenida y un cuadro de recursos/decisiones, sin implementar,
> instalar, descargar pesos, contratar, entrenar, generar ni admitir campaña.
> Conservá N3/N4 y el gate original bloqueados; no uses X1 como fallback.

## 2. Prerregistro de validación semántica y presupuesto de pruebas

Próxima spec propuesta: **VSG-2B / N5V · Contrato de validación y recursos de prueba**.
Puede redactarse antes de implementar. Resuelve cómo distinguir un efecto útil de
ruido o pérdida protegida y evita adquirir datos/cómputo sin un criterio de cierre.

Prompt para copiar:

> Prepará la spec «VSG-2B / N5V · Contrato de validación y recursos de prueba» a partir
> de N4S y su propuesta versionada, sin asumir aprobación ni pesos disponibles.
> Diseñá un prerregistro que separe cobertura textual, semántica del resampler,
> dependencia causal del canal B, persistencia temporal y preservación visual.
> Detallá control beta0.3, candidato beta1, neutralización, réplica y mutación
> aislada con el mismo patch/weights/source/texto/RNG; los hashes de campaña deben
> rechazar el D mutado. Definí corpus independiente/licenciado, exclusiones de
> D/E/Kenny/C para training/tuning, cegamiento, métricas de relaciones, literal,
> identidad y pérdidas protegidas. Indicá qué evidencia falta para fijar umbrales
> de utilidad, efecto mínimo y tamaño muestral; no rellenes esos valores sin base.
> Enumerá llamadas aprendidas, decodes, posibles intentos y costos por prueba;
> proponé techos, STOP y ledger sin declarar exentos forwards ni alterar los ocho
> intentos vigentes. Evitá doble conteo de receipts reutilizados. Entregá una spec
> y matriz de pruebas/prerrequisitos/presupuesto listas para revisión. No ejecutes
> pruebas con pesos, adquieras corpus, generes imágenes ni modifiques política,
> settings, manifests o gates. Todos los resultados futuros siguen NOT_RUN.
