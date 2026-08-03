---
description: Audit E3's conditional energy difference and physical nuclear-yield interpretation
author: vantasner
created: '2026-08-07T16:00:00Z'
updated: '2026-08-07T16:30:00Z'
tags:
- substrate-framework
- campaign-proposal
- rational-map
- energy-difference
- migration-E3
category: proposals
confidence: exploratory
status: active
---
# P106 E3 Conditional Energy-Difference Audit

## Question and Positive Deliverable

P106 must deliver an exact and independently rederived ledger for the signed
linear combination formed from accepted E2 stationary-branch coefficients,
including its normalization, multiplicity, sign, inverse, limiting cases,
uncertainty propagation, and mutations. It must determine whether that ledger
is a distinct framework claim or a direct composition already owned by
C-RPROF-002 and dimensional-coordinate claims.

Completion also requires a terminal E3 adjudication that separates a
dimensionless reduced-model difference from a physical mass, binding energy,
deuteron or helium state, reaction channel, empirical energy, deposited yield,
or overbinding prediction. Reproducing E3's five checks or advertised decimal
does not complete this campaign.

## Base Release and Provenance

The accepted base is release `v0.89.0` at parent checkpoint
`0a2805732df5c6db701f71311f04fb9be553aa96`; the scientific transaction is
P105 at `f28cf74e646fc1eaca0a2593520b8b22d91cc526`. Source evidence remains
pinned to `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`.
Unrelated dirty Phase 47/48 work and the explicit external NumPy compatibility
overlay remain outside scientific authority.

E3 is
`/home/dan/substrate/merged-framework/bridges/phase-29/bridge_E3_yield_coefficient_overbinding.py`,
13,377 bytes, SHA-256
`aa76b9e675d4fbb45594e9d3df5107af175e927a24840260ca71ffda1bad3315`,
and git blob `cecea225e4735cfbb393389a23903b4eeab4286c`. It matches the pinned
commit. The generated queue marks E3 pending, names E2, E4, HE4, M1, NY1, and
NY2 as candidate dependencies, and records five literal checks. E2 is
qualified through C-RPROF-001/002; HE4 is qualified only through unrelated
sine-Gordon claims; NY1 and NY2 are duplicate evidence for C-SK-001; E4 and M1
remain pending. Only accepted registry claims may enter as authority.

The queue synopsis exposes E3's formula `3*pi^2*(2*b(2)-b(4))`, its advertised
coefficient near 8.4, empirical 23.86 MeV comparison, and factor-near-nine
overbinding narrative. P105's consumer audit already exposes that E3 composes
the accepted B=2 and B=4 branch values and calls the result a D+D yield
coefficient. P106 therefore claims no comparator blinding. It has not opened
or executed E3's source body or inspected its five predicates.

Authority recall read v0.89.0, C-RPROF-001/002, C-RMAP-001/002, C-SK-001,
C-DIM-002/003, P105's consumer audit, P084/P085's NY1/NY2 adjudications, and
the parent effort. Memory search located the P104/P105 rational-map reviews and
P085 coefficient audit; every reused fact was checked at the registry,
campaign, queue, or source metadata. Collision search found no accepted or
reserved C-RDIFF-001, C-RCOMB-001, or P106 identifier. P106 reserves no claim
identifier before nonduplication.

## Invariants, Conventions, and Allowed Imports

Let `b_i` and `b_f` be real dimensionless reduced-model coefficients, `n` an
exact multiplicity, `alpha` a declared dimensionless normalization, and `U` a
positive energy scale. If, and only if, one separately declares
`M_i=alpha*b_i*U`, `M_f=alpha*b_f*U`, and `Q=n*M_i-M_f`, elementary algebra
gives `Q/U=alpha*(n*b_i-b_f)`. Its sign is the sign of
`alpha*(n*b_i-b_f)`; for positive `alpha` it is the sign of
`n*b_i-b_f`. Neither dimensions nor this identity supplies the mass premise,
the identities of the states, the reaction channel, or the scale.

For independent intervals `b_i in [l_i,u_i]` and `b_f in [l_f,u_f]`, positive
`alpha`, and nonnegative `n`, monotonicity gives the sharp rectangular bound
`alpha*(n*l_i-u_f) <= kappa <= alpha*(n*u_i-l_f)`. A method-to-method spread
may support a transparent sensitivity interval but is not automatically a
statistical confidence interval or rigorous discretization enclosure.

