# Semantic Text Lock (STL)

Text is documentary geometry and semantics at the same time.

## States

- `LEGIBLE_EXACT` — text is confidently readable. Exact semantic reproduction is permitted.
- `PARTIAL` — only some characters/words are readable. Preserve the known portion and the uncertainty.
- `ILLEGIBLE` — graphic form may be preserved, but semantic content must not be invented.
- `OCCLUDED` — hidden text remains unknown unless corroborated by another authoritative view.
- `ABSENT` — do not add text.

## Hard rules

1. Graphic resemblance never authorizes semantic invention.
2. An unreadable sign may remain sign-like, but cannot acquire a plausible new business name, number, slogan or street name.
3. Known text must not be paraphrased when the task is faithful reinterpretation.
4. Typography may be visually reconstructed only within the evidence state.
5. New semantic text requires explicit user authorization or authoritative evidence.

`UNKNOWN` is a valid output.
