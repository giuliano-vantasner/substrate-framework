---
description: Derive reflected first-passage dynamics and audit BD5's stochastic escape claims
author: vantasner
created: '2026-08-03T13:42:00Z'
updated: '2026-08-03T13:42:00Z'
tags:
- substrate-framework
- campaign-proposal
- first-passage
- migration-BD5
category: proposals
confidence: exploratory
status: active
---
# P103 BD5 Kramers Escape Audit

## Question and Positive Deliverable

P103 must deliver an importable, mutation-sensitive theorem and numerical
evaluator for the mean first-passage time of a declared one-dimensional
overdamped diffusion with a reflecting left boundary and absorbing right
boundary. It must independently solve the backward problem, quantify numerical
error, and adjudicate every BD5 predicate against the exact stochastic object.

The campaign is not complete merely because thirteen source checks pass or a
four-point log-rate fit has a slope near minus one. It must distinguish the
uncensored mean first-passage time from a completed-only finite-horizon sample,
a restricted mean, a hazard, and an asymptotic Kramers approximation; expose
boundary, timestep, ensemble, horizon, seed, and uncertainty assumptions; and
close the source without importing a physical inertia, bath, temperature
optimum, population event, or DBD interpretation.

## Base Release and Provenance

The accepted base is `v0.86.0` at parent commit
`b562048fcf00f82f0cf3fa473bac62faa078bad7`; the latest scientific transaction
is P102 at `bb94cc1ed281090f37fa4f1d04a6f2da63f77bf3`. Source evidence is pinned
to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; unrelated dirty Phase
47/48 work and the explicit NumPy compatibility overlay are excluded from
scientific authority.

BD5 is
`/home/dan/substrate/merged-framework/bridges/phase-28/bridge_BD5_kramers_escape_pde.py`,
10,583 bytes, SHA-256
`fd1fd9e54990bbac4a60bc669a37f1c15a89ebd2595203aef7d2bddb88b99cf9`,
and git blob `6cfb444f3ab0bda8b456ac188f00a7faf904ccb8`. It is clean relative to the
pinned commit. The queue marks it pending, records thirteen literal checks,
and lists candidate dependencies BD1, BD2, and BD4. Those units are now bounded
by accepted C-RG-002, C-TH-002, and C-COL-001 respectively, none of which
supplies BD5's damping, noise, boundaries, or event map.

No genuine source body, method, parameter, or tally blinding remains. P102
executed BD5 as a consumer and exposed `ALL 13 CHECKS PASS`; the generated queue
and parent effort exposed its scaled barrier, overdamped Langevin equation,
reflection and absorption, Arrhenius regression, temperature and population
headlines, and convergence claim. P103 claims no formula or comparator
blinding. It freezes competing structural interpretations and decisive tests
before renewed BD5 inspection or execution.

Direct accepted sources read before freeze are release `v0.86.0`, relevant
registry entries C-RG-001, C-RG-002, C-COL-001, C-TH-001, C-TH-002,
C-COH-001, C-COH-002, and C-PRB-001, plus their canonical radial-energy,
collective-coordinate, thermal, coherence, and conditional backward-BVP
implementations. Durable memory was re-sourced at those authority surfaces.
Repository-wide collision search found no accepted first-passage-time claim or
reserved `C-FPT-001` identifier.

## Invariants, Conventions, and Allowed Imports

Declare a real coordinate `x` on `[a,b]`, a continuously differentiable real
potential `U`, positive thermal scale `Theta`, and positive friction `gamma`.
The reflected Itô diffusion has interior generator
`L f=-(U'/gamma) f' + (Theta/gamma) f''`, reflection at `a`, absorption at
`b`, and stopping time `T_b`. Its mean `tau(x)=E_x[T_b]` must solve
`Theta*tau''-U'*tau'=-gamma`, `tau'(a)=0`, and `tau(b)=0`.

Under the declared regularity, the candidate integral is
`tau(x)=(gamma/Theta)*integral_x^b exp(U(y)/Theta)
integral_a^y exp(-U(z)/Theta) dz dy`. A constant added to `U` must cancel.
For the soluble linear potential `U=F*(x-a)`, the start-point result must be
`gamma*Theta*(exp(s)-1-s)/F^2`, where `s=F*(b-a)/Theta`, with continuous
zero-force limit `gamma*(b-a)^2/(2*Theta)`. These are conditional mathematical
objects; physical units require `gamma` to make drift and diffusion dimensions
consistent.

