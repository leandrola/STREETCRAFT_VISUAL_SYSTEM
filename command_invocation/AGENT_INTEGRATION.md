# CIL Agent Integration

1. Scan the request for `/sc-*`.
2. Expand through `COMMANDS.json`.
3. Reject unknown commands and profile conflicts.
4. Apply modifiers over macro defaults.
5. Re-apply normal Streetcraft source authority and routing.
6. If `/sc-status` is present, report the resolved configuration before generation.
7. Continue with normal Streetcraft execution.

CIL never grants authority that the underlying SVS does not already possess.

## 1.6.4 Contract Expansion
CIL commands resolve into the Compact Generation Contract before normal generation. CIL remains an invocation layer and cannot weaken hard source-authority locks.

## SVS 1.7 Archive-Aware Behavior
CIL syntax is unchanged. Reference retrieval is automatic and follows the resolved CGC. A short command such as `/sc-2b` does not authorize broad Archive imitation.
