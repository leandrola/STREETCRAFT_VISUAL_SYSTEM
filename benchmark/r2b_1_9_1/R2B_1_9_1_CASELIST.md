# R2B 1.9.1 · CRITICAL CASELIST

| Case | Block | Required | Primary risk | Gate |
|---|---|---|---|---|
| R2B-191-A | VP02 CG-A | YES | camera collapse / identity drift | no S3 |
| R2B-191-B | VP02 CG-B | YES | camera collapse / geometry redesign | no S3 |
| R2B-191-C | Fear City / Reference Isolation | YES | geographic/reference bleed | no S3 |
| R2B-191-D | Semantic Text Lock | YES | exact-token substitution / invented microtext | no S3 |
| R2B-191-E | Occlusion Lock | YES | hidden geometry invention | no S3 |
| R2B-191-F | VP02 CG-F / Elevation | YES | frontalization identity drift / hidden reconstruction | no S3 |

## Run order
1. Semantic Text Lock
2. Fear City / Reference Isolation
3. VP02 CG-A
4. VP02 CG-B
5. Occlusion Lock
6. VP02 CG-F / Elevation

## Global release gate
All six valid + S3 = 0 + global weighted score >= 90.
