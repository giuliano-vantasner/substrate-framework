---
description: Independent review of C-MOD-002 conditional hedgehog profile and box spectrum
author: vantasner-review
created: '2026-08-02T20:50:00Z'
updated: '2026-08-02T20:50:00Z'
tags:
- substrate-framework
- claim-review
- radial-spectrum
category: decisions
confidence: established
status: archived
---
# C-MOD-002 Claim Review

## Claim Under Review

C-MOD-002 records resolution-bounded numerical evidence for a nontrivial
stationary branch of C-MOD-001's declared radial model and for the finite-box
continuum ladder of its complete Hessian. It reports the fitted origin slope,
energy coefficient, virial and stationarity refinement, solver residuals,
box-level and node ordering, domain collapse, and zero-threshold
classification. It claims neither continuum existence or uniqueness nor a
positive bound mode, physical Skyrmion, nucleon, Roper, or mass.

## Sourced Inputs

The review reads the same accepted base, P062 contract, hash-pinned PG3 unit,
source reproduction, attempt history, exact C-MOD-001 derivation, primary and
independent raw diagnostics, package module, focused tests, and impact report.
PG3's 0.097 floor is inspected only as source audit evidence after the model,
bound-state criterion, mutations, and structural selection were frozen.

## Independence

The primary route uses DOP853 shooting with an asymptotic Robin tail,
trapezoidal energy, consistent-mass linear FEM, and sparse `eigsh`. The
independent route imports no canonical radial API and instead uses
`solve_bvp` collocation with a fitted origin slope, Simpson energy, a
mass-lumped finite-volume transform, and `eigh_tridiagonal`. Their background
and spectrum solvers, quadratures, mass matrices, and eigen algorithms are
distinct.

## Verification Status

The maximum verdict is `numeric_evidence`. The primary float64 route uses
inner radius 1e-4, walls 12/18/24, 801/1201/1601 samples, DOP853 tolerances
1e-10 and 1e-12 with max step 0.02, root tolerances 1e-12, and eigensolver
tolerance 1e-10. The independent route uses inner radius 1e-3, 500 initial
collocation nodes, tolerance 2e-8, at most 50000 nodes, the same audit grids,
and maximum collocation RMS residual below 2.0e-8. Numeric evidence does not
become an exact continuum existence theorem.

## Sensitivity and Counterexamples

Finite-difference EOM residuals decrease from 3.76e-3 to 9.43e-4 to 2.36e-4
under spacing halving. The virial imbalance decreases from 4.65e-4 to
5.81e-5 across domain growth. The complete-Hessian lowest levels fall from
0.131132 to 0.061072 to 0.034754 as walls grow, while wall-squared products
stabilize and node counts remain 0,1,2,3. Independent levels agree within
0.07 percent. Mixed-term, kinetic-weight, and potential mutations change or
cross the relevant verdicts. A constant-coefficient soluble Dirichlet problem
recovers its analytic levels and node counts.

## Framework Compatibility

The claim depends only on C-MOD-001 and keeps all numerical model data visible.
It uses the massless r^-2 Robin tail rather than fitting a finite-wall zero and
classifies every positive box level against the exact zero continuum edge. Its
`qualified` epistemic ceiling is natural: it supplies useful profile and box
evidence without converting a continuum ladder into a particle.

## Dependency and Consumer Replay

The direct dependency is C-MOD-001. New consumers are the P062 module, focused
tests, verifiers, governance, generated documentation, and future Skyrme-like
profile audits. Existing SciPy evidence helpers and all prior numerical claims
remain unchanged. Targeted numerics and full workflow replay are required and
create no unresolved debt.

## Competing Candidate Audit

Candidate D was registered as conditional on complete action-level closure.
Its stationary-profile part survives through two independent methods, while
its bound-mode part fails the predeclared threshold and domain criteria.
Candidates B and C determine the operator and continuum classification before
any physical comparator is considered.

## Four-Axis Decision

The axes support a qualified numeric claim, not the source's physical
headline.

- Verification: `numeric_evidence`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `qualified`
- Relationship: depends on C-MOD-001 and narrows PG3's numerical content

## Promotion Transaction

Promotion adds C-MOD-002 to release `v0.56.0`, retains its complete numerical
conditions in the registry, archives P062, qualifies PG3 with durable evidence,
regenerates the queue, and synchronizes package tests, docs, and memory. Both
numeric routes, focused consumers, registry closure, one full workflow gate,
graph change detection, and diff checks must pass.

## Continuation if Not Accepted

This clause is inactive because the bounded numeric claim is accepted. A
future resonance or physical excitation claim must add an infinite-domain
scattering or pole oracle, quantization and state dictionary, and physical
scale under separate governance.

## Done Gate

The claim-level debt is empty after replay and synchronization. The absence of
a positive bound state is not presented as completion by itself; the accepted
stationary-profile and corrected continuum object are the positive result.

## Cross-References

See P062, PG3, C-MOD-001, `radial_modes.py`, `test_radial_modes.py`, release
`v0.56.0`, and the parent migration effort.
