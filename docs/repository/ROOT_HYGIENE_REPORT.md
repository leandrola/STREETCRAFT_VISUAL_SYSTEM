# Root hygiene report

Baseline: **SVS 1.10.0 STABLE**. Starting commit: `9a9840cec39da18062d3bb40a1d345d90f1e510e`. Scope: structural/documentation archival only. No release, runtime, schema, threshold, policy, scoring, benchmark or validation-result changes. No commit or push performed by this task.

## Root inventory

**ROOT FILE COUNT BEFORE: 40**
**ROOT FILE COUNT AFTER: 12**

Counts include regular files directly in root, including `.gitignore`; component directories and ignored local environment/browser directories are excluded. The reduction is 28 relocated files, not 28 deleted documents.

Originally present:

```text
.gitignore
CAMERA_ROUTING_PATCH_SCOPE.md
CAMERA_ROUTING_VALIDATION_SCOPE.md
CHANGELOG.md
CHANGELOG_1_9_1.md
CHEAT_SHEET.md
CIL_1_1_RECOVERY.md
CIL_PATCH_SCOPE.md
CIL_SYNC_STATUS_696afe5.md
DEV_SHA256SUMS.json
HITO2_RR2_REAL_ARCHIVE_COMPLETION.md
HITO3_CGC_END_TO_END_COMPLETION.md
HITO4_SVS_1_10_0_PROMOTION.md
IMAGE_EXPORT_FORMATS.md
INTEGRATED_SHA256SUMS.json
INTEGRATION_NOTES.md
PACKAGE_MANIFEST.json
PATCH_MANIFEST_1_9_1.json
PATCH_NOTES_1_9_1.md
PREP_MANIFEST.json
PREP_SHA256SUMS.json
README.md
RECONSTRUCTION_PROVENANCE.json
RECONSTRUCTION_PROVENANCE.md
REFERENCE_REASONING_ARCHIVE_INTEGRATION.md
REFERENCE_V2_ARCHIVE_INTEGRATION.md
RELEASE_NOTES_1_10_0.md
RELEASE_NOTES_1_6_2.md
RELEASE_NOTES_1_6_3.md
RELEASE_NOTES_1_6_4.md
RELEASE_NOTES_1_7_0.md
RELEASE_NOTES_1_8_0.md
RELEASE_NOTES_1_8_1.md
RELEASE_NOTES_1_9_0.md
RELEASE_NOTES_1_9_1.md
RELEASE_NOTES_CIL_1_1.md
ROADMAP.md
RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md
STREETCRAFT.md
SVS_1_10_0_SHA256SUMS.json
```

Remaining:

```text
.gitignore
CHANGELOG.md
CHEAT_SHEET.md
IMAGE_EXPORT_FORMATS.md
PACKAGE_MANIFEST.json
README.md
RECONSTRUCTION_PROVENANCE.json
REFERENCE_REASONING_ARCHIVE_INTEGRATION.md
RELEASE_NOTES_1_10_0.md
ROADMAP.md
STREETCRAFT.md
SVS_1_10_0_SHA256SUMS.json
```

## Files moved

