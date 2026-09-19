# Visual Benchmark Runbook

R2 is intentionally not faked by the package.

A visual benchmark requires a candidate image generation runtime.

## Procedure

For each VISUAL case in `BENCHMARK_CASES.json`:

1. use the declared fixture(s);
2. execute the specified Streetcraft behavior for the candidate release;
3. save the generated output outside the golden fixture directories;
4. inspect source and candidate side by side;
5. score with `VISUAL_SCORING_RUBRIC.md`;
6. record critical failures and S0–S3 findings;
7. calculate the suite verdict with `score_visual_results.py`.

## Reproducibility record

Record:
- SVS version
- model/provider
- model version if known
- command / CIL input
- seed if supported
- source fixture ID
- generation timestamp
- candidate file SHA-256

## Rule

A model-generated image may not declare itself PASS.

The PASS/FAIL decision belongs to the benchmark evaluation layer.
