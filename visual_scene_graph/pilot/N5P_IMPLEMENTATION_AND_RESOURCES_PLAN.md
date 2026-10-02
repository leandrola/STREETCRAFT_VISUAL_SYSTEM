# N5P implementation and resources plan

**RECONSTRUCTION DRAFT — 2026-10-02. Not a recovered original or approved plan.**
The three historical Markdown deliverables could not be located in the bounded
local/history search. This draft reconstructs committed evidence at `2a489a6` and
the hash-verified [authoritative spec](../../validation/vsg_2b/orchestration_pilot/VSG_2B_N5P_N5V_PREEXECUTION_SPEC.md).
The separate [audit](../../validation/vsg_2b/orchestration_pilot/AUDIT.json) corrects
documentary availability without modifying historical N5PV/N4S results.

Design basis: `VSG-2B-N4R-GLIGEN-FULL-SCHEDULE@0.1.0`, PROPOSED_NOT_APPROVED.
Settings applied, implementation authorized and execution authorized are all false.
Execution budget complete and semantic criteria frozen are false. This draft is
for review; the original Markdown contents remain unknown.

Sources: [N4S decision](N4S_CLOSURE_AND_SETTINGS_DECISION.md),
[N5PV historical result](../../validation/vsg_2b/N5PV_RESULT.json),
[input manifest](../../validation/vsg_2b/n5pv/INPUT_MANIFEST.json),
[budget proposal](../../validation/vsg_2b/n5pv/EXECUTION_BUDGET_PROPOSAL.json),
[validation matrix](../../validation/vsg_2b/n5pv/VALIDATION_MATRIX.json), and
[campaign policy](campaign_policy.json). Counts below are inherited proposals,
not measurements or approved quotas. New effort estimates are UNKNOWN.

## Contract and comparison

A receives common plus exact JSONL text, with R absent. B receives common text plus
ten typed records; B is never serialized into the prompt and A is never parsed to
produce R. Both use the same composed checkpoint/patch, source association S,
preprocessing, RNG and scheduler settings. R-neutral retains attention/FF/S;
zero keys or a whole-fuser bypass are invalid substitutes. Common already contains
protected relations, so the endpoint measures incremental representation benefit.

The proposed full-text route has 75-token blocks and 128 shared resampler slots:
A 7,305 content / 7,307 including specials; B 5,686 / 5,688. Existing tokenizer
evidence is preserved, not rerun. The source is D at 347×389 with edge padding to
512, M_KEEP1 and latent reinjection. Evidence regions confer no editing authority;
pixel-exact preservation is not promised. Beta1.0 candidate and beta0.3 diagnostic
control use the same future patch. For the fixed 50-step PNDM proposal, 51 UNet
calls are planned; other settings require their own resolver check.

## Sequential future deliveries

All paths in this table are proposals, not implemented artifacts. Each stage stops
on failed acceptance; no later stage begins by default. Owners are UNASSIGNED until
authorization. Per-stage engineering effort is UNKNOWN; the inherited D2 40-hour
cap is a ceiling, not an estimate or promise.

| Stage / proposed modules | Input → output | Dependencies / future acceptance | Rollback / permission |
| --- | --- | --- | --- |
| Contract/settings/log scaffold: `visual_scene_graph/pilot/n5_scaffold/` | Immutable contract/config → validated envelope and reservation/error records | Explicit D1/D2; allowlist and static checks below; stdlib only, no dispatch or model imports | Remove disabled scaffold integration; retain logs; D2 only |
| Environment lock: proposed `validation/vsg_2b/n5_environment/LOCK.json` | Core pins/package metadata → transitive wheel hashes, container and driver digest | D3; complete compatible target lock, rights and hardware plan; no install/load in documentary tranche | Reject incomplete lock; retain prior DRY_RUN state |
| Shared patch: proposed `visual_scene_graph/pilot/n5_model/shared_patch.py` | UNet inputs, shared S and optional R → conditional prediction | Separate implementation authorization beyond D2; neutral path retains attention/FF/S; same architecture/weights A/B | Disable candidate ID; no READY fallback |
| Full text: proposed `n5_model/full_text.py` | Exact ordered blocks → 128 shared slots | Shared learned resampler; reject truncation/overflow; coverage does not prove comprehension | Reject checkpoint/route; no silent short-prompt fallback |
| Source/R: proposed `n5_model/projectors.py` | Source association, five nodes/two edges → shared S and typed R | Rights, masks, supported predicates and authority checks; no mutation admitted as frozen D | Disable candidate; preserve frozen source/payload |
| Data/training: proposed `validation/vsg_2b/n5_data/SPLITS.json` and `n5_model/training.py` | Licensed disjoint scene pairs → trained composite artifact and receipts | D3 rights/review closure then explicit staged D4; no D/E/Kenny/C tuning; fixed bounded training proposal | Stop, retain counters and rejected checkpoints |
| Load/causal probe: proposed `n5_model/diagnostics.py` | Frozen weights/config/RNG → hooks, repeats and final-observable evidence | Complete budget, trained modules, classified counters and explicit D4; eight matrix tests | Stop on mismatch/cap/no sensitivity; preserve evidence |
| Visual campaign: future versioned manifest/admission only | Authorized outputs → independent rubric and paired endpoint | N5V calibration/freeze, reviewers, new settings/admission, existing policy coverage | Reject protected loss/UNKNOWN; preserve all attempts |

