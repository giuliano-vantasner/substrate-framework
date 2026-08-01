---
description: Independent review of C-GAU-001
author: vantasner-review
created: '2026-08-01T16:27:00Z'
updated: '2026-08-01T16:27:00Z'
tags:
- substrate-framework
- claim-review
- local-u1
- gauge-covariance
category: decisions
confidence: working
status: archived
---
# Review of C-GAU-001

## Claim Under Review

Conditional on the accepted complex scalar and a declared local-U1 connection,
the claim gives exact covariant transformation, invariant matter kinetic
algebra, curvature and commutator identities, and a separately conditional
integer-winding flux result without gauge dynamics or physical interpretation.

## Sourced Inputs

The review read `v0.25.0`, `C-U1-001`, P030, both exact routes, package APIs and
tests, hash-pinned EM2, its successful reproduction, and source adjudication.

## Independence

The main route uses the package module and full arbitrary functions. The
independent route uses abstract jets, expands the polar cross term, nests the
two covariant derivatives directly, and solves the winding coefficient without
calling any gauge helper.

## Verification Status

Exact complex differentiation, arbitrary-function simplification, matrix-free
Lorentz-sign expansion, commutators, polynomial solving, and phases support
`symbolic_verified`. No numerical or empirical comparator is involved.

## Sensitivity and Counterexamples

Reversing the derivative, matter-phase, or connection-shift sign independently
breaks covariance. The accepted Noether-current sign reverses EM2's label while
preserving its raw cross term. Pure and non-pure connections distinguish
covariance from zero curvature; arbitrary `F^2` coefficients remain allowed.
Half winding is rejected by the integer domain, and every constant phase—not
only minus one—is momentum independent.

## Framework Compatibility

The claim is a compatible extension of `C-U1-001` in the same current and
signature convention. The connection, positive coupling, local transformation,
and optional winding boundary data are explicit premises. The complex scalar
remains independent of the real sine-Gordon sector.

## Dependency and Consumer Replay

The sole accepted dependency is `C-U1-001`. Direct consumers are
`gauge_u1.py`, package exports/tests, EM2's disposition, and pending EM3, EM6,
and later gauge-sector audits. The vortex flux is an exact convention cross-check,
not a physical model identity. Focused consumers pass and no debt remains.

## Competing Candidate Audit

Candidate A was selected because curvature, the commutator, and conditional
integer flux survive the corrected sign audit as reusable exact content.
Candidate B would discard those valid consequences. Candidate C fails the free
gauge-kinetic-coefficient and missing-sector tests.

## Four-Axis Decision

The axes describe local gauge algebra and its explicit conditional boundary.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new local-U1 extension of C-U1-001

## Promotion Transaction

Promotion adds pure gauge APIs/tests, registry entry, immutable P030, qualified
EM2 disposition, release/generated records, and parent synchronization.

## Continuation if Not Accepted

A sign failure would select Candidate B and retain covariance only. Gauge-field
dynamics, fractional flux, or physical electromagnetism require separate
proposals with additional actions and topology.

## Done Gate

Covariance, signs, curvature, commutator, topology, dynamics boundary,
mutations, consumers, qualification, and debt closure are complete.

## Cross-References

See P030, EM2, `gauge_u1.py`, `C-U1-001`, and the parent migration effort.
