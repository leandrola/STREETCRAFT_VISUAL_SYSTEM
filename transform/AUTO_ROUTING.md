# Auto-Routing

## Purpose
Auto-Routing determines the default Streetcraft Mode/Profile/Camera path from source identity before aesthetic interpretation.

Routing is conservative. It may choose a safer path automatically, but it may not silently erase source identity.

## Routing precedence
1. Explicit source identity
2. Explicit user Mode/Profile instruction
3. Fear City source detection
4. Transformation intent
5. Default profile selection
6. Camera family selection

A direct user instruction to override Fear City routing must be explicit. Merely naming an RDR profile while supplying a Fear City source is not enough to erase Fear City authorship.

## AR-01 Fear City explicit route
If the user explicitly identifies the source/task as Fear City:

MODE = T06 FEAR CITY INTERPRETATION
PROFILE = VP03 FEAR CITY
CAMERA = CG-FC

No additional profile inference is required.

## AR-02 Fear City detected route
If the input is recognized with high confidence as a photograph of the authored Fear City physical model/world:

MODE = T06
PROFILE = VP03
CAMERA = CG-FC

Detection may use:
- known Fear City multi-view identity;
- repeated authored facade/layout relationships;
- model construction cues consistent with the known project;
- explicit Fear City signage/world evidence;
- project context linking the source to Fear City.

The route is based on source identity, not on visual resemblance to New York or other real cities.

## AR-03 Ambiguous model route
If an image appears to be a miniature/diorama but Fear City identity is uncertain:

- Do not auto-promote to VP03.
- Preserve the user-selected Mode/Profile when present.
- Otherwise default to VP00 with source-preserving camera behavior.
- Flag FEAR_CITY_IDENTITY = UNRESOLVED.
- Never import Fear City geography, signage or authorship by resemblance.

## AR-04 Real-world / historical photo route
For real-world or historical urban photography with no Fear City authorship:

- Use explicit user Mode/Profile when supplied.
- If no profile is specified, default PROFILE = VP00.
- Camera defaults:
  - T01 → CG-S unless the source already conforms naturally to CG-A/CG-B.
  - Transformative/reconstructive work → choose CG-A or CG-B according to architectural geometry.

## AR-05 RDR profile routing
When the user explicitly selects VP01 or VP02 on non-Fear-City material:

- retain selected profile;
- select CG-A by default;
- select CG-B when corner/side-depth geometry materially contributes;
- select CG-S when source preservation is the higher-order requirement.

## AR-06 Explicit Fear City override
To apply VP00/VP01/VP02 to a confirmed Fear City source, the instruction must explicitly authorize overriding normal Fear City routing.

Even then:
- source authorship remains protected;
- no geographic substitution is allowed;
- no RDR camera rule may redesign Fear City geometry;
- T06 preservation constraints remain active unless the user also explicitly changes Mode.

## Routing matrix

| Source identity | Explicit profile? | Default Mode | Default Profile | Camera |
|---|---|---|---|---|
| Fear City confirmed | none | T06 | VP03 | CG-FC |
| Fear City confirmed | VP00/01/02 but no explicit override | T06 | VP03 | CG-FC |
| Fear City confirmed | explicit routing override | T06 unless Mode also overridden | requested profile with Fear City preservation | CG-FC or source-safe equivalent |
| Miniature/diorama, Fear City uncertain | yes | requested/compatible | requested | CG-S / profile-safe |
| Miniature/diorama, Fear City uncertain | none | T01 | VP00 | CG-S |
| Historical/real photo | yes | requested/derived | requested | CG-S, CG-A or CG-B |
| Historical/real photo | none | T01 | VP00 | CG-S |
| Generated/reference image | yes | requested/derived | requested | profile-dependent |

## Non-goals
Auto-Routing does not:
- classify Canon;
- infer geography from visual similarity;
- create historical facts;
- change source authority;
- authorize object removal;
- authorize new architecture;
- replace explicit transformation budgets.
