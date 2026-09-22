# Streetcraft · Roadmap vigente · 21/09/2026

1. **SVS 1.9.1 / CIL 1.1: SUPERSEDED STABLE BASELINE.** R2b final: 6/6, S3=0, 91.0/100 PASS.
2. **SVS 1.10.0 · Reference Reasoning 2.0: STABLE.** Gate 4 final PASS y promoción ejecutada.
3. **Archive-aware reasoning: REAL VALIDATED V1.** Needs, query budget, cache reuse, provenance, cross-ID dedupe, structured contradictions, Semantic Text Lock, Fear City isolation y locked unknowns validados con 8/8 casos reales.
4. **CGC end-to-end: COMPLETADO Y ESTABLE.** CIL → SAR2 → CGC draft → RR2/Archive → CGC enriquecido → hardening/preflight → `GENERATION_READY` o bloqueo explícito. Validación 8/8 PASS.
5. **Gate final SVS 1.10: COMPLETADO.** Regression PASS + R2b 91.0/S3=0 + evidencia visual íntegra + RR2 real 8/8 + CGC E2E 8/8 + Archive runtime 20/20 SHA match.

**Release activa: SVS 1.10.0 STABLE.**

Critic avanzado, Profile Evolution e Image Export Runtime permanecen fuera del roadmap activo 21/9 salvo reincorporación explícita.

## Próximos tracks autorizados · 22/09/2026

### VSG · Visual Scene Graph

1. **VSG-0 Observer: COMPLETADO Y VALIDADO.** Proyección pasiva SAR2 + observaciones RR2 → grafo explícito, con nodos tipados, relaciones, confidence, locks, provenance y circuitos funcionales. No gobierna generación. Fixture inicial: Kenny's Shop / rooftop volumétrico.
2. **VSG-1 Locks: PENDIENTE.** Consolidar Semantic Text, Geometry, Occlusion y Reference Isolation como propiedades verificables del grafo.
3. **VSG-2 Generation Compiler: PENDIENTE Y CONDICIONADO.** Solo entra al runtime si VSG-0/1 demuestra valor diagnóstico sin regresiones.
4. **VSG-3 Graph Critic: PENDIENTE.** Comparación Expected Graph vs Observed Output Graph y emisión de Graph Delta.

El track VSG permanece desacoplado de Build Kit durante sus primeras etapas. El punto de integración futuro será un `BK Compiler` consumidor del mismo grafo, no una dependencia de VSG-0.
