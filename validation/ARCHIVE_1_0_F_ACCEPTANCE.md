# Archive 1.0-F Acceptance

## Implemented
- Real-browser acquisition driver: PASS
- pin.it redirect support through browser navigation: PASS by design
- DOM pin enumeration: PASS
- repeated-scroll stabilization: PASS
- duplicate collapse by pin id: PASS
- highest-resolution srcset candidate selection: PASS
- block/login detection: PASS
- FULL safety gate: PASS
- PARTIAL fallback: PASS
- target board configuration: PASS
- 1.0-E normalized record compatibility: PASS

## Environment limitation
Live acquisition of the target board was attempted from the ChatGPT execution environment on 2026-09-08.

The public short URL could not be fetched because this environment did not resolve `pin.it` through its outbound network path. Therefore no real board contents are claimed in this release.

This is an environment limitation, not a successful live-sync result.

## Exit criterion for live validation
Run the included acquisition driver in an environment with public web access and obtain:
- resolved canonical board URL,
- at least one real pin,
- no false FULL declaration,
- normalized snapshot accepted by the downstream adapter/sync runtime.
