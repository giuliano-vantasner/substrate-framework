---
description: Independent review of C-GW-002
author: vantasner-review
created: '2026-08-01T18:12:13Z'
updated: '2026-08-01T18:12:13Z'
tags:
- substrate-framework
- claim-review
- tt-projector
- polarization-basis
category: decisions
confidence: working
status: archived
---
# Review of C-GW-002

## Claim Under Review

The claim states the exact rank-two image and normalized complete real basis of
the three-dimensional TT projector, together with its piecewise transverse-
frame construction, double-angle rotation, and circular weight-two algebra.
Physical gravitational and helicity interpretations are excluded.

## Sourced Inputs

The review read `v0.33.0`, `C-GW-001`, P038, both exact routes, package APIs and
tests, and hash-pinned GW3 with its successful reproduction. G6's graviton
count and the G1/GW2 radiation connection were inventoried as unaccepted
physical relationships rather than claim dependencies.

## Independence

The main route uses the shared TT operator, its orthonormal six-tensor matrix,
an arbitrary rational direction, normalized frames, and basis reconstruction.
The independent route solves all axis-direction linear constraints directly,
constructs its own tensors from rotated vectors, and does not import the new
polarization APIs.

## Verification Status

Exact matrix rank/spectrum, basis contractions, reconstruction, axis coverage,
rotation identities, and constraint solving support `symbolic_verified`. The
claim is finite linear algebra; it contains no simulation or evidence for a
physical propagating field.

## Sensitivity and Counterexamples

Unit, half, and doubled basis scales fail the normalized completeness predicate;
only magnitude `1/sqrt(2)` works. Rotation weights one, three, and minus two
fail the direct vector construction. Retaining the in-plane trace raises the
transverse symmetric image from two to three. A cross-sign flip correctly
preserves the span and is classified as convention, not failure.

## Framework Compatibility

The claim is a compatible extension of `C-GW-001` and does not duplicate its
sphere integral. The frame is deterministic and covers nonzero directions
piecewise; no impossible globally continuous tangent frame is claimed. Every
plus/cross and circular label is basis-conventional without an accepted field
action or orientation observable.

## Dependency and Consumer Replay

The only accepted dependency is `C-GW-001`. Direct consumers are the expanded
`tt_angular.py`, exports/tests, P038, GW3's disposition, and later waveform
audits. C-GW-001's prior tests replay unchanged, and focused closure has no
debt.

## Competing Candidate Audit

Candidate A is selected because rank, normalization, completeness, frame
coverage, and rotation all close. Candidate B is unnecessarily weak. Candidate
C fails because a spatial projector image alone supplies no time evolution,
gauge constraint analysis, physical observable, or quantum state.

## Four-Axis Decision

The axes apply only to the finite TT image and basis theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-GW-001

## Promotion Transaction

Promotion expands pure TT APIs, adds exact tests, freezes P038, qualifies GW3,
adds `v0.34.0`, and synchronizes generated records and the parent effort. It
does not promote GW3's physical graviton, helicity, or radiation terminology.

## Continuation if Not Accepted

If completeness or axis coverage had failed, Candidate B would retain only the
constraint nullity. Physical mode counting still requires a separate governed
action, equations, constraints, gauge quotient, boundary data, and observable
construction.

## Done Gate

Novelty, rank, basis normalization, completeness, frame coverage, rotation,
mutations, source inconsistencies, physical boundary, consumers, and campaign
debt are closed.

## Cross-References

See P038, GW3, `C-GW-001`, `tt_angular.py`, and the parent migration effort.
