---
description: Audit GW1's conserved multipole identities and radiation claim
author: vantasner
created: '2026-08-01T17:37:02Z'
updated: '2026-08-01T17:44:29Z'
tags:
- substrate-framework
- campaign-proposal
- conserved-stress
- multipole-moments
- migration-GW1
category: proposals
confidence: exploratory
status: archived
---
# P036 GW1 Conserved Stress-Moment Audit

## Question and Positive Deliverable

P036 must derive the exact moment ladder of a localized symmetric tensor obeying
`partial_mu T^{mu nu}=0` in flat `3+1` spacetime and decide whether those
identities establish a gravitational radiation channel. The positive
deliverable is a reusable boundary-explicit theorem through the second mass
moment; merely rejecting GW1's radiation language would not complete the
campaign.

## Base Release and Provenance

The accepted base is `v0.31.0` at framework commit `9b42159`. Its forty-four
claims contain no accepted `3+1` gravitational field equation, TT projector,
wave-zone solution, radiation power, or source-to-metric map. The pending
hash-pinned candidate is GW1 at
`merged-framework/bridges/phase-12/bridge_GW1_multipole_lowest_quadrupole.py`,
SHA-256 `3aba56675f887f98c015de7caad1834893ffdbc27ca1daf3c7056694953102fc`.
Bundled-memory search found no accepted framework moment or quadrupole theorem.

## Invariants, Conventions, and Allowed Imports

The campaign may declare a smooth symmetric tensor on inertial flat `3+1`
coordinates and import exact integration by parts. Spatial integrals require
localization or explicit vanishing surface terms. With signature-independent
contravariant conservation written as `partial_t T^{0 nu}+partial_j T^{j nu}=0`,
total energy and momentum are conserved. The energy dipole is generally affine,
not constant. No integrated identity is itself a gravitational wave equation.

## Candidate Preregistration

The alternatives are frozen from queue metadata before the full GW1 executable
body or any source comparator is inspected.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Exact energy, momentum, dipole, second-moment, and trace-free identities with boundary terms | Smooth localized symmetric conserved tensor | Tensor components and spatial dimension three | Native conditional mathematics | Two integrations by parts, translation check, flux and symmetry counterexamples |
| B | Energy/momentum conservation and affine dipole only | Conservation plus boundary control | Same tensor | Selected if second moment needs undeclared structure | Independent moment derivation and index audit |
| C | Lowest physical gravitational radiating multipole | Linearized gravity, retarded solution, gauge/TT map, wave zone | Coupling and field equations | Dependency conflict | Accepted-claim closure and nonradiating quadrupole counterexamples |

## Selection Criteria and Blinding

Selection is ordered by local-to-global derivation, explicit surface terms,
stress symmetry, sign/index consistency, exact derivative hierarchy,
translation and inertial-motion limits, sensitivity to flux/symmetry mutations,
and accepted dependency closure. No imported radiation formula or observed
gravitational comparator may select a candidate.

## Proposed Claim Delta

Provisional `C-MOM-001` would state conserved total energy and momentum, affine
energy dipole, and the exact second-moment relation
`d^2 I_ij/dt^2=2 integral T^{ij} d^3x`, plus its trace-free version, under
declared boundary and symmetry assumptions. It will explicitly exclude a
metric perturbation, retarded Green function, TT projection, radiative
multipole ordering, nonzero quadrupole radiation, waveform, power law,
gravitational coupling, or substrate interpretation.

## Implementation and Oracle Plan

Pure APIs will encode moment definitions, surface-term bookkeeping, and exact
derivative identities without simulating a field. SymPy will verify index-level
integration-by-parts reductions and analytic localized examples. Mutations will
change a divergence sign, retain a nonzero surface flux, drop `T^{0i}=T^{i0}`,
and substitute a uniformly translating source whose dipole is not constant.
An independent weak-form or explicit Gaussian route will rederive the
load-bearing factors and trace subtraction.

## Attempts and Continuation

Attempt `0001` will reproduce GW1 and inventory its conservation assumptions,
moments, derivative orders, origin/frame choices, boundary conditions,
quadrupole definition, and imported radiation statements. A missing second-
moment premise selects Candidate B only if a clean conditional repair cannot be
implemented. Missing gravity rejects Candidate C and does not reduce the
positive conserved-stress theorem.

## Debt Ledger

This ledger tracks boundary closure, tensor symmetry, derivative factors,
frame dependence, and radiation scope.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Local conservation may be integrated without a surface audit | Display every boundary term and state localization/vanishing-flux conditions | discharged: the claim states ordinary and coordinate-weighted surface conditions and a finite-flux counterexample changes M |
| The dipole may be incorrectly called constant | Derive `dot D_i=P_i` and `ddot D_i=0`, then test a moving source | discharged: the translating Gaussian and inertial particles have affine nonconstant dipoles |
| The second-moment factor may be asserted or convention-mixed | Independently derive `ddot I_ij=2 integral T^{ij}` and its trace-free form | discharged: main and independent routes recover factor two and both STF normalizations |
| Energy flux may be silently identified with momentum density | Require tensor symmetry and supply a nonsymmetric counterexample | discharged: an exactly conserved nonsymmetric packet yields distinct D-dot and P |
| Lower-moment suppression may be called proof of quadrupole radiation | Audit field equations, Green functions, gauge projection, and nonzero radiation evidence | discharged: all are absent or imported and explicitly excluded from C-MOM-001 |

## Review and Promotion Plan

The provisional claim receives an independent weak-form and normalization
review. Promotion requires pure APIs/tests, immutable attempt evidence,
claim-level adjudication, terminal GW1 disposition, release/docs/memory
synchronization, targeted replay, and one unchanged full repository gate.

## Done Gate

P036 closes only when boundary terms, symmetry, all moment derivatives,
normalization, frame limits, mutations, radiation boundary, source disposition,
consumers, and debt satisfy the framework contract.

## Adjudication Result

Candidate A is accepted as `C-MOM-001`. Thirty main and nine independent
checks close conservation, boundary, symmetry, factor, STF, and translation
obligations. GW1 is qualified because its explicit sloshing current and stress
are locally inconsistent for arbitrary `g(t)`, its binary is externally held,
and no gravitational field or radiation oracle is executed. All campaign debt
is discharged.
