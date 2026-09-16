# Reference Need Model (RNM) 1.0

A Reference Need exists only when the source and governing SVS rules leave a scoped evidence deficit that matters to the requested transformation.

## States

### `RN_NONE`
Source evidence is sufficient. Do not query Archive.

### `RN_SUPPORT`
External evidence may improve material behavior, period plausibility or implementation detail, but is not required for source identity.

Archive retrieval is allowed with a small evidence budget.

### `RN_REQUIRED`
The requested transformation requires scoped documentary support that the source does not contain.

Query Archive. If unresolved, preserve ambiguity or block the unsupported branch.

### `RN_BLOCKED`
The missing information is protected by a hard lock and generic external references cannot legitimately fill it.

Examples:
- exact unreadable source text
- hidden authored geometry with no corroborating source
- exact Fear City geography outside evidence
- exact identity of an unseen object

Do not query Archive to manufacture an answer.

## Decision inputs

Reference Need is evaluated from:
- source sufficiency
- transformation demand
- mode
- profile
- CGC `infer`
- CGC `unknown`
- Semantic Text Lock
- Occlusion Locks
- geographic identity constraints
- transfer risk

## Core rule

`UNKNOWN` does not automatically imply `RN_REQUIRED`.

Some unknowns must remain unknown.

## SVS 1.9 Scene-Derived Needs

Scene Intelligence may emit Reference Need hints.

`UNKNOWN_LOCKED` maps to `RN_BLOCKED`, not to automatic retrieval.

`TRANSFORM_SCOPED` may map to `RN_SUPPORT` or `RN_REQUIRED` only when a declared Archive domain can legitimately support the transformation.
