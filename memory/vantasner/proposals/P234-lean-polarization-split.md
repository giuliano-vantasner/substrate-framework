---
description: Synthesis of C-GW-013 - axisym/triaxial TT polarization split
author: prime-agent
created: '2026-08-18T21:00:00+02:00'
updated: '2026-08-18T21:55:00+02:00'
tags:
- substrate-framework
- theorem-synthesis
category: proposals
confidence: working
status: archived
---

## Exact Theorem Target
C-GW-013 (core layer): axisym/triaxial TT polarization split. The full statement is the registry entry; the glue is
machine-checked Lean in `Phase16QB_TwoPolarizations.lean` with entrypoint `Phase16QB.axisym_vs_triaxial_split`.

## Accepted Composition Boundary
C-GW-002, C-GW-005 at v0.161.0, quoted only at their exact accepted scopes (the two-dimensional
TT image; the axisymmetric zero-cross projection; the spherical STF null with guard; the
even-harmonic 2*omega moment structure). These atoms are inputs, not objects of renewed
acceptance review.

## Structural Gap
how many of the two accepted TT polarization dimensions a source of each symmetry class excites, and that the cross excitation alone separates and saturates them.

## Assumptions and Exclusions
The declared symmetry/channel classifications are the only added inputs and are recorded in
the claim assumptions; exclusions forbid re-deriving the dependencies and any physical
radiation assertion. Core layer; no interpretive hypothesis.

## Proof Route
target_kind fixed_theorem, one complete Lean route: the ingested capstone file,
kernel-checked at the pinned toolchain with no proof escape and a standard-axiom footprint.
Imports are Mathlib plus the ingested namespace; the mapping to the physics statement is
the census scope record.

## Evidence Ledger
Lean kernel proof only; no numerical or measurement modality is claimed.

| Method | Artifact | Exact scope | Verdict |
| --- | --- | --- | --- |
| lean | formal/SubstrateFramework/Ingested/Phase16QB_TwoPolarizations.lean | the composed discrete dictionary/channel statement | pass |

## Outcome
Accepted into v0.163.0 through campaigns/P234-lean-polarization-split;
individual review at campaigns/P234-lean-polarization-split/reviews/C-GW-013-claim-review.md.
