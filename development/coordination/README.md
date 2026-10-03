# Streetcraft development coordination pilot

This repository state coordinates development; it does not change the image-generation
protocol in `agent/AGENT_PROTOCOL.md` or launch an unattended service. The product
roadmap remains [ROADMAP](../../ROADMAP.md). Active tasks and resume state are in
[CHECKPOINT](CHECKPOINT.json); reconciliation evidence is in
[audit](../../validation/vsg_2b/orchestration_pilot/AUDIT.json).

Authority: user instruction `RUN IT` on 2026-10-02 invokes
`/Users/macbookpro/Documents/STREETCRAFT_ORCHESTATION_PILOT/ORCHESTRATION_PILOT_BOOTSTRAP.md`.
The bootstrap permits setup, documentary recovery, static checks, task-owned commits
and normal pushes. This current permission supersedes the historical N5 spec's
no-commit/no-push restriction for this pilot only. The bootstrap itself grants no
D1–D4 approval. On 2026-10-02 the user explicitly approved D1 as a design basis and
D2 exclusively for the proposed isolated scaffold, including its limits, M3 closure,
verification, commit and push. The exact approval is preserved in CHECKPOINT.
No applicable AGENTS.md was found in the checkout or its ancestor directories.

Permitted: this coordination layer, evidence audit, source preservation, clearly
labeled N5PV reconstruction drafts and the approved eight-file D2 stdlib scaffold.
The scaffold is isolated and provides contracts/settings validation and simulated
zero-unit log transitions only. Forbidden: consumer/model patch implementation,
settings application, weight downloads/loading, tokenization/model calls, training,
generation, paid provisioning and production promotion. Preserve historical records.
No production/provider readiness may follow from documentary checks.

State meanings:

| State | Meaning |
| --- | --- |
| DOCUMENTARY_READY | Required files exist, sources are traceable and unknowns are explicit; ready for document review only. |
| IMPLEMENTED | Authorized artifacts were written; no verification implied. |
| VERIFIED | Acceptance checks passed and independent review examined actual evidence. |
| BLOCKED | A named dependency or authorization prevents the next milestone. |
| CLOSED | All acceptance criteria for that particular milestone passed; never inherited by a parent milestone. |

Sequential milestones:

| Milestone | Owner | Dependencies and acceptance |
| --- | --- | --- |
| M1 coordination setup | Root agent | Scope, permissions, task ownership, state definitions, gates and readable checkpoint exist and parse; close setup before M2. |
| M2 N5PV documentary reconciliation | Root agent; recovery specialist; independent verifier | M1 closed; source hash verified; bounded recovery recorded; all declared input hashes audited; three originals recovered or labeled drafts created; correction record preserves historical results; static checks and independent evidence review pass. Closure certifies reconciliation only. |
| M3 D2 isolated scaffold | Root agent; independent verifier | M2 closed; explicit D1/D2 decisions cited in checkpoint; eight approved files, sixteen meaningful static checks, preserved operational/historical inputs, zero execution budgets and independent review. CLOSED only when these criteria pass; see current checkpoint. |
| Next D3 metadata/data/criteria/lock closure | Unassigned; authorization pending | Separate bounded D3 decision; rights, reviewer availability, quotes, criteria/calibration and environment lock dependencies. No model execution or purchase permission is implied. |
| VSG-2B visual closure | Unassigned | Original campaign policy coverage, admission, authorized runtime and genuine visual/semantic evidence. Remains BLOCKED / PENDING_VISUAL. |

Decisions: D1 is APPROVED_DESIGN_BASIS_ONLY; D2 is APPROVED_ISOLATED_SCAFFOLD_ONLY.
D3 metadata/data/criteria/lock closure and D4 staged model execution remain PENDING.
The [historical decision package](../../visual_scene_graph/pilot/N5PV_WORK_MODE_NEXT_STEPS.md)
and M2 audit/results retain their earlier pending flags as historical evidence;
CHECKPOINT records the current explicit approval. No historical proposal is rewritten.

The root agent writes task-owned artifacts. The recovery specialist searches read-only.
The verifier reviews files, hashes and gates independently; it is not a visual evaluator.
No reviewer for future model outputs has been appointed. Findings require correction
and recheck before milestone closure. Bound each failed operation to one corrective retry;
then save the cause and checkpoint. Push once normally; a failure preserves the commit.

Resume: read CHECKPOINT, verify git status/HEAD and audit evidence, preserve unrelated
work, then satisfy the current blocker before starting the next milestone. Never bypass
a failed gate. Usage telemetry is UNKNOWN; no percentage compliance is certified.

Current M3 code, versioned fixtures, commands, evidence and review are linked from
[scaffold README](../../visual_scene_graph/pilot/n5_scaffold/README.md) and
[STATIC_RESULT](../../validation/vsg_2b/n5_scaffold/STATIC_RESULT.json). Exactly eight
new files belong to the approved allowlist; these two existing coordination files
record authorization/checkpoint updates. M2's historical checker asserts the earlier
pending state and must be interpreted at its `8ca0422` baseline. Current M3 checks
read repository-backed sources only and verify preservation of all prior files
except these explicitly authorized coordination updates.
