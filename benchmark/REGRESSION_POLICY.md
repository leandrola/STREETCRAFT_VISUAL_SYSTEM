# Regression Policy

A behavior-changing release cannot become Stable on deterministic tests alone.

Stable 1.9.1 requires a fresh R2b visual candidate run with:
- no S3 findings;
- global score >= 90;
- no semantic text mutation/invention;
- no Fear City geographic leakage;
- no locked-occlusion invention;
- no reference bleed outside admitted scope.