C-RPROF-002's B=2 and B=4 values are resolution-bounded stationary-branch
coefficients, not proven minima or physical masses. A claimed upper bound
`x<=X` and another `y<=Y` does not order `x-y` against `X-Y`; explicit
counterexamples must guard any attempted variational-bound interpretation.
C-SK-001 remains a conditional ratio from supplied premises and supplies no
physical electron value, pion constant, coupling, or nuclear scale by itself.

Exact P106 work uses no sampled integration. If any post-freeze immutable
source path aborts only because `np.trapz` is absent, P106 records an alias-only
replay before adjudication. Mutable new work uses `np.trapezoid`, while
canonical sampled integration would use `trapezoid_integral`.

## Candidate Preregistration

The candidate set is frozen before E3's body, predicate implementation, or
terminal output is opened.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal E3 promotion | Every imported normalization, state, scale, and reaction premise is accepted | Source literals | Fails if any physical dependency is absent | Registry closure, AST ledger, and predicate-by-predicate audit |
| B | Direct coefficient algebra | Declared real coefficients and normalization | `alpha,n,b_i,b_f` | Exact signed combination with free premises visible | SymPy derivation, inverse, sign, zero limit, and factor or multiplicity mutations |
| C | Independent mass/binding ledger | Declared masses and one consistent subtraction convention | Same symbols plus `U` | Agrees with B only after all declarations are explicit | Fresh derivation from masses and binding cancellations without importing P106 helpers |
| D | Resolution-bounded specialization | Accepted C-RPROF-002 decimals and declared error envelopes | Interval endpoints | Combination retains numeric evidence status | Directed interval endpoints, method-spread sensitivity, and decimal mutations |
| E | Difference-of-bounds reading | Separate upper bounds on two energies | Bounds and unknown slacks | Signed difference is generally uncontrolled | Exact counterexamples with either ordering and zero-slack limit |
| F | Physical yield interpretation | Action normalization, state map, corrections, reaction, and deposition are accepted | Physical inputs | No physical conclusion if any input is missing | Dependency and consumer closure independent of decimal proximity |
| G | Nonduplication | A distinct theorem, API, or accepted consumer exists | None | Direct composition may require no new claim | Registry, canonical API, and downstream comparison |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit action
normalization, state map, multiplicity, and reaction convention; exact algebra,
units, signs, cancellation, limits, interval propagation, and mutation
sensitivity; preservation of resolution-bounded status; rejection of
difference-of-upper-bounds inference; assumption economy; nonduplication; and
complete consumer classification. Empirical 23.86 MeV proximity or mismatch
cannot select a coefficient, normalization, model, or candidate.

No comparator blinding remains because the generated queue and prior consumer
audit expose the formula and advertised values. P106 freezes every decisive
structural test and interpretation ceiling before body inspection or source
execution.

## Proposed Claim Delta

P106 froze with no proposed claim. Candidate G then found no accepted registry
statement for the signed mass/binding identity or its interval propagation,
while E4, KI2--KI5, MK5, MR2, and MR5 reuse the combination and several retain
E3's biased 8.46 anchor or promote it to a ceiling. Recorded proposal revision
0001 therefore reserves two claims before package implementation.

`C-RDIFF-001` may state the exact conditional theorem
`Q=n*M_A-M_(nA)=B_E(nA)-n*B_E(A)=alpha*U*(n*b_A-b_(nA))`, its scale-free
coefficient, inverse, sign and zero surfaces, sharp rectangular interval
propagation for positive normalization, and the countertheorem that separate
upper bounds do not order their signed difference without a slack relation.
Every mass normalization, multiplicity, coefficient, scale, and binding
definition remains an explicit premise.

`C-RDIFF-002` may record the separately reviewed resolution-bounded
specialization of C-RDIFF-001 to C-RPROF-002's B=2 and B=4 stationary-branch
coefficients and declared `alpha=3*pi^2`. The canonical composition is about
8.4824173188 and the independent P105 route about 8.4824148688; a rectangular
two-method sensitivity envelope is not a confidence interval or rigorous error
bound. This claim remains a conditional reduced-model coordinate and names no
physical mass, state, reaction, or yield.

