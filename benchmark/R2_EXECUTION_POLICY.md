# R2 Execution Policy

## Framework releases
A release whose only change is benchmark infrastructure may pass its release gate when:
- R0 PASS
- R1 PASS
- R2a baseline calibration PASS
- governing runtime behavior is unchanged

SVS 1.8.1 qualifies.

## Behavior-changing releases
Any future release that changes:
- generation contract
- routing
- camera behavior
- profiles
- hardening
- Archive admission
- source preservation
- visual critic behavior

must run R2b Candidate Regression.

## Baseline updates
A baseline update requires an explicit design decision and cannot be made merely because a candidate failed.
