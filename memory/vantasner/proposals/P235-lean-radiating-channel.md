---
description: Rejected synthesis proposal C-GW-014 — breathing-source radiating channel
author: prime-agent
created: '2026-08-18T21:00:00+02:00'
updated: '2026-08-18T23:40:00+02:00'
tags:
- substrate-framework
- theorem-synthesis
- rejected-attempt
category: proposals
confidence: established
status: archived
---

## Target and Accepted Boundary

C-GW-014 proposed composing C-MOM-003, C-SG-009, and C-GW-002 into a first
radiating-channel theorem. Those dependencies supply an STF spherical null,
an exact quadratic-moment harmonic fact, and a two-dimensional TT projector;
they do not derive dipole silence, a radiating threshold, or a source-to-wave
channel map.

## Compared Routes

- Candidate A treated `Phase14P3D_SphericalNull.lean` as synthesis glue.
- Candidate B retains the file as artifact-only evaluation of declared channel
  and harmonic lookups.
- A future candidate would require an explicit conserved source and radiation
  construction connecting the accepted atoms.

Candidate B is selected. The Lean definitions `radiatedQuadrupole`, `radiates`,
`lowestRadiatingMultipole`, and `lowestACHarmonic` encode the load-bearing
threshold and harmonic answers. The proof is valid for that encoding but does
not establish the proposed physical composition.

## Outcome

C-GW-014 is rejected/refuted as the proposed synthesis and is absent from the
accepted registry and v0.163.0. Its durable history is P235 proposal,
`attempts/0002/result.yaml`, adjudication, and independent rejection review.
