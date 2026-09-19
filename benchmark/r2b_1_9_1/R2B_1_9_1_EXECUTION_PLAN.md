# R2B 1.9.1 · EXECUTION PLAN

Status: PREPARED
Release under test: SVS 1.9.1 Candidate
Baseline authority: SVS 1.8.1 R2 visual baseline
Promotion gate: S3 = 0 AND global score >= 90

## Purpose

Run a fresh visual candidate regression after the 1.9.1 critical patch. Every candidate must be an individual output derived from a real fixture. No benchmark dashboards, score labels, PASS overlays or self-certification may appear in generated images.

## Required critical blocks

CIL 1.1 recovery adds a sixth required camera-regression block. The original five blocks remain unchanged.

### R2B-191-A · VP02 CG-A
Goal:
- validate CG-A as frontal-oblique architectural immersion;
- preserve source/building identity;
- maintain eye-level/slightly-low camera;
- dominant architectural plane;
- no collapse into CG-B or theatrical wide-angle;
- no invented architecture, text or geography.

Candidate requirements:
- one clean image;
- source fixture recorded;
- command/config recorded;
- no score or evaluation text embedded in image.

### R2B-191-B · VP02 CG-B
Goal:
- validate CG-B as street-level oblique monumentality;
- same source identity class as CG-A comparison;
- principally two-point perspective;
- stronger side-depth reading than CG-A;
- no wide-angle spectacle;
- no geometry redesign.

Candidate requirements:
- one clean image;
- source fixture recorded;
- command/config recorded;
- explicit later comparison against CG-A.

### R2B-191-C · Fear City / Reference Isolation
Goal:
- preserve authored Fear City geometry;
- preserve CG-FC authored-view relationship;
- prevent New York or other geographic import;
- prevent reference-specific signage, props, wetness, camera or architecture from leaking into the source;
- keep Archive/reference evidence strictly scoped.

Critical S3 triggers:
- geographic import;
- authored-world topology change;
- reference-specific geometry copied out of scope;
- unauthorized CG-FC replacement.

### R2B-191-D · Semantic Text Lock
Goal:
- preserve LEGIBLE_EXACT text literally;
- preserve known portions of PARTIAL text only;
- keep ILLEGIBLE/OCCLUDED text semantically unresolved;
- prevent token mutation such as 315 → 313;
- prevent invented microtext.

Critical S3 triggers:
- substitution of exact text;
- invented exact wording from illegible/partial source text.

### R2B-191-E · Occlusion Lock
Goal:
- preserve LOCKED_UNKNOWN regions;
- use only minimum continuity when reconstruction is authorized;
- do not reveal exact hidden geometry without multi-view or explicit reconstruction authority;
- avoid reference-filling of hidden content.

Critical S3 triggers:
- specific hidden object/geometry invention;
- reference-derived hidden reconstruction outside authority.


### R2B-191-F · VP02 CG-F / RDR2 Elevation
Goal:
- validate `/sc-rdr2-elevation` as `VP02 + T02 + CG-F`;
- strict frontalization without redesigning source architecture;
- enforce Identity Lock and `LOCKED_UNKNOWN` Occlusion Lock;
- retain 16:9 output contract and minimal street presence;
- ensure CG-F remains visually distinct from CG-A and CG-B.

Critical S3 triggers:
- facade proportions/opening rhythm redesigned to achieve frontal view;
- exact hidden geometry invented to complete elevation;
- identity-bearing signage/relationships displaced or substituted;
- CG-F collapses into oblique CG-A/CG-B behavior when strict elevation is requested.

## Candidate-generation rule

Generator produces image only. Evaluation happens afterward in a separate pass.

The generation layer may receive:
- source fixture;
- resolved CIL configuration;
- SAR2;
- CGC;
- admitted scoped reference evidence when allowed.

The generation layer may not receive:
- expected score;
- PASS/FAIL target;
- baseline verdict;
- previous evaluator prose that names the desired result.

## Evaluation sequence

1. Verify source/fixture identity.
2. Verify candidate is a fresh individual output.
3. Compare source → candidate.
4. Compare baseline 1.8.1 expectations → candidate.
5. Apply visual scoring rubric.
6. Record S0/S1/S2/S3 findings.
7. Evaluate critical gate.
8. Only evaluation layer may issue PASS/FAIL.

## Promotion condition

SVS 1.9.1 may be promoted to Stable only when:
- all six required R2b critical blocks have valid fresh candidates;
- total S3 count = 0;
- global weighted score >= 90/100;
- no critical gate violation;
- source identity and protected authored-world constraints survive.

Otherwise Candidate status remains active.