BD5's scaled source potential is provisionally treated only as the declared
dimensionless family `U(rho)=E*(2*rho-rho^2)` on a separately declared interval.
The left endpoint is a constrained boundary, not a stationary potential well;
the interior top is at one, and moving the absorbing boundary changes the
first-passage observable. Absolute-value Euler reflection and discrete
absorption are numerical boundary rules requiring timestep convergence.

For administrative horizon `c`, the completed-only population mean is
`E[T_b | T_b<=c]`, not `E[T_b]`, whenever survival beyond `c` has positive
probability. The empirical restricted mean uses `min(T_b,c)` and still does
not recover the infinite-horizon tail without a tail model or near-complete
absorption. An inverse mean is not a constant hazard unless a separately
verified exponential first-passage law supplies that equivalence.

## Candidate Preregistration

The candidates are frozen before renewed source-body inspection, execution,
or new evaluation at the source parameter values.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal reproduction | Pinned source environment | Source symbols, arrays, and literals | Tally proves only implemented finite-sample predicates | Hash, AST, process, output, and predicate ledger |
| B | Exact backward theorem | Reflected Itô diffusion and regular potential | U, Theta, gamma, a, b, x | Positive integral uniquely solves the mean first-passage BVP | Differentiate the integral, boundaries, uniqueness, constant-shift and coefficient mutations |
| C | Adaptive integral evaluator | Finite continuous potential on a compact interval | Quadrature tolerances | Controlled numeric MFPT follows from B | Error estimates, tolerance refinement, soluble linear and zero-force limits |
| D | Independent backward solver | Same generator and boundary data | Mesh and solver tolerance | A separate BVP route converges to the integral | Mesh/tolerance refinement, residual, boundary, and method agreement |
| E | Reflected path ensemble | Itô convention and explicit discrete boundary rule | dt, n, tmax, seed | Simulation approaches the backward result only with controlled censoring and refinement | Coupled timestep/ensemble study, uncertainty, escape fraction, analytic comparator |
| F | Censoring audit | Administrative cutoff | cutoff and event-time law | Completed-only inverse mean generally overstates inverse MFPT | Exact conditional-mean inequality and synthetic censored counterexample |
| G | Boundary-well Arrhenius route | Deep quadratic source barrier | E/Theta and absorbing point | Leading exponential may survive with boundary-specific prefactor corrections | Laplace asymptotic, slope window, and exact-integral ratios |
| H | Temperature and population separation | Accepted conditional algebra only | declared q, kT, E, N, V | Monotonic response and a chosen half-ratio are not an optimum or event | Derivative/objective audit and absent-coupling countermodels |
| I | Consumer and interpretation audit | Accepted dependencies only | none | No material inertia, DBD ignition, or observed rate follows | Registry and executable dependency ledger |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure and nonduplication; exact
backward derivation, boundary conditions, dimensions, positivity, invariances,
and soluble limits; independent quadrature and BVP convergence; honest
censoring, uncertainty, and hazard semantics; assumption and parameter economy;
canonical extraction; and complete consumer classification. A source tally,
fitted slope, or numerical closeness cannot select the concept.

The source formulas, broad parameter choices, terminal tally, and intended
headlines were exposed before P103. The campaign claims no source or comparator
blinding. It freezes the integral representation, BVP, numerical methods,
censoring distinction, boundary mutations, deep-barrier asymptotic candidate,
temperature-objective test, and no-event ceiling before renewed inspection or
execution.

## Proposed Claim Delta

P103 reserves `C-FPT-001`. Collision searches across the registry, campaigns,
proposals, durable memory, source modules, and tests found no use of that
identifier and no accepted theorem combining a reflected overdamped generator,
absorbing first-passage BVP, positive integral solution, and finite-horizon
censoring distinction. C-PRB-001 owns a different supplied absorbing BVP on a
unit interval and explicitly derives no stochastic generator; it is a
nonduplication anchor, not a dependency.

The proposed claim has no scientific dependency on the capillary, thermal,
collective-coordinate, or coherence sectors because it is conditional on its
own declared generator and boundaries. Those claims are compatibility and
interpretation ceilings for the BD5 specialization. No accepted claim is
challenged or superseded. Promotion may be abandoned if exact or collision
review defeats novelty, but BD5 must still receive terminal adjudication.

## Implementation and Oracle Plan

If candidate B survives, a pure importable module will expose the reflected-to-
absorbing backward residual, adaptive integral evaluator, soluble linear-force
control, source quadratic potential, and explicit censored-ensemble summary.
It will accept potential, interval, coordinate, thermal scale, friction,
tolerances, event times, completion flags, and horizon explicitly. Imports
will execute no simulation or print output.