C-RPROF-001/002, C-SK-001, C-DIM-002/003, and C-RMAP-001/002 are reviewed but
not challenged or superseded. No physical mass map, binding hierarchy,
deuteron, helium, reaction, empirical scale, quantum correction, BPS model,
generalized-model interpolation, engine literal, or observation may enter an
accepted claim in P106.

## Implementation and Oracle Plan

SymPy is the strongest oracle for the exact direct coefficient, independent
mass-ledger reduction, common one-body cancellation, inverse, sign and zero
surfaces, factor or multiplicity mutations, and counterexamples to subtracting
upper bounds. Decimal or explicit interval endpoints are appropriate for
propagating C-RPROF-002's resolution-bounded inputs without implying exactness.
No ODE, BVP, PDE, quadrature, or new solver rerun is warranted because P106
does not change the accepted branch evidence.

The primary verifier will derive expressions from symbols rather than compare
copied literals. It will import accepted branch values from a durable P105
snapshot or canonical evidence API if one exists, never from E3. Mutations
change `3*pi^2`, multiplicity two, subtraction sign, B=2 or B=4 coefficient,
and scale; the relevant verdict must fail or shift. Counterexamples will show
that separate upper bounds do not bound their difference. The independent
review will rebuild the mass and binding ledger from fresh symbols without
importing primary expressions.

Post-freeze work pins and executes E3, inventories imports and literal checks,
adjudicates each predicate, traces E4, HE4, M1, NY1, NY2 and narrative
consumers, and compares the surviving surface with accepted claims and APIs.
Proposal revision 0001 records Candidate G's positive nonduplication result. A
minimal pure `energy_differences.py` module will own only the normalized linear
difference, scaled coefficient, and monotone interval transformation; it will
not own E3's physical vocabulary, empirical literals, or profile solves. The
campaign verifiers call that API for regression after their independent exact
derivations. Targeted checks, repository schema, generated queue and memory
checks, one full workflow at the terminal boundary, and `git diff --check`
close the campaign.

## Attempts and Continuation

Every source reproduction, algebra, interval, bound, normalization,
dependency, state-map, reaction, comparator, nonduplication, consumer, or
verifier failure is recorded append-only with its command, mechanism, and next
materially different route. Missing physical premises reject that candidate
but do not end the required exact ledger and terminal E3 adjudication.

## Debt Ledger

P106 tracks source hash and execution, every predicate, coefficient
normalization, multiplicity, branch-number convention, numeric provenance,
input error envelope, scale, mass map, binding convention, state assignment,
variational status, quantum correction, reaction and deposition channel,
empirical comparator, downstream consumer, nonduplication, disposition,
generated state, and parent continuation. Each item must be derived, declared,
rejected, or excluded before closure.

## Review and Promotion Plan

The primary and independent exact routes, source reproduction and AST audit,
dependency and consumer ledgers, interval sensitivity, bound counterexamples,
candidate comparison, and impact analysis must agree. Each surviving claim, if
any, receives an individual four-axis review and importable implementation.
Otherwise E3 receives a terminal disposition against existing accepted claims
without a release or package ceremony. Generated queue and memory state are
synchronized, then the unchanged or promoted boundary runs once. A final
attempt is created in progress before that gate and finalized afterward with
only record-sensitive validation repeated.

## Done Gate

P106 closes only when the exact conditional combination and independent
binding ledger exist, accepted numeric inputs retain honest error status,
difference-of-bounds and physical-interpretation pitfalls have explicit
counterexamples, every E3 predicate and consumer is adjudicated, nonduplication
is resolved, canonical records agree, campaign debt is empty, and the parent
migration advances. A five-check tally, an 8.4 coefficient, an empirical
mismatch, or a well-documented missing mass map is not completion alone.

## Cross-References

This campaign cross-references E2 through E5, HE4, M1, NY1, NY2,
C-RPROF-001, C-RPROF-002, C-RMAP-001, C-RMAP-002, C-SK-001, C-DIM-002,
C-DIM-003, P084, P085, P104, P105, and the framework-migration effort.
