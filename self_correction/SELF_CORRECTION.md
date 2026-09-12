# SVS 1.5 Self-Correction

Goal: generate → inspect → diagnose → choose correction → revise → re-inspect → stop.

## Correction Orchestrator
Inputs: SAR, Transformation Plan, Output, VCR, VFR[], Compliance Result, Revision History.
Decision: ACCEPT / REVISE / REGENERATE / STOP.

## Revision zones
ACTIVE — must change.
DEPENDENT — may change only when necessary to correct ACTIVE.
LOCKED — must remain stable.

Freeze capability may be PIXEL, SEMANTIC or NONE depending on adapter.

## Correction Budget
CB0 NONE
CB1 LOCAL
CB2 REGIONAL
CB3 STRUCTURAL
CB4 RESTART

Use the smallest correction budget capable of resolving the failure.

## Best Known Output (BKO)
Maintain the best validated output across revisions. A candidate cannot replace the BKO if it introduces a hard failure or an equal/greater regression in a higher-authority domain.

Protected Success Set (PSS) stores domains that must be revalidated after each revision.
Regression severity: RG0 none / RG1 negligible / RG2 material / RG3 major / RG4 critical.

Never build a later revision on a rejected regressed branch. Return to BKO first.

## Escalation
LOCAL_EDIT → REGIONAL_EDIT/REGENERATION → FULL_REGENERATION only when the more invasive strategy adds new leverage.

If evidence is insufficient, REQUEST_REFERENCE.
If model repeatedly violates a clear Revision Contract despite sufficient evidence, MODEL_SWITCH_ADVISED.
If ambiguity is authorial or canon-related, HUMAN_REVIEW.

Maximum: output initial + up to three automatic revisions. Early stop is preferred.

## Stop signals
PASS achieved; only S0/S1 remain within Failure Budget; correction risk exceeds benefit; Acceptance Floor reached; revisions exhausted; regression persists; evidence insufficient; capability insufficient; human decision required.

Detect diminishing returns and revision oscillation.
