# Archive 1.0-D Acceptance

Acceptance conditions:
- connector output boundary is provider-neutral;
- full vs partial enumeration is explicit;
- incremental diff is idempotent;
- only changed/new items trigger downstream work;
- missing pins are never hard-deleted;
- missing detection occurs only after FULL enumeration;
- connector cannot assign documentary or Canon authority;
- per-item failure does not invalidate successful items;
- SQLite stores sync runs and job state;
- reference implementation passes incremental-sync tests.
