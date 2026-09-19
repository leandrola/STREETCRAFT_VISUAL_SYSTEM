# Low-Confidence Text Mask (LCTM)

LCTM converts uncertain text into non-semantic visual instructions before generation.

For `MASK_GRAPHIC_ONLY`, generation may preserve:
- approximate line count
- block/label shape
- tonal contrast
- typographic density
- placement and orientation

Generation may not emit:
- a business name
- product name
- price
- address
- slogan
- street name
- newspaper title
- readable poster copy

`UNKNOWN` is preferable to plausible invented text.
