# Repository cleanup report

Date: 2026-09-21. Release baseline: **SVS 1.10.0 STABLE**. Scope: housekeeping and documentation only; no branch, release promotion, runtime behavior, public schema, score, threshold or policy changes. No commit or push was performed by the cleanup agent. External workspace activity created commits during this task; see the Git section below.

## Inventory before changes

[INVENTORY_BEFORE.json](INVENTORY_BEFORE.json) records every repository-content file with its primary category, tracked status, byte size and SHA-256, plus duplicate groups and the starting Git commit. The starting working tree was clean.

Counts exclude Git internals, `.venv` and `.browser-profile`, which are separately counted in the inventory and preserved. Byte sizes are logical file sizes, not filesystem allocation. Symlinks inside local state are not followed or counted.

| Category | Before | Treatment |
| --- | ---: | --- |
| A · Runtime | 10 | Preserve byte-for-byte |
| B · Contract / schema | 19 | Preserve byte-for-byte |
| C · Test | 32 | Preserve active runners and fixtures |
| D · Validation evidence | 232 | Preserve bytes and original manifests |
| E · Documentation | 63 | Update current entry points and status |
| F · Historical | 25 | Preserve; contextualize superseded instructions |
| G · Generated / temporary | 7 | Remove local macOS metadata |
| H · Obsolete / duplicate | 0 safely deletable | Duplicates have evidence/fixture roles; retained |

The categories are primary roles: tests and evidence can also contain schemas and executable examples. Policy/specification documents under `core`, `transform`, `hardening`, `patch`, `reference` and `scene_intelligence` are retained in full. Every relevant directory is represented in the per-file inventory.

## Changes and consolidation

- Replaced the short root README with the product entry point, implemented architecture, real command examples, validation evidence and repository map.
- Updated the Cheat Sheet release heading; commands are unchanged.
- Corrected the current RR2 document's outdated promotion-pending statement.
- Replaced the real catalog README's obsolete session limitation with completed validation and the actual external-runtime dependency.
- Marked `INTEGRATION_NOTES.md`, `HITO3_CGC_END_TO_END_COMPLETION.md`, `RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md` and `REFERENCE_V2_ARCHIVE_INTEGRATION.md` as historical, linking to current final results. Historical measurements and decisions are retained.
- Repaired two obsolete executable path occurrences in `REFERENCE_V2_ARCHIVE_INTEGRATION.md` to the existing `reference_runtime/run_reference_archive.py`.
- Consolidated current-status navigation through the stable integration document and final gate; no evidence files were merged or removed.
- Extended `.gitignore` for `.cache`, `.tox`, `.nox`, Python package metadata and root `build`, `dist`, `tmp`, `outputs` directories. No blanket JSON, image, ZIP or log ignore rule was added.

## Exact deleted files

Only these seven ignored, untracked macOS files were deleted (47,132 bytes). **No versioned files were deleted.**

```text
.DS_Store
benchmark/.DS_Store
benchmark/r2b_1_9_1/.DS_Store
validation/.DS_Store
validation/camera_routing/.DS_Store
validation/cgc_e2e/.DS_Store
validation/rr2_real_archive/.DS_Store
```

No repository-content `__pycache__`, `.pyc`, nested ZIP, accidental log or named backup candidate was found. Existing ignored browser state and the virtual environment are local working resources; they were not deleted or incorporated into the deliverable. Validation stdout/stderr/exit-code files are deliberate gate evidence, including empty files.

## Protected files and duplicates

All original `.py` files, public schemas, configurations, Canon assets, release decisions, CHANGELOG, final release notes and validation artifacts are unchanged. Protected evidence includes:

