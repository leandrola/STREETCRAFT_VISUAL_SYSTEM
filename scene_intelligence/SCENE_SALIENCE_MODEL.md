# Scene Salience Model (SSM) 1.0

Salience controls analytical attention. It does not create authority.

## Axes

Each entity may receive 0–1 values for:
- `identity_salience`
- `structural_dependency`
- `task_relevance`
- `relationship_centrality`
- `temporal_relevance`

Weighted attention score:

- identity: 30%
- structural dependency: 25%
- task relevance: 20%
- relationship centrality: 15%
- temporal relevance: 10%

## Bands

- `CRITICAL_ATTENTION` >= 0.75
- `MAJOR_ATTENTION` >= 0.50
- `SUPPORT_ATTENTION` >= 0.25
- `MINOR_ATTENTION` < 0.25

## Rule

A high salience score cannot upgrade P2 to P0.

A PR0 or P0 constraint can override a low salience score.
