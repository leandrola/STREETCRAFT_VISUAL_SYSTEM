# Semantic Token Freeze (STF)

STF strengthens the existing Semantic Text Lock by protecting source text at token level.

## Classification

### `FROZEN_EXACT`
Use when the source token is legible with high confidence and is P0/P1 identity-bearing text or a visible numeral.

The output must reproduce the exact semantic token.

Examples:
- `CBGB`
- `OMFUG`
- `315`
- `PALACE HOTEL`
- authored Fear City street names visible in the source

Any semantic mutation is S3.

### `MASK_PARTIAL`
Some characters are visible, but not enough for exact reconstruction. Preserve graphic density and known fragments only. Do not complete the word.

### `MASK_GRAPHIC_ONLY`
Low-confidence or illegible microtext. Preserve only sign/poster-like graphic behavior. No readable semantic token may be invented.

## Rule

Text confidence affects semantics, not whether a sign-like shape can remain visible.
