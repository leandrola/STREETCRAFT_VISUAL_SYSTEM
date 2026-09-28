# Backdrop Reinterpretation Presets · BD01 / BD02

**Preset promotion: PASS — Inferred Validation (`PASS_INFERRED`).** Command
expansion and CGC contracts are implemented and tested. The ten-case visual
promotion matrix is accepted by inference at the user’s direction; no ten new
independently inspected outputs are claimed. Physical print validation remains
**PENDING**. See the [promotion record](../validation/BD_VISUAL_VALIDATION_BENCHMARK.md). These are compound presets on **VP02**, not new
visual profiles, Transformation Modes, camera grammars or a Build Kit mode.

## Purpose and invocation

Photo-driven panoramic urban architectural backgrounds should read clearly behind
scale-model scenes, especially 1:64. The presets make that output target explicit:
wide lateral continuity, a frontal/elevational reading, compressed spatial
structure, architectural primacy, subordinate foreground and low narrative density.

| Preset | Intent | Priority | Source fidelity |
| --- | --- | --- | --- |
| BD01 · Urban Backdrop Reinterpretation | A backdrop based on this photo; improve a messy composition within the available transformation scope. | Scenic usability | Medium structural fidelity in unprotected areas; high fidelity to urban character. |
| BD02 · Urban Backdrop Preserve | This recognizable photo translated into a Streetcraft backdrop. | Structural fidelity | High fidelity to composition, structure, massing and layout. |

Short compound invocations:

```text
/sc-bd01
/sc-bd02
```

Equivalent explicit invocations:

```text
/sc-vp02 /sc-t02 /sc-cg-f /sc-rdr2-elevation /sc-bd01
/sc-vp02 /sc-t08 /sc-cg-f /sc-rdr2-elevation /sc-preserve /sc-bd02
```

Both select VP02, CG-F, strict frontalization, 16:9, minimal street presence,
strict source identity and locked unknowns. BD01 selects T02; BD02 selects T08
and strict observed-evidence preservation. T02 retains its existing canonical
name **FRONTALIZATION**; T08 retains **BACKDROP EXTRACTION**. Neither is redefined
as a new general transformation mode.

The explicit profile/mode/camera selectors above are supported. Elevation aliases
also work. Command ordering cannot downgrade the selected backdrop bundle:
BD02 retains T08 even if `/sc-rdr2-elevation` comes later. Mixing BD01/BD02,
conflicting profiles, oblique/automatic camera overrides or incompatible modes
returns a command error. Existing profile-conflict rules remain in effect.
`/sc-bd01 /sc-preserve` further restricts BD01 to cleanup without major recomposition.

## Shared visual contract

- **Framing:** horizontal, wide and panoramic, with lateral continuity. Default
  16:9; 2:1 and other horizontal ratios can be supplied explicitly.
- **Geometry:** frontal or near-frontal architectural reading, stable horizon,
  upright verticals and minimal dramatic convergence. No bird's-eye conversion,
  strong oblique perspective, corner streetscape or hero-shot framing.
- **Primary subjects:** architecture, urban massing, skyline layers, rooftops,
  painted walls, building rhythm and structural silhouettes.
- **Secondary detail:** water towers, rooftop equipment, signage, restrained
  street information, industrial traces and distant towers.
- **Narrative:** people, vehicles and action must not become the main subject.
  Background-first composition; no excessive clutter or dramatic street event.
- **Foreground:** subordinate. A neutral street edge, sidewalk/curb strip,
  rooftop/vacant-lot edge, quiet open space or infrastructure band is acceptable.
- **Print readability:** legible large masses, controlled complexity, consistent
  tonal hierarchy and clarity at model-viewing distance.

Shared internal locks are Panoramic Framing, Backdrop Continuity, Architectural
Priority, Narrative Reduction, Foreground Suppression and Print Readability.
These are backdrop contract fields, not new VSG Graph Lock types.

## BD01 scope and compatibility decision

BD01 treats the source as a starting point. It may reorganize unprotected masses,
complete plausible continuity, simplify/merge forms, replace weak unprotected
sections, adjust spacing and reinterpret unprotected skyline areas. Its emphasis
is plausible recomposition, skyline completion and continuity optimization.
It must retain the source's urban character, not produce a generic unrelated scene.

