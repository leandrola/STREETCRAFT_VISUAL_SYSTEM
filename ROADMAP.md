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
2. **VSG-0.5 Diagnostic Benchmark: COMPLETADO Y VALIDADO.** Fault injection controlado sobre percepción/SAR2, RR2, proyección VSG, shadow compiler y salida observada. Resultado 13/13, accuracy 100%, cobertura causal completa y control sano sin falsos positivos. No implica todavía extracción de grafos desde píxeles.
3. **VSG-1 Graph Locks: COMPLETADO Y VALIDADO.** Ledger determinista con Semantic Text, Geometry, Occlusion y Reference Isolation Locks. Validación `VALIDATE_ONLY`, IDs estables, strength, estado esperado y provenance. Fixture crítico 5/5 locks; 25/25 tests; mutaciones negativas detectadas sin gobernar generación.
4. **VSG-1.5 Causal Trace: COMPLETED AND VALIDATED.** 19/19 casos causales, 100% de atribución primaria, 0 ciclos, 0 referencias sin resolver y control sano sin falsos positivos. Trazas deterministas `TRACE_ONLY`, sin autoridad sobre generación. [Contrato y evidencia](visual_scene_graph/VSG_1_5_CAUSAL_TRACE.md).
5. **VSG-2A Generation Compiler Shadow: COMPLETED AND VALIDATED.** 25/25 casos controlados, contrato shadow determinista y comparación automática contra CGC estable + restricciones de origen. Control sano: preservación P0 9/9, PR0 2/2, PR1 3/3 y locks 6/6; cero falsos positivos. Sin cambios de generación. [Arquitectura y verificación](visual_scene_graph/VSG_2A_GENERATION_COMPILER_SHADOW.md). Una integración de producción requiere autorización y gate propios.
6. **VSG-3 Graph Critic: PENDIENTE.** Comparación Expected Graph vs Observed Output Graph y emisión de Graph Delta. Requiere primero extracción confiable del grafo de salida.

El track VSG permanece desacoplado de Build Kit durante sus primeras etapas. El punto de integración futuro será un `BK Compiler` consumidor del mismo grafo, no una dependencia de VSG-0.
