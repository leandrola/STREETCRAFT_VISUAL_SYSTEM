# Evidence Admission Policy (EAP) 1.0

Archive retrieval produces candidates. SVS must still admit or reject each candidate.

## Decisions

### `ADMITTED_SCOPED`
Evidence may inform only its declared domain and `permitted_learning`.

### `ADMITTED_NEGATIVE_ONLY`
The item is useful only as an anti-pattern or forbidden-transfer warning.

### `REVIEW_REQUIRED`
Evidence is potentially useful but contains a conflict, medium/high transfer risk, provenance weakness or ambiguous compatibility.

### `REJECTED`
Evidence violates domain, source, provenance, transfer or hard-lock constraints.

## Hard rejection

Reject when:
- candidate domain does not match the Reference Need;
- candidate is UNUSABLE/REJECTED;
- candidate violates `forbidden_transfers`;
- candidate would violate Semantic Text Lock;
- candidate would fill a LOCKED_UNKNOWN occlusion;
- candidate imports geographic identity;
- candidate attempts camera transfer over CG-S or CG-FC;
- candidate creates Canon authority by similarity.

## Admission score

Authority and compatibility lead.

Visual similarity is tertiary and cannot rescue ineligible evidence.

## Conflicts

Conflicting visible facts do not get averaged into a synthetic fact.

The leading item may guide if authority is materially stronger, but the dissent remains in the runtime record.
