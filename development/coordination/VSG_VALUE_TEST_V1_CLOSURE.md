# VSG value test v1 · Closure

Date: 2026-10-14
Status: **CLOSED / PARKED**

## 1. Frozen mechanical verdict

The frozen scoring rule remains authoritative and is not rewritten after inspection.

**Result: NO PASS — 0/3 pairs.**

Reason:
- D: 4/4 vs 3/4, maximum difference = 1 point.
- E: 4/4 vs 4/4, tie.
- Kenny's Shop: 4/4 vs 4/4, tie.

The frozen rule requires B to preserve (Preservation = 1) and beat A by at least 2 total points in a pair. No pair satisfies that condition under any A/B assignment compatible with the recorded scores.

## 2. Interpretation of the result

**INCONCLUSIVE / NO VALUE CLAIM.**

This is separate from the mechanical verdict.

The v1 test could not evaluate the value hypothesis for VSG because:
- there was no control condition without VSG;
- there was only one run per condition;
- there was no estimate of within-condition variance;
- the corpus saturated: SC did not visibly fail in a way that created room for VSG to demonstrate recovery;
- the effective A/B difference was limited to representation/serialization of `relations_and_locks`;
- generator/runtime conditions differ from the September benchmark, so changes between September and October cannot be attributed to reasoning;
- reasoning was not isolated as a causal variable.

Therefore, v1 provides **no evidence in favor of or against VSG's value**.

## 3. Payload comparison

For D, E and Kenny's Shop, A and B are semantically equivalent except for `relations_and_locks`.

- **A:** `relations_and_locks` is a JSONL-like serialized string.
- **B:** `relations_and_locks` is a native JSON array of objects.

All other compared payload fields are equal within each case, including common/stable CGC content, preserve/forbid/unknown directives, source identity, scene intelligence, regions, nodes, priorities, locks, camera policy and text render plan.

Thus the effective experimental manipulation was **serialization/representation of the same relations and locks**, not a broader content change.

## 4. Provenance and execution limitations

Repository provenance records the six outputs as generated through the ChatGPT integrated image generator using the repository frozen payloads, with source and payload bindings matching the repository manifest.

This does **not** provide independent byte-for-byte transport evidence of what the generator actually consumed. The run did not use the local VSG CLI, provider bridge, CommandGenerator or VSG-2B harness receipts.

Additional limitations:
- the effective execution order grouped both D outputs, then both E outputs, then both Kenny outputs, rather than following the planned randomized order;
- output SHA-256 values were operator-reported and were not independently recalculated from locally available output bytes;
- the exact timestamp for the first valid image remains unrecovered;
- the first-valid clock therefore remains without an exact anchor.

## 5. Learning for future experiments

Before opening a new experimental milestone:
1. verify what input channels the target generator actually accepts;
2. define the control condition first;
3. use multiple runs per condition;
4. choose a case where current SC behavior exhibits a concrete, reproducible failure.

## 6. Parking decision

**VSG and GLIGEN are PARKED.**

Reopen only when both conditions are met:
1. a concrete and reproducible case exists where current Streetcraft fails in a meaningful way; and
2. Streetcraft is willing to adopt a generation engine that accepts spatially structured input such as layout, boxes, masks, depth or an equivalent conditioning channel.

The v1 test did not establish that VSG is beneficial or harmful. It failed to evaluate that hypothesis under the current design.

## 7. Streetcraft priority after closure

Return active development to:
**SC-MULTIAGENT-06 → SC-MULTIAGENT-04 → SC-MULTIAGENT-05**, plus the manual operating flow.

SC-MULTIAGENT-06 must not be relaunched without new explicit authorization.
