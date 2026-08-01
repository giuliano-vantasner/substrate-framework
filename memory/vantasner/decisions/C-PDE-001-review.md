---
description: Independent review of C-PDE-001
author: vantasner-review
created: '2026-08-01T19:57:49Z'
updated: '2026-08-01T19:57:49Z'
tags:
- substrate-framework
- claim-review
- radial-sine-gordon
- simulation-evidence
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-001

## Claim Under Review

The claim records finite-time simulation evidence for one declared
dimensionless 3+1 radial sine-Gordon initial-value problem. It states the
action, equation, origin and outer conditions, initial data, domain, time
interval, discretization, energy and localization metrics, conservative
frequency interval, and numerical error controls. It is not an exact existence,
periodicity, lifetime, stability-basin, gravitational, particle, or substrate
claim.

## Sourced Inputs

The review read `v0.38.0`, the normalized sine-Gordon convention in
`C-SG-001`, P044's preregistered candidates and criteria, canonical radial and
numerics modules, tests, the passing attempt, the transformed-field review, and
hash-pinned P3D1. P3D1's cited C1/E1/E2 and P3D2/P3D3/P3D4 consumers were not
admitted as dependencies. Its exponential, gravitational, and ontology
subclaims remain outside the delta.

## Independence

The primary route evolves `u` directly with a centered radial leapfrog and
trapezoidal shell energy. The independent review instead evolves `v=r*u` with
adaptive DOP853, reconstructs the regular center from neighboring radii, and
uses Simpson quadrature. It does not import the canonical radial Laplacian or
energy function. The exact transformed equation and the regular linear
spherical mode provide separate analytic checks on the singular-origin
treatment.

## Verification Status

The strongest earned status is `simulation_evidence`. Exact SymPy checks cover
the action variation, energy continuity, linear mass threshold, and transformed
identity, but localization and sub-gap oscillation are properties of a
finite-grid trajectory. Solver completion, finite values, mesh/timestep/domain
studies, conservation convergence, two frequency estimators, a soluble limit,
and an independent method support that trajectory without converting it into a
continuum existence theorem.

## Sensitivity and Counterexamples

The three-grid center differences and closed-energy variations decrease at
second order. Halving the timestep and moving the sponge/domain preserve the
load-bearing metrics. Frequency estimates are repeated on two settled windows
and by crossings as well as FFT. Changing the radial geometric coefficient
breaks exact and discrete identities; a dispersive seed loses its core and
approaches the continuum edge; an invalid Courant factor is rejected. The
source's exact-periodic and exponential-law readings fail because its measured
leak is nonzero and two seeds cannot determine an exponential family law.

## Framework Compatibility

The claim is a compatible 3+1 extension of the normalized sine-Gordon
potential convention. It adds no dimensional constant or fitted comparator.
All coordinates, field values, energy, and frequencies are dimensionless. The
finite outer boundary and sponge are numerical devices whose sensitivity is
explicitly checked; no result is mixed with the exact 1+1 breather family.

## Dependency and Consumer Replay

The only accepted dependency is `C-SG-001`, used for its normalized potential
and mass convention rather than its exact 1+1 solution. Direct framework
consumers are the radial solver API, numerics compatibility integration, and
their tests. No accepted claim depends on the new object. Pending P3D2-P3D4
are identified prospective consumers and must import the canonical solver
rather than duplicate P3D1's integrator when adjudicated. The pre-promotion
targeted replay covers radial, numerics, and vortex quadrature tests.

## Competing Candidate Audit

Candidate A is selected because the direct IVP produces a localization object
that passes every preregistered refinement and independent-method criterion.
Candidate B's Fourier/BVP quasi-breather is unnecessary for this finite-time
claim and would require a separate radiative-tail contract. Candidate C is
rejected structurally because an enveloped exact 1+1 solution does not satisfy
the radial equation.

## Four-Axis Decision

The four axes retain the finite-resolution ceiling independently.

- Verification: simulation_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: depends on C-SG-001 only for the normalized model convention

## Promotion Transaction

Promotion adds the pure radial solver and diagnostics, shared NumPy trapezoid
compatibility helper, targeted tests, immutable P044 evidence, accepted claim,
qualified P3D1 mapping, release manifest, generated documentation, and accepted
memory. The source reproduction and both verifier tallies remain hash-linked.

## Continuation if Not Accepted

Failure of the finite-time IVP evidence would activate Candidate B with an
explicit tail and collocation contract. It would not justify weakening the
metrics or importing P3D1's exponential narrative.

## Done Gate

The positive trajectory, equation, boundaries, solver status, localization,
frequency, conservation, refinements, independent route, mutations, scope,
consumers, and claim debt are closed.

## Cross-References

See P044, P3D1, `C-SG-001`, the radial and numerics modules, the transformed-
field review, and the parent migration effort.
