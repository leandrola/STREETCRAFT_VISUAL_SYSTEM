# CGC Enrichment · End-to-End

SVS 1.10.0 wires Reference Reasoning 2.0 into the single Streetcraft orchestration path.

`CIL → SAR2 → CGC draft → Reference Need → Archive → RR2 admission → CGC enrichment → 1.9.1 preflight → adapter handoff`

Primary orchestration: `integration/streetcraft_orchestrator.py`.
CLI with explicit Archive root/catalog: `integration/run_streetcraft_orchestration.py`.

Only `READY` RR2 evidence projects into the CGC. Required unresolved/review evidence blocks before preflight. Scoped evidence carries bundle IDs, admissions, traces and negative evidence. SAR2 unknown locks and protected relationships remain authoritative. Preflight may still block Semantic Text mutation, Fear City geography import, reference bleed or unauthorized material intensity.

`GENERATION_READY` means the final Compact Generation Contract is cleared for a vendor adapter. It is not a claim that an image was generated or visually approved.
