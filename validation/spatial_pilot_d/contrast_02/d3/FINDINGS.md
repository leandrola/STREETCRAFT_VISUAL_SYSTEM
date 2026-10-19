# D3 — all planned injection outcomes

| Case | Ink height | Expected | Rendered | Recognized | Classes obtained | Image / truth |
| --- | --- | --- | --- | --- | --- | --- |
| sans_8_sharp | 8 | ADVERTENCIA | True | True | {'ADVERTENCIA': 1, 'VIOLACION': 1} | [image](execution/synthetic/sans_8_sharp.png) / [truth](execution/synthetic/sans_8_sharp.json) |
| sans_8_blur | 8 | ADVERTENCIA | True | True | {'ADVERTENCIA': 1, 'VIOLACION': 1} | [image](execution/synthetic/sans_8_blur.png) / [truth](execution/synthetic/sans_8_blur.json) |
| sans_12_sharp | 12 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/sans_12_sharp.png) / [truth](execution/synthetic/sans_12_sharp.json) |
| sans_12_blur | 12 | VIOLACION | True | True | {'ADVERTENCIA': 1} | [image](execution/synthetic/sans_12_blur.png) / [truth](execution/synthetic/sans_12_blur.json) |
| sans_20_sharp | 20 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/sans_20_sharp.png) / [truth](execution/synthetic/sans_20_sharp.json) |
| sans_20_blur | 20 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/sans_20_blur.png) / [truth](execution/synthetic/sans_20_blur.json) |
| sans_40_sharp | 40 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/sans_40_sharp.png) / [truth](execution/synthetic/sans_40_sharp.json) |
| sans_40_blur | 40 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/sans_40_blur.png) / [truth](execution/synthetic/sans_40_blur.json) |
| sans_80_sharp | 80 | VIOLACION | False | NOT_EVALUATED | SKIPPED_DOES_NOT_FIT_FROZEN_ZONE | No image: frozen zone too narrow / [truth](execution/synthetic/sans_80_sharp.json) |
| sans_80_blur | 80 | VIOLACION | False | NOT_EVALUATED | SKIPPED_DOES_NOT_FIT_FROZEN_ZONE | No image: frozen zone too narrow / [truth](execution/synthetic/sans_80_blur.json) |
| serif_8_sharp | 8 | ADVERTENCIA | True | True | {'VIOLACION': 1, 'ADVERTENCIA': 1} | [image](execution/synthetic/serif_8_sharp.png) / [truth](execution/synthetic/serif_8_sharp.json) |
| serif_8_blur | 8 | ADVERTENCIA | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_8_blur.png) / [truth](execution/synthetic/serif_8_blur.json) |
| serif_12_sharp | 12 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_12_sharp.png) / [truth](execution/synthetic/serif_12_sharp.json) |
| serif_12_blur | 12 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_12_blur.png) / [truth](execution/synthetic/serif_12_blur.json) |
| serif_20_sharp | 20 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_20_sharp.png) / [truth](execution/synthetic/serif_20_sharp.json) |
| serif_20_blur | 20 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_20_blur.png) / [truth](execution/synthetic/serif_20_blur.json) |
| serif_40_sharp | 40 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_40_sharp.png) / [truth](execution/synthetic/serif_40_sharp.json) |
| serif_40_blur | 40 | VIOLACION | True | True | {'VIOLACION': 1} | [image](execution/synthetic/serif_40_blur.png) / [truth](execution/synthetic/serif_40_blur.json) |
| serif_80_sharp | 80 | VIOLACION | False | NOT_EVALUATED | SKIPPED_DOES_NOT_FIT_FROZEN_ZONE | No image: frozen zone too narrow / [truth](execution/synthetic/serif_80_sharp.json) |
| serif_80_blur | 80 | VIOLACION | False | NOT_EVALUATED | SKIPPED_DOES_NOT_FIT_FROZEN_ZONE | No image: frozen zone too narrow / [truth](execution/synthetic/serif_80_blur.json) |
| duplicate | 20 | ADVERTENCIA_DUPLICADO | True | True | {'ADVERTENCIA_DUPLICADO': 1} | [image](execution/synthetic/duplicate.png) / [truth](execution/synthetic/duplicate.json) |
| core_control | 20 | IGNORADO_POR_SOLAPE | True | True | {'IGNORADO_POR_SOLAPE': 1} | [image](execution/synthetic/core_control.png) / [truth](execution/synthetic/core_control.json) |

## D3 baseline findings

