# CIL 1.1 RECOVERY

Recovered before R2b continuation.

## Recovered definition
- `/sc-rdr2-elevation`
- resolution: `VP02 + T02 + CG-F`
- Identity Lock
- Occlusion Lock
- strict frontalization
- 16:9
- minimal street
- `/sc-front`
- aliases: `/sc-2f`, `/sc-rdr2-front`, `/sc-elevation`

## Provenance limitation
The project identified historical commit `696afe5`, but that SHA was not available through the connected GitHub repository at recovery time. No exact diff could therefore be imported.

This package reconstructs the explicitly supplied behavior without inventing additional CIL features. If `696afe5` becomes available later, compare it against this recovery before replacing any file.

## Reconstruction decisions
Only one implementation detail was necessary to make the supplied definition operational: `/sc-front` is treated as a camera modifier (`CG-F + STRICT frontalization`) and does not silently switch Profile/Mode or activate the full elevation macro locks. The three stated aliases expand to `/sc-rdr2-elevation`.
