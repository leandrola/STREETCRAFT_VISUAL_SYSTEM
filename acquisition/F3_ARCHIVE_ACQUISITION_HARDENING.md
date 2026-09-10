# Streetcraft Archive 1.0-F3

F3 hardens the successful F2 enumeration before Archive Snapshot 001 is frozen.

Observed live corpus: **547 unique enumerated items**.

## Corrections

### 1. Canonical board provenance lock
Every acquired item is bound to:

`https://ar.pinterest.com/leolaudicina/us-image-archive`

The browser's final `page.url` is no longer allowed to collapse item provenance to the Pinterest locale root.

### 2. High-resolution image candidate
Pinterest resize URLs such as `/236x/` are promoted to `/originals/` candidates.

Important: this is an acquisition candidate, not automatic documentary truth. Network validation of the resulting URL remains required before durable image ingestion.

### 3. 536 is no longer a permanent corpus size
The earlier `536 Pins` text was a completeness hint, not Archive truth. F2 enumerated 547 unique pins. F3 therefore removes 536 from the normal target runner.

Completeness remains governed by stable enumeration. A visible total may still be used diagnostically when available.

### 4. No automatic deletion of the 11-item delta
The 547 candidates are retained. Pin-ID uniqueness is not equivalent to image uniqueness. Image-level/perceptual deduplication belongs to the next audit stage.

## Freeze policy

The included `target-board.F3-normalized-candidate.json` is **not yet Archive Snapshot 001**.

Snapshot 001 should be frozen only after:
1. a fresh F3 live run,
2. canonical board provenance is verified,
3. high-resolution image candidates are reachable or safely downgraded,
4. exact and perceptual duplicate audit is complete.