| Crop | OCR text | Confidence | Normalized xyxy | Class |
| --- | --- | --- | --- | --- |
| [tile_000_line_000](execution/D3_baseline/crops/tile_000_line_000.png) | & CO. | 0.300 | 0.41056, 0.61278, 0.45043, 0.66111 | IGNORADO_POR_SOLAPE |
| [tile_001_line_000](execution/D3_baseline/crops/tile_001_line_000.png) | Business 23/4/o pime | 0.300 | 0.48428, 0.13674, 0.62000, 0.27677 | IGNORADO_POR_SOLAPE |
| [tile_001_line_001](execution/D3_baseline/crops/tile_001_line_001.png) | Loans | 1.000 | 0.49024, 0.17374, 0.53725, 0.22604 | IGNORADO_POR_SOLAPE |
| [tile_001_line_003](execution/D3_baseline/crops/tile_001_line_003.png) | ec Business | 0.300 | 0.56293, 0.25441, 0.61961, 0.31456 | IGNORADO_POR_SOLAPE |
| [tile_001_line_004](execution/D3_baseline/crops/tile_001_line_004.png) | Loan | 1.000 | 0.58568, 0.29499, 0.61762, 0.33967 | IGNORADO_POR_SOLAPE |
| [tile_001_line_005](execution/D3_baseline/crops/tile_001_line_005.png) | 722 LOAN | 0.500 | 0.48574, 0.24273, 0.56340, 0.32329 | IGNORADO_POR_SOLAPE |
| [tile_001_line_006](execution/D3_baseline/crops/tile_001_line_006.png) | Center | 1.000 | 0.58017, 0.30958, 0.62026, 0.36245 | IGNORADO_POR_SOLAPE |
| [tile_001_line_007](execution/D3_baseline/crops/tile_001_line_007.png) | TERMINAL | 1.000 | 0.49133, 0.53659, 0.53826, 0.56809 | IGNORADO_POR_SOLAPE |
| [tile_001_line_008](execution/D3_baseline/crops/tile_001_line_008.png) | DINER | 1.000 | 0.48888, 0.55890, 0.54080, 0.60374 | IGNORADO_POR_SOLAPE |
| [tile_001_line_009](execution/D3_baseline/crops/tile_001_line_009.png) | HаCO. | 0.300 | 0.40000, 0.61303, 0.45388, 0.67050 | IGNORADO_POR_SOLAPE |
| [tile_002_line_000](execution/D3_baseline/crops/tile_002_line_000.png) | ssiness 39 lo Prma, | 0.300 | 0.49041, 0.13800, 0.62497, 0.27549 | IGNORADO_POR_SOLAPE |
| [tile_002_line_001](execution/D3_baseline/crops/tile_002_line_001.png) | oans | 1.000 | 0.49677, 0.17855, 0.53693, 0.22400 | IGNORADO_POR_SOLAPE |
| [tile_002_line_003](execution/D3_baseline/crops/tile_002_line_003.png) | ccBusiness | 0.300 | 0.56233, 0.25554, 0.61950, 0.31466 | IGNORADO_POR_SOLAPE |
| [tile_002_line_005](execution/D3_baseline/crops/tile_002_line_005.png) | 22-LOAN | 0.500 | 0.49385, 0.24939, 0.56356, 0.32431 | IGNORADO_POR_SOLAPE |
| [tile_002_line_007](execution/D3_baseline/crops/tile_002_line_007.png) | ERMINAL | 1.000 | 0.49847, 0.53875, 0.53804, 0.56809 | IGNORADO_POR_SOLAPE |
| [tile_002_line_008](execution/D3_baseline/crops/tile_002_line_008.png) | INER | 1.000 | 0.49811, 0.56177, 0.54066, 0.60340 | IGNORADO_POR_SOLAPE |
| [tile_002_group_000](execution/D3_baseline/crops/tile_002_group_000.png) | oans 1-800 | 0.500 | 0.49677, 0.17855, 0.54764, 0.28386 | IGNORADO_POR_SOLAPE |
| [tile_003_line_000](execution/D3_baseline/crops/tile_003_line_000.png) | LKATZENS | 0.300 | 0.30819, 0.62261, 0.39224, 0.67050 | IGNORADO_POR_SOLAPE |
| [tile_004_line_000](execution/D3_baseline/crops/tile_004_line_000.png) | Business e | 1.000 | 0.49123, 0.14266, 0.55724, 0.20897 | IGNORADO_POR_SOLAPE |
| [tile_004_line_002](execution/D3_baseline/crops/tile_004_line_002.png) | 23/2% Prime | 0.300 | 0.54432, 0.18408, 0.61978, 0.26251 | IGNORADO_POR_SOLAPE |
| [tile_004_line_003](execution/D3_baseline/crops/tile_004_line_003.png) | 1-800 | 1.000 | 0.49984, 0.22447, 0.54748, 0.28359 | IGNORADO_POR_SOLAPE |
| [tile_004_line_004](execution/D3_baseline/crops/tile_004_line_004.png) | Business | 0.500 | 0.56432, 0.25580, 0.61936, 0.31480 | IGNORADO_POR_SOLAPE |
| [tile_004_line_010](execution/D3_baseline/crops/tile_004_line_010.png) | A&CO. | 0.300 | 0.40000, 0.61111, 0.45388, 0.67050 | IGNORADO_POR_SOLAPE |
| [tile_005_line_000](execution/D3_baseline/crops/tile_005_line_000.png) | usiness o 3/2 lo Prime | 0.300 | 0.49074, 0.13985, 0.62067, 0.27951 | IGNORADO_POR_SOLAPE |
| [tile_005_line_004](execution/D3_baseline/crops/tile_005_line_004.png) | Loam | 0.300 | 0.58624, 0.29570, 0.61774, 0.34066 | IGNORADO_POR_SOLAPE |
