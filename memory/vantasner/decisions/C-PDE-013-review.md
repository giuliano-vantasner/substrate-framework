---
description: Accepted qualified review of finite-wall spherical Einstein-scalar branch C-PDE-013
author: vantasner-review
created: '2026-08-11T07:12:00Z'
updated: '2026-08-11T07:12:00Z'
tags: [substrate-framework, claim-review, C-PDE-013, numerical-bvp]
category: decisions
confidence: established
status: archived
---
# C-PDE-013 Claim Review

## Claim Under Review

C-PDE-013 is one declared amplitude-three, `alpha=0.03` finite-wall solution
of the C-STG-002 phase-averaged BVP. It fixes origin and wall data, precision,
solver controls, residual norms, refinement axes, and an independent method.

## Sourced Inputs

The review uses C-STG-002, C-PDE-012, P179's frozen numeric revisions and
thresholds, every numeric attempt, the complete matrix, both numerical routes,
tests, and source adjudication. SC2's printed digits do not set pass gates.

## Independence

Adaptive collocation is the primary route. A fresh reviewer rewrites the ODE
and data and solves by DOP853 plus root shooting with wall continuation. The
failed one-shot long-wall initialization remains preserved as attempt 0007.

## Verification Status

The claim earns `numeric_evidence` and remains epistemically qualified. The
finest collocation result has frequency `0.890839827775792`, mass
`0.290960714264522`, central lapse `-0.182426921486489`, off-grid residual
`7.01e-11`, and minimum `f=0.879013430362296`.

## Sensitivity and Counterexamples

All twelve mesh, tolerance, origin, and wall levels pass frozen gates. The
largest state drift is `1.84e-8`. Fresh shooting agrees to much better than
`1e-8`. Zero coupling, wrong central amplitude, and wrong `J1` sign all break
their relevant verdicts.

## Framework Compatibility

The solver never clips a nonpositive metric function and treats the Robin
tail as approximate finite-wall data. Amplitude and coupling are declared
branch coordinates, not selected physical constants. Full-PDE discarded
harmonics remain outside the numeric object.

## Dependency and Consumer Replay

Dependencies close through C-STG-002 and C-PDE-012. Direct consumers are the
new tests and P179 verifier. The source graph passes while TX1 remains pending.
Mutable quadrature uses `numpy.trapezoid`; immutable legacy spellings cause no
scientific failure.

## Competing Candidate Audit

Candidate D was preregistered with all controls. A full oscillaton is a
different pointwise problem, and no Horndeski action exists. D is selected by
residual and refinement closure rather than source-digit agreement.

## Four-Axis Decision

The four axes retain the numerical and finite-wall ceilings.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: additive claim with no challenge or supersession

## Promotion and Scope Ceiling

Release v0.131.0 adds C-PDE-013. It establishes no uniqueness, exact half-line
state, pointwise Einstein-scalar solution, physical scale, observation,
material gravity, or substrate mechanism.

## Cross-References

See P179, SC2, C-STG-002, C-PDE-012, the numerical audit, and
`spherical_einstein_scalar_bvp.py`.
