---
description: Derive and audit the BD1 conditional capillary constitutive map
author: vantasner
created: '2026-08-04T18:30:00Z'
updated: '2026-08-04T18:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- capillary-barrier
- migration-BD1
category: proposals
confidence: exploratory
status: active
---
# P099 BD1 Capillary Constitutive Map

## Question and Positive Deliverable

P099 must deliver an importable exact conditional composition from positive
Frank/core line-tension inputs and a declared quadratic loading law to the
C-RG-001 critical radius and barrier. It must retain every free parameter,
dimension convention, monotonicity, and identifiability symmetry, keep line
tension distinct from thermodynamic temperature, determine whether alternative
drive laws fit equally naturally, and terminally adjudicate every BD1 claim.

The requested positive object is `C-RG-002`, a typed constitutive ledger and
not a material prediction. Failure of BD1's sourced interpretation does not
complete the campaign; the strongest dependency-closed conditional theorem,
its APIs, mutations, consumer replay, and source disposition must all exist.

## Base Release and Provenance

The accepted base is `v0.83.0` at parent commit `6277786`; the latest
scientific transaction is P098 at `8ad0ed8`. The predecessor remains pinned at
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, with later dirty Phase
47/48 and synthesis artifacts excluded. BD1 is
`/home/dan/substrate/merged-framework/bridges/phase-28/bridge_BD1_real_variable_barrier.py`,
10,653 bytes, SHA-256
`42579012eda87243639248664c6f90945c454046aa66c8de166ad6d2e594abc7`,
and git blob `df313ad5586ce3288cf6f7b46a319c7426f7c9b0`.

The generated queue marks BD1 pending, records eighteen literal checks and no
assert statement, and names B1, BD4, E1, and E2 as candidate dependencies.
All four remain pending and are not accepted imports. The queue excerpt already
exposes the generic capillary maximum and the candidate substitutions
`T_line=pi*K_F*s^2*log(R_o/r_c)+epsilon_core` and
`P_drive=g*A^2*k^2*l_m/2`. The source body, runtime output, full predicate
logic, citations, literals, and additional consumer outputs remain unopened at
this freeze.

Direct accepted sources are release `v0.83.0`, C-RG-001, the canonical radial
energy API and tests, and P006's immutable evidence. P086 independently
recorded that C-RG-001 supplies only a declared capillary maximum and that BD1
was pending. Memory recall adds no accepted constitutive or material theorem;
every reused fact is verified at its registry, module, or campaign source.

## Invariants, Conventions, and Allowed Imports

Use `tau` or `T_line` for positive line tension with dimension energy per
length, `p` or `P_drive` for positive area drive with energy per area, `R` for
positive length, and `E_barrier` for energy. Thermodynamic temperature is a
separate symbol and does not enter BD1's exact capillary substitution.
C-RG-001 fixes
`E(R)=2*pi*R*tau-pi*R^2*p+E_core`, its unique strict maximum
`R_*=tau/p`, and coefficient independence. P099 may compose those exact APIs
but may not relabel the generic result as new.

The candidate Frank/core ledger takes a Frank constant with energy-per-length
dimension, real dimensionless defect strength, ordered positive cutoffs
`R_o>r_c`, and positive core line energy. Its logarithm is dimensionless. The
candidate drive ledger takes positive thickness, nonzero real amplitude and
wavenumber, and positive coupling under the declared quadratic law
`h=g*A^2*k^2/4`, `p=2*h*l_m`. The law itself is a premise.

To prevent a hidden amplitude convention, let `[A]=L^alpha` and `[k]=L^-1`.
Dimensional closure requires `[g]=E*L^(-1-2*alpha)`, which makes
`[h]=E*L^-3`, `[p]=E*L^-2`, `[R_*]=L`, and `[E_barrier]=E` for every declared
real `alpha`. No dimension argument selects `alpha`, `g`, a material, or any
parameter value.

## Candidate Preregistration

The candidates are frozen before BD1 execution, body inspection, cited-source
inspection, or additional consumer output.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal reproduction | Pinned source environment | Source symbols | Tally proves only implemented predicates | Hash, AST, process, output, predicate ledger |
| B | Generic capillary replay | C-RG-001 positivity | tau, p, core | Exact but wholly duplicate | API and claim collision audit |
| C | Conditional constitutive composition | Frank/core ledger and quadratic drive premise | K_F,s,R_o,r_c,eps,g,A,k,l_m | Exact positive radius and barrier with every factor retained | Substitution, units, coefficient mutations |
| D | Amplitude-dimension family | A has length exponent alpha | alpha | Coupling dimension changes with convention; observables remain closed | Dimension matrix and symbolic exponent cancellation |
| E | Sensitivity ledger | Positive domain and fixed-variable partials | same inputs | Constant elasticities only for tau,g,A,k,l_m; composite inputs are state dependent | Exact derivatives and limits |
| F | Identifiability classes | One barrier/radius observation | positive rescaling factors | Multiple parameter orbits preserve outputs | Jacobian rank/nullspace and constructive families |
| G | Domain alternatives | Positive, zero, or negative p | sign/domain inputs | Only p>0 gives a finite strict maximum | Exact derivative and limiting cases |
| H | Alternative drive laws | Any positive h(A,k) | alternative exponents/functions | Capillary algebra composes but cannot select the quadratic source law | Countermodels with equal dimensions and different scaling |
| I | Consumer/nonduplication audit | Governed downstream role | none | BD2-BD4 cannot promote BD1 premises or erase free inputs | Hashes, dependency trace, registry/API comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted capillary closure, symbol and dimension
consistency, complete assumption/parameter ledger, correct extrema and domains,
mutation sensitivity, identifiability rank and counterfamilies, alternative-law
comparison, parameter economy, canonical reuse, and consumer closure. A source
tally, sourced prose, or later rate-law agreement cannot select the quadratic
constitutive ansatz.

