# Archive 1.0-B — Ingestion and Classification Pipeline

## Purpose
Convert each newly discovered archive image into a normalized Streetcraft evidence record without requiring manual tagging.

The pipeline is incremental and source-agnostic. Pinterest is currently the intake surface, but the analysis contract must work the same for any future connector.

## Pipeline
DISCOVER
→ ACQUIRE
→ FINGERPRINT
→ DUPLICATE CHECK
→ VISUAL INSPECTION
→ FACT / INFERENCE SEPARATION
→ DOMAIN CLASSIFICATION
→ EVIDENCE UNIT EXTRACTION
→ TEMPORAL / REGIONAL ESTIMATION
→ PROVENANCE RESOLUTION
→ TRANSFER-RISK REVIEW
→ RETRIEVAL METADATA
→ VALIDATE
→ INDEX

## Stage 1 — Discover
Input: connector item metadata.

Required output:
- source_item_id
- source_url
- board_url or collection identifier
- discovery_timestamp
- caption when available

Discovery never grants authority.

## Stage 2 — Acquire
Acquire a viewable image representation and preserve source metadata when runtime policy permits.

Do not crop, color-correct, restore, sharpen, denoise or otherwise improve the image before analysis. Classification must operate on the evidence as supplied.

## Stage 3 — Fingerprint and Duplicate Check
Create stable fingerprints for:
- source identity
- image bytes when available
- perceptual similarity when available

Duplicate policy:
- exact duplicate → reuse existing SCA identity where provenance confirms same source;
- near duplicate / alternate scan / crop → preserve separate source record if provenance differs, but create a relationship;
- repost without resolvable source → do not treat the repost as independent corroboration.

## Stage 4 — Visual Inspection
The classifier first describes only what is visually supported.

Separate:
- OBSERVED: directly visible;
- DERIVED: conservative property derived from visible structure;
- INFERRED: plausible but not established;
- UNKNOWN: cannot be determined.

Low resolution, occlusion, blur, crop or compression must reduce confidence rather than invite completion.

## Stage 5 — Domain Classification
Evaluate only domains materially present in the image.

Core domains:
ARCHITECTURE
STOREFRONT
SIGNAGE
MATERIALS
WEATHERING
STREET_FURNITURE
TRANSIT_INFRASTRUCTURE
INDUSTRIAL
URBAN_RESIDUE
PEOPLE_ACTIVITY
VEHICLES
CAMERA
LIGHT_ATMOSPHERE
RAIN_SNOW_ASPHALT
TEMPORAL_LAYERING
REGIONAL_CHARACTER

Do not emit empty boilerplate Evidence Units merely to cover every domain.

## Stage 6 — Evidence Unit Extraction
Each useful observation becomes a scoped Evidence Unit.

An Evidence Unit must answer:
1. What is evidenced?
2. Where is it evidenced?
3. How strong is the evidence?
4. What may Streetcraft learn from it?
5. What must not transfer from it?

Evidence Units should be granular enough that retrieval can select signage behavior without importing architecture, business identity or atmosphere.

## Stage 7 — Temporal and Regional Estimation
Estimate only when the image contains supporting cues.

Temporal output:
- exact_year, year_range, decade, broad_period or UNKNOWN
- confidence
- basis[]

Regional output:
- city, region, country or UNKNOWN
- confidence
- basis[]

A caption may be used as source metadata but must be distinguished from visual evidence.

Do not hallucinate a city because a scene resembles the Canon.

## Stage 8 — Provenance Resolution
Use the provenance ladder defined in `core/PROVENANCE.md`.

Pinterest is normally a discovery/provenance surface, not the original documentary source.

If the original source is not resolved, retain that uncertainty explicitly.

## Stage 9 — Transfer-Risk Review
For each Evidence Unit, assign transfer risk:
- LOW: generic physical/material behavior;
- MEDIUM: form or period pattern that could alter design identity;
- HIGH: semantic, geographic, commercial, human or unique architectural identity.

High-risk evidence is still indexable but retrieval must narrow its permitted learning.

## Stage 10 — Retrieval Metadata
Generate compact search metadata from evidence, not aesthetic vibes.

Good retrieval terms:
- painted masonry storefront sign
- galvanized roll-down gate
- exterior steel fire escape
- mixed brick repair patterns
- wet asphalt reflection behavior

Bad retrieval terms:
- gritty
- cinematic
- cool vintage city
- Fear City look

Aesthetic similarity is not documentary authority.

## Stage 11 — Validation
Reject or quarantine a record when:
- image cannot be inspected;
- all meaningful fields are unsupported;
- duplicate identity is unresolved;
- provenance is contradictory;
- generated metadata contains invented readable text;
- exact location/date is asserted without evidence;
- classification leaks Canon terminology into documentary facts.

## Stage 12 — Index
Only validated items enter retrieval.

Indexable classes:
- DOCUMENTARY_EVIDENCE
- INFLUENCE_REFERENCE when retrieval explicitly permits it
- CANON_CANDIDATE under candidate rules
- CANONICAL through Canon governance

REJECTED items are not returned by normal documentary retrieval.
