---
description: Audit LB3 damped sine-Gordon ring-down numerics and nonduplication
author: vantasner
created: '2026-08-04T09:30:00Z'
updated: '2026-08-04T09:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- damped-sine-gordon
- migration-LB3
category: proposals
confidence: exploratory
status: active
---
# P093 LB3 Damped Sine-Gordon Ring-Down Audit

## Question and Positive Deliverable

P093 must determine whether LB3 adds a distinct, dependency-closed simulation
claim beyond accepted C-SG-016, or only reproduces its conditional damped-family
tracking with weaker core-energy, FFT, refinement, and high-damping semantics.
The positive deliverable is an exact scheme, control-volume energy, fit-window,
frequency-estimator, refinement, transient-classifier, dependency, consumer,
and nonduplication classification; promotion only of genuinely distinct
reusable content; and a terminal LB3 disposition.

## Base Release and Provenance

The accepted base is `v0.79.0` at parent commit `0c04650`; the latest
scientific adjudication is P092 at commit `f17091e`. The predecessor is pinned
at `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. LB3 is
`/home/dan/substrate/merged-framework/bridges/phase-26/bridge_LB3_damped_sg_ringdown.py`,
27,522 bytes, with SHA-256
`1b54ef5704fce1502464f44bd675c01824cfa48b6b98688b1df8f000d1030a2b`
and git blob `f4305bce529bc4dc0288ac364c64802cb6f08763`.

The generated queue marks LB3 pending, records eight runtime checks from two
literal and six dynamic sites, one assert statement, and candidate dependencies
LB1, LB2, MC3, P3D1, and SA3. The complete source body and declared numerical
values were necessarily exposed during earlier consumer audits. P093 therefore
claims no fresh source or value blinding. LB3 has not been executed under P093,
its terminal output remains unopened, and additional downstream consumer
outputs remain closed until the freeze.

Direct accepted sources are current release `v0.79.0`, C-SG-001, C-SG-002,
C-SG-012, C-SG-016, C-DYN-001, C-PDE-011, the canonical sine-Gordon, damped
oscillator, 1D solver, and numerical integration APIs, and P089/P091/P092
campaign evidence. Memory recall found the parent continuation and those
accepted reviews; every reused statement is verified at its registry, module,
or immutable campaign source. Pending MC3/LB4 and rejected LB2 physical
readings are not authority.

## Invariants, Conventions, and Allowed Imports

C-SG-001 and C-SG-002 fix the exact undamped normalized breather and full-space
energy. C-SG-012 fixes local energy conservation with explicit flux and bulk
loss. For a symmetric finite core `[-R,R]` under uniform damping,
`dE_R/dt=[phi_t*phi_x]_{-R}^{R}-Gamma*integral_{-R}^{R}phi_t^2 dx` in the
accepted sign convention. A fitted core-energy decay therefore mixes damping
with radiation through the diagnostic boundary unless that flux is measured or
shown negligible.

C-SG-016 fixes the exact family form factor and conditional phase-averaged law
`J(t)=J0*exp(-Gamma*t)` with nonlinear evolving energy and frequency. It already
contains total-energy PDE evidence at three meshes, a larger domain, DOP853, a
slower damping rate, a lossless control, and an energy ledger. LB3 may provide
regression at another initial frequency or longer time, but numerical proximity
cannot create a distinct claim or turn a window-average slope into a pointwise
instantaneous rate.

C-DYN-001 fixes that normalized real Fourier modes have natural frequency
`sqrt(1+k^2)>=1`, and that exact nontrivial periodic finite-energy fields are
excluded for every positive uniform damping value under zero integrated flux.
LB3's `Gamma>=2*omega_b` label is neither the accepted field-mode boundary nor
an exact nonlinear existence theorem. Finite-time sign changes and residual
core energy form an operational transient classifier only after its time,
threshold, core, and robustness conventions are declared.

The source recurrence matches the canonical centered-damping leapfrog before
its separate sponge update. The source's diagnostic integral chooses
`np.trapezoid` on current NumPy and falls back to the removed `np.trapz` name on
older NumPy. New framework code and evidence must call the shared
`trapezoid_integral` compatibility API; exact work uses no quadrature.

## Candidate Preregistration

The candidates are frozen before LB3 execution, terminal output, or additional
consumer outputs are opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal LB3 reproduction | Source code and environment | All source values | Tally reproduces but proves only implemented predicates | Hash, AST, process status, output, mutations |
| B | Canonical scheme equivalence | Same stencil, damping centering, and data | dx, dt, Gamma | Source recurrence duplicates existing solver before sponge | Algebraic update comparison and Gamma-zero limit |
| C | Finite-core balance | C-SG-012 and smooth data | R and boundary flux | Core slope includes flux as well as damping | Exact local balance and source diagnostic trace |
| D | Reduced-law window average | C-SG-016 adiabatic hypotheses | Initial action, Gamma, fit window | Log slope averages a drifting instantaneous rate | Exact endpoint/least-squares reduced-law comparison |
| E | Frequency-estimator audit | Sampled center trace | Window, cadence, estimator | FFT bin width and drift bound precision | Bin spacing, endpoint closure, alternate estimator |
| F | Distinct numerical convergence | Same PDE and classifier | dx, dt, domain, method, R, window | A new simulation claim needs independent refinements | One-at-a-time variations and energy ledger |
| G | High-damping transient | Declared operational classifier | Gamma, time, R, thresholds | Relaxation may occur but is not the LB2 field boundary | C-DYN countermodel and classifier sensitivity |
| H | Second-frequency regression | Accepted reduced law | omega0 and Gamma sweep | Likely supports but does not extend C-SG-016 | Claim/API collision and predictive-reach audit |
| I | Canonical implementation | Distinct reusable object exists | None | Copied solver/integral/form factor should not be promoted | Package and test search |
| J | Consumer and claim audit | Governed downstream role | None | Physical consumers inherit missing maps | Registry, LB4, lifetime, DBD, synthesis trace |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure, exact PDE/stencil/flux
and observable definitions, independent numerical refinement, load-bearing
mutation sensitivity, parameter economy, canonical reuse, and nonduplication.
Agreement with LB1 values or the source's terminal tally cannot select a claim.

Fresh source and numerical blinding is impossible because P091/P092 exposed the
complete body and configurations. That exposure is recorded rather than hidden.
Contracts, hashes, criteria, and countermodels still freeze before execution,
output, additional consumers, or any decision based on reported agreement.

## Proposed Claim Delta

P093 reserves no identifier. Repository-wide registry, campaign, memory,
package, and test searches show that C-SG-016 already governs the exact form
factor, evolving reduced law, and controlled damped-PDE tracking; C-DYN-001
governs the oscillator/field-mode and periodicity semantics; C-PDE-011 governs
the reusable solver and classifier machinery. A new claim is admissible only
if LB3 contains a distinct, independently refined statement with a governed
consumer. Otherwise LB3 maps existing claims and receives a qualified or
duplicate-evidence disposition.

## Implementation and Oracle Plan

SymPy or direct algebra is the strongest oracle for recurrence equivalence,
the finite-core balance, reduced-law instantaneous rate, endpoint-average
rate, critical-boundary countermodels, and mutations. Static AST analysis must
count the actual check sites, imports, local solver/form-factor definitions,
and chosen integration compatibility branch rather than trusting prose.

The unchanged source is the primary reproduction oracle for its numerical
output. Its equation is the normalized damped sine-Gordon PDE on `[-120,120]`
with exact phase-zero breather data, uniform Gamma, homogeneous endpoint field,
a quadratic edge sponge, centered spatial differences, semi-implicit damping,
`dt=0.4*dx`, core radius 14, fit window `[40,120]`, and float64 NumPy. P093 will
record every executed mesh, final time, fit, FFT resolution, tolerance, and
process status from the source. The source's own `dx` halving couples spatial
and temporal refinement and cannot be relabeled as independent timestep
evidence.

No new expensive PDE campaign is preregistered merely to repeat C-SG-016's
stronger accepted evidence. If source output reveals a distinct surviving
statement, Candidate F opens a separately recorded canonical run using
`evolve_bulk_driven_sine_gordon_leapfrog` and DOP853 with one-at-a-time mesh,
timestep, domain, method, core-radius, and window changes, total-energy and
control-volume ledgers, and the shared integration API. Otherwise accepted
P091 refinements are dependency replay, not a second claim.

Mutations change damping sign and magnitude, remove the sponge, move the core
boundary, change the fit window, replace `omega_d` by an FFT-bin frequency,
use total rather than core energy, vary the high-damping threshold, and remove
the accepted mass gap. The exact `Gamma=1.75`, `omega_b=0.7`, `k=0`
countermodel remains underdamped as a normalized field mode because
`1.75<2`, even though LB3 labels it overdamped via `2*omega_b=1.4`.

## Attempts and Continuation

Source execution, numerical, representation, integration, and classifier
failures remain append-only. A reproduced rate match is classified at its
actual finite-window and diagnostic scope. A failed high-damping interpretation
does not end P093; scheme, flux, estimator, nonduplication, and terminal source
classification remain positive deliverables.

## Debt Ledger

P093 tracks source hash and blob, equation, domain, endpoints, exact initial
phase, mesh, timestep, damping, sponge, core radius, total versus core energy,
control-volume flux, fit interval, log transformation, FFT cadence and bin
width, endpoint closure, current versus averaged frequency, family inversion,
form-factor evaluation, lossless control, second initial frequency, Gamma
sweep, spatial and temporal refinement, domain, method, solver status, energy
ledger, high-damping classifier, integration compatibility, physical units,
consumers, and every accepted or pending dependency. Every item must be
derived, declared, rejected, or excluded before closure.

## Review and Promotion Plan

Claim-level review compares source reproduction, exact scheme/flux/window
audits, source mutations, existing independent accepted evidence, candidate
comparison, impact and consumer maps, and nonduplication. Distinct surviving
content receives package extraction, tests, a four-axis review, release update,
generated docs, and accepted memory. Otherwise P093 changes no release and
records a terminal qualified or duplicate-evidence LB3 disposition with
durable evidence. The integrated workflow runs once only if executable,
scientific, governance, generated, or disposition state changes require it.

## Done Gate

P093 closes only when the positive scheme/flux/window/frequency/refinement/
transient/nonduplication classification exists, all source predicates have
individual verdicts, necessary source and mutation oracles pass, consumers
replay, campaign debt is empty, and the parent migration can continue. A
passing source tally or a failed over-damping interpretation is not completion.

## Cross-References

See LB3, LB1, LB2, LB4, MC3, P3D1, SA3, P089, P091, P092, C-SG-001,
C-SG-002, C-SG-012, C-SG-016, C-DYN-001, C-PDE-011, the canonical 1D solver
and numerical APIs, and the parent framework-migration effort.
