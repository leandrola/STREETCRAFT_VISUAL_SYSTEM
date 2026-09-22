# STREETCRAFT.md
## Entry point for AI agents
Version: SVS 1.10.0
Status: STABLE / single Streetcraft client
Base: SVS 1.9.1 / CIL 1.1; R2b final gate PASS 91.0, S3=0.

Streetcraft is a visual transformation specification.

## Primary objective
Interpret a supplied source while preserving its authored or documentary identity. Transform only what the task authorizes.

## Authority hierarchy
1. Explicit user intent
2. P0 source invariants
3. Transformation Mode
4. Visual Profile
5. Camera Grammar / Auto-Routing constraints
6. Streetcraft Core Visual Grammar
7. Period and regional constraints
8. Creative preferences

## Camera routing summary
- CG-A: frontal-oblique architectural immersion
- CG-B: street-level oblique monumentality
- CG-F: strict frontal elevation camera (CIL 1.1)
- CG-S: source-locked camera
- CG-FC: Fear City authored-view camera

Confirmed Fear City defaults to:
`T06 → VP03 → CG-FC`

## Command Invocation Layer
CIL 1.1 commands include:
`/sc-core`, `/sc-classic`, `/sc-2`, `/sc-2a`, `/sc-2b`, `/sc-rdr2-elevation`, `/sc-fear`, `/sc-fear2`, `/sc-clean`, `/sc-lock`, `/sc-auto`, `/sc-front`, `/sc-preserve`, `/sc-noinvent`, `/sc-status`, `/sc-help`.

Elevation aliases: `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`.

`/sc-rdr2-elevation` → `VP02 + T02 + CG-F` with strict Identity Lock, `LOCKED_UNKNOWN` Occlusion Lock, strict frontalization, 16:9 and minimal street. See `command_invocation/CG_F_FRONTAL_ELEVATION.md`.

## Operational Hardening 1.6.4
Use Semantic Text Lock, Material Intensity Delta, Occlusion Locks, Compact Generation Contract and Micro-Drift Critic.

## Archive-Aware Reference Runtime 1.7
Reference Need states: `RN_NONE`, `RN_SUPPORT`, `RN_REQUIRED`, `RN_BLOCKED`. Archive evidence is scoped and never outranks source identity.

## Regression & Benchmark Suite 1.8 / 1.8.1
R0 automated regression, R1 fixture integrity, R2a calibrated visual baseline, R2b candidate regression for behavior-changing releases.

## Scene Intelligence 1.9
Before final CGC resolution, build SAR2:
`Entities → Roles → Relationships → Authority → Salience → Action Plan → Reference Gaps`.

## Critical Hardening Patch 1.9.1
Before generation run:
1. Semantic Token Freeze
2. Low-Confidence Text Mask
3. Fear City Geographic Null Lock
4. Reference Bleed Preflight
5. Atmosphere / Material Carryover Guard

Any S3-class violation blocks generation.

Read `patch/PATCH_RUNTIME_ORDER.md` and `integration/PATCH_HOOKS_1_9_1.md`.

## Reference Reasoning 2.0
Primary reference entry: `reference_runtime/reference_reasoning.py`. It extends the single Streetcraft flow and uses Archive-aware admission as an internal component. It is not a separate client or alternative runtime.

SVS 1.10.0 is STABLE. Final Gate 4 passed regression, visual evidence, real Archive/RR2 evidence and CGC end-to-end orchestration. Primary orchestration: `integration/streetcraft_orchestrator.py`.

## Visual Scene Graph · VSG-0 Observer

VSG-0 is an optional passive projection of SAR2. When a request includes
`"vsg": {"mode": "OBSERVER"}`, orchestration emits `visual_scene_graph` with
typed nodes, explicit relations, confidence, locks, provenance, and functional
subgraphs. It is diagnostic only and must keep `governs_generation=false`.
Absence of VSG must preserve the stable response shape. See
`visual_scene_graph/VSG_0_OBSERVER.md`.

VSG-0.5 adds a non-governing diagnostic benchmark. It localizes controlled
faults to perception/SAR2, RR2, graph projection, shadow compilation or
generation output. It does not perform pixel-level output-graph extraction and
does not authorize VSG to govern generation. See
`visual_scene_graph/diagnostic_benchmark/README.md`.

## VSG-1 · Graph Locks

VSG-1 adds a deterministic `graph_locks` ledger to every enabled VSG graph.
Semantic Text, Geometry, Occlusion and Reference Isolation locks carry stable
IDs, strength, expected state and provenance. The validator compares a candidate
graph against that ledger and emits typed S3/S2 findings. Enforcement remains
`VALIDATE_ONLY`; VSG-1 cannot alter CGC, adapter input or `generation_ready`.
See `visual_scene_graph/VSG_1_GRAPH_LOCKS.md`.