The queue already exposed the main substitutions, so formula blinding is not
claimed. P099 freezes the still-load-bearing dimension family, positive and
wrong-sign domains, identifiability symmetries, alternative-law criterion,
source-import ceiling, and consumer gate before opening the body or output.

## Proposed Claim Delta

P099 reserves collision-free identifier `C-RG-002`. Repository-wide registry,
campaign, proposal, durable-memory, module, and test searches found no prior
use. The proposed claim depends only on C-RG-001 and states a conditional
constitutive composition, dimension family, sensitivities, and
non-identifiability ceiling. It neither challenges nor supersedes C-RG-001.

Anticipated consumers are extensions to `radial_energy.py`, package exports if
needed, focused tests, P099 exact and independent verifiers, governance,
release/docs/accepted memory if promoted, and later audited BD2-BD4 units.
Pending consumers cannot broaden the claim or select its premises.

## Implementation and Oracle Plan

Reusable pure functions will expose the Frank/core line tension, quadratic
loading area drive, capillary barrier height, composed result record,
dimension-exponent ledger, and exact elasticity or identifiability surfaces.
Existing C-RG-001 functions remain the canonical generic energy and critical
radius. Imports execute no checks and select no numerical constants.

SymPy is the strongest oracle for substitution, dimensions, derivatives,
limits, Hessian sign, log elasticities, Jacobian rank/nullspace, arbitrary-
target families, and alternative drive laws. The primary verifier calls the
canonical APIs. An independent route completes the square and eliminates
variables without importing the new constitutive functions. Mutations drop
factors two or pi, swap line tension with temperature, remove the squared
amplitude or wavenumber, reverse cutoff ratios, set zero/negative drive, change
the amplitude convention without changing g, and pretend one barrier
identifies all inputs.

No numerical solver or quadrature is needed. Exact P099 work must contain no
NumPy dependency or integration alias. Focused replay covers radial energy,
coherence gates that accept a generic barrier, dimensional utilities, and
later BD consumer surfaces only after their hashes and authority are audited.

## Attempts and Continuation

Every source, representation, dimension, import, or verifier failure is
append-only. A dimensionally incomplete source convention is repaired to the
general `alpha` family; an unsupported material reading is qualified while the
positive conditional composition continues. If the quadratic drive law fails
natural-fit comparison, P099 retains it only as a declared specialization and
does not rewrite C-RG-001.

The first contract-validation attempt on 2026-08-04 failed because the review
section began with the code-formatted claim identifier, which the memory
schema does not accept as plain prose. Repository validation and diff hygiene
passed. The repair changes only the review section's opening grammar and then
replays the targeted contract validators before any source exposure.

## Debt Ledger

P099 tracks source hash and blob, every check and import, capillary domain,
line-tension versus temperature notation, Frank/core dimensions, cutoff order,
drive-pressure units, amplitude convention, coupling dimension, every factor
two and pi, critical radius and barrier, derivatives, limits, log
elasticities, alternative laws, identifiability rank and counterfamilies,
pending dependencies, BD2-BD4 and engineering consumers, nonduplication,
claim review, generated state, source disposition, and parent continuation.
Every item must be derived, declared, rejected, or excluded before closure.

## Review and Promotion Plan

The proposed claim C-RG-002 receives its own independent claim review.
Acceptance requires
exact primary and independent routes, sensitive mutations, complete dimensions
and parameter ledger, canonical APIs/tests, affected-consumer replay, and no
material or rate-law overreach. Promotion updates the registry, a pinned
release, generated docs and accepted memory, while BD1 receives a terminal
qualified disposition if its exact composition survives but its sourced
physical reading does not. Each of eighteen source predicates and every named
import receives a durable verdict. One integrated workflow gate runs at the
final scientific boundary; later record closure uses targeted checks only.

## Done Gate

P099 closes only when the positive conditional constitutive ledger exists,
dimensions and consumers close, primary and independent exact oracles are
mutation sensitive, every BD1 predicate and cited dependency is terminally
adjudicated, generated state agrees, and campaign debt is empty. A reproduced
barrier formula, generic C-RG-001 replay, or unsupported material map is not
completion.

## Cross-References

See BD1-BD4, B1, E1, E2, C-RG-001, P006, P086, the radial-energy and
coherence-gate APIs, and the parent framework-migration effort.
