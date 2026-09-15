# Micro-Drift Critic (MDC)

MDC runs after the normal Visual Critic and looks for small identity drift.

## Critical micro-drift classes

- text substitution or invented readable text
- window/door count changes
- door/window displacement
- storefront segmentation drift
- roofline/parapet drift
- curb/track/sidewalk relationship drift
- recurring graffiti identity changes
- unauthorized prop additions
- material intensity escalation
- camera family drift
- geographic identity import
- reconstruction of occluded detail without evidence

## Severity

- `S0` none
- `S1` cosmetic
- `S2` meaningful identity drift
- `S3` source/world identity violation

Any S3 fails Streetcraft.
Multiple S2 findings require revision even if the image is aesthetically strong.
