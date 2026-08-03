---
description: Audit SA3's driven sine-Gordon PDE seeding and bound-state classifier
author: vantasner
created: '2026-08-04T04:10:00Z'
updated: '2026-08-04T06:25:00Z'
tags:
- substrate-framework
- campaign-proposal
- driven-sine-gordon
- migration-SA3
category: proposals
confidence: working
status: archived
---
# P089 SA3 Driven-PDE Seeding Audit

## Question and Positive Deliverable

P089 must determine whether SA3 constructs a well-posed and converged driven
sine-Gordon experiment whose post-drive state is demonstrably a bound accepted
breather preferentially seeded by a structurally defined fast or resonant
deposition, or only a source-specific finite-box trajectory and classifier. The
positive deliverable is an exact source, energy-work, boundary-flux, damping,
drive-normalization, numerical-convergence, bound-state, radiation-rejection,
dependency, consumer, and nonduplication classification, individual promotion
of any distinct surviving object, and a terminal SA3 disposition.

## Base Release and Provenance

The accepted base is `v0.76.0`; the latest terminal adjudication is P088 at
commit `aee1890`, and the parent effort synchronization is `e7cd684`. The
predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. SA3 is
`/home/dan/substrate/merged-framework/bridges/phase-25/bridge_SA3_driven_sg_pde_seeding.py`,
27,023 bytes, with SHA-256
`3aec2a8bca448f28bceb175e44ff2a6c3dcba3b57c22a0dcbd93f8d405a17e8f`
and git blob `dd8ae6fc142d201a8d3aa0045e73149ee2914e36`.

The generated queue marks SA3 pending and names P3D1, SA1, and SA2 as
candidate dependencies. Its synopsis exposes a normalized nonlinear driven
sine-Gordon PDE, a localized `sech(eta*x)` spatial source, fast or resonant
versus slow deposition, absorbing quadratic sponge boundaries, and a claimed
bound-core classifier. Source metadata and synopsis are navigation evidence;
the SA3 body, complete equations, parameter values, mesh, timestep, boundaries,
checks, output, thresholds, and consumer implementation remain unopened until
the freeze gate.

The accepted sources read directly are the current release, C-SG-001,
C-SG-002, C-SG-011, C-SG-012, C-SG-015, C-PDE-001, the canonical sine-Gordon,
1D evolution, and numerical-evidence APIs, P3D1's terminal finite-time ceiling,
and P087/P088's terminal rejection ceilings. Memory search found the parent
continuation plus the earlier governed 1D and radial numerical contracts; every
reused fact is checked at the registry, campaign, package source, or pinned
source metadata.

## Invariants, Conventions, and Allowed Imports

C-SG-001 and C-SG-002 provide an exact undriven 1+1 breather and normalized
energy, not an external source, plasma interaction, formation probability, or
seeding efficiency. C-SG-015 supplies its fixed-point temporal spectrum but no
susceptibility. SA1 and SA2 are qualified and their rejected physical response,
population, voltage-slew, breakdown, and engine meanings cannot be inherited.
C-PDE-001 is a separately declared 3+1 radial finite-time IVP and explicitly is
not a lift of the exact breather; it contributes numerical standards only.

For a declared `phi_tt-phi_xx+sin(phi)=J`, exact Hamiltonian accounting must
retain source work `integral J*phi_t dx`, boundary flux, and every damping or
sponge term with explicit signs. A spatial source profile is an external
forcing premise unless an accepted interaction derives it and its units. Once
the source switches off, a claimed breather must be distinguished from retained
box modes, radiation, kinks or kink pairs, residual drive, sponge reflections,
and generic nonlinear oscillatory cores. Sub-gap frequency or nonzero core
energy alone is insufficient.

Finite-box persistence is not asymptotic binding. Domain, sponge, grid,
timestep, integration tolerance, duration, analysis window, and source shutoff
must be independently audited. Fast, slow, resonant, and off-resonant drives
need preregistered common normalizations; raw outcomes from drives that also
change amplitude, duration, work, or spatial overlap do not identify the causal
feature. Sampled accepted work must use the shared numerical layer and
`trapezoid_integral`, never a direct version-specific NumPy alias.

## Candidate Preregistration

The candidates are frozen before the SA3 source body, literal checks,
executable output, parameter values, grid, boundary implementation, thresholds,
classifier, or consumer code are opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal SA3 promotion | Every source, classifier, and dependency is accepted | Source premises | Fails if any physical or numerical object is missing | Registry, AST, solver, and consumer closure |
| B | Forced energy theorem | Smooth driven field and declared damping/boundary data | Source and damping | Exact source-work/flux/dissipation ledger only | Variational derivation, signs, units, and mutations |
| C | Classifier calibration | Exact breathers and planted nonbreathers | Diagnostic choices | Valid classifier accepts breathers and rejects counterstates | Exact-family convergence and false-positive suite |
| D | Source-defined driven IBVP | Frozen PDE, data, source, domain, and numerics | Mesh, timestep, tolerances | At most resolution-bounded trajectory evidence | Solver success, refinements, limits, independent method |
| E | Post-drive bound state | Source off and radiation separated | Windows and core radius | Requires multiple convergent diagnostics | Localization, energy, residual, projection, and flux probes |
| F | Drive selectivity | Common drive normalization and frozen family | Frequency, width, phase | Scalar fast/resonant labels may not order outcomes | Equal-work and alternative-normalization controls |
| G | Mutation-sensitive source oracle | Every load-bearing input changes a relevant verdict | None | Weak tallies fail targeted mutations | Source, sponge, domain, amplitude, shutoff, and classifier mutations |
| H | Physical seeding mechanism | Accepted deposition-to-source interaction | Coupling and units | Absent unless independently derived | Action, field map, absorption, formation, and count audit |
| I | Consumers | Actual import and threshold path | Consumer inputs | No engine result without an implemented accepted path | SA4, engineering, and C035 trace |
| J | Nonduplication | Distinct theorem/API/consumer | None | No claim for duplicated solver or standard energy algebra | Registry, package, and consumer comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted closure of source action, physical deposition
map, energy work, post-drive formation, and consumer; well-posed PDE/data and
complete numerical specification; exact signs, units, limits, convergence,
independent-method agreement, and mutation sensitivity; a classifier that
rejects planted false positives; fair drive normalization; parameter economy;
and nonduplication. Source values, plots, thresholds, and pass tallies cannot
select the classifier or drive concept.