| Original repository-root path | New repository-relative path |
| --- | --- |
| `CAMERA_ROUTING_PATCH_SCOPE.md` | `docs/history/CAMERA_ROUTING_PATCH_SCOPE.md` |
| `CAMERA_ROUTING_VALIDATION_SCOPE.md` | `docs/history/CAMERA_ROUTING_VALIDATION_SCOPE.md` |
| `CIL_1_1_RECOVERY.md` | `docs/history/CIL_1_1_RECOVERY.md` |
| `CIL_PATCH_SCOPE.md` | `docs/history/CIL_PATCH_SCOPE.md` |
| `CIL_SYNC_STATUS_696afe5.md` | `docs/history/CIL_SYNC_STATUS_696afe5.md` |
| `CHANGELOG_1_9_1.md` | `docs/history/CHANGELOG_1_9_1.md` |
| `PATCH_NOTES_1_9_1.md` | `docs/history/PATCH_NOTES_1_9_1.md` |
| `INTEGRATION_NOTES.md` | `docs/history/INTEGRATION_NOTES.md` |
| `REFERENCE_V2_ARCHIVE_INTEGRATION.md` | `docs/history/REFERENCE_V2_ARCHIVE_INTEGRATION.md` |
| `RELEASE_NOTES_1_6_2.md` | `docs/releases/RELEASE_NOTES_1_6_2.md` |
| `RELEASE_NOTES_1_6_3.md` | `docs/releases/RELEASE_NOTES_1_6_3.md` |
| `RELEASE_NOTES_1_6_4.md` | `docs/releases/RELEASE_NOTES_1_6_4.md` |
| `RELEASE_NOTES_1_7_0.md` | `docs/releases/RELEASE_NOTES_1_7_0.md` |
| `RELEASE_NOTES_1_8_0.md` | `docs/releases/RELEASE_NOTES_1_8_0.md` |
| `RELEASE_NOTES_1_8_1.md` | `docs/releases/RELEASE_NOTES_1_8_1.md` |
| `RELEASE_NOTES_1_9_0.md` | `docs/releases/RELEASE_NOTES_1_9_0.md` |
| `RELEASE_NOTES_1_9_1.md` | `docs/releases/RELEASE_NOTES_1_9_1.md` |
| `RELEASE_NOTES_CIL_1_1.md` | `docs/releases/RELEASE_NOTES_CIL_1_1.md` |
| `HITO2_RR2_REAL_ARCHIVE_COMPLETION.md` | `docs/milestones/HITO2_RR2_REAL_ARCHIVE_COMPLETION.md` |
| `HITO3_CGC_END_TO_END_COMPLETION.md` | `docs/milestones/HITO3_CGC_END_TO_END_COMPLETION.md` |
| `HITO4_SVS_1_10_0_PROMOTION.md` | `docs/milestones/HITO4_SVS_1_10_0_PROMOTION.md` |
| `RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md` | `docs/milestones/RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md` |
| `RECONSTRUCTION_PROVENANCE.md` | `docs/provenance/RECONSTRUCTION_PROVENANCE.md` |
| `PREP_MANIFEST.json` | `docs/provenance/PREP_MANIFEST.json` |
| `PREP_SHA256SUMS.json` | `docs/provenance/PREP_SHA256SUMS.json` |
| `DEV_SHA256SUMS.json` | `docs/provenance/DEV_SHA256SUMS.json` |
| `INTEGRATED_SHA256SUMS.json` | `docs/provenance/INTEGRATED_SHA256SUMS.json` |
| `PATCH_MANIFEST_1_9_1.json` | `docs/provenance/PATCH_MANIFEST_1_9_1.json` |

All 28 originals have a destination. Twenty-five are byte-identical; three Markdown documents contain only repaired relative link targets. No files were deleted. Historical statements, release notes, milestones and numeric results were not rewritten.

## Role decisions and protected paths

- `INTEGRATION_NOTES.md`: historical 1.9.1 reconstruction record → history.
- `REFERENCE_V2_ARCHIVE_INTEGRATION.md`: superseded development/synthetic integration record → history.
- `REFERENCE_REASONING_ARCHIVE_INTEGRATION.md`: **current** 1.10 stable Archive integration documentation. It remains in root because the single-client test opens its exact root path. It is linked from the current section of the documentation index; it was not misclassified as history.
- `PACKAGE_MANIFEST.json`: current version 1.10.0, Stable and single-client metadata → root, unchanged.
- `SVS_1_10_0_SHA256SUMS.json`: original promotion evidence → root, unchanged.
- `IMAGE_EXPORT_FORMATS.md`: export design specification outside the closed active roadmap; not clearly superseded, so retained in root for manual review.
- `.gitignore`, README, agent entry, Cheat Sheet, Roadmap, Changelog and active 1.10 release notes remain current root entry points. All remain byte-identical in this task.

### Protected by path dependency

