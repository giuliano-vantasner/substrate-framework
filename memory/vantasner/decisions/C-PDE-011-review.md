---
description: Independent review of C-PDE-011
author: vantasner-review
created: '2026-08-04T06:25:00Z'
updated: '2026-08-04T06:25:00Z'
tags:
- substrate-framework
- claim-review
- driven-sine-gordon
- simulation-evidence
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-011

## Claim Under Review

The claim records finite-time simulation evidence for one completely specified
dimensionless bulk-forced 1+1 sine-Gordon initial-boundary-value problem. It
states the source, proxy normalization, damping, initial and boundary data,
domain, final and analysis times, spatial and temporal refinements, exact-family
classifier errors, source-work balance, independent method, and mutation
ceiling. It is not a robust formation window, selectivity theorem, physical
deposition model, population, probability, absolute-scale, or eternal-breather
claim.

## Sourced Inputs

The review read release `v0.76.0`, accepted `C-SG-001`, `C-SG-002`,
`C-SG-012`, and `C-SG-015`, P089's frozen contract, all append-only attempts,
the canonical 1D and numerical modules, the primary and adaptive verifiers,
hash-pinned SA3, its five source predicates, and every named consumer. SA3.3,
the source's FFT interpretation in SA3.4, the second-frequency single-breather
reading in SA3.5, and every voltage/plasma/population statement remain outside
the delta.

## Independence

The primary route uses the canonical centered leapfrog, a constrained nonlinear
exact-family fit, and three spatial grids. The independent route uses adaptive
DOP853, a separately coded rising-zero-crossing frequency estimator, refined
diagnostic quadrature, and timestep approach to the adaptive result. A further
half-grid DOP853 run independently checks spatial-method agreement. The source's
raw FFT values, core-only classifier, and local sponge update are not reused as
oracles.

## Verification Status

The maximum earned status is `simulation_evidence`. SymPy verifies the exact
forced energy identity and exact Gaussian norm, while unit tests validate
planted exact solutions and convergence limits. Formation and late-state
classification remain properties of finite-grid trajectories. Clean solver
exit, spatial and timestep convergence, domain and sponge changes, controlled
energy ledger, full phase-space snapshots, an independent integrator, and
load-bearing mutations support the stated bounded object without proving a
continuum existence or asymptotic stability theorem.

## Sensitivity and Counterexamples

Three leapfrog grids contract fitted-frequency differences by about four and
core-energy differences by more than four. Source-work residuals converge to
about `3.0e-5` relative. DOP853, zero crossings, timestep halving, and a
half-grid adaptive run agree. The classifier accepts a planted exact breather
and rejects amplitude rescaling, standing radiation, and a single kink. The
proxy-target mutations 380 and 420 fail while 400 passes. The slow control has
more than 64 total energy, maximum field above `7*pi`, and eight transitions,
directly falsifying the alleged vacuum guard.

## Framework Compatibility

The claim is a compatible driven extension of the accepted normalized 1+1
sine-Gordon convention. The external source and damping profile are declared
dimensionless model data rather than derived medium physics. Exact C-SG-001
amplitude, width, velocity, and energy relations constrain the classifier; no
independent fit amplitude or source-to-voltage conversion is admitted. The
Dirichlet walls and sponge are finite-domain numerical data whose sensitivity
is explicit.

## Dependency and Consumer Replay

Dependencies are `C-SG-001`, `C-SG-002`, and `C-SG-012`. Direct governed
consumers are the new pure bulk-source solver/classifier APIs, their unit tests,
and P089's campaign verifier. SA4, engineering, LB3, and MC4 are noncanonical or
pending and do not import the formation result. Generated claim/release docs,
accepted memory, and the source queue are replayed. No unresolved consumer debt
is created.

## Competing Candidate Audit

Candidates A-J and structural criteria were frozen before source values were
opened. The exact-parameter trajectory is selected because its equation,
energy ledger, classifier, refinements, independent method, and reusable role
close. The broad fast-versus-slow candidate is rejected structurally because
proxy equality is not work equality and the slow output is not vacuum. The
exact energy theorem is not separately promoted because C-SG-012 already owns
the underlying stress-energy identity.

## Four-Axis Decision

The four axes retain the numerical and source-specific ceiling independently.

- Verification: simulation_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: depends on C-SG-001, C-SG-002, and C-SG-012; challenges and supersedes none

## Promotion Transaction

Promotion adds `C-PDE-011`, pure package APIs and tests, immutable P089 evidence,
qualified SA3 disposition, release `v0.77.0`, generated documentation, accepted
claim/release memory, and parent-effort continuation. The expensive adaptive
half-grid evidence is preserved with exact reproduction parameters rather than
rerun as validation ceremony.

## Continuation if Not Accepted

Failure of the narrow numerical object would return Candidate D for a repaired
method or source representation. It would not revive the rejected physical
selectivity story or justify widening the classifier tolerances.

## Done Gate

The exact source trajectory, dependency closure, energy ledger, classifier,
refinements, independent route, mutations, source subclaim verdicts, package
consumers, and campaign debt are closed. The parent corpus migration remains
active with SA4 next.

## Cross-References

See P089, SA3, `C-SG-001`, `C-SG-002`, `C-SG-012`, `C-SG-015`, `C-PDE-001`,
the canonical 1D solver, the adaptive review, and the parent migration effort.
