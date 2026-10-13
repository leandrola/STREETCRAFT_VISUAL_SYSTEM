# Continuidad acotada de Streetcraft

El supervisor local usa un sobre registrado en `development/coordination/CHECKPOINT.json`. Sus observaciones viven bajo `.git/sc-supervisor/`; nunca sustituyen el checkpoint ni cierran tareas por sí mismas.

Antes de comenzar, cerrar cualquier otro orquestador integrador y comprobar que HEAD y el digest del checkpoint coincidan con el sobre. La primera tanda usa cero imágenes, cero gasto adicional, hasta dos invocaciones Codex y 30 minutos totales.

```bash
python3 scripts/sc_supervisor.py start --envelope SC03-PILOT-READONLY-01
python3 scripts/sc_supervisor.py status
python3 scripts/sc_supervisor.py stop
python3 scripts/sc_supervisor.py reconcile
```

`start` toma un lock no bloqueante por el repositorio canónico, inicia Codex con argumentos estructurados y conserva JSONL, stderr y metadata por `run_id`. El plazo no se renueva. En timeout pide interrupción al grupo de procesos, escala a terminación y comprueba si el PID continúa observable.

`status` separa el estado autorizado del checkpoint de la observación del proceso. `stop` no modifica decisiones de negocio. `reconcile` compara base y checkpoint y nunca relanza automáticamente. Un resultado `ORPHANED_OR_UNKNOWN`, un cambio externo de HEAD/checkpoint o una aprobación nueva requerida bloquea otra tanda hasta reconciliar.

La reanudación futura debe usar un ID de sesión persistido explícito; nunca “la última sesión”. `SC_CONTINUITY_READY` exige además una tanda real, revisión por modelos efectivos distintos y pruebas completas de recuperación. Mientras esos gates falten, el estado correcto es `SC_CONTINUITY_PREPARED_PENDING_LIVE` o `SC_CONTINUITY_BLOCKED`.
