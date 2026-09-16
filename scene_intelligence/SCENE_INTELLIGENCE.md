# SVS 1.9 · Scene Intelligence

## Purpose

Scene Intelligence turns a source image from a flat collection of visible objects into an explicit scene model before Streetcraft decides what to preserve, transform, remove, infer or leave unknown.

The pipeline is:

`SOURCE → Entities → Roles → Relationships → Authority → Salience → Action Plan → Reference Gaps → CGC`

Scene Intelligence does not create new visual authority. It makes existing evidence and dependencies explicit.

## Core problem solved

A facade, sign, parked car, graffiti layer, fire escape, street pole and dark occluded region are not equivalent simply because all are visible.

Streetcraft must understand:
- what carries identity;
- what carries structure;
- what is contextual;
- what is transient;
- what merely occludes something else;
- which relationships are more important than the individual objects;
- what can be removed under the selected Mode;
- what must remain unknown.

## Output

The primary output is `Scene Analysis Record v2 (SAR2)` containing:
- scene entities;
- scene roles;
- protected relationships;
- preservation authority;
- salience;
- entity actions;
- unknown locks;
- reference-need hints;
- scene-level warnings.

SAR2 feeds the Compact Generation Contract.

## Non-goals

Scene Intelligence does not:
- identify unknown geography from resemblance;
- invent unreadable text;
- infer hidden geometry without authority;
- convert salience into preservation authority;
- override Mode/Profile/Camera;
- auto-promote references to Canon.
