---
description: Independent review of C-QBL-003
author: vantasner-review
created: '2026-08-01T17:01:00Z'
updated: '2026-08-01T17:01:00Z'
tags:
- substrate-framework
- claim-review
- quartic-qball
- fluctuation-spectrum
category: decisions
confidence: working
status: archived
---
# Review of C-QBL-003

## Claim Under Review

Conditional on `C-QBL-001` and its declared quartic energy, the claim gives the
exact scalar Hessian, complete two-level bound spectrum, mode functions and
roles, and continuum threshold without a stability or particle-family map.

## Sourced Inputs

The review read `v0.28.0`, `C-QBL-001`, P033, both exact routes, package
APIs/tests, hash-pinned FG2, its successful reproduction, and the source
check-family adjudication. `C-QBL-002` was inspected for the rejected
exact-sine consumer but is not a dependency of the accepted quartic claim.

## Independence

The main route derives the functional Hessian and combines exact eigenpair
checks with terminating partner factorization and numerical regression. The
independent route constructs the factorization, bound seeds, norms, parity,
translation tangent, and threshold without importing the new module or FG2's
analytic spectrum statement.

## Verification Status

Exact functional differentiation, hyperbolic identities, L2 integrals,
intertwining relations, and factorization support `symbolic_verified`.
Finite-difference results are regression evidence. The source's exact-sine
third level fails its boundary oracle and earns no accepted numeric claim.

## Sensitivity and Counterexamples

Changing the constant shift or depth breaks the exact pair. Mesh and box
refinement converge to both exact quartic eigenvalues. Shallow and flat wells
reduce the count. The source exact-sine background falls toward zero then
returns to `0.29` at its wall, exposing its near-threshold third level as
unresolved.

## Framework Compatibility

The claim is a compatible conditional extension of `C-QBL-001`. Its energy
functional, dimensionless 1+1 domain, positive kappa, scalar perturbation
space, and L2 whole-line boundary are explicit. It does not import EM1,
Standard-Model sectors, or an exact-sine spectral result.

## Dependency and Consumer Replay

The sole accepted dependency is `C-QBL-001`. Direct consumers are
`qball_fluctuations.py`, exports/tests, FG2's disposition, and future
charge-constrained stability proposals. The rejected generation and mass maps
are not framework consumers. Focused replay passes with no debt.

## Competing Candidate Audit

Candidate A was selected because factorization proves completeness and the
threshold, so Candidate B is unnecessarily weak. Candidate C fails the
negative/zero mode-role audit and lacks every physical state and quantum-number
mapping premise.

## Four-Axis Decision

The axes describe the conditional scalar Hessian only.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: fluctuation-spectrum extension of C-QBL-001

## Promotion Transaction

Promotion adds pure spectral APIs, guarded finite-difference regression/tests,
immutable P033, qualified FG2 disposition, `v0.29.0`, generated records, and
parent synchronization.

## Continuation if Not Accepted

If factorization had not closed, Candidate B would retain exhibited
eigenpairs. Stability requires the full coupled complex perturbation problem
at fixed charge. A particle-family proposal requires an independently derived
state space, positive mass map, and quantum numbers.

## Done Gate

Functional, operator, domain, exact spectrum, completeness, threshold, parity,
translation, negative-mode role, refinement, source boundary, interpretation,
consumers, disposition, and debt closure are complete.

## Cross-References

See P033, FG2, `qball_fluctuations.py`, `C-QBL-001`, and the parent migration
effort.
