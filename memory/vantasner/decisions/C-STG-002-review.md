---
description: Accepted review of exact phase-averaged spherical Einstein-sine-Gordon claim C-STG-002
author: vantasner-review
created: '2026-08-11T07:12:00Z'
updated: '2026-08-11T07:12:00Z'
tags: [substrate-framework, claim-review, C-STG-002, einstein-scalar]
category: decisions
confidence: established
status: archived
---
# C-STG-002 Claim Review

## Claim Under Review

C-STG-002 is the exact, dimensionally explicit, phase-averaged
single-harmonic canonical Einstein-sine-Gordon reduction in static spherical
areal gauge. It includes the stress, mass and lapse constraints, projected
scalar equation, conservation factorization, origin laws, and explicit
discarded harmonics.

## Sourced Inputs

The review uses v0.130.0, C-STG-001, C-PDE-005, C-PDE-009, hash-pinned SC2,
all P179 attempts and audits, the pure exact API and tests, and the primary,
independent, and source-graph verifiers. No source decimal or physical scale
is an exact premise.

## Independence

The independent route imports neither P179 module. It reconstructs the
Christoffels, Einstein tensor, canonical averaged stress, scalar projection,
conservation factor, Bessel defects, and direct phase average from fresh
expressions.

## Verification Status

The claim earns `symbolic_verified`. The primary exact gates and fresh review
reduce every displayed residual to exact zero where claimed. Wrong `J1` sign
and radial divergence fail, while flat and vacuum limits pass. The nonzero
`2J3(a)` scalar defect and density second harmonic prevent a pointwise
full-PDE interpretation.

## Sensitivity and Counterexamples

The first discarded scalar coefficient is `a^3/24+O(a^5)`. A zero scalar is
vacuum, and zero coupling with flat metric recovers the accepted radial
projection. These exact limits and mutations are load bearing rather than
checks of copied output.

## Framework Compatibility

The action, signature, stress sign, dimensions, and conservation convention
are native to C-STG-001. C-PDE-005 and C-PDE-009 supply compatible projection
and averaging ceilings. No Horndeski, Gordon, physical-scale, or substrate
premise is added.

## Dependency and Consumer Replay

Dependencies close through C-STG-001, C-PDE-005, and C-PDE-009. The API is
additive and LOW risk, with no prior upstream caller or affected indexed
process. The 29-check graph replay keeps TX1 pending and creates no blanket
authority.

## Competing Candidate Audit

Seven candidates were frozen. Exact composition alone omitted the new
spherical object, while a full oscillaton and nonminimal Horndeski theory are
distinct larger proposals. Candidate C wins structurally, not numerically.

## Four-Axis Decision

The narrow exact object is accepted on all four axes.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive claim with no challenge or supersession

## Promotion and Scope Ceiling

Release v0.131.0 adds C-STG-002. It does not establish solution existence,
uniqueness, a full oscillaton, exact half-line breather, physical gravity,
observation, material dynamics, or a substrate mechanism.

## Cross-References

See P179, SC2, C-STG-001, C-PDE-005, C-PDE-009, C-PDE-013, and
`spherical_einstein_scalar.py`.
