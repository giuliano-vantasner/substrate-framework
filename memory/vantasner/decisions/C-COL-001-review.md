---
description: Independent review of C-COL-001 collective-coordinate pullback and stationary classification
author: vantasner-review
created: '2026-08-05T12:00:00Z'
updated: '2026-08-05T12:00:00Z'
tags:
- substrate-framework
- claim-review
- collective-coordinate
- stationary-stability
category: decisions
confidence: established
status: archived
---
# Review of C-COL-001

## Claim Under Review

C-COL-001 conditionally pulls the C-MED-003 kinetic density onto a declared
one-parameter profile family. It states the induced metric, variable-metric
Euler-Lagrange equation, rest-stationary linearization, curvature-sign
classification, and coordinate-reparameterization law. Its C-RG-001
specialization classifies the capillary maximum's square-root magnitude as an
unstable exponential rate. It explicitly excludes a derived profile, material,
cross-sector coefficient map, stable capillary mode, hbar onset, escape law, or
event.

## Sourced Inputs

The review reads base release `v0.85.0`, C-MED-003, C-RG-001, C-RG-002,
C-VAR-001, C-BRK-001, C-DYN-001, their canonical modules and reviews, P102's
frozen proposal, all append-only attempts, primary and independent verifiers,
focused tests, source and check ledgers, formal encoding audit, consumer map,
and the pinned BD4 source. Legacy rung098 is resolved by hash as leg M2, not the
unrelated phase-7 source unit M2. BD4's unsupported profile, ceiling-retirement,
stable-frequency, and onset subclaims remain outside the claim delta.

## Independence

The independent route imports no canonical collective-coordinate API. It
freshly differentiates a symbolic field composition, derives the reduced
Euler-Lagrange equation, solves the characteristic equations, differentiates
the capillary energy, constructs linear and nonlinear coordinate changes,
integrates finite, zero, and divergent profiles, and rebuilds the dimension and
identifiability matrices. The source's expected check conditions and terminal
tally are not its oracle.

## Verification Status

The maximum status is `symbolic_verified`. All promoted equations are exact
SymPy expressions with evaluated concrete integrals where used. The primary
route passes forty-six checks and the independent route seventeen. Seventy-one
focused package and dependency tests pass. The source's fourteen checks and
the compiling Lean file are separately classified and do not raise the claim
status beyond their exact encodings. No numerical tolerance, fit, simulation,
or unevaluated integral is used as proof of the headline.

## Sensitivity and Counterexamples

Mutations change the geometric-integral exponent, omit or double the metric
connection term, remove the potential force, flip the curvature sign, or use a
single rather than squared coordinate Jacobian; each load-bearing verdict
fails. A coordinate-independent profile has zero inertia, while a linear-in-x
profile diverges on the whole line. A nonlinear coordinate map exposes the
nonstationary gradient term. Common action scaling cancels from the stationary
ratio, while inertia-only scaling changes it. Barrier plus local-rate
observations retain the constructive parameter orbit `(T,P,M)->(rho*T,
rho^2*P,rho^2*M)`.

## Framework Compatibility

The claim is a native compatible extension. It imports C-MED-003's declared
field kinetic density without selecting its common coefficient scale and
C-RG-001's capillary curvature without altering its strict-maximum invariant.
It requires an explicit profile family, spatial domain, regularity, finite
positive metric, reduced potential, and locally invertible coordinate map.
Separate continuum and capillary sectors are coupled only conditionally; no
unrelated accepted invariant is revised.

## Dependency and Consumer Replay

Direct governed consumers are the new pure module, additive package exports,
focused tests, P102 verifiers, governance, generated documentation, and memory.
The pinned Lean file compiles. The engineering adapter and pending BD5 execute
with sixteen and thirteen checks, but BD4 appears only in their prose; BD5's
actual model is overdamped and contains no radius inertia. Later legacy rungs
execute with eleven and four checks and independently recover the saddle sign.
GitNexus reports LOW additive risk and no pre-existing affected execution flow.
No NumPy quadrature compatibility path is involved.

## Competing Candidate Audit

Candidates A through I and ordered structural criteria froze before renewed
source inspection. Literal reproduction is retained only as evidence.
Dimensions-only closure is retained as a ceiling because zero and divergent
profiles defeat existence. The genuine pullback, variable-metric equation,
sign classification, coordinate covariance, profile counterexamples,
normalization orbit, and consumer ceiling are selected by exact framework fit,
not the source tally or a comparator value.

## Four-Axis Decision

The conditional theorem earns acceptance without challenging or superseding an
accepted claim.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-MED-003 and C-RG-001; challenges and supersedes none

## Promotion Transaction

Promotion adds C-COL-001, the importable collective-coordinate module and
tests, immutable P102 evidence, qualified BD4 disposition, release `v0.86.0`,
generated documentation, and accepted-state memory. The source queue is
regenerated from the editable disposition record. The proposal becomes an
adjudicated campaign and the parent migration advances to BD5.

## Continuation if Not Accepted

This clause is inactive after the integrated promotion gate. A physical
capillary-radius mode or onset would require a separate proposal deriving the
profile, cross-sector action, coefficient normalization, stable or stochastic
dynamics, state map, and observable without importing the desired result.

## Done Gate

The exact conditional object, dependencies, independent route, mutations,
counterprofiles, formal audit, consumer classification, importable APIs/tests,
and synchronized promotion surfaces close with empty claim-level debt. The
parent corpus migration remains active because BD5 and later units are pending.

## Cross-References

See P102, BD4, BD5, legacy rung098 leg M2, C-MED-003, C-RG-001, C-RG-002,
C-VAR-001, C-BRK-001, the collective-coordinate module, release `v0.86.0`, and
the framework-migration effort.