**Conservative resolution of the proposed spec's lock conflict:** the inherited
CG-F/elevation policy does not authorize overriding P0, identity anchors, PR0/PR1
relationships, semantic text locks or locked unknowns. This implementation limits
BD01's recomposition allowance to unprotected regions. Plausible continuation
cannot fill a locked unknown as if it were observed evidence. Existing source
locks take precedence over all preset allowances. If the entire layout is
protected, the available recomposition scope may be empty.

This is narrower than an unrestricted interpretation of “free reinterpretation”.
Redesigning protected source geometry would require an explicit separate policy
change. T02/elevation behavior outside BD01 is unchanged.

## BD02 scope

BD02 treats the reference as a layout contract. It allows minor interference
cleanup, geometry stabilization, silhouette clarification, authorized clutter
simplification, evidence-supported clarification of small ambiguities and a
consistent backdrop presentation. It adds Reference Layout, Structural Fidelity
and Recognition Preservation locks.

It forbids relocation of major masses, free skyline redesign, key-building
substitution, erasure of dominant layout relationships and genericization.
Clutter suppression never silently authorizes removal of a protected element.
The current T08 description mentions reconstructed occlusions; this preset's
explicit unknown locks keep that reconstruction evidence-dependent.

## Request options and CGC integration

Optional request fields, used only with a backdrop command:

```json
{
  "command_text": "/sc-bd02",
  "backdrop": {
    "aspect_ratio": "2:1",
    "target_scale": "1:64"
  }
}
```

The request still requires its normal `scene` input. The default nominal scale is
1:64. Ratios must be positive integer `width:height` strings with width greater
than height; they are normalized. Portrait/square ratios, malformed scales and
unknown options are rejected. No unsupported “unlock” option is accepted.

`backdrop_presets.build_backdrop_contract` produces a deterministic contract in
`cgc_draft.backdrop_contract`, retained in `cgc_final.backdrop_contract`, with:

- preset intent, shared visual requirements and allowed/forbidden operations;
- effective source-node, PR0/PR1 and unknown locks linked by existing IDs;
- effective aspect ratio, nominal scale and a canonical SHA-256;
- `visual_validation=PENDING` and print readiness requiring output review.

Preset prohibitions also enter the CGC's `forbid` list. The CGC remains the active
contract; existing hardening/preflight still decides `generation_ready`. There
is no new rendering adapter. Requests without BD01/BD02 have no backdrop contract
and retain their prior behavior. VSG-2A recognizes the optional contract as an
explicit policy passthrough; its shadow output remains non-governing.

A nominal scale is not a computed physical print size. Dimensions, resolution,
DPI, tiling, bleed and color workflow are not inferred from these presets.

## Suitable references and non-goals

Good candidates include skyline panoramas, frontal low-angle massing, layered
rooftops, vacant-lot-to-skyline views, continuous street walls and lateral city
fragments. Poor candidates include close character scenes, diagonal streets,
corner action scenes, interiors, single-building portraits and references whose
main value depends on human activity.

These presets do not define a new aesthetic movement, a general urban illustration
mode, a narrative scene mode, facade-only flattening, texture extraction, pixel
analysis, automatic regeneration or Build Kit integration.

## Validation

```sh
python command_invocation/test_backdrop_presets.py
python benchmark/run_regression_suite.py
```

The tests verify shorthand/full invocations, all invocation order permutations,
conflicts, contract propagation/schema/digests, source locks, options, opt-out
behavior, preflight blocks and VSG shadow compatibility. Full regression also
checks the existing VSG and stable R2b evidence. Results are recorded in
[BACKDROP_PRESETS_QA.json](../validation/BACKDROP_PRESETS_QA.json).

The preset promotion is inferred; acceptance of individual generated images still
requires visual review. Each CGC output keeps `visual_validation=PENDING` until
actual output evidence exists. Review criteria:

| Gate | Shared | BD01 | BD02 |
| --- | --- | --- | --- |
| Visual success | Reads as a usable wide backdrop; stable elevation; architecture first; low clutter; print-friendly hierarchy. | Source character remains recognizable; composition benefits from permitted reinterpretation. | Layout and skyline remain recognizable; no major redesign. |
| Typical failure | Narrative dominance, excessive foreground, oblique drift, overpopulation or poor distance legibility. | Genericization, incoherent skyline or unauthorized protected-geometry changes. | Building substitution, changed mass hierarchy, lost recognition or style overriding preservation. |

No generated backdrop or printed sample is validated by the unit tests.
