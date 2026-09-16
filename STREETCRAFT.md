# STREETCRAFT.md
## Entry point for AI agents
Version: SVS 1.9.0

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
- CG-S: source-locked camera
- CG-FC: Fear City authored-view camera

Confirmed Fear City defaults to:
`T06 → VP03 → CG-FC`

## Command Invocation Layer
This release includes CIL 1.0 with:
`/sc-core`, `/sc-classic`, `/sc-2`, `/sc-2a`, `/sc-2b`, `/sc-fear`, `/sc-fear2`, `/sc-clean`, `/sc-lock`, `/sc-auto`, `/sc-preserve`, `/sc-noinvent`, `/sc-status`, `/sc-help`

See `command_invocation/COMMAND_INVOCATION_LAYER.md`.


## Operational Hardening 1.6.4
See `hardening/OPERATIONAL_HARDENING.md`. Every generation should resolve a Compact Generation Contract and every inspection should include a Micro-Drift pass.


## Archive-Aware Reference Runtime 1.7
When a scoped documentary deficit matters to the transformation, evaluate Reference Need.

`RN_NONE` → source-only  
`RN_SUPPORT` → optional scoped Archive support  
`RN_REQUIRED` → Archive support required for that branch  
`RN_BLOCKED` → unknown must remain unknown

Read `reference_runtime/ARCHIVE_AWARE_REFERENCE_RUNTIME.md`.


## Regression & Benchmark Suite 1.8
Future releases should pass R0 automated regression, R1 golden fixture integrity and R2 visual benchmarks before being promoted to stable.

See `benchmark/REGRESSION_BENCHMARK_SUITE.md`.


## R2 Baseline 1.8.1
The visual benchmark baseline is calibrated. Future behavior-changing releases must execute R2b Candidate Regression.


## Scene Intelligence 1.9
Before final CGC resolution, build SAR2:
`Entities → Roles → Relationships → Authority → Salience → Action Plan → Reference Gaps`.

Read `scene_intelligence/SCENE_INTELLIGENCE.md`.
