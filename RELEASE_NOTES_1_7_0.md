# SVS 1.7.0 Release Notes

## Release focus
Archive-Aware Reference Runtime.

## Core change
SVS can now determine whether external documentary evidence is needed, query Streetcraft Archive V1, admit only eligible scoped Evidence Units, and project those units into the Compact Generation Contract.

## Reference Need states
- RN_NONE
- RN_SUPPORT
- RN_REQUIRED
- RN_BLOCKED

## Safety/authority properties
- source invariants remain above Archive evidence
- Semantic Text Lock remains active
- Occlusion Locks remain active
- Fear City geographic identity remains locked
- visual similarity cannot create authority
- conflicts remain conflicts
- zero-result retrieval preserves uncertainty
- Archive unavailable never silently falls back to fake Archive evidence

## CIL
No new slash-like command is required. Archive use is automatic after Reference Need evaluation.