| File retained in root | Hardcoded consumer | Why not moved |
| --- | --- | --- |
| `RECONSTRUCTION_PROVENANCE.json` | `benchmark/run_regression_suite.py` | Active embedded-asset identity check opens `ROOT / 'RECONSTRUCTION_PROVENANCE.json'` |
| `REFERENCE_REASONING_ARCHIVE_INTEGRATION.md` | `validation/test_single_client_1_10_0.py` | Governing-document list expects the root pathname |
| `PACKAGE_MANIFEST.json` | `validation/test_single_client_1_10_0.py` | Current version, single-client flags and RR2 entrypoint are validated here |

No consumer was rewritten, no forwarding file or symlink was added, and no test expectation was relaxed.

### Manifest dependency review before moving

Search scope: all tracked Python, Markdown, JSON and text files, including tests, manifests and validation evidence. Counts include historical inventories; they do not imply active execution.

| Candidate | Referencing files | Python path consumer | Decision |
| --- | ---: | --- | --- |
| `RECONSTRUCTION_PROVENANCE.json` | 8 | benchmark/run_regression_suite.py | Keep root |
| `PREP_MANIFEST.json` | 6 | None found | Archive byte-for-byte |
| `PREP_SHA256SUMS.json` | 5 | None found | Archive byte-for-byte |
| `DEV_SHA256SUMS.json` | 3 | None found | Archive byte-for-byte |
| `INTEGRATED_SHA256SUMS.json` | 6 | None found | Archive byte-for-byte |
| `PATCH_MANIFEST_1_9_1.json` | 7 | None found | Archive byte-for-byte |

For the five moved JSON manifests, all pathname consumers found were documentary/frozen checksum or inventory records, not active Python readers. `PREP_MANIFEST`, `PREP_SHA256SUMS` and `PATCH_MANIFEST` are recorded by earlier build manifests; `INTEGRATED_SHA256SUMS` is recorded by DEV/Stable snapshots. Those references continue to describe the **original package layout**. Their values and bytes were not updated. The complete pre-move dependency listing is preserved in the verification artifact.

The same principle applies to historical release-document paths in the Stable SHA manifest. Archival changes where the current checkout stores those documents; it does not claim that the original package had this layout. The move map above enables provenance lookup. Original release/validation manifests and the prior cleanup checksum artifact remain frozen; the separate post-cleanup manifest describes this tree.

## Links and documentation inspection

**BROKEN LINKS BEFORE: 0**
**BROKEN LINKS AFTER: 0**

All repository Markdown relative links are checked, including the root entry points, new index, moved documents, component docs, benchmark and validation docs. Root README requires no rewrite. The six affected Markdown destinations were repaired:

| Document at new location | Old link target | Repaired target |
| --- | --- | --- |
| `docs/history/INTEGRATION_NOTES.md` | `RELEASE_NOTES_1_10_0.md` | `../../RELEASE_NOTES_1_10_0.md` |
| `docs/history/INTEGRATION_NOTES.md` | `validation/RELEASE_GATE_1_10_0_FINAL.json` | `../../validation/RELEASE_GATE_1_10_0_FINAL.json` |
| `docs/history/REFERENCE_V2_ARCHIVE_INTEGRATION.md` | `REFERENCE_REASONING_ARCHIVE_INTEGRATION.md` | `../../REFERENCE_REASONING_ARCHIVE_INTEGRATION.md` |
| `docs/milestones/RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md` | `validation/RR2_REAL_ARCHIVE_VALIDATION_V1.json` | `../../validation/RR2_REAL_ARCHIVE_VALIDATION_V1.json` |
| `docs/milestones/RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md` | `validation/CGC_END_TO_END_REAL_ARCHIVE_V1.json` | `../../validation/CGC_END_TO_END_REAL_ARCHIVE_V1.json` |
| `docs/milestones/RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md` | `reference_runtime/run_reference_archive.py` | `../../reference_runtime/run_reference_archive.py` |

Historical old path literals in original manifests, audit inventories, exact historical file lists and build records remain as evidence, not live hyperlinks. Fenced executable examples in historical notes retain repository-root working-directory semantics. No intentionally external artifact was given a fabricated local link.

Unavailable external/historical artifacts remain documented: `STREETCRAFT_ARCHIVE_V1_FINAL`, original build ZIPs, the already-integrated `RR2_REAL_CATALOG_CODE.patch`, and historical commit `696afe5`. These are not broken local Markdown links. The external Archive runtime was not found in accessible Documents/Desktop or the local filename index.

