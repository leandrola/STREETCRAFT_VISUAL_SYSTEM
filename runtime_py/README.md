# Reference Python Runtime

`sync_runtime.py` is deliberately small and provider-agnostic. It demonstrates:
- stable connector item keys;
- normalized metadata fingerprinting;
- NEW / CHANGED / UNCHANGED / MISSING diff;
- FULL-enumeration protection for missing detection;
- idempotent sync-state upsert.

It does not scrape Pinterest, download images, call GPT or create embeddings. Those are adapter/runtime responsibilities layered after the normalized connector boundary.