SymPy or direct exact calculus is the strongest oracle for the generator,
integrating-factor derivation, boundary conditions, additive-potential
invariance, linear-potential result, zero-force limit, dimensions, positivity,
and completed-versus-full population-mean distinction. SciPy adaptive
quadrature in IEEE-754 binary64 will use `epsabs=1e-11`, `epsrel=1e-11`, finite
status/output gates, and repeated tolerances `1e-8`, `1e-10`, and `1e-12`.
It must agree with the soluble linear control to relative error below `2e-9`.

An independently written backward BVP route will use the explicit first-order
system `tau'=v`, `v'=(U'*v-gamma)/Theta`, Neumann data `v(a)=0`, and Dirichlet
data `tau(b)=0`. Collocation or a second-order finite-difference scheme will be
run on at least four meshes from no more than 51 to at least 401 intervals,
with solver status, residual, boundary error, and float64 precision recorded.
The final solution must agree with adaptive quadrature below `2e-5` relative
and show decreasing error with a final observed order above `1.7` for a fixed
second-order discretization; an adaptive collocation route instead must refine
tolerance independently and report its residual.

Euler-Maruyama is regression evidence, not the independent oracle. Any new
ensemble must state the exact drift, diffusion, initial point, absolute-value
or alternative reflection, discrete absorption rule, `dt`, `tmax`, trajectory
count, seed or seed family, escaped fraction, completed-only mean, restricted
mean, and batch or bootstrap uncertainty. At least three timesteps and three
ensemble sizes are required at a moderate barrier with the horizon chosen
before results. Timestep and Monte Carlo effects must be varied separately;
the refined estimate must be statistically compatible with the backward
result or the attempt is preserved and repaired.

Load-bearing mutations change the drift sign, diffusion factor two, reflecting
condition, absorbing position, barrier normalization, thermal scale, and
completed-only censoring rule; each must break a relevant verdict. Countermodels
include zero force, a linear force with exact solution, a deep barrier whose
finite-horizon source convention returns zero despite a positive exact MFPT
rate, a nonexponential first-passage law, a monotonic temperature family with
no finite optimum, and uncoupled population algebra.

The compatibility preflight expects no sampled quadrature in the new exact
route. Adaptive integration uses SciPy; any sampled canonical integration must
use `trapezoid_integral`, and mutable current-environment scripts must use
`np.trapezoid`, never `np.trapz`. If an immutable source aborts solely on the
removed alias, an alias-only replay precedes scientific adjudication and the
abort is not candidate failure. Focused replay covers the new module and the
accepted radial, thermal, collective, coherence, probability, and numerics
tests. One full workflow gate runs only at the promotion/adjudication boundary.

## Attempts and Continuation

Every source, representation, exact, numerical, boundary, stochastic,
statistical, asymptotic, dependency, consumer, or verifier failure is preserved
append-only with its command, environment, output, diagnosis, and next route.
A failed Monte Carlo convergence claim does not finish P103; the backward
theorem and terminal source audit continue through a repaired method or a
different candidate.

## Debt Ledger

P103 tracks source hash and prior exposure; the exact generator, stochastic
convention, coordinate domain, initial state, potential and unit conventions,
reflection and absorption, first-passage definition, integrating factors,
quadrature tolerances, BVP mesh and residual, timestep, ensemble, horizon,
seeds, censoring, uncertainty, asymptotic regime, temperature objective,
population coupling, every literal source check, consumers, disposition,
generated state, and parent continuation. Every item must be derived, declared,
rejected, or excluded before closure.

## Review and Promotion Plan

The proposed claim receives a primary exact-and-numeric verifier, an independent
backward-equation rederivation, claim-level prose review, source predicate
adjudication, impact analysis, and affected-consumer replay. Acceptance requires
canonical package extraction, sensitive tests, governance and release updates,
generated docs, accepted-memory synchronization, a terminal BD5 disposition,
and one full workflow validation. A final record-only update reruns only
record-sensitive repository, generation, memory, and diff checks.

## Done Gate

P103 closes only when the conditional reflected first-passage object exists,
exact and independent numerical routes validate it, censoring and boundary
semantics are explicit, every BD5 predicate and consumer is adjudicated, claim
and release surfaces agree, campaign debt is empty, and the parent migration
advances. A near-minus-one fit or thirteen-check tally is not completion.

## Cross-References

This campaign cross-references BD1 through BD5, C-RG-001, C-RG-002,
C-COL-001, C-TH-001, C-TH-002, C-COH-001, C-COH-002, C-PRB-001, P079,
P086, P094, P099, P100, P102, and the canonical radial, thermal, coherence,
collective-coordinate, fixation-probability, and numerics modules.
