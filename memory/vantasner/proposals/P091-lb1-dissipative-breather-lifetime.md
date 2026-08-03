---
description: Derive and audit LB1's damped-breather action and energy lifetime
author: vantasner
created: '2026-08-04T07:55:00Z'
updated: '2026-08-04T07:55:00Z'
tags:
- substrate-framework
- campaign-proposal
- damped-breather
- migration-LB1
category: proposals
confidence: exploratory
status: active
---
# P091 LB1 Dissipative Breather Lifetime

## Question and Positive Deliverable

P091 must determine whether LB1 derives an exact or controlled physical
breather lifetime under linear damping, or conflates the exact damped energy
balance, an undamped-family time average, a small-amplitude limit, and an
inserted medium loss rate. The positive deliverable is an exact boundary-flux,
kinetic-integral, period-average, form-factor, adiabatic action, nonlinear
energy-decay, lifetime-convention, approximation-error, damping-regime,
physical-units, dependency, consumer, and nonduplication classification;
individual promotion of any distinct surviving object; and a terminal LB1
disposition.

## Base Release and Provenance

The accepted base is `v0.77.0`; the latest scientific adjudication is P090 at
commit `f79909e`, and the parent effort synchronization is `bb3ab57`. The
predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. LB1 is
`/home/dan/substrate/merged-framework/bridges/phase-26/bridge_LB1_dissipative_lifetime.py`,
18,031 bytes, with SHA-256
`d2e36e0d9d8ff831bcd58efb264b68dc156f7f87eca7a104f53a6f287eed2b80`
and git blob `0be1ee0510232a04a2342fedd730752eeb0485b4`.

The generated queue marks LB1 pending, records twenty-two runtime checks from
twenty-one literal sites, and names pending MC3 as a candidate dependency. Its
synopsis exposes the normalized damped equation, exact energy-loss balance,
small-amplitude approximation, a claimed time-averaged kinetic integral equal
to energy, exponential energy decay with `tau=1/Gamma`, and a full-amplitude
form factor whose values remain unopened. Navigation and consumer searches also
expose later noncanonical formulas such as
`g_window=exp[-delta*(1/2+theta)*n_w]` and an overdamped cutoff. The LB1 body,
full-amplitude formulas, parameter values, predicate bodies, output, fits, and
consumer implementations remain unopened until the freeze gate.

The accepted sources read directly are the current release, C-SG-001 through
C-SG-003, C-SG-012, C-PDE-011, the canonical exact sine-Gordon action/energy
APIs, P002's independent phase-space derivation, and the canonical damped
finite-interval numerical machinery. Memory search found the parent
continuation and the accepted action and finite-time ceilings; every reused
fact is checked at its registry, campaign, package, or pinned source record.

## Invariants, Conventions, and Allowed Imports

C-SG-001 and C-SG-002 supply the exact undamped normalized breather and energy.
C-SG-003 supplies the canonical action
`J=16*acos(omega)`, `dE/dJ=omega`, and `E=16*sin(J/16)`. Its definition implies
that the undamped period average of `integral(phi_t^2)dx` is `omega*J`, but does
not by itself state a damped trajectory. C-SG-012 supplies the exact off-shell
energy divergence, so for residual `R=-Gamma*phi_t` the integrated identity is
`dE/dt=boundary_flux-Gamma*integral(phi_t^2)dx` under explicit smoothness and
boundary hypotheses.

The undamped breather ansatz is not an exact solution of the damped equation
for positive Gamma. Replacing its frequency or action by a slowly varying
coordinate is an adiabatic approximation whose regime, phase averaging,
radiation, deformation, boundary, and error terms must remain explicit. Within
that reduced model, the exact undamped-family average gives
`D(omega)=omega*acos(omega)/sqrt(1-omega^2)`,
`dJ/dt=-Gamma*J`, and hence exponential action but nonlinear energy
`E(t)=16*sin[(J0/16)*exp(-Gamma*t)]`. Energy becomes exponential only in the
small-action limit. Energy, action, amplitude, and field-envelope e-fold times
are not interchangeable away from that limit.

