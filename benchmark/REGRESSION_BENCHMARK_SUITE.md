# SVS 1.8 · Regression & Benchmark Suite

## Purpose

The Regression & Benchmark Suite is the release gate for future Streetcraft versions.

A new version should not be considered stable merely because its new feature works. It must also prove that it did not break previously validated Streetcraft behavior.

The suite separates three layers:

1. **R0 Automated Regression** — deterministic code, routing, schema and invariant tests.
2. **R1 Fixture Integrity** — hashes and identity of stable visual/evidence fixtures.
3. **R2 Visual Benchmark** — controlled generation/inspection cases scored against Streetcraft invariants.

## Release gate

A candidate release is:

### `PASS`
- R0 = 100% pass
- R1 = 100% fixture integrity
- R2 weighted score >= 90
- all critical invariants pass
- no S3 finding
- no unapproved governing-file drift

### `REVIEW`
- R0 and R1 pass
- R2 score 85–89, or
- exactly one non-critical S2 regression that has an explicit waiver

### `FAIL`
Any of:
- R0 < 100%
- R1 < 100%
- any critical invariant fails
- any S3
- Visual Canon / source-authority regression
- Fear City false-positive routing
- semantic text invention
- unsupported geographic identity import
- hidden-geometry invention under a lock
- unapproved protected-file drift

## Principle

The suite measures Streetcraft behavior, not image beauty.

A visually impressive output can fail the benchmark.


## SVS 1.8.1 calibration rule

R2 is split into:
- **R2a Baseline Calibration** — establishes golden visual expectations.
- **R2b Candidate Regression** — required for future behavior-changing releases.

SVS 1.8.1 completes R2a. It does not falsely label existing goldens as fresh candidate generations.
