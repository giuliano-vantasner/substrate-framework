---
description: Audit G1's radiating 1+1 dilaton-source and Larmor-analogue claim
author: vantasner
created: '2026-08-09T12:50:00Z'
updated: '2026-08-09T14:25:00Z'
tags:
- substrate-framework
- campaign-proposal
- scalar-radiation
- retarded-wave
- migration-G1
category: proposals
confidence: exploratory
status: archived
---
# P141 G1 Radiating Dilaton Audit

## Question and Positive Deliverable

P141 must reproduce and adjudicate G1's claim that an accelerating breather
sources a time-dependent 1+1 dilaton field with an outgoing Larmor-like power.
The positive deliverable is an importable, action-normalized retarded-wave
theorem that derives the field equation, distributional jump, outgoing
solution, Noether energy, flux, source work, and total power from explicit
kinetic, source, and signal-speed inputs. If the physical dilaton or
accelerating-breather route does not close, P141 must still construct the
strongest distinct conditional scalar-radiation object rather than treating a
no-go as success.

## Base Release and Provenance

The accepted base is v0.107.0 at scientific commit `078fa1c`; the parent S4
checkpoint is `bdd4328`. G1 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-5/bridge_G1_radiating_dilaton_source.py`, and
SHA-256
`580783a214736b24e6f36a4c035b2c608f931f4ba8ece202ff7f6d260d46f876`.
Its dossier is separately pinned at
`merged-framework/bridges/phase-5/dossiers/G1-dossier.md`, SHA-256
`55d1ecc6c1a19c7018befbdef520c3f925b996bc6fae4ccd0dcb31f40388916b`.

The generated queue exposes ten literal checks, one assertion, symbolic and
numeric oracle hints, and dependencies G2, G3, and T2A. G2 and G3 remain
pending and grant no authority. T2A is qualified only through C-SG-001,
C-SG-002, C-SG-008, and C-SG-012; its review explicitly withholds a dilaton
action, time-dependent solution, and radiation claim. Queue and prior consumer
records expose the headline, tally, dependencies, and immutable legacy-NumPy
compatibility path. They do not license G1's exact formulas or physical
interpretation. Twenty-seven reverse source consumers are known before freeze;
their chronology supplies impact scope, not authority.

The predecessor worktree remains dirty with excluded Phase 47/48, engineering,
synthesis, and memory artifacts. The pinned G1 and dossier hashes match the
committed source baseline; those unrelated changes remain excluded.

## Invariants, Conventions, and Allowed Imports

The accepted framework keeps constant-velocity kinematics, on-shell stress
conservation, static optical geometry, a declared scalar wave action, and a
physical gravitational dictionary separate. C-SG-008 cannot be made
accelerating by replacing `v` with `v(t)`. C-SG-012 supplies local conservation
only on shell and requires boundary-flux conditions for integrated charges.
C-OG-001 through C-OG-003 are static conditional identities and contain no
retarded energy or flux normalization.

P141 may use exact distributions, the d'Alembert Green function, Noether's
energy balance, and a separately declared linear 1+1 scalar action. That
action must retain independent positive kinetic coefficient and signal speed,
a visible source coupling, one signature, and retarded boundary data. A
field-equation coefficient does not by itself determine field energy. Pending
G2, G3, and later consumers grant no premise. Primary literature may be read
after freeze only to check convention and scope.

## Candidate Preregistration

Six candidates cover literal replay, exact point and smooth retarded sources,
the accelerated-breather residual, source work, and governance closure.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Reproduce and type every G1 predicate | Hash-pinned source only | Source literals | Some narrow algebra may survive but cannot create missing action data | AST and equation/data-flow audit |
| B | Exact retarded point-source theorem | Declared linear scalar action and retarded data | Kinetic coefficient, source coupling, speed, source history | Power retains the ratio of squared source coupling to kinetic normalization | Distributional jump plus Noether-flux equality |
| C | Smooth compact-source far-field theorem | Candidate B action and compact source | Source profile and moments | Directed far fields depend on retarded integrals, not a named multipole slogan | Exact characteristic solution and moment limits |
| D | Accelerated-breather residual audit | Accepted breather with declared time-dependent collective coordinate | Trajectory and frequency | Generic acceleration produces a nonzero sine-Gordon residual and source work | Direct symbolic residual and constant-velocity limit |
| E | Field-plus-source work and reaction ledger | Candidate B action plus explicit source dynamics | Source work and regularization data | Energy balance closes, but a local self-force needs extra source dynamics | Noether identity and nonuniqueness countermodel |
| F | Claim and migration governance | Frozen graph and accepted registry | No scientific fit parameter | Only dependency-closed distinct surfaces can promote | Novelty, impact, replay, release, and debt gates |

## Selection Criteria and Blinding

Selection is ordered by complete action and convention closure, exact retarded
boundary data, distributional validity, energy-flux derivation, on-shell source
conservation, limiting behavior, parameter economy, accepted-sector fit,
reusable API value, and downstream compatibility. Kinetic and source
rescalings, standing-wave counterexamples, zero coupling, constant source,
static and constant-velocity limits, and direct residuals are load bearing.
Any numerical power comparator remains excluded until equations, conventions,
oracles, mutations, and thresholds are frozen.

## Proposed Claim Delta

P141 provisionally reserves C-RAD-001 for a distinct exact conditional
retarded scalar point-source theorem. Direct registry, campaign, package, and
memory searches find no accepted or reserved C-RAD identifier and no canonical
action-to-retarded-flux API. C-SG-012 and C-OG-003 remain narrower dependencies
or convention ceilings rather than being re-promoted.

C-RAD-001 cannot claim an accelerating sine-Gordon solution, dilaton gravity,
a universal lowest multipole, a physical Larmor law, radiation reaction,
absolute power, material realization, or substrate mechanism without those
separate premises. If the exact surface duplicates an accepted theorem, P141
will terminally qualify G1 without promotion and preserve the reservation.

## Implementation and Oracle Plan

The source gate begins with the AST compatibility audit. Mutable scripts use
`np.trapezoid` when sampled integration is genuinely required, canonical
sampled work uses `trapezoid_integral`, and immutable G1 with legacy access
receives a recorded alias-only replay backed by `np.trapezoid`. A native
version abort is compatibility evidence, not scientific rejection. Exact
distributional and algebraic obligations should avoid sampled quadrature.

SymPy is the primary oracle for Euler--Lagrange variation, characteristic
derivatives, jump conditions, energy continuity, flux, parameter rescaling,
and the accelerated-ansatz residual. A fresh independent route derives the
retarded solution from left/right characteristic matching without importing
the canonical helper. If smooth-source numerics remain necessary, P141 will
predeclare the equation, domain, initial/boundary data, precision, grid,
timestep, tolerance, error norm, energy balance, refinement, and independent
method before execution; same-equation regression will not be called an
independent proof.

Mutations change the kinetic coefficient, source coupling, signal speed,
field normalization, source sign, retarded orientation, outgoing versus
standing boundary condition, acceleration, and source history. Static,
constant-source, zero-coupling, constant-velocity, and left-right symmetry
limits are explicit. The primary verifier pins G1, its dossier, this frozen
contract, source predicates, data flow, and new APIs. A frozen graph pins
dependencies and reverse consumers without asserting that future queue state
remains unchanged.

## Attempts and Continuation

Attempt 0001 freezes this contract before G1 source execution or body
inspection. Later failures are appended with the failed implementation,
mathematical, representation, candidate, or foundation mechanism and a
materially different next route. Failure of G1's physical headline advances
Candidates B through F and does not close the positive conditional object.

## Debt Ledger

The campaign debt ledger is empty. Hash and compatibility replay, action and
data-flow inventory, independent jump and flux derivations, accelerated-profile
and static-history countermodels, physical-scope review, the 31-node dependency
and consumer graph, and the governed-state transaction discharge every frozen
item without importing G2 or G3 authority.

## Results

P141 promotes C-RAD-001 in v0.108.0. The exact canonical scalar theorem derives
the point-source equation, retarded distributional jump, equal outgoing
one-side fluxes, total source-work balance, field-rescaling invariance, and a
same-equation static zero-flux countermodel. Primary and fresh independent
routes pass 37 and 29 checks, 75 focused tests pass, and the 31-node graph pins
339 predicates and passes 73 checks.

G1 is qualified rather than accepted wholesale. Its two immutable `np.trapz`
calls are a version-only compatibility event: alias-only replay backed by
`np.trapezoid` passes all ten source predicates. Scientific inspection then
rejects its extra source derivative, factor-four two-side flux error,
gamma-boosted scalar trace, same-RHS ODE regression, target-selected coupling,
accelerated-breather, dilaton-gravity, multipole, reaction, and substrate
readings. The one integrated boundary passes all 1,209 tests, validates 573
memory records, and reports `ALL REPOSITORY WORKFLOW CHECKS PASS`.

## Review and Promotion Plan

Any C-RAD-001 candidate receives a fresh independent derivation and an
individual claim review. Reusable action, retarded-solution, and energy-flux
logic moves under `src/substrate_framework/`; orchestration and physical-
ceiling evidence remain in P141. The review assigns verification, review,
compatibility, and epistemic axes separately and audits every dependency,
mutation, consumer, and convention.

G1 receives terminal predicate-level disposition whether or not a claim is
promoted. A mixed source maps only accepted surfaces and records every rejected
dilaton, gravity, Larmor, multipole, reaction, physical, or substrate clause.
Release, queue, docs, accepted memory, proposal memory, and parent effort
change only at actual boundaries. A final gate record begins in progress,
finalizes after the one integrated gate, and receives only record-sensitive
checks afterward.

## Done Gate

P141 closes only with a complete positive exact or controlled retarded-wave
object, sensitive primary and independent evidence, individual review for any
new claim, terminal G1 disposition, closed dependencies and consumers,
synchronized governed state, and an empty campaign ledger. A clean source
tally, nonzero waveform, fitted power, energy-loss identity, or Larmor label
does not complete the campaign.

## Cross-References

The governing references are P004, P010, P012, P036, P049, P132, P140, T2A,
G1, G2, G3, G4, G5, C-OG-001, C-OG-002, C-OG-003, C-SG-008, C-SG-012,
C-RAD-001, v0.107.0, v0.108.0, and the parent migration effort.