Gamma is dimensionless inverse time in the normalized equation. A collision
rate, density, cross-section, material damping, physical time conversion, or
per-medium frequency requires a separately accepted map. Pending MC3 and later
LB units cannot be imported as authority. C-PDE-011 contributes reusable
finite-time solvers and energy ledgers only, not its forcing mechanism. All
sampled integration must use `trapezoid_integral` or a claim-appropriate SciPy
method rather than a version-specific NumPy alias.

## Candidate Preregistration

The candidates are frozen before the LB1 source body, literal predicates,
full-amplitude values, executable output, or consumer implementations are
opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal LB1 promotion | Undamped ansatz remains exact and MC3 is accepted | Source premises | Fails if energy and action lifetimes are conflated | Registry, residual, source, and consumer closure |
| B | Exact damped energy balance | Smooth field and declared boundary flux | Gamma | Exact for every field solving the damped equation | Stress-energy substitution, signs, units, mutations |
| C | Exact undamped kinetic average | C-SG-001 through C-SG-003 | Omega | Mean kinetic integral is omega*J | Action definition and independent field integration |
| D | Adiabatic action modulation | Slow damping and family tracking | Gamma and J0 | J decays exponentially; E follows a sine law | Chain rule, limits, residual ceiling, and mutations |
| E | Full-amplitude energy form factor | Candidate C and accepted energy | Omega | D differs from one except at the small-amplitude edge | Exact formula, monotonicity, endpoints, working point |
| F | Direct damped-PDE validation | Uniform damping, distant walls, exact-family initial data | Mesh, timestep, domain, Gamma | Adiabatic error decreases with slower damping/refinement | Energy ledger, action inversion, snapshot fit, two methods |
| G | Lifetime convention audit | Declared observable and e-fold threshold | Observable | Only action has exact 1/Gamma e-fold in Candidate D | Solve energy/action/envelope crossings exactly |
| H | Physical medium lifetime | Accepted normalized-to-physical Gamma map | Material inputs | Absent unless independently derived | Units, density, cross-section, frequency, and consumer audit |
| I | Mutation-sensitive source oracle | Every load-bearing coefficient affects a relevant verdict | None | Literal tallies expose copied limits or weak samples | Gamma, factor, form, frequency, average, and fit mutations |
| J | Consumers and nonduplication | Distinct API and governed downstream role | None | Exact balance may duplicate C-SG-012; action law may be distinct | Registry, LB2/LB3, engineering, package, and test trace |

## Selection Criteria and Blinding

Selection is ordered by accepted closure for equation, damping, boundary flux,
action, physical units, and consumers; exact residuals, normalization, signs,
domains, chain rules, limits, and lifetime conventions; controlled adiabatic
error and numerical convergence; mutation sensitivity; parameter economy; and
nonduplication. Source form-factor values, fitted curves, check tallies, and
engineering agreement cannot select the lifetime concept.

Comparator blinding remains intact beyond the generated synopsis and search-
exposed downstream formula names. Both contracts, hashes, repository
validation, and an immutable freeze record must exist before the LB1 body,
complete formulas, checks, output, numerical values, or consumer code is
opened.

## Proposed Claim Delta

P091 provisionally reserves `C-SG-016` for the distinct exact conditional
statement that the C-SG-001 family has mean kinetic integral `omega*J`, form
factor `omega*J/E`, and that phase-averaged linear damping on the adiabatic
family gives exponential action and the corresponding nonlinear energy law.
A repository-wide registry, campaign, generated-document, and durable-memory
search found no prior or rejected use of `C-SG-016`. The claim depends on
C-SG-001, C-SG-002, C-SG-003, and C-SG-012; it challenges and supersedes none.
Promotion requires Candidate J to show that the damped action/energy consequence
is distinct from the accepted action definition and stress balance, with
canonical APIs, tests, controlled interpretation, and a governed consumer.

