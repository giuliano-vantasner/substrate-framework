---
description: Independent review of C-QBL-001
author: vantasner-review
created: '2026-08-01T16:37:00Z'
updated: '2026-08-01T16:37:00Z'
tags:
- substrate-framework
- claim-review
- quartic-qball
- charge-curve
category: decisions
confidence: working
status: archived
---
# Review of C-QBL-001

## Claim Under Review

Conditional on the declared quartic stationary ODE and `C-U1-001`, the claim
gives the exact positive translated sech solution, forces both parameters
within the nonzero sech ansatz, and derives its exact charge curve and slope
branches without assigning a stability verdict.

## Sourced Inputs

The review read `v0.26.0`, `C-U1-001`, P031, both exact routes, package APIs and
tests, hash-pinned EM6, its successful reproduction, and the check-family
adjudication. `C-GAU-001` was checked as context but is not a dependency.

## Independence

The main route substitutes the canonical profile and separately collects sech
powers. The review route starts from the localized first integral, fixes the
nonzero turning point, reconstructs the homoclinic profile, and integrates the
current without importing any quartic-Q-ball package helper.

## Verification Status

Exact differentiation, polynomial coefficient solving, hyperbolic identities,
limits, integration, and sign evaluation support `symbolic_verified`. EM6's
quadrature and same-data IVP are regression evidence only. No spectral or
nonlinear stability oracle was executed.

## Sensitivity and Counterexamples

Changing the width to EM1's width, halving the amplitude, or changing the
quartic coefficient breaks the residual. A Gaussian fails exactly. Both charge
endpoints vanish, the unique maximum is 24 at frequency one-half, and samples
on each side catch a reversed slope classification.

## Framework Compatibility

The claim is a compatible conditional extension of `C-U1-001` in its
stationary-phase current convention. The dimensionless 1+1 ODE, quartic
coefficient, profile ansatz, and frequency domain remain explicit. It creates
no ontology map to the accepted real sine-Gordon breather or a gauge sector.

## Dependency and Consumer Replay

The sole accepted dependency is `C-U1-001`. Direct consumers are
`quartic_qball.py`, exports/tests, EM6's disposition, and pending FG1. The EM1
width countercheck prevents accidental profile identity. Focused consumers
pass and the campaign creates no debt.

## Competing Candidate Audit

Candidate A was selected because exact profile and charge obligations close
while stability does not. Candidate B would unnecessarily discard the exact
accepted-current integral. Candidate C fails because no fluctuation operator
or VK hypotheses are encoded and the cited dimensional premise mismatches the
declared model.

## Four-Axis Decision

The axes describe the conditional exact family only.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new conditional extension of C-U1-001

## Promotion Transaction

Promotion adds pure profile APIs/tests, registry entry, immutable P031,
qualified EM6 disposition, reproducible disposition-source repair,
release/generated records, and parent synchronization.

## Continuation if Not Accepted

A charge convention failure would select Candidate B. Stability can be
revisited only in a separate proposal that supplies a precise action,
linearized operator, theorem hypotheses, and an appropriate independent
oracle; it cannot be inferred from this promotion.

## Done Gate

Profile, coefficient forcing, charge, domains, slope branches, mutations,
stability boundary, ontology scope, consumers, source qualification, and debt
closure are complete.

## Cross-References

See P031, EM6, `quartic_qball.py`, `C-U1-001`, and the parent migration effort.
