# Archive 1.0-E Acceptance

## Goal
Provide a public-Pinterest acquisition boundary and tested normalization runtime without falsely claiming a stable live scraper where Pinterest runtime behavior is environment-dependent.

## Acceptance criteria
- public board is an intake source, not Canon
- shared short URL can be stored without becoming durable identity
- pin identity prefers provider pin ID
- highest-quality exposed still image is selected
- unknown metadata remains null
- duplicate provider IDs collapse within enumeration
- FULL snapshot requires verified complete enumeration
- PARTIAL cannot imply deletion of unseen prior pins
- acquisition is replaceable and separated from normalization
- structured-record normalizer passes tests
- embedded-JSON parser passes fixture test

## Status
PASS for adapter contract and local normalization runtime.
LIVE BOARD ACQUISITION remains environment-dependent and is not falsely marked complete.