## Implementation and Oracle Plan

The canonical exact module may add pure APIs for the mean kinetic integral,
damping form factor, adiabatic action, frequency, and energy trajectories and
their observable-specific e-fold times. SymPy is the primary oracle for the
field derivative and spatial/time average, action normalization, form factor,
energy-chain rule, exact solution of the reduced action ODE, endpoint series,
monotonicity, lifetime crossings, dimensions, and load-bearing mutations. An
independent route will reconstruct the phase-space integral without calling the
new APIs and derive the reduced law from `dE/dJ=omega`.

Actual damped-PDE evidence, if needed for interpretation, will use the existing
homogeneous-Dirichlet bulk evolvers with zero source, uniform nonnegative
damping, exact-breather initial data at zero field phase, float64, and explicit
energy-loss ledger. The preregistered central branch is
`omega0=1/sqrt(2)`, `Gamma=0.02`, normalized final time 50, domains
`[-60,60]` and `[-80,80]`, spatial steps `0.2,0.1,0.05`, leapfrog timestep
`dx/2`, and diagnostic interval 0.25. DOP853 at `dx=0.2` with relative and
absolute tolerances `1e-9` and `1e-11` supplies a method cross-check. A slower
`Gamma=0.01` branch is compared at equal slow time `Gamma*t=1`; zero damping
is the soluble conservation limit. Error metrics are relative action-trajectory
RMS, final energy and phase-space exact-family errors, and energy-balance
residual relative to dissipated energy. A physical approximation needs errors
below five percent on the central branch, improvement with slower damping or
refinement, solver success, and no wall sensitivity; failure limits the claim
to the exact conditional reduction.

## Attempts and Continuation

Failed symbolic representations, source predicates, adiabatic closures, PDE
discretizations, and physical maps are append-only. A source exponential that
fails at full amplitude is replaced by the exact reduced sine law, not rescued
by relabeling action as energy. A numerical mismatch is diagnosed as method,
boundary, phase-average, radiation, deformation, or candidate failure before a
new route. The accepted action campaign is the nearest transferable
construction and its normalization is verified before inventing another
lifetime coordinate.

## Debt Ledger

P091 tracks the damped equation, residual sign, Gamma domain and units,
boundary flux, exact kinetic integral, period and average, action convention,
form factor, small-amplitude expansion, full-amplitude behavior, collective
coordinate, phase averaging, radiation and deformation error, energy/action/
amplitude lifetime convention, initial phase, domain, boundary data, mesh,
timestep, solver, tolerances, stopping time, energy ledger, independent method,
physical time map, collision or material model, consumer, and every accepted or
pending dependency. Every item must be derived, declared, rejected, or excluded
before closure.

## Review and Promotion Plan

Review compares primary and independent exact derivations, any damped-PDE
evidence, all source subclaim verdicts, mutations, candidate comparison, impact
and consumer maps, and nonduplication. `C-SG-016`, if it survives, receives an
individual review with four-axis status, package implementation and tests,
registry and release transaction, generated documentation, and accepted-memory
synchronization. A terminal LB1 disposition will preserve any rejected physical
Gamma, exact-damped-solution, or universal-lifetime reading and regenerate the
source queue.

## Done Gate

P091 closes only when the positive balance/average/action/energy/lifetime/
approximation classification exists, every source predicate has an individual
verdict, primary and independent routes plus load-bearing mutations pass,
affected consumers replay, campaign debt is empty, and the parent migration can
continue. An exact energy balance, small-amplitude limit, fitted form factor,
or `ALL CHECKS PASS` tally is not sufficient alone.

## Cross-References

See LB1, MC3, LB2, LB3, P002, P049, P089, C-SG-001 through C-SG-003,
C-SG-012, C-PDE-011, the canonical exact and 1D numerical APIs, and the parent
migration effort.
