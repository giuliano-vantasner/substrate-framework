---
description: Independent review of C-MOM-002
author: vantasner-review
created: '2026-08-01T19:03:00Z'
updated: '2026-08-01T19:03:00Z'
tags:
- substrate-framework
- claim-review
- separable-density
- stf-moments
category: decisions
confidence: working
status: archived
---
# Review of C-MOM-002

## Claim Under Review

The claim states exact moment, STF, derivative-norm, and viewing-projection
algebra for a declared centered axisymmetric separable density. It excludes a
dynamical or conserved 3+1 source and every gravitational interpretation.

## Sourced Inputs

The review read `v0.36.0`, `C-SG-009`, `C-MOM-001`, `C-GW-002`, the canonical
moment and TT modules, P041, and hash-pinned FS2. Pending FS3 and P3D3 remain
candidate consumers, not dependencies.

## Exact Derivation

Fubini factorization with normalized centered longitudinal and transverse
factors produces the diagonal second moment. Direct trace subtraction produces
the normalized tensor, and multiplication by three produces the source's
triple convention. Differentiation then removes the constant transverse term;
direct contraction fixes both norm factors.

## Independence

The independent route integrates separate normalized Gaussian factors over the
full line, derives per-axis and radial variances, reconstructs the STF tensor
without the new helper, and projects it independently. It also differentiates
the exact breather moment on three time grids and observes second-order
convergence.

## Verification Status

Finite exact algebra and the accepted exact breather specialization support
`symbolic_verified`. The source replay and finite differences are corroborating
numeric evidence rather than authority for exactness.

## Sensitivity and Counterexamples

Scales one-half, two, and three fail the per-axis variance predicate. STF scales
one, two, and four fail the triple convention. Arbitrary pure trace is correctly
annihilated by TT projection. A time-varying density can keep its total integral
constant while failing local continuity when paired with zero current, showing
why a density moment alone is not conservation closure.

## Framework Compatibility

The theorem is a compatible extension of `C-MOM-001` and uses only algebraic
projection from `C-GW-002`. Its breather specialization depends on `C-SG-009`.
The transverse input is a nonnegative per-axis variance and radial variance is
twice that value. The coordinate origin and symmetry axis are declared.

## Source Defects and Scope

FS2 reproduces but calls a same-data FFT reference analytic. Its working
variance `0.64` conflicts with an unaccepted later annotation's `3.84`. It
constructs density moments but no complete stress/current system, transverse
dynamics, conserved 3+1 solution, or gravitational theory.

## Dependency and Consumer Replay

Accepted dependencies are `C-SG-009`, `C-MOM-001`, and `C-GW-002`. Direct
consumers are `separable_moments.py`, exact tests, P041, and FS2's disposition.
Sine-Gordon and TT tests replay unchanged. FS3 and P3D3 stay pending.

## Competing Candidate Audit

Candidate A is selected because all derivative and viewing consequences remain
exact conditional algebra. Candidate B is unnecessarily narrow. Candidate C
fails because a declared density factorization is not a 3+1 PDE solution or a
locally conserved stress tensor and no accepted gravity maps it to radiation.

## Four-Axis Decision

The axes apply only to the declared separable-density moment theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-SG-009, C-MOM-001, and C-GW-002

## Promotion Transaction

Promotion adds a pure separable-moment API and tests, freezes P041, qualifies
FS2, adds `v0.37.0`, and synchronizes generated and durable records. It does not
promote a physical 3+1 breather, gravitational source, or radiation channel.

## Done Gate

Normalization, centering, variance, STF factors, derivatives, norms, viewing
geometry, source runtime reuse, physical boundary, consumers, and campaign debt
are closed.

## Cross-References

See P041, FS2, `C-SG-009`, `C-MOM-001`, `C-GW-002`,
`separable_moments.py`, and the parent migration effort.
