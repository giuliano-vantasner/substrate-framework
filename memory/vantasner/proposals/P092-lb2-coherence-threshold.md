---
description: Separate LB2's damped-oscillator threshold from nonlinear coherence claims
author: vantasner
created: '2026-08-04T08:30:00Z'
updated: '2026-08-04T08:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- damped-oscillator
- migration-LB2
category: proposals
confidence: exploratory
status: active
---
# P092 LB2 Coherence Threshold Audit

## Question and Positive Deliverable

P092 must determine which parts of LB2 are exact properties of a declared
damped harmonic oscillator, which follow from the normalized damped
sine-Gordon linearization, and which overreach into nonlinear breather
existence, coherence survival, spark/DBD selection, or physical medium
thresholds. The positive deliverable is an exact characteristic-root,
solution-branch, energy/amplitude, damped-period, cycle-count, field-mode,
periodic-existence, units, dependency, consumer, and nonduplication
classification; importable promotion of any distinct surviving object; and a
terminal LB2 disposition.

## Base Release and Provenance

The accepted base is `v0.78.0` at parent commit `90170bf`; the latest scientific
adjudication is P091 at commit `6c444a6`. The predecessor is pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. LB2 is
`/home/dan/substrate/merged-framework/bridges/phase-26/bridge_LB2_coherence_threshold.py`,
12,157 bytes, with SHA-256
`ae159aee3c076c1f86d77628a6bbbf206ad7e28dccd832e397250b71a981b28d`
and git blob `f5f0283886e686722bf9a10dce9172cd285b680d`.

The generated queue marks LB2 pending, records seventeen literal checks, and
names LB1, pending MC3, and qualified-without-claim SA2 as candidate
dependencies. Its synopsis advertises a damped-SHO premise, critical boundary
`Gamma=2*omega_b`, no coherent breather above that boundary, and nominal cycle
count `omega_b/(2*pi*Gamma)`. P091's preregistered consumer audit necessarily
opened the complete LB2 implementation, so P092 records full source-body
exposure rather than claiming fresh blinding. LB2 has not yet been executed in
P092, its output is unopened, and additional downstream consumer bodies and
physical comparator values remain closed until the freeze.

Direct accepted sources are the current release, C-SG-001, C-SG-011,
C-SG-012, C-SG-016, their canonical modules and tests, and the P048/P091
campaign evidence. Memory search recovered only P091 and the parent
continuation; every reused formula is rechecked at the registry, package, or
immutable campaign source. The predecessor worktree's later dirty artifacts
remain excluded.

## Invariants, Conventions, and Allowed Imports

C-SG-001 fixes the normalized nonlinear equation and undamped breather family.
C-SG-011 fixes its small-amplitude limit as massive Klein-Gordon with mass gap
one. C-SG-012 gives the exact energy balance, and C-SG-016 gives the exact
undamped-family form factor plus a qualified slow-damping action law. None
supplies a material Gamma, survival probability, nonlinear sharp existence
threshold, or spark/DBD selector.

For an abstract oscillator `q''+Gamma*q'+Omega^2*q=0` with positive `Omega`
and nonnegative Gamma, the discriminant classifies its roots. In the
underdamped regime the damped angular frequency is
`omega_d=sqrt(Omega^2-Gamma^2/4)` and the amplitude envelope is
`exp(-Gamma*t/2)`. Exact mechanical energy obeys
`dE/dt=-Gamma*qdot^2`; it is not pointwise `-Gamma*E`. Actual oscillation cycles
inside a declared window use `omega_d`, whereas replacing it by `Omega` is a
weak-damping nominal convention.

The normalized damped sine-Gordon linearization is
`psi_tt-psi_xx+psi=-Gamma*psi_t`. A Fourier mode has
`Omega_k=sqrt(1+k^2)>=1`, not an arbitrary sub-gap breather frequency. A
localized nonlinear breather is therefore not one real linear Fourier mode.
Separately, positive uniform damping with zero boundary flux forbids every
nontrivial exactly periodic finite-energy trajectory because the integrated
dissipation over a period must vanish. Exact periodic existence, underdamped
transient response, and a probabilistic survival gate remain distinct.

Pending MC3/LB3/LB4 and SA2 cannot be imported. Exact code uses no numerical
quadrature; any sampled work must use `trapezoid_integral` or a
claim-appropriate SciPy method rather than `np.trapz`.

## Candidate Preregistration