## Proposed Claim Delta

No new claim identifier is assigned. The registry, adjudicated campaigns, and
durable memory must be searched for identifier collisions before any later
promotion; rejected and provisional identifiers remain reserved. Existing
accepted claims already own the exact undriven breather, stress-energy and
boundary identities, and reusable numerical machinery. A claim proceeds only
if Candidate J identifies a distinct exact forced-energy theorem or a genuinely
resolution-bounded driven-formation object with complete assumptions, canonical
implementation, sensitive verification, and a governed consumer. No accepted
claim is challenged or superseded.

## Implementation and Oracle Plan

SymPy is the primary oracle for variation, source-work and boundary-flux signs,
damping terms, linearized limits, dimensions, exact planted-breather identities,
and normalization counterfamilies. NumPy/SciPy are appropriate only for an
explicit driven IBVP whose domain, initial/boundary data, source, floating
precision, spatial operator, timestep or adaptive tolerances, sponge, stopping
rule, diagnostic norm, and solver-success state are recorded. Any serious
numeric result requires mesh, timestep, domain, sponge, duration, window, and
tolerance refinement, controlled energy balance, a soluble or exact limit, an
independent method, and load-bearing mutations.

The primary route will pin and reproduce SA3, audit every source equation and
predicate, calibrate its classifier on exact breathers and nonbreather
counterstates, then replay only source-defined trajectories that survive those
structural tests. The independent route will use a different time integrator or
spatial representation and an independently coded energy/classifier ledger.
Reusable package code is added only if existing `sine_gordon_1d.py` and
`numerics.py` do not already supply the needed pure API. One integrated
unchanged-boundary gate closes the campaign; later record finalization receives
record-sensitive checks only.

## Attempts and Continuation

Failed solver, classifier, source, and concept routes are append-only. A source
trajectory that disperses, forms a different object, depends on a wall or
sponge, or cannot distinguish fast/resonant drive is preserved as evidence and
followed by a repaired method, alternative classifier, fair normalization, or
different candidate. A no-go or absent mechanism does not complete the parent
migration.

## Debt Ledger

P089 tracks PDE and action conventions, source sign and units, spatial profile,
temporal drive, amplitude, duration, phase, injected work, initial data, domain,
boundary data, sponge, mesh, timestep, floating precision, solver, tolerances,
success state, stopping time, source shutoff, core radius, diagnostic window,
energy balance, flux, dissipation, localization, frequency, residual,
exact-breather projection, radiation, topology, refinement, independent method,
analytic limit, counterstates, physical interaction, absorption, formation,
count, threshold, consumer, and every accepted or rejected dependency. Every
item must be derived, declared, rejected, or excluded.

## Review and Promotion Plan

Review compares primary and independent exact/numeric routes, source
reproduction and AST audit, classifier calibration, convergence and energy
ledgers, dependency closure, mutations, candidate comparison, impact map,
consumer inspection, and nonduplication. A terminal SA3 disposition will name
durable evidence and regenerate the source queue. Any accepted claim receives
its own collision-free registry decision, package tests, release, generated
documentation, and accepted-memory synchronization; otherwise `v0.76.0` and
the package remain unchanged.

## Done Gate

P089 closes only when the positive source/energy/numerics/classifier/formation
classification exists, every source predicate has an individual verdict, both
routes and load-bearing mutations pass, affected consumers replay, campaign
debt is empty, and the parent migration can continue. A source tally, sub-gap
FFT peak, late core energy, fast-versus-slow plot, or absence of physical
formation is not sufficient alone.

## Terminal Adjudication

P089 accepts qualified `C-PDE-011` for the exact parameter-pinned fast-source
IBVP and no broader mechanism. Three leapfrog grids, timestep refinement,
domain and sponge changes, adaptive DOP853, exact-family temporal and snapshot
fits, a convergent source-work ledger, and proxy-target mutations support the
finite-time object. SA3.3 is rejected because the slow run receives more than
three times the actual source work and ends in a high-energy eight-transition
state rather than vacuum. SA3.4's raw FFT stability is bin locking, and SA3.5's
second core energy exceeds the single-breather maximum. SA3 is terminally
qualified; the release advances to `v0.77.0`, campaign debt is empty, and the
parent effort continues to SA4.

## Cross-References

See SA3, P3D1, SA1, SA2, P044, P087, P088, C-SG-001, C-SG-002,
C-SG-011, C-SG-012, C-SG-015, C-PDE-001, the canonical 1D and numerical
APIs, and the parent migration effort.