- All of `benchmark/baselines/`, `benchmark/fixtures/` and `benchmark/r2b_1_9_1/`, including all six final R2b cases, their sources, initial/rerun candidates and scorecards.
- All of `validation/rr2_real_archive/`, `validation/cgc_e2e/` and `validation/gate4_2026_09_21/`: eight real cases each, requests, results, traces, bundle IDs, input/module hashes and identity records.
- `reference_runtime/real_catalog/*.json`, `reference/assets/`, camera evidence, all original SHA manifests and reconstruction provenance.
- CIL, SAR2, CGC, RR2, hardening/preflight and single-client governance code, tests and contracts.

The byte-hash inventory found **18 duplicate groups**. Exact membership and SHA-256 values are in the inventory. None was deleted:

| Duplicate | Reason to retain |
| --- | --- |
| `R2B-191-D_candidate_PASS.png` / `R2B-191-F_candidate_initial.png` | Separate final/initial benchmark roles, both in final evidence manifest |
| `R2B-FC-001_source.jpg` / `FCV001_VIEW_01.jpg` | R2b and camera-validation provenance paths |
| `RDR-F01_L_KATZENSTEIN.jpg` / `RDR-F07_DAVES_CORNER.png` | Deliberate cross-ID duplicate used by real RR2 deduplication cases |
| Eight RR2 result pairs across original validation and Gate 4 | Evidence of both original validation and promotion rerun |
| CGC report / captured stdout, repeated stdout, exit codes and empty stderr | Separate execution records; equality is not grounds for deleting audit evidence |

## References and historical manifests

The initial Markdown-link scan found no broken Markdown links. A broader literal-path scan found 638 absent path literals; [REFERENCE_AUDIT.json](REFERENCE_AUDIT.json) preserves the exact findings and classifications. These are predominantly historical manifest entries, external Archive modules or original execution paths, not 638 broken current links. Code-resolved fixture basenames also appear in that heuristic scan and pass their tests.

The confirmed obsolete runner path was corrected in two places. The no-longer-needed patch named in the historical implementation checklist is explicitly identified as already integrated. Historical package names, unavailable original build paths and old cache hashes remain as provenance, not current setup requirements. Deleting the seven local metadata files broke no document references.

All 377 entries of the original release manifest matched before editing. The original manifest and final package integrity report are preserved. Current documentation differences are explicitly recorded as old/new hashes in [CLEANUP_VERIFICATION.json](CLEANUP_VERIFICATION.json), and a supplemental [CLEANUP_SHA256SUMS.json](CLEANUP_SHA256SUMS.json) covers the post-cleanup content. This does not claim byte identity between edited documentation and the original release package.

## Tests and verification

See [CLEANUP_VERIFICATION.json](CLEANUP_VERIFICATION.json) for exact commands, interpreter/dependency versions, outputs and results, and [VERIFICATION.md](VERIFICATION.md) for reproduction instructions.

Before editing, unified regression passed all 14 checks. Fresh post-cleanup validation runs in an isolated copy so that existing runners cannot overwrite signed release evidence. It includes unified regression, both camera runners, all schema definitions, stored CGC/SAR2 instances, R2b hashes/score arithmetic, RR2/CGC provenance, protected-file identity and internal documentation links.

**External execution limitation:** `STREETCRAFT_ARCHIVE_V1_FINAL` is not present in this repository or in the accessible locations searched. Downloads access was denied by the OS, and a runtime location was requested. Consequently RR2 real-case execution, CGC real E2E execution and the two external Archive integration scripts cannot be freshly certified here. Their preserved release evidence is verified separately. No mock or reconstructed runtime was substituted.

The recorded release remains RR2 real 8/8 PASS and CGC E2E 8/8 PASS; those historical results must not be reported as fresh runs. The complete requested validation is therefore pending the external dependency even if every available local check passes.

## Manual review candidates

Deliberately retained:

