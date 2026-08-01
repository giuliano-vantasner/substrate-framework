---
description: Independent review of C-MOM-003
author: vantasner-review
created: '2026-08-01T20:21:47Z'
updated: '2026-08-01T20:21:47Z'
tags:
- substrate-framework
- claim-review
- spherical-moments
category: decisions
confidence: working
status: archived
---
# Review of C-MOM-003

## Claim Under Review

The claim states that every integrable radial density has Cartesian second
moment `I=(J/3)*identity`, where `J=integral rho*r^2 d^3x`, and therefore zero
normalized and triple STF moments. It is an exact angular theorem, not a
statement about dynamics or radiation.

## Sourced Inputs

The review read `v0.39.0`, `C-MOM-001`, P045, the canonical moment API and
tests, the passing exact verifier, direct angular quadrature, and hash-pinned
P3D2. The radial sine-Gordon simulation is unnecessary for this claim. P3D2's
gravity and forced-channel prose remains outside the delta.

## Independence

The primary route integrates all Cartesian unit-vector products symbolically.
The review also reduces the axisymmetric integrals to independent polynomial
moments in `mu=cos(theta)` and evaluates the tensor with 24-point
Gauss-Legendre and 48-point azimuthal quadrature without using the moment API.

## Verification Status

The strongest earned status is `symbolic_verified`. The free scalar `J`
remains symbolic, no radial profile or sampled value is inserted, and exact
matrix subtraction proves both STF conventions. Numerical angular quadrature
is regression evidence only.

## Sensitivity and Counterexamples

Mutating the isotropic coefficient away from one third fails the simultaneous
tensor and trace requirements even though trace-free projection alone would
still annihilate any multiple of identity. A nonzero `P2` amplitude gives
`I_STF=diag(-aJ/15,-aJ/15,2aJ/15)` and returns continuously to zero at `a=0`.
This separates spherical symmetry from a tautological zero construction.

## Framework Compatibility

The claim is a native specialization of the accepted `C-MOM-001` conventions.
It introduces no coupling, scale, field equation, sign condition, or gravity
premise. Integrability of the radial second moment is the only analytic domain
condition.

## Dependency and Consumer Replay

The direct dependency is `C-MOM-001` for normalized and triple STF
conventions. The package moment API and tests are direct consumers. P3D2 maps
to this claim; P3D3 and P3D4 are pending prospective consumers and gain no
dynamical or gravitational authority from the exact null.

## Competing Candidate Audit

Candidate A is selected for the exact theorem because both exact and
independent angular routes close and the P2 mutation is nonzero. Candidate B
would unnecessarily discard this profile-independent result. Candidate C is
rejected because moment kinematics alone does not define a radiation theory.

## Four-Axis Decision

The axes apply only to the exact angular statement.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: specializes C-MOM-001 to integrable radial densities

## Promotion Transaction

Promotion adds the importable radial/P2 moment API, exact tests, immutable
campaign evidence, qualified P3D2 mapping, registry entry, release, generated
documentation, and accepted memory.

## Continuation if Not Accepted

Failure of exact angular closure would require correcting the tensor or
convention before any P3D2 numeric work could proceed; a numerical near-zero
would not replace it.

## Done Gate

Angular integration, trace normalization, both STF conventions, deformation
sensitivity, scope, dependencies, consumers, and debt are closed.

## Cross-References

See P045, P3D2, `C-MOM-001`, the conserved-moments module, and the parent
migration effort.
