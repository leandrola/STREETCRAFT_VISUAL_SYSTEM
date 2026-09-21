# Component reachability audit

Scope: the SVS 1.10.0 STABLE repository at the start of root archival. No listed directory was deleted, moved or changed.

“Yes” denotes an observed dependency/reference, not inferred runtime execution. Python imports, explicit orchestrator references, tests, documentation and manifests were searched separately. A documentary concept does not count as an executable import, and checksumming a file does not make it runtime code. References introduced by this audit itself are excluded as evidence.

| Directory | Imported by runtime? | Referenced by orchestrator? | Referenced by tests? | Referenced by documentation? | Referenced by manifests? | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| `critic/` | No | No | No | Yes | Yes | SUPPORT |
| `intelligence/` | No | No | No | Yes | Yes | SUPPORT |
| `self_correction/` | No | No | No | Yes | Yes | SUPPORT |
| `legacy/` | No | No | No | Yes | Yes | HISTORICAL |
| `patch/` | Yes | Yes | Yes | Yes | Yes | ACTIVE |
| `release_decisions/` | No | No | Yes | Yes | Yes | ACTIVE (validation governance) |

## Evidence

- **Critic:** contains [VISUAL_CRITIC.md](../../critic/VISUAL_CRITIC.md), no Python implementation. [AGENT_PROTOCOL.md](../../agent/AGENT_PROTOCOL.md) step 6 invokes Visual Critic conceptually; [PATCH_RUNTIME_ORDER.md](../../patch/PATCH_RUNTIME_ORDER.md) and [R2_EXECUTION_POLICY.md](../../benchmark/R2_EXECUTION_POLICY.md) reference critic behavior. `PACKAGE_MANIFEST.json` lists `critic`, and release/build checksum manifests include the file. No automated post-generation Critic invocation was found in the orchestrator.
- **Intelligence:** contains [VISUAL_INTELLIGENCE.md](../../intelligence/VISUAL_INTELLIGENCE.md), no Python module. Agent protocol step 2 references Visual Intelligence; the Changelog records its analysis stack. The package lists `intelligence` and checksum manifests cover it. The implemented orchestrator imports **`scene_intelligence`**, not `intelligence`; the two were not conflated in this audit.
- **Self-correction:** contains [SELF_CORRECTION.md](../../self_correction/SELF_CORRECTION.md), no executable module. Agent protocol step 7 and the Changelog reference its revision policy. Release/build checksum manifests include it; it is not listed in the current package module array. No executable correction loop was found in the central orchestrator.
- **Legacy:** [STREETCRAFT_WEBAPP_HANDOFF.md](../../legacy/STREETCRAFT_WEBAPP_HANDOFF.md) explicitly marks the former web-app direction as frozen. The [earlier cleanup report](REPOSITORY_CLEANUP_REPORT.md) references this file; historical/current release checksum snapshots include its path. It is not listed as a current package module and has no runtime or test caller.
- **Patch:** [streetcraft_orchestrator.py](../../integration/streetcraft_orchestrator.py) adds `patch` to its import path, imports `classify_text_token`, `low_confidence_render_hint` and `patch_pre_generation_gate` from `svs_1_9_1_patch`, and calls the gate before handoff. [test_patch_1_9_1.py](../../validation/test_patch_1_9_1.py) imports the patch; the unified runner executes it, and orchestrator tests exercise integration. [STREETCRAFT.md](../../STREETCRAFT.md), patch hooks and the package manifest reference the active controls.
- **Release decisions:** [test_single_client_1_10_0.py](../../validation/test_single_client_1_10_0.py) reads `release_decisions/SVS_1_10_0_SINGLE_CLIENT.json` and checks the promotion gate. The earlier cleanup report lists the directory as protected evidence; the Stable checksum manifest records both decision files. It is active governance input to tests, not imported runtime code; the older 1.9.1 decision remains historical evidence within the same directory.

## Limits and future review

Static searches establish the checked-in consumers only; an external host may read these specifications. The SUPPORT classification does not claim a currently implemented autonomous Critic or self-correction runtime. None of the absent Python edges justifies deletion. Any future consolidation requires a separate scope and provenance review.
