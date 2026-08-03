---
description: Audit MC4 physical-coordinate sine-Gordon PDE simulations and nonduplication
author: vantasner
created: '2026-08-04T17:00:00Z'
updated: '2026-08-04T17:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- physical-sine-gordon
- migration-MC4
category: proposals
confidence: exploratory
status: active
---
# P098 MC4 Physical PDE Regression Audit

## Question and Positive Deliverable

P098 must determine whether MC4 adds a distinct, dependency-closed simulation
claim for the physical-coordinate sine-Gordon equation, or only finite-grid
regression evidence for the exact C-SG-017 breather and the C-SG-018 gapless
control. The positive deliverable is an exact similarity, numerical-method,
mesh/timestep/domain/tolerance, conservation, phase-space-error, control,
interpretation, dependency, consumer, and nonduplication classification;
promotion only of genuinely distinct reusable content; and a terminal MC4
disposition.

## Base Release and Provenance

The accepted base is `v0.83.0` at parent commit `cb1e182`; the latest
scientific transaction is P097 at `8ddc58b`. The predecessor evidence remains
pinned at `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; later dirty
Phase 47/48 and memory files are excluded. MC4 is
`/home/dan/substrate/merged-framework/bridges/phase-27/bridge_MC4_physical_units_pde.py`,
29,430 bytes, SHA-256
`db001de1fde9684282bb5353ec0a5ef4ddcf168809e0c02ca99878fb3f5ff698`,
and git blob `cd790522ac0ea9f5c7f331ac230c7372292b2e38`.

The generated queue marks MC4 pending and records five dynamic checks, one
assertion, numeric oracle hints, and candidate dependencies B1, G1, G2, LB3,
P3D1, and SA3. MC4's complete body was exposed during P097's required consumer
audit, so fresh body or configuration blinding is impossible and is not
claimed. MC4 has not been executed under P098 and its terminal output remains
unopened at this freeze.

Direct accepted sources are release `v0.83.0`, C-MED-003, C-SG-001,
C-SG-002, C-SG-017, C-SG-018, and C-PDE-011 with the canonical dimensional,
exact, 1D solver, and numerical modules and their adjudicated P089/P095/P096
evidence. Memory recall found the parent frontier and accepted reviews only;
every reused statement is checked at its registry, module, or immutable
campaign source. Pending consumers and MC4's imported source dependencies are
not authority.

## Invariants, Conventions, and Allowed Imports

The declared physical PDE is
`u_tt-c^2*u_xx+omega_0^2*sin(u)=0` with positive `c`, positive `ell`, and
`omega_0=c/ell`. Under `X=x/ell` and `tau=omega_0*t`, it is exactly the
accepted normalized equation. The field is a real dimensionless angle, `x`
has length, `t` has time, and the exact physical breather uses a dimensionless
frequency ratio `0<omega<1`; its laboratory angular frequency is
`omega*omega_0` and its profile scale is `ell/sqrt(1-omega^2)`.

C-SG-017 already proves the pulled-back nonlinear solution, period, width
scales, energy, action, and limits exactly. C-SG-018 fixes the conditional
linear spectrum and supplies a localized finite-energy gapless traveling
packet; it forbids treating one failed gapless trial as a universal
localization no-go. C-PDE-011 supplies reusable finite-grid evolution surfaces
and energy diagnostics, not an exact existence or material theorem.

Any new sampled integration uses `trapezoid_integral`. A source-local choice
between `np.trapezoid` and `np.trapz` may reproduce on the pinned environment,
but it is historical evidence and cannot enter new canonical or campaign
work. Finite-box and finite-time persistence remains simulation evidence even
when compared with an exact solution.

## Candidate Preregistration

The candidates are frozen before MC4 execution or terminal-output inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal MC4 reproduction | Pinned source and environment | Source configuration | Tally validates only its five implemented predicates | Hash, AST, process, output, predicate ledger, mutations |
| B | Exact similarity audit | C-MED-003 coordinates | c, ell, omega_0 | Physical PDE is the normalized PDE in scaled coordinates | Chain rule, dimensions, coefficient mutation |
| C | Canonical leapfrog regression | Periodic centered operator and exact data | domain, dX, dTau | Exact breather phase-space error and energy drift converge | Three meshes, independent time step, exact reference |
| D | Adaptive MOL cross-check | Same spatial operator, DOP853 time evolution | tolerances, max step | Time-method agreement isolates spatial error | Solver status and three tolerance levels |
| E | Gapless exact control | C-SG-018 wave family | profile and translation speed | Gapless media retain localized traveling packets | Exact residual/energy plus numerical translation error |
| F | Persistence semantics | Declared finite box and time | observation window, norms | Persistence is regression, not stability or existence proof | Boundary/domain changes and interpretation ledger |
| G | Nonduplication audit | Canonical package and accepted claims | none | No new object exists unless MC4 exceeds current APIs/evidence | Claim/API/test/campaign collision search |
| H | Consumer audit | Hash-pinned downstream uses | none | Consumers cannot backfill material or absolute-scale premises | Dependency trace and source hashes |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency and convention closure, exact
similarity, analytic-solution comparison, explicit numerical specification,
one-at-a-time refinement, conservation, mutation sensitivity, independent time
integration, parameter economy, canonical reuse, and nonduplication. Agreement
with MC4 output or its reported persistence cannot select a claim.

Fresh body or configuration blinding is impossible because P097 exposed MC4.
P098 nevertheless freezes every load-bearing equation, candidate, error norm,
refinement requirement, interpretation ceiling, and nonduplication criterion
before source execution or terminal-output inspection.

## Proposed Claim Delta

P098 reserves no identifier. Repository-wide claim, campaign, memory, module,
and test recall shows that C-SG-017 already governs the exact physical
breather; C-SG-018 governs the spectrum and gapless packet ceiling; and
C-PDE-011 plus the canonical periodic solvers govern finite-grid evolution and
energy diagnostics. A new claim is admissible only if MC4 yields a distinct,
independently refined simulation statement with a governed consumer. Otherwise
MC4 maps existing claims and receives a qualified or duplicate-evidence
disposition.

## Implementation and Oracle Plan

SymPy is the strongest oracle for the coordinate pullback, dimensions, exact
breather residual, exact gapless traveling-wave residual, energy scaling, and
load-bearing coefficient mutations. Static AST analysis will enumerate all
five checks, numerical configurations, imports, local solvers, boundary
conditions, diagnostics, and quadrature dispatch before interpreting the
source tally.

The unchanged source is the reproduction oracle for its own finite-grid
output. The independent canonical experiment is frozen at `c=3/2`,
`ell=5/4`, `omega_0=6/5`, normalized breather frequency `3/5`, float64,
periodic normalized domains of half-width 20, 30, and 40, spatial steps
`1/5`, `1/10`, and `1/20`, and four exact normalized periods. Leapfrog uses
Courant ratios `2/5` and `1/5`; the primary phase-space error is the square
root of the trapezoid-integrated squared field-plus-velocity error divided by
the corresponding exact norm. Relative energy drift is normalized by initial
energy. Errors must decrease at all three spatial levels, the two finest
observed spatial orders must exceed 1.5 when roundoff has not saturated, the
finest phase-space error and relative energy drift must each be below 0.5
percent, time-step halving must reduce its error, and increasing the domain
must not change the finest error by more than 20 percent.

DOP853 uses the same centered spatial operator and three `(rtol,atol)` levels:
`(1e-8,1e-11)`, `(1e-9,1e-12)`, and `(1e-10,1e-13)`, with maximum normalized
step `1/50`. Solver success and finite state are prerequisites. Tolerance
refinement must not worsen the final phase-space error beyond 2 percent; the
tightest DOP853 and time-refined leapfrog states must agree within 0.5 percent
in the same relative phase-space norm. Because both routes share the spatial
operator, this is an independent time-integrator check, not independent
spatial evidence.

Mutations set `omega_0` independently of `c/ell`, break
`eta^2+omega^2=1`, zero the exact initial velocity at the phase where it is
nonzero, flip the on-site sign, replace periodic with incompatible endpoint
data, and confuse physical with normalized time. Each must break a relevant
exact or numerical verdict. Domain and boundary-tail effects are reported
separately from discretization error. No finite simulation earns exact,
stability, material, or infinite-time status.

## Attempts and Continuation

Source, solver, convergence, tolerance, representation, or interpretation
failures are appended with their precise mechanism. A failed numerical route
is repaired or replaced, and a source overclaim is qualified while the exact
similarity, numerical classification, nonduplication, and source disposition
remain positive obligations.

## Debt Ledger

P098 tracks source hash and blob, every check and import, equation, units,
coefficient map, exact initial data, domain, boundary condition, float
precision, spatial operator, timestep and stability ratio, solver status,
sampling, error norm, exact reference, energy convention, mesh/time/domain/
tolerance refinement, independent time method, gapless control, mutations,
quadrature compatibility, persistence semantics, exact-versus-simulation
status, canonical nonduplication, consumers, source disposition, generated
state, and parent continuation. Every item must be derived, declared,
rejected, or excluded before closure.

## Review and Promotion Plan

Claim-level review compares source reproduction, exact similarity, the
predeclared convergence and conservation study, the adaptive time-method
cross-check, mutations, gapless counterexamples, prior accepted evidence,
candidate comparison, impact and consumer maps, and nonduplication. Distinct
content receives canonical extraction, tests, four-axis review, release and
generated-state updates. Otherwise P098 changes no accepted release and
records a terminal qualified or duplicate-evidence MC4 disposition with
durable evidence. One integrated workflow gate runs at the final meaningful
boundary; later record closure receives record-sensitive checks only.

## Done Gate

P098 closes only when the positive similarity/numerical/refinement/
conservation/control/interpretation/nonduplication classification exists,
every MC4 predicate and imported premise has an individual verdict, required
source and sensitive canonical oracles pass, consumers replay, campaign debt
is empty, and the parent migration can advance. A passing five-check source
tally or an already exact breather formula is not completion.

## Cross-References

See MC4, P089, P093, P095, P096, C-MED-003, C-SG-001, C-SG-002, C-SG-017,
C-SG-018, C-PDE-011, the dimensional and exact sine-Gordon modules, the 1D
solver and numerics modules, and the parent framework-migration effort.
