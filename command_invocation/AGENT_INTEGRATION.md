# CIL Agent Integration

1. Scan the request for `/sc-*`.
2. Expand through `COMMANDS.json`.
3. Reject unknown commands and profile conflicts.
4. Apply modifiers over macro defaults.
5. Re-apply normal Streetcraft source authority and routing.
6. If `/sc-status` is present, report the resolved configuration before generation.
7. Continue with normal Streetcraft execution.

CIL never grants authority that the underlying SVS does not already possess.
