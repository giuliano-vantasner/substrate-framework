---
description: Derive and audit the BD2 conditional thermal rate family
author: vantasner
created: '2026-08-03T11:46:23Z'
updated: '2026-08-04T22:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- thermal-rate
- migration-BD2
category: proposals
confidence: exploratory
status: archived
---
# P100 BD2 Thermal Rate Audit

## Question and Positive Deliverable

P100 must deliver the strongest importable dependency-closed conditional
theorem behind BD2's composition of a capillary barrier, exact two-level gate,
declared coth effective scale, and dimensionful attempt frequency. It must
derive the exact temperature, loading, and drive behavior, determine whether a
fully declared response has a stationary operating point, compare alternative
prefactors and noise laws, preserve every free parameter and symbol role, and
terminally adjudicate every BD2 predicate.

The positive object is the proposed exact conditional claim C-TH-002 and its
pure APIs, not a physical medium-noise mechanism or fitted optimum. If the
source's advertised operating temperature fails its own formula, that failure
must be preserved while the correct conditional stationary theorem, model-
dependence ceiling, mutations, consumer replay, and source disposition are
completed.

## Base Release and Provenance

The accepted base is `v0.84.0` at parent commit
`c8bef91123bdac3b0cc8a0b7c3ca31d1527f8fe9`; the latest scientific transaction
is P099 at `bda89f264f27c8dd77ebcb6975ce99247e1da923`. The predecessor remains
pinned at `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, with later
dirty Phase 47/48 and synthesis artifacts excluded. BD2 is
`/home/dan/substrate/merged-framework/bridges/phase-28/bridge_BD2_scaling_law_thermal_optimum.py`,
10,677 bytes, SHA-256
`91f2344bd59618b5915d018e1ee7d728b86f59a29e42e1a0a60cd833747f7a65`,
and git blob `901b16a0c05e81da0867a6c19dbdce37df87d139`.

The generated queue marks BD2 pending, records sixteen literal checks with no
dynamic check or assert statement, and names BD1 as its candidate dependency.
The queue excerpt already exposes the normalized two-level gate, the
conditional BD1 barrier, the coth effective scale, the rate expression,
positive loading and drive statements, and an advertised optimum near the
energy quantum. The source body, imports, full predicates, numerical examples,
citations, runtime output, and additional consumer values remain unopened at
this freeze.

Direct accepted sources are release `v0.84.0`, C-TH-001, C-RG-001,
C-RG-002, C-COH-001, their canonical thermal, radial-energy, and coherence-gate
modules and tests, and their immutable campaign evidence. Durable recall adds
no accepted physical coth noise law, k-omega relation, Kramers process, or
operating-temperature theorem; every reused fact is verified at the registry,
module, or campaign source.

## Invariants, Conventions, and Allowed Imports

Use `tau` for positive line tension with dimension energy per length, `p` for
positive area drive with energy per area, `E` for a positive relative barrier,
`q` for a declared positive energy quantum, `vartheta=k_B*T_temp` for a
positive thermal-energy coordinate, `Theta` for a declared positive activation
scale, and `nu` for a positive attempt frequency. Line tension is never
thermodynamic temperature. Identifying `q` with any breather, medium, drive, or
barrier-curvature frequency requires a separate accepted claim.

C-TH-001 supplies only
`W(x)=sech(x/2)^2/2`. C-COH-001 supplies only the dimensionless factor
`exp(-E/Theta)` and expressly does not make it a rate. C-RG-001 gives
`E=pi*tau^2/p`, while C-RG-002 conditionally supplies the BD1 constitutive
specialization and no thermal or frequency law. A dimensionful rate therefore
requires the separately declared frequency `nu`; a stochastic interpretation
requires additional dynamics not imported here.

For the candidate coth family, declare
`x=q/vartheta`, `u=tanh(x/2)` in `(0,1)`, and
`Theta_coth=q/(2*u)`. The exact gate is `(1-u^2)/2`. Eliminating `tau/p`
through the capillary barrier turns the source-style rate into
`nu*sqrt(E/(pi*Theta_coth))*exp(-E/Theta_coth)*W`, so its dimensionless
temperature shape is proportional to
`sqrt(u)*(1-u^2)*exp(-2*b*u)` for `b=E/q>0`.

## Candidate Preregistration

The candidates are frozen before BD2 execution, source-body inspection,
cited-source inspection, numerical examples, or additional consumer output.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal reproduction | Pinned source environment | Source symbols and literals | A tally proves only its implemented predicates | Hash, AST, process, output, predicate ledger |
| B | Exact gate replay | C-TH-001 only | x | Wholly duplicate normalized gate | API and claim collision audit |
| C | Conditional coth-gated rate | Positive q, vartheta, E, and supplied nu | q,vartheta,E,nu | A dimensionful conditional response, not a physical escape law | Identities, units, domains, limits, coefficient mutations |
| D | Capillary elimination | C-RG-001 or C-RG-002 barrier | tau,p or constitutive inputs | The line/drive prefactor collapses to the same barrier ratio | Exact substitution and dimension ledger |
| E | Source-prefactor optimum | Prefactor proportional to Theta^-1/2 | b=E/q | One exact interior maximum with an implicit, bounded root | Strict log-concavity, endpoint limits, stationary polynomial |
| F | Prefactor/noise alternatives | Separately declared admissible families | exponent and noise-map inputs | The existence and location of a finite optimum are model dependent | Countermodels, limits, and root classification |
| G | Loading and drive partials | Fixed q, gate, nu, and other named inputs | BD1 inputs | Loading and k partials can be signed only under the frozen convention | Exact partials and total-derivative counterfamilies |
| H | Identifiability classes | One response curve or point | free scales and constitutive inputs | Multiple parameter orbits preserve the observed rate | Rank/nullspace and arbitrary-target constructions |
| I | Consumer/nonduplication audit | Governed downstream role | none | Pending consumers cannot supply missing dynamics or broaden the theorem | Hashes, dependency trace, registry/API comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; separation of gate,
activated factor, rate, stochastic process, objective, and physical operating
point; exact dimensions and symbol roles; positivity domains, limits,
stationary equations, global extrema, and mutation sensitivity; robustness to
alternative prefactors and noise laws; derivative discipline; identifiability;
parameter economy; canonical reuse; and consumer closure.

The queue has already exposed the main formulas, so formula blinding is not
claimed. P100 freezes the transformed response, the derivative equation
`1/(2*u)-2*u/(1-u^2)-2*b=0`, its strictly decreasing left side, and the
resulting unique root `0<u_*<1/sqrt(5)`. Because `u` decreases with
`vartheta`, the candidate source family predicts the exact lower bound
`vartheta_*>q/(2*atanh(1/sqrt(5)))`, approximately `1.039*q`; it cannot place
the optimum near `vartheta=q/2`. These tests, the constant-prefactor
countermodel, the fixed-q derivative convention, and the pending-dependency
ceiling are frozen before the body or output is opened.

## Proposed Claim Delta

P100 reserves collision-free identifier C-TH-002. Repository-wide registry,
campaign, proposal, durable-memory, module, and test searches found no prior
use. The proposed claim depends on C-TH-001, C-RG-001 or C-RG-002 as used, and
C-COH-001. It states only a conditional coth-gated rate identity, exact
stationary theorem for the declared inverse-square-root prefactor, alternative-
model ceiling, derivative convention, and identifiability limits. It neither
challenges nor supersedes an accepted claim.

Anticipated consumers are additions to `thermal.py`, focused package tests,
P100 primary and independent exact verifiers, governance, release/docs and
accepted memory if promoted, and later audited BD3-BD5, CM2, CM4, and
engineering surfaces. Pending consumers cannot convert the mathematical
maximum into an empirical operating recommendation.

## Implementation and Oracle Plan

Reusable pure functions will expose the declared coth scale, reduced gated
activation shape, conditional rate, stationary numerator, and general
prefactor-exponent family. Existing C-TH-001, C-RG-001/C-RG-002, and C-COH-001
functions remain canonical for their owned pieces. Imports execute no checks,
choose no numerical constants, and make no medium identification.

SymPy is the strongest oracle for hyperbolic substitutions, capillary
elimination, units, limits, exact derivatives, strict monotonicity of the log
derivative, unique-root bracketing, partial derivatives, rank/nullspaces, and
counterfamilies. The primary verifier calls canonical APIs. An independent
route differentiates directly in `u` and rederives the capillary elimination
without importing the new composition helpers. High-precision root finding,
if used to illustrate a declared barrier ratio after the exact theorem closes,
is numeric evidence only and must check solver status, precision convergence,
and the exact residual; it cannot select the theorem or optimum label.

Mutations drop the factors two or pi, confuse line tension with temperature,
replace the normalized gate by one, reverse the coth/tanh relation, omit the
attempt frequency, change the prefactor exponent, replace the noise law, bind
`q` to `k` without a declared map, hard-code an expected optimum, or treat a
partial derivative as a total derivative. The constant-prefactor family gives
`(1-u^2)*exp(-2*b*u)`, which is strictly decreasing in `u` and hence strictly
increasing with temperature toward a finite plateau; this exact countermodel
removes the finite optimum without violating dimensions when its amplitude is
supplied independently.

No quadrature, ODE, PDE, NumPy, or SciPy solver is needed for the exact P100
claim. Exact campaign and canonical work must contain no NumPy integration
alias. Focused replay covers thermal, radial-energy, coherence-gate, P005,
P006, P086, P099, and affected source consumers after their hashes and
authority are audited. One integrated workflow gate runs at the final
scientific promotion boundary; later record closure receives only targeted
record-sensitive validation.

## Attempts and Continuation

Every source, representation, import, stationary-point, dimension, or verifier
failure is append-only. A false advertised optimum is preserved as attempt
evidence while the corrected conditional theorem continues. A missing physical
noise or kinetic model qualifies the source interpretation but does not end the
campaign; P100 continues through the exact rate-family deliverable, terminal
predicate audit, consumers, and debt closure.

## Debt Ledger

P100 tracks the source hash and blob, every check and import, line-tension and
temperature notation, energy quantum, thermal coordinate, effective-scale
premise, gate normalization, capillary barrier, rate prefactor and units,
stochastic interpretation, objective and operating domain, stationary root,
limits, alternative prefactors and noise laws, loading and drive derivative
conventions, k-omega independence, identifiability, numerical examples,
pending BD3-BD5/CM2/CM4 and engineering consumers, nonduplication, claim
review, generated state, source disposition, and parent continuation. Every
item must be derived, declared, rejected, or excluded before closure.

## Review and Promotion Plan

The proposed claim C-TH-002 receives its own independent claim review.
Acceptance requires primary and independent exact routes, sensitive mutations,
complete dimensions and parameter ledgers, canonical APIs/tests, alternative-
model counterexamples, affected-consumer replay, and explicit exclusion of a
physical noise, dispersion, or Kramers mechanism. Promotion updates the
registry, a pinned release, generated docs and accepted memory, while BD2
receives a terminal qualified disposition if its conditional composition
survives but its derived physical optimum does not. Each of sixteen source
predicates and every named import receives a durable verdict. One integrated
workflow gate runs at the final scientific boundary; later record closure uses
targeted checks only.

## Done Gate

P100 closes only when the positive conditional rate-family theorem exists,
the exact stationary root and model-dependence ceiling are verified, dimensions
and consumers close, primary and independent oracles are mutation sensitive,
every BD2 predicate and dependency is terminally adjudicated, generated state
agrees, and campaign debt is empty. A reproduced gate, terminal tally, false
source optimum, or missing physical mechanism is not completion.

## Cross-References

This campaign cross-references BD1-BD5, CM2, CM4, C-TH-001, C-RG-001,
C-RG-002, C-COH-001, P005, P006, P086, P099, and the canonical thermal,
radial-energy, and coherence-gate modules.

## Terminal Adjudication

P100 accepts C-TH-002 and qualifies BD2. The source reproduces all sixteen
checks, while the primary canonical route passes 41 checks, the independent
route passes 21, and 55 focused thermal, coherence, and radial-energy tests
pass. The promoted result is the exact declared coth-gated conditional
response, its unique source-prefactor maximum above `1.039*q`, its
prefactor-dependent optimum ceiling, exact sign regimes, and scale
non-identifiability.

The source's `q/2` point is a convention rather than the full-rate optimum.
Its loading and fixed-q wavenumber signs reverse at `E/Theta=1/2`, a declared
`q(k)` map can reverse the total derivative, and a constant prefactor removes
the finite maximum. Rungs 056, 096, and 097 supply no accepted bath or mode
authority. BD3-BD5, CM2, and CM4 remain pending. The DBD pipeline consumers
fail on version-specific `np.trapz`; canonical P100 code imports no NumPy or
quadrature. Claim debt is empty and migration continues to BD3.
