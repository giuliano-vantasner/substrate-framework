---
description: Independent review of C-SG-016
author: vantasner-review
created: '2026-08-03T07:41:50Z'
updated: '2026-08-03T07:41:50Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- damping
category: decisions
confidence: working
status: archived
---
# Review of C-SG-016

## Claim Under Review

The claim records the exact undamped-family kinetic average and form factor,
then a conditional phase-averaged slow-damping action law with explicit energy,
frequency, instantaneous-rate, and integrated-e-fold semantics. It includes a
finite-time simulation ceiling and excludes exact damped-family, global
exponential, material-lifetime, coherence, population, and substrate readings.

## Sourced Inputs

The review read release `v0.77.0`, accepted `C-SG-001`, `C-SG-002`,
`C-SG-003`, `C-SG-012`, and `C-PDE-011`, P091's frozen proposal and attempts,
the canonical sine-Gordon and 1D solver modules, hash-pinned LB1, and every
named LB2/LB3/LB4/engineering consumer. Pending MC3 was not imported.

## Independence

The primary route derives the average from canonical action and proves the
closed form symbolically. The independent route integrates the exact field
velocity with SciPy quadrature, solves the reduced action IVP with DOP853, and
finds the energy crossing with Brent's method. The PDE route uses three
leapfrog grids, a second domain, independent DOP853, a slower damping rate, and
a lossless control; it does not reuse LB1's nested mpmath results as an oracle.

## Verification Status

The maximum status is `simulation_evidence` because the claim includes actual
damped-PDE tracking. The family identities and reduced ODE are exact conditional
statements, while closeness of the damped field to that family remains
finite-grid and finite-time. All solvers exit successfully, energy ledgers
refine, and exact and numerical obligations remain explicitly separated.

## Sensitivity and Counterexamples

Factor-two action mutations fail both exact and direct-field checks. The
integrated e-fold check rejects the frozen initial-D time and `1/Gamma` at
finite amplitude. The nonlinear trajectory is more than four times closer to
the PDE energy than frozen D. Mesh halving gives second-order ledger refinement,
domain extension is inert, DOP853 agrees with leapfrog, halving Gamma at equal
slow time halves the adiabatic error, and Gamma zero recovers the lossless
control within numerical resolution.

## Framework Compatibility

The claim is a compatible bulk-damped extension of the accepted normalized 1+1
sine-Gordon conventions. Gamma has normalized inverse-time units and is not a
material parameter. The exact family is used only for period averages and an
adiabatic coordinate; it is not asserted to solve the positive-Gamma PDE.

## Dependency and Consumer Replay

Dependencies are `C-SG-001`, `C-SG-002`, `C-SG-003`, and `C-SG-012`. Governed
consumers are the pure APIs, focused tests, and P091 verifiers. LB2's limiting
use is compatible, LB3's local current-frequency rate is structurally
compatible, and LB4/engineering remain pending or noncanonical. No unresolved
consumer debt is created.

## Competing Candidate Audit

Candidates A-J and structural criteria were frozen before LB1's body, values,
and consumers were opened. Exact family and observable-specific candidates are
selected by dependency closure and semantics, not numerical closeness. Literal
full-amplitude e-fold promotion and physical-medium readings are rejected.

## Four-Axis Decision

The four axes retain the simulation and adiabatic ceilings independently.

- Verification: simulation_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: depends on C-SG-001, C-SG-002, C-SG-003, and C-SG-012; challenges and supersedes none

## Promotion Transaction

Promotion adds `C-SG-016`, pure APIs and tests, immutable P091 evidence,
qualified LB1 disposition, release `v0.78.0`, generated documentation, accepted
claim/release memory, and parent-effort continuation.

## Continuation if Not Accepted

Failure of PDE tracking would retain the exact conditional identities and
return the approximation statement for a repaired method or narrower regime;
it would not revive the frozen-D or material-lifetime headlines.

## Done Gate

The claim, dependency closure, exact and independent derivations, PDE
refinements, mutations, consumer audit, APIs, and campaign debt are closed. The
parent corpus migration remains active with LB2 next.

## Cross-References

See P091, LB1, `C-SG-001`, `C-SG-002`, `C-SG-003`, `C-SG-012`, `C-PDE-011`,
the canonical sine-Gordon modules, and the parent corpus-migration effort.