Future D2 allowlist v0.1 (review proposal; no files created now):

1. `visual_scene_graph/pilot/n5_scaffold/README.md`
2. `visual_scene_graph/pilot/n5_scaffold/__init__.py`
3. `visual_scene_graph/pilot/n5_scaffold/contract.py`
4. `visual_scene_graph/pilot/n5_scaffold/settings.py`
5. `visual_scene_graph/pilot/n5_scaffold/ledger.py`
6. `visual_scene_graph/pilot/n5_scaffold/fixtures.json`
7. `visual_scene_graph/pilot/n5_scaffold/static_checks.py`
8. `validation/vsg_2b/n5_scaffold/STATIC_RESULT.json`

Its proposed sixteen static acceptance checks cover: valid envelope; missing field;
unknown field; supported predicate; unsupported predicate; exact input hash;
mutated D rejection; protected lock completeness; A R absence; B typed records;
explicit config identity; A/B shared-setting equality; zero execution caps;
reservation cap rejection; retained failed reservation/no retry; no model imports,
dispatch or operational settings/policy changes. The reviewer must approve the
allowlist/check definitions before D2 execution. It implements contracts/logs only.

## Environment, learned modules and resources

The committed manifest proposes Diffusers0.29.0 at
`39aa3909e8e2dfe30f4807aedaadf42c1d8b1a8f`, Transformers4.41.2 at
`573565e35a5cc68f6cfb6337f5a93753ab16c65b`, PyTorch2.3.1 and a CPython3.11
Linux x86_64 target. Checkpoint `masterful/gligen-1-4-inpainting-text-box` revision
`d6d957f8d27c40889c0d570a616571a5645c8be3`, fp16 storage, is a design dependency.
Metadata evidence does not establish an installed compatible runtime. Full
transitive lock/container/driver digest remain incomplete. No package installation,
weight download, loading or tokenizer execution occurs in this pilot.

Proposed learned modules: resampler, S projector, R projector and fuser rank8
LoRA/gates. Their weights do not exist as verified trained deliverables. The budget
estimates 42,868,128 trainable parameters and 685,890,048 bytes for fp32 parameter,
gradient and Adam states (16 bytes/parameter). Frozen residency, activations and
workspace remain unmeasured; published payload size is not peak memory evidence.
48 GiB GPU /64 GiB host /256 GiB storage and 38.4 GiB GPU STOP are planning caps.
Actual peak RAM/VRAM and runtime are NOT_MEASURED; hardware adequacy is unproven.

The inherited data scenario proposes train1,024, validation128, calibration24 and
holdout128 disjoint scenes, 1,304 total licensed pairs. Available pairs, rights for
image/annotation/transformation, annotator capacity, evaluator availability and
costs are UNKNOWN. D/E/Kenny/C are excluded from training/tuning/calibration.
The committed bounded optimizer/loss scenario remains conditional and unapproved;
no hyperparameter search or extra learned loss network is implicitly allowed.

## Unified budget and gates

Use the budget JSON's receipt DAG, not sums of overlapping test rows. The diagnostic
proposal totals 425 invocations /915 processed units: CLIP47/180 sequences,
UNet357/714 CFG units, seven trajectories, five decodes, one matched A/B pair.
Text/source caches are shared only by complete immutable keys. Repeat tests reuse
declared caches and do not prove uncached preprocessing reproducibility. Internal
hooks add no invocation; four direct fuser calls are counted. Retry cap is zero.

Training preparation/training/validation proposes 93,121 invocations, 4,096
backward passes and 512 optimizer steps; all stages together propose 93,546
invocations. GPU-hour caps are 8 preparation +24 training/validation +2 diagnostics
=34. These are STOP ceilings, not measured durations. All approved learned calls,
attempts, outputs, training steps and spend remain zero.

The current policy allows eight attempts and requires four distinct pairs.
Seven diagnostic trajectories plus six additional E/Kenny/C branches total thirteen
unique attempts, exceeding eight. The D-only diagnostic proposal cannot close the
campaign, is not admitted, and has no approved counter classification. Full
latent-only trajectories still count as generative compute; diagnostics are not
exempt. E/Kenny remain unsupported by this design; C remains blocked.

Money stays UNKNOWN, including a monetary ceiling. Preserve the complete cost
formula in the budget JSON (GPU/CPU/storage/egress/data/annotation/review/engineering
and tax/fees); unknown rates are never zero. STOP before any learned call if rights,
lock, measurement, classification, approved caps, calibration or reviewers are
missing. Cancel/failed actions retain reservation and attempt records. Rollback
disables the candidate without resetting counters or promoting beta0.3 to READY.

[N5V reconstruction](N5V_SEMANTIC_VALIDATION_PREREGISTRATION.md) defines the evidence
needed; [next decisions](N5PV_WORK_MODE_NEXT_STEPS.md) identify the authorization
gate. VSG-2B stays BLOCKED / PENDING_VISUAL; production/provider_READY remain false.