## Component reachability

See [COMPONENT_REACHABILITY_AUDIT.md](COMPONENT_REACHABILITY_AUDIT.md) for import, orchestrator, test, documentation and manifest reachability of all six requested directories. None of `critic`, `intelligence`, `self_correction`, `legacy`, `patch` or `release_decisions` was changed or moved.

## Verification

The full available unified regression, both camera suites and schema validation are run in an isolated temporary copy. Existing runners write outputs there, preserving checked-in benchmark/validation results. This copy is only for test isolation, not another product runtime or client.

Fresh local results and exact commands/output are in [ROOT_HYGIENE_VERIFICATION.json](ROOT_HYGIENE_VERIFICATION.json): CIL 19/19, hardening 12/12, Archive-aware unit 10/10, RR2 18/18, SAR2 24/24, orchestrator 10/10, patch 24/24, single-client governance, unified regression 14/14, camera matrix/L3, 16 schema definitions and 22 stored reference/CGC/SAR2 instances.

R2b files and all of `validation/rr2_real_archive/`, `validation/cgc_e2e/` and `validation/gate4_2026_09_21/` are compared byte-for-byte to the starting tree. Stored request/catalog SHA values and Archive module identity maps are checked across 16 recorded RR2/CGC results. The release gate still records R2b 6/6, score 91.0, S3=0 and RR2/CGC real 8/8 each.

**NOT RERUN · EXTERNAL ARCHIVE UNAVAILABLE**: real RR2, real CGC E2E and external Archive integration scripts. This is not a failing local test, and preserved historical PASS evidence is not represented as a fresh execution.

## Checksums

`SVS_1_10_0_SHA256SUMS.json` and every historical SHA/evidence artifact remain unchanged. Five archived JSON manifests retain their exact hashes. [POST_CLEANUP_TREE_SHA256SUMS.json](POST_CLEANUP_TREE_SHA256SUMS.json) is a new current-tree audit, excluding itself and local Git/browser/environment/cache state. No original Stable checksum was regenerated.

## Exact content changes and created files

Moved documents with content changes (relative link targets only):

```text
docs/history/INTEGRATION_NOTES.md
docs/history/REFERENCE_V2_ARCHIVE_INTEGRATION.md
docs/milestones/RR2_REAL_CATALOG_IMPLEMENTATION_STATUS.md
```

Created:

```text
docs/README.md
docs/provenance/README.md
docs/repository/COMPONENT_REACHABILITY_AUDIT.md
docs/repository/ROOT_HYGIENE_REPORT.md
docs/repository/ROOT_HYGIENE_VERIFICATION.json
docs/repository/POST_CLEANUP_TREE_SHA256SUMS.json
```

Deleted: **none** (including filesystem junk). No runtime Python or schema files changed. Existing JSON files were either retained in place or moved byte-for-byte. Git rename detection is used for review; removal of an old path accompanied by its listed destination is a move, not evidence deletion.

## Manual review

- `IMAGE_EXPORT_FORMATS.md`: retained at root; decide its future documentation location separately.
- `RECONSTRUCTION_PROVENANCE.json`: root path protected by regression reader; relocation would require separately authorized test/tool changes.
- `REFERENCE_REASONING_ARCHIVE_INTEGRATION.md`: current documentation with a root path protected by governance tests; a future relocation must update that consumer explicitly.
- External `STREETCRAFT_ARCHIVE_V1_FINAL`: locate the matching runtime to rerun real integration; recorded evidence remains preserved.
- `STREETCRAFT_VISUAL_SYSTEM_V1_6_2.zip`, `STREETCRAFT_VISUAL_SYSTEM_V1_8_1.zip`, `STREETCRAFT_VISUAL_SYSTEM_V1_9_1_CIL_1_1_R2B_PREP.zip`, `RR2_REAL_CATALOG_CODE.patch` and commit `696afe5`: unavailable historical provenance, not new dependencies or unresolved release gates.

No runtime-component obsolescence is inferred from missing imports or directory age.