The candidates are frozen after unavoidable LB2 body exposure but before P092
execution, output, new consumer inspection, or comparator use.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal LB2 promotion | SHO premise equals nonlinear breather dynamics | Source premises | Fails if mode or observable semantics differ | Source, dependency, and consumer audit |
| B | Exact abstract damped SHO | Linear constant-coefficient ODE | Omega and Gamma | Exact roots and three damping regimes | Polynomial residual, branch domains, mutations |
| C | Observable-specific decay and cycles | Candidate B plus declared window | Initial data and time | Envelope, energy, and actual cycles differ | Exact solution, energy derivative, zero crossings |
| D | Linearized damped SG modes | C-SG-011 and Fourier mode | k and Gamma | Critical boundary is `2*sqrt(1+k^2)` | PDE substitution, gap and k mutations |
| E | No exact damped periodic orbit | Positive uniform damping and zero flux | Period | Only static periodic solutions survive | Period-integrated energy balance |
| F | Exact source countermodels | Candidates B-D | Source omega_b | Sub-gap frequency cannot label a real linear mode | Gap inequality and threshold counterexample |
| G | Nonlinear transient classifier | Declared finite-time observable | PDE data and threshold | Requires separate numerical evidence | Refinement, domain, method, and sensitivity |
| H | Physical threshold map | Accepted Gamma/Omega unit map | Material inputs | Absent unless independently derived | Units and constitutive consumer audit |
| I | Mutation-sensitive oracle | Every load-bearing convention affects a verdict | None | Wrong factors and observables fail | Sign, gap, k, period, and lifetime mutations |
| J | Consumers and nonduplication | Distinct API and governed use | None | Basic roots may merit generic dynamics API | Registry, package, LB3/LB4, engineering trace |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency and normalized-unit closure; exact
equations, roots, branches, signs, energy identity, mode frequency, and
observable semantics; separation of exact periodic existence from transient
oscillation and survival; correct zero-damping, critical, overdamped, gap,
long-wavelength, and weak-damping limits; mutation sensitivity; parameter
economy; nonduplication; and controlled numerical evidence only for genuinely
nonlinear finite-time claims.

Fresh LB2 blinding is impossible because P091 already opened it as a named
consumer. That exposure is fixed provenance, not a license to select thresholds
from output. Contracts and criteria freeze before execution, output, further
consumer bodies, or comparator values.

## Proposed Claim Delta

P092 provisionally reserves `C-DYN-001` for a distinct exact theorem combining
the declared damped-oscillator branch classification, observable-specific
energy/envelope/cycle semantics, normalized damped Klein-Gordon Fourier-mode
application, and the positive-damping exact-periodic ceiling. A repository-wide
registry, campaign, generated-document, package, test, and durable-memory
search found no prior or rejected use of `C-DYN-001`, `C-OSC-001`, or an
equivalent damped-oscillator API. The candidate depends on C-SG-011 and
C-SG-012 only for its field application; the abstract ODE portion is exact
algebra. It challenges and supersedes no accepted claim.

## Implementation and Oracle Plan

The likely canonical surface is a pure `damped_oscillator.py` module exposing
characteristic roots, regime, damped frequency, underdamped solution/envelope,
mechanical energy and derivative, nominal and damped cycle counts, and the
normalized sine-Gordon linear-mode frequency. SymPy is the primary oracle for
roots, ODE residuals, discriminants, limits, energy balance, Fourier-mode PDE
substitution, gap inequalities, cycle conventions, and the period-integrated
dissipation theorem. An independent route will reconstruct roots through a
first-order matrix spectrum and verify selected solutions without calling the
new helpers.

Mutations change the damping sign, coefficient, natural frequency, mass gap,
wavenumber, factor two, damped versus undamped period, energy versus amplitude
window, and sub-gap frequency label. Exact countermodels include
`Omega=1,Gamma=1.2,omega_b=0.5`, for which the normalized long-wavelength
linear mode is underdamped while LB2's substituted breather-frequency test is
overdamped, and the critical limit where the actual cycle count tends to zero
but the nominal count does not. Numerical PDE work is admitted only if a
well-defined nonlinear transient statement survives exact classification; no
simulation is planned merely to repeat the exact roots.

## Attempts and Continuation

The recall-stage `memory grep --limit` interface failure is preserved as the
first attempt after freeze; removing the unsupported option recovered the
relevant parent and P091 entries without changing scientific state. Further
source, representation, oracle, implementation, and consumer failures remain
append-only. A rejected nonlinear coherence threshold does not end P092: the
exact oscillator/mode/periodic-existence classification and terminal source
adjudication remain positive deliverables.

## Debt Ledger

P092 tracks the ODE, characteristic convention, root branches, Gamma and Omega
domains, solution initial data, amplitude envelope, exact mechanical energy,
cycle and period convention, quality-factor convention, critical limit,
linearized PDE, mass gap, Fourier sign, spatial wavenumber, localized versus
plane-wave semantics, exact periodicity, boundary flux, nonlinear transient
observable, physical units, survival/probability/population map, consumer, and
every accepted or pending dependency. Every item must be derived, declared,
rejected, or excluded before closure.

## Review and Promotion Plan

Claim-level review compares primary and independent exact routes, every source
predicate, mutations, candidate comparison, impact and consumer maps, and
nonduplication. A surviving `C-DYN-001` receives pure APIs and tests, four-axis
review, registry/release transaction, generated docs and memory, and a
qualified LB2 disposition preserving every nonlinear and physical remainder.

## Done Gate

P092 closes only when the positive oscillator/field-mode/periodic-existence/
observable classification exists, all seventeen source predicates have
individual verdicts, primary and independent mutation-sensitive routes pass,
consumers replay, campaign debt is empty, and the parent migration can
continue. An exact discriminant or terminal source tally is not sufficient.

## Cross-References

See LB2, LB1, LB3, LB4, MC3, SA2, P048, P091, C-SG-001, C-SG-011,
C-SG-012, C-SG-016, the canonical exact modules, and the parent migration
effort.
