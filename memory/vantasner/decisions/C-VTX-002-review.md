---
description: Independent review of C-VTX-002
author: vantasner-review
created: '2026-08-01T15:41:27Z'
updated: '2026-08-01T15:41:27Z'
tags:
- substrate-framework
- claim-review
- abelian-higgs-vortex-numeric
category: decisions
confidence: working
status: archived
---
# Review of C-VTX-002

## Claim Under Review
For `(v,n,lambda,g)=(1,1,2,1)` and explicit truncated-domain Dirichlet data,
there is resolution-bounded numerical evidence for a monotone nontrivial radial
solution with finite positive tension approximately `4.21160`. The verdict is
limited to the declared numerical family and is not an exact existence theorem.

## Sourced Inputs
The review read `v0.22.0`, proposed `C-VTX-001`, P026, the shared BVP evidence
wrapper, package solver and tests, main refinements, independent finite
differences, hash-pinned CF1, and its failed current-environment reproduction.

## Independence
The main method is adaptive collocation through `solve_bvp`. The independent
method discretizes both second-order equations by central finite differences
and solves the sparse nonlinear residual with `least_squares`; it imports
neither package BVP equations nor the collocation profile.

## Verification Status
The strongest earned status is `numeric_evidence`. Solver success, maximum RMS
collocation residual, boundary residual, nonnegative energy, tolerance/domain/
cutoff/guess studies, and an independent discretization all pass. These do not
constitute a continuum existence or uniqueness proof.

## Sensitivity and Counterexamples
Tolerance tightening reduces tension error by more than a factor twenty.
Cutoff errors decrease monotonically; domains 10 through 25 agree within
`1e-5`; exponential and rational guesses reach the same branch. Wrong
asymptotic gauge boundaries fail exact finite energy. The source's v=0 solve is
not a uniqueness proof and is excluded.

## Framework Compatibility
The claim is a qualified compatible extension of `C-VTX-001`. It declares all
parameters, equations, interval, cutoff, boundary data, tolerance, quadrature,
residual metric, and refinements. The tension is dimensionless in the `v=1`
demo convention and supplies no absolute scale or physical confinement map.

## Dependency and Consumer Replay
The direct dependency is `C-VTX-001`. Consumers are the package BVP/tension
APIs/tests, CF1's disposition, and pending CF2/CF5 tension constructions. The
reference collocation tension is `4.2116046`; finite differences at 101, 201,
and 401 points approach it as `4.1921205`, `4.2065776`, and `4.2103691`.

## Competing Candidate Audit
Candidate A was selected over exact-only Candidate B because the independent
discretization and preregistered refinements close the numerical evidence.
Candidate C remains rejected because numerical existence in a declared Abelian
model does not select its physical interpretation.

## Four-Axis Decision
The axes retain the resolution-bounded epistemic ceiling.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: conditional numerical consumer of C-VTX-001

## Promotion Transaction
Promotion adds the solver/tension APIs, numerical tests, separate registry
entry, immutable attempts including source failure, P026 evidence, qualified
CF1 disposition, release, generated records, and parent synchronization.

## Continuation if Not Accepted
Loss of residual or refinement closure would select Candidate B and continue
with another genuinely independent numerical method. It would not weaken the
exact claim.

## Done Gate
The numerical object, diagnostics, refinements, independent method, scope
ceiling, consumers, and debt closure are complete.

## Cross-References
See `C-VTX-001`, P026, CF1, the vortex/numerics modules, and the parent migration
effort.
