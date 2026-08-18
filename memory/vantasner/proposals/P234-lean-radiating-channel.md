---
description: Synthesis of C-GW-014 - breathing-source radiating channel
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
C-GW-014 (core layer): breathing-source radiating channel. The full statement is the registry entry; the glue is
machine-checked Lean in `Phase14P3D_SphericalNull.lean` with entrypoint `Phase14P3D.selfconsistent_channel_ties_GWL_FSL`.

## Accepted Composition Boundary
C-MOM-003, C-SG-009, C-GW-002 at v0.161.0, quoted only at their exact accepted scopes (the two-dimensional
TT image; the axisymmetric zero-cross projection; the spherical STF null with guard; the
even-harmonic 2*omega moment structure). These atoms are inputs, not objects of renewed
acceptance review.

## Structural Gap
the channel tie: spherical null plus silent monopole/dipole plus 2*omega doubled moment plus two-dimensional TT image as one radiating-channel statement.

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
| lean | formal/SubstrateFramework/Ingested/Phase14P3D_SphericalNull.lean | the composed discrete dictionary/channel statement | pass |

## Outcome
Accepted into v0.162.0 through campaigns/P234-lean-radiating-channel;
individual review at campaigns/P234-lean-radiating-channel/reviews/C-GW-014-claim-review.md.
