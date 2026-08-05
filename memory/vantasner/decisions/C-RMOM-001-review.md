---
description: Accepted review of exact conditional rational-map intrinsic moment claim C-RMOM-001
author: vantasner-review
created: '2026-08-11T07:43:00Z'
updated: '2026-08-11T07:43:00Z'
tags: [substrate-framework, claim-review, C-RMOM-001, rational-map, intrinsic-moment]
category: decisions
confidence: established
status: archived
---
# C-RMOM-001 Claim Review

## Claim Under Review

C-RMOM-001 is the exact conditional local-density closure and angular/radial
STF factorization for declared rational maps, including the exact B1 null and
B2 axial form and sign.

## Sourced Inputs

The review uses v0.131.0, C-RMAP-001, C-RPROF-001, C-MOM-001, C-MOM-003,
hash-pinned TX1, every P180 audit, the pure moment API, and focused tests. The
local density is a new explicit premise whose exact average is checked against
the accepted radial functional.

## Independence

The independent route reconstructs the R=z-squared Jacobian from
stereographic coordinates and integrates its first and second powers without
importing the canonical moment module. Direct tensor cubature converges to the
same exact angular tensors.

## Verification Status

The claim earns `symbolic_verified`. Both B2 axial coefficients are exact and
strictly negative, while trace, axial form, factor-three convention, local-to-
radial closure, and the B1 null reduce exactly.

## Sensitivity and Counterexamples

Sphericalization gives an exact null. Removing the J-squared term changes the
tensor, reversing the axial kernel changes the sign verdict, using source Q
notation loses a factor three, and the source monopole-tail mutation differs
from the dimensionally correct term by R squared.

## Framework Compatibility

The theorem preserves accepted sphere, radial-functional, and STF conventions
and adds no fitted constant or physical state. It is a compatible conditional
extension, not a physical action or solution.

## Dependency and Consumer Replay

Dependencies close through C-RMAP-001, C-RPROF-001, and C-MOM-001. The module
is additive. Focused rational-map, moment, and TT consumers pass, while TX2 and
TX3 remain separately pending.

## Competing Candidate Audit

Accepted composition did not include the local density or B2 factorization.
The exact candidate wins by closure, sign, convention, and assumption economy;
source decimals did not select it.

## Four-Axis Decision

The narrow exact object is accepted on all four axes.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive claim with no challenge or supersession

## Promotion and Scope Ceiling

Release v0.132.0 adds C-RMOM-001. It supplies no full 3D field, conserved
physical stress, minimum, physical state, absolute scale, gravity, rotation,
waveform, radiation, observation, or substrate mechanism.

## Cross-References

See P180, TX1, C-RMAP-001, C-RPROF-001, C-RMOM-002, C-MOM-001/003, and
`rational_map_moments.py`.
