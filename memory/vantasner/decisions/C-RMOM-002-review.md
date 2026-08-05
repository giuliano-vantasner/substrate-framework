---
description: Accepted qualified review of corrected degree-two intrinsic moment claim C-RMOM-002
author: vantasner-review
created: '2026-08-11T07:43:00Z'
updated: '2026-08-11T07:43:00Z'
tags: [substrate-framework, claim-review, C-RMOM-002, numerical-evidence]
category: decisions
confidence: established
status: archived
---
# C-RMOM-002 Claim Review

## Claim Under Review

C-RMOM-002 is resolution-bounded evidence for the intrinsic STF moment of one
corrected conditional degree-two stationary rational-map branch.

## Sourced Inputs

The numeric object uses C-RMOM-001, C-RPROF-002, `(B,I)=(2,pi+8/3)`, the
frozen binary64 solver contract, and no physical scale or source-decimal
input.

## Independence

The canonical DOP853 vacuum-complement shooting and shared trapezoidal route
is compared with a fresh solve_bvp collocation, two-power initial profile, and
Simpson integration. Angular tensor cubature is also independent of the
canonical exact API.

## Verification Status

The claim earns `numeric_evidence`. The normalized ratio is
`-0.338851662271835`; the accepted triple-Q ratio is
`-1.016554986815505`. The independent ratio differs by `2.865e-7` relative.

## Sensitivity and Counterexamples

Outer, inner, sample, tolerance, and step axes converge separately. Solver,
endpoint, finite-data, monotonicity, trace, normalization, endpoint, and
density-term mutations are sensitive. The source's coupled wall/mesh route
and wrong tail do not set a gate.

## Framework Compatibility

The value is conditional on accepted corrected branch evidence and has
declared radial-coordinate-squared units. No physical state or length is
inferred.

## Dependency and Consumer Replay

Dependencies close through C-RMOM-001 and C-RPROF-002. Fifty-four focused
tests and the source graph pass without granting authority to TX2 or TX3.

## Competing Candidate Audit

The corrected two-method branch wins over literal source reuse because it
separates every refinement axis and fixes conventions and endpoint formulas.
Comparator closeness did not select it.

## Four-Axis Decision

The narrow numeric object is accepted with qualified epistemic status.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: additive claim with no challenge or supersession

## Promotion and Scope Ceiling

Release v0.132.0 adds C-RMOM-002. It proves no existence, uniqueness, minimum,
full 3D solution, physical mass or scale, conserved stress, rotation,
stability, gravity, waveform, radiation, observation, or substrate mechanism.

## Cross-References

See P180, TX1, C-RMOM-001, C-RPROF-002, and `rational_map_moments.py`.