- All 18 duplicate groups, especially the RDR-F01/F07 pair and initial R2b candidates; do not deduplicate by byte equality alone.
- DEV/PREP/INTEGRATED and older versioned checksum manifests, partial/earlier QA reports, reconstruction records, camera routing patch material and earlier release notes. Their scope is historical; removing them requires an explicit provenance-retention decision.
- `legacy/STREETCRAFT_WEBAPP_HANDOFF.md` and image-export planning: historical/adjacent design material, not proof of a current SaaS or export implementation.
- Historical `RR2_REAL_CATALOG_CODE.patch` and original ZIP references: not present as local files, but useful provenance of already integrated material.
- External Archive software: required to repeat the remaining real integration runs. Its 20 recorded hashes are preserved, but metadata cannot replace missing executable bytes.
- `.browser-profile` and `.venv`: ignored local state with potential ongoing utility, outside tracked-package cleanup.

No abandoned script could be demonstrated safe to delete: executable files are current runtime/tests or retained validation tooling covered by provenance. Older filenames alone were not treated as evidence of obsolescence.

## Fresh local results

| Check | Post-cleanup result |
| --- | --- |
| Unified regression | 14/14 checks PASS |
| CIL / hardening / Archive-aware unit | 19/19 · 12/12 · 10/10 PASS |
| RR2 / orchestrator unit | 18/18 · 10/10 PASS |
| Scene Intelligence / patch | 24/24 · 24/24 PASS |
| Single-client governance | PASS |
| Camera matrix / L3 routing | PASS (counts and output in verification JSON) |
| Schemas and stored contract instances | PASS |
| Original runtime, contracts and protected evidence | Unchanged |
| R2b evidence | 14/14 SHA/size matches; 6 final cases, score 91.0, S3=0 |
| Recorded RR2/CGC provenance | 16 cases; request/evidence hashes and 20-module recorded maps match |
| Internal Markdown links | PASS |
| Fresh external Archive RR2/CGC execution | NOT RUN — external runtime unavailable |

The RR2 cache-reuse case repeats a bundle ID across traces; its summary lists unique bundle IDs. Audit comparison uses unique IDs while retaining every original trace. No original test or expected result was changed.

## Git and exact file lists

Starting commit: `ba7c2c19d9eeb09d88644112fac95ff09e4e9aea`. During this task, external workspace activity created `274bc6d` and `8144132`, incorporating documentation work. The cleanup agent did not issue commit/push/reset commands and did not undo that activity. Therefore the ordinary final `git diff --stat` may contain only the remaining changes; compare to the starting commit for the complete task diff.

Original versioned files modified by this task:

```text
.gitignore
CHEAT_SHEET.md
HITO3_CGC_END_TO_END_COMPLETION.md
INTEGRATION_NOTES.md
README.md
REFERENCE_V2_ARCHIVE_INTEGRATION.md
RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md
reference_runtime/REFERENCE_REASONING_2.md
reference_runtime/real_catalog/README.md
```

Added audit/documentation files:

```text
docs/repository/CLEANUP_SHA256SUMS.json
docs/repository/CLEANUP_VERIFICATION.json
docs/repository/INVENTORY_BEFORE.json
docs/repository/REFERENCE_AUDIT.json
docs/repository/REPOSITORY_CLEANUP_REPORT.md
docs/repository/VERIFICATION.md
```

The exact deleted local paths are listed above. No tracked paths were deleted, moved or renamed. No runtime or API changes were made.

<!-- FINAL_COUNTS -->
## Final file counts and size

| Scope | Before | After |
| --- | ---: | ---: |
| Repository content files (excluding Git/env/browser local state) | 388 | 387 |
| Logical bytes in that scope | 49,455,778 | 49,730,354 |
| Original tracked paths retained | 381 | 381 |
| Added audit/documentation files | 0 | 6 |
| Removed ignored metadata files | 0 | 7 |

Local metadata removal saved 47,132 bytes. The total size changed by +274,576 bytes because the expanded documentation and explicit inventory, reference audit, test outputs and current SHA manifest are retained for review. This is not a binary-evidence size reduction. The final supplemental manifest verifies every retained repository-content file except itself.
<!-- END_FINAL_COUNTS -->
