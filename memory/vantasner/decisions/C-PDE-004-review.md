---
description: Independent review of C-PDE-004
author: vantasner-review
created: '2026-08-01T20:50:36Z'
updated: '2026-08-01T20:50:36Z'
tags:
- substrate-framework
- claim-review
- sine-gordon-l2
- simulation-evidence
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-004

## Claim Under Review

The claim records a finite-time regular l=2 perturbation IVP about the declared
radial sine-Gordon initial-data branch and its nonzero first-order triple-STF
energy moment. It fixes the seed, domain, time interval, discretization,
moment convention, convergence bounds, and strict linearized scope.

## Sourced Inputs

The review read `v0.40.0`, `C-PDE-001`, `C-PDE-003`, `C-MOM-003`, P046's
proposal and four attempts, canonical implementation/tests, the 31-check
primary verifier, the 12-check transformed DOP853 review, and hash-pinned
P3D3. The source's nonregular finite deformation and 2D run are not substituted
for the corrected evidence.

## Independence

The primary route uses direct radial `P` with velocity-Verlet and evolves
`v=r*psi` on three meshes. The independent route evolves both transformed
variables with adaptive DOP853 and reconstructs fields only afterward. An
exact free spherical-Bessel box mode supplies a separate soluble limit. The
first-order STF normalization is rederived by exact angular integration.

## Verification Status

The strongest earned status is `simulation_evidence`. The perturbation equation
and moment normalization are exact, but the nonzero trace and finite-time mode
trajectory are numerical. Clean solver exits, finite values, three-mesh
self-convergence, timestep/domain/amplitude studies, boundary causality,
energy convergence, a soluble limit, and DOP853 support the specified IVP.

## Sensitivity and Counterexamples

Background, mode, and Q-trace errors decrease approximately by four under mesh
halving. Closed-box energy error does likewise. Timestep halving changes the Q
trace by less than 0.001 relative RMS, and a domain extension outside the
causal region changes the compared mode by zero at machine precision. Halving
the seed halves mode and Q exactly; zero seed preserves exact zeros. Wrong
barrier coefficients fail the solid-harmonic and independent symbolic guards.

## Framework Compatibility

The claim is a native linearized consumer of the accepted radial model and
moment convention. The perturbation amplitude and width are declared initial
data, not fitted parameters. All quantities remain dimensionless. The claim
does not infer nonlinear stability, a periodic eigenmode, frequency doubling,
gravity, radiation, scale, or ontology.

## Dependency and Consumer Replay

Dependencies are `C-PDE-001`, `C-PDE-003`, and `C-MOM-003`. Direct consumers
are the l-mode evolution/moment APIs, their tests, and P046. P3D4, QB2, QB3,
and BX1 are prospective consumers and must retain this claim's linearized and
finite-time ceiling. P044 and P045 are replayed because the new module imports
their canonical radial and moment conventions.

## Competing Candidate Audit

Candidate A is selected because every preregistered numerical gate closes and
an independent method agrees. Candidate B remains the proper fallback for an
exact-only promotion but is unnecessary. Candidate C is structurally rejected
by `C-PDE-003`, irrespective of its nonzero assembled moment.

## Four-Axis Decision

The four axes retain the finite-grid and linearized ceiling.

- Verification: simulation_evidence
- Review: accepted
- Compatibility: native
- Epistemic: qualified
- Relationship: depends on C-PDE-001, C-PDE-003, and C-MOM-003

## Promotion Transaction

Promotion adds the importable regular-mode solver and moment diagnostic,
targeted tests, immutable failed and passing attempts, independent review,
qualified P3D3 disposition, registry entry, release, generated records, and
consumer replay.

## Continuation if Not Accepted

If refinement or DOP853 comparison failed, Candidate B would retain only the
exact equation and the numerical branch would stay attempt evidence. The
source's nonregular 2D result would not rescue it.

## Done Gate

The positive finite-time mode, equation, regularity, moment, solver status,
refinements, independent route, mutations, dependencies, consumers, and scope
are closed with no numeric-claim debt.

## Cross-References

See P046, P3D3, `C-PDE-001`, `C-PDE-003`, `C-MOM-003`, the l-mode module, and
the parent migration effort.
