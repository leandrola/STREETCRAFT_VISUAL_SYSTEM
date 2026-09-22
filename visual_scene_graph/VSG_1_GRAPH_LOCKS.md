# VSG-1 · Graph Locks

VSG-1 converts Streetcraft preservation flags into a normalized lock ledger.
Every lock has a stable ID, type, target, strength, expected state, provenance,
and `VALIDATE_ONLY` enforcement.

The four lock families are:

- `SEMANTIC_TEXT_LOCK`: exact identity-bearing text;
- `GEOMETRY_LOCK`: node type plus protected PR0/PR1 topology;
- `OCCLUSION_LOCK`: protected occlusion edge or locked unknown region;
- `REFERENCE_ISOLATION_LOCK`: permitted learning and forbidden transfers from an admitted RR2 observation.

`validate_graph_locks(expected_graph, candidate_graph)` verifies a candidate and
emits typed S3/S2 findings. It never modifies the candidate, CGC, adapter input,
or generation status. VSG-1 remains non-governing until a future compiler gate
is explicitly passed.
