# SVS 1.6 Fear City Vision

Fear City is the authored physical model/world. T06 must make Fear City perceptually real without making it less Fear City.

## Evidence layers
FC-W WORLD EVIDENCE — what exists in the represented world.
FC-M MODEL EVIDENCE — how that world is physically constructed.
FC-C CAPTURE EVIDENCE — how the model was photographed.

An element may belong to more than one layer.

## Authored World Authority
AWA3 DEFINING
AWA2 STRONG
AWA1 SUPPORTING
AWA0 NON-WORLD
AWA-U AUTHORSHIP UNKNOWN

When uncertain between authorial choice and construction/capture error, preserve.

## Authorial Persistence
AP3 persistent
AP2 usually persistent
AP1 variable
AP0 capture-only

## Multi-View Consistency Evidence
Consistent evidence across views increases confidence in geometry and relationships, but never invents information absent from all views.

## Scale Translation Intelligence
Classify scale cues as SCALE_CUE_WORLD / SCALE_CUE_MODEL / SCALE_CUE_CAPTURE / AMBIGUOUS.
Scale-Breaking Artifacts may include visible thickness, glue, paper fiber, base edges, workshop background, macro depth-of-field and model-specific reflections.

Goal: increase World Scale Cues relative to unintended Model Scale Cues while preserving Authored Information.

## Material World Translation
PHYSICAL APPEARANCE → REPRESENTATIONAL INTENT → WORLD MATERIAL → WORLD BEHAVIOR

Material Identity (MI) is preserved. Material Behavior (MB) may be translated.

Material Translation Levels:
MT0 NONE
MT1 BEHAVIORAL
MT2 REPRESENTATIONAL
MT3 RECONSTRUCTIVE
MT4 GENERATIVE

Fear City normally uses MT1–MT2. MT3 requires evidence. MT4 is normally forbidden.

Surface Memory Anchors (SMA) preserve authored weathering, graffiti, paint loss, repairs, grime and their location/intensity hierarchy.

World Interaction Coherence (WIC) improves contact shadows, occlusion, weight, reflection and material continuity before added detail.

## Unsupported World Extension
Do not convert a limited model background or ambiguous void into a detailed metropolitan continuation unless the task authorizes extension and evidence/budget support it.

World-depth translation may improve atmospheric depth and scale credibility, but may not silently add buildings, streets, fire escapes, signs, landmarks or infrastructure.

## Geographic discipline
Fear City may visually resemble New York or other North American cities, but that resemblance does not authorize importing real-world place names, landmarks, signage systems or geographic identity absent from authored evidence.

## Decay and atmosphere discipline
Translate the existing intensity of wear. Do not amplify a used street into abandonment, turn dry pavement wet for cinematic effect, or increase grime merely to sell realism.

## T06 Domain Budgets default
GEOMETRY TB0
AUTHORSHIP TB0
RELATIONSHIPS TB0
MATERIAL BEHAVIOR TB2
LIGHT TB2
SCALE CUES TB2
CAPTURE ARTIFACTS TB2
ATMOSPHERE TB1–TB2
NEW CONTENT TB0–TB1

## T06 hard constraints
Preserve P0 geometry, PR0 relationships, AWA3 decisions, major signage, graffiti composition, street topology, material identity and surface-memory anchors.
Translate material behavior, scale cues, lighting behavior, contact shadows, atmospheric depth and model-specific reflections.
Suppress only confirmed capture artifacts and unintended scale breakers.
Forbid architectural redesign, geographic substitution, new landmarks, generic Americana, period cosplay, decay amplification, prop spam and unsupported world extension.

## World Depth Budget
WDB0 SOURCE-BOUNDED — preserve only visible/established depth.
WDB1 MINIMAL CONTINUITY — replace capture/model termination with the least specific plausible continuation.
WDB2 EVIDENCE-SUPPORTED EXTENSION — extend only when multi-view or explicit source evidence supports it.
WDB3 INTERPRETIVE EXTENSION — requires explicit user authorization and a higher transformation budget.

Default T06 uses WDB0–WDB1.

SC-63 Evidence Boundary Controls World Depth — do not create deep streets, skylines or infrastructure beyond the evidence boundary under conservative T06 budgets.
SC-64 Atmosphere Cannot Hide Invention — haze, darkness, wetness, bloom or depth-of-field may not be used to disguise unsupported additions.
SC-65 Geographic Resemblance Is Not Geographic Identity — resemblance to a known city never licenses imported place names, landmarks, street systems or civic graphics.
SC-66 Background Continuity Must Be Minimal — when a model/capture background must be replaced, continue only what is needed for perceptual coherence.

## Adapter lexical guardrails for T06
Unless supported by source/task, avoid instructions such as: gritty, cinematic, dramatic, Brooklyn, NYC, wet pavement, neon-soaked, hyper-decayed, dystopian, noir, abandoned. These terms have high semantic leakage and can cause production-design drift.

## Validation-derived hard failures
UNSUPPORTED_WORLD_EXTENSION — invented background depth, buildings, streets or infrastructure exceed evidence/budget.
GEOGRAPHIC_IDENTITY_IMPORT — real-world place identity is imported without authored evidence.
ATMOSPHERIC_INFLATION — mood, wetness, haze, darkness or color intensity exceeds source/task authority.
MATERIAL_INTENSITY_DRIFT — aging, grime, rust or damage is amplified beyond authored/source intensity.
