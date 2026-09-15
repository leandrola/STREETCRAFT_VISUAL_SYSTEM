# Compact Generation Contract Enrichment

SVS 1.7 extends the 1.6.4 CGC with a `reference_runtime` block.

```json
{
  "reference_runtime": {
    "status": "READY",
    "needs": ["RN-..."],
    "evidence_bundle_ids": ["EB-..."],
    "admitted_evidence": [],
    "negative_evidence": [],
    "unresolved_needs": [],
    "authority_map": "RAM-1.0"
  }
}
```

## Prompt-safe evidence projection

Only the following should reach generation instructions:
- scoped visible facts
- permitted learning
- explicit negative evidence
- unresolved uncertainty

Do not pass unrestricted reference captions or globally imitate a retrieved image.

## Reference isolation

Each admitted item carries:
- domain
- evidence unit ID
- Archive ID
- provenance
- authority score
- transfer risk
- permitted learning
- forbidden transfer

This preserves auditability and prevents reference bleed.
