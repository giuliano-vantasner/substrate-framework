---
description: Audit E4's BPS bound, saturation, zero binding, and near-BPS interpretation
author: vantasner
created: '2026-08-03T16:16:02Z'
updated: '2026-08-07T18:00:00Z'
tags:
- substrate-framework
- campaign-proposal
- bps-bound
- topological-degree
- migration-E4
category: proposals
confidence: established
status: archived
---
# P107 E4 BPS Zero-Binding Audit

## Question and Positive Deliverable

P107 must deliver an exact, premise-explicit, and independently rederived
Bogomolny bound for the declared sextic-plus-potential energy, including the
signed degree normalization, target-space average, equality condition,
dimensions, and load-bearing sign and normalization mutations.

Completion also requires an exact theorem stating when sectorwise attainment
turns the bound into linear sector energy and zero signed binding, plus a
controlled near-BPS expansion whose coefficient and remainder remain visible.
E4 must be adjudicated predicate by predicate. A valid square completion, five
passing checks, or a formal `O(epsilon)` statement does not by itself prove a
saturating field in every degree, a physical state dictionary, or a numerical
small-binding mechanism.

## Base Release and Provenance

The accepted base is `v0.90.0` at parent checkpoint
`7dbe02f90b09c378e4a92ddb13542eda20753b09`; the latest scientific transaction
is P106 at `e0c2142`. Source evidence remains pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. The predecessor worktree's
unrelated Phase 47/48 work and explicit NumPy compatibility overlay are not
scientific authority.

E4 is
`/home/dan/substrate/merged-framework/bridges/phase-29/bridge_E4_bps_zero_binding_resolution.py`,
10,719 bytes, SHA-256
`f1815eefc73e577734992a3147d9ec6cea2b50fad8532e9f436e1afb465dfea7`,
and git blob `279bfb747a8663577d9f040df4cb6a822503c287`. It matches the pinned
commit. The queue marks E4 pending, names E2, E3, and M1 as candidate
dependencies, and records five literal checks. E2 and E3 are qualified through
accepted conditional mathematical claims; M1 remains pending and is an
unrelated Anderson-Higgs mass-matrix unit, so it is not an allowed import.

No source-body or comparator blinding remains. The generated queue exposes the
energy, square completion, target average, bound, BPS equation, asserted
sectorwise saturation, exact zero binding, and near-BPS story. P106's consumer
audit exposed E4's intended composition, while generated later-unit summaries
expose KI, MK, and MR uses and a normalization dispute. P107 has not executed
E4 or inspected its five predicate implementations. All decisive definitions,
routes, mutations, and interpretation ceilings are frozen first.

Authority recall read `v0.90.0`, C-DIM-002, C-RDIFF-001/002, the relevant
canonical modules and reviews, P106's dependency and consumer audits, the
generated E4 queue entry, and the parent effort. Memory search found no
accepted BPS claim. Repository-wide collision search found no P107 or
C-BPS-001 through C-BPS-003 identifier; those identifiers are reserved here.

## Invariants, Conventions, and Allowed Imports

Let the target be an oriented unit three-sphere with volume form `Omega` and
`integral Omega=2*pi^2`. For a sufficiently regular finite-energy map `U` from
compactified oriented physical space, define the signed normalized pullback
density by `U*Omega/(2*pi^2)=B0 d^3x`, so `integral B0 d^3x=B`, the integer
degree. Signed degree, absolute degree, a physical baryon number, and a nucleus
remain distinct without a separately accepted map.

Let `lambda,mu>0`, let `V>=0` be a declared dimensionless measurable target
potential with integrable square root, and define
`W=(1/(2*pi^2))*integral_target sqrt(V) Omega`. The declared energy is
`E[U]=integral[(lambda*pi^2*B0)^2+(mu*sqrt(V(U)))^2]d^3x`. When physical
coordinates carry length, `B0` has dimension `L^-3`, `lambda` has dimension
`E^(1/2)L^(3/2)`, `mu` has dimension `E^(1/2)L^(-3/2)`, and `lambda*mu`
has energy dimension. These are consistency conditions, not a derivation of
the couplings or action.

The standard oriented degree/pullback integration theorem is an approved
mathematical import. Applied to `sqrt(V) Omega`, it gives
`integral B0 sqrt(V(U))d^3x=B W`. A square completion or AM-GM inequality may
use this identity, but neither route is allowed to assume a saturating field.
Equality, sector infima, attainment, and physical interpretation are separate
obligations.

Exact P107 work requires no sampled quadrature. If any immutable source path
aborts only because `np.trapz` is absent, the campaign records an alias-only
compatibility replay before scientific adjudication. Mutable current-environment
scripts use `np.trapezoid`; canonical sampled integration would use
`trapezoid_integral`.

## Candidate Preregistration

The candidate set is frozen before E4 execution or predicate inspection.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal E4 promotion | Every action, potential, saturation, and state premise is accepted | Source symbols | Fails if existence or physical closure is merely asserted | AST, predicate, dependency, and output audit |
| B | Square-completion theorem | Declared energy and normalized pullback density | `lambda,mu,V,B0` | Exact lower bound with an a.e. equality condition | Both sign branches, degree substitution, wrong-sign and coefficient mutations |
| C | Independent AM-GM route | Nonnegative density terms and oriented degree theorem | Same declared objects | Agrees with B without reusing the square identity | Pointwise AM-GM, absolute-value inequality, and degree pairing |
| D | Sector-attainment theorem | Defined degree-sector infimum and an attained bound in each compared sector | Positive `A,n` | Exact linear sector mass and zero difference only conditionally | Infimum ledger, missing-attainment countermodel, C-RDIFF composition |
| E | Saturation obstruction | Admissible field or potential classes need not contain equality solutions | Potential and function class | Bound survives while universal existence fails | Zero-potential and regularity or topology counterexamples |
| F | Near-BPS theorem | Dimensionless epsilon, fixed-degree coefficients, controlled remainders | `epsilon,Delta_B,r_B` | Linear BPS term cancels, but coefficient remains free | Exact expansion, little-o or big-O remainder propagation, coefficient mutations |
| G | Consumer audit | Later units are noncanonical evidence | None accepted | Convention and coupling imports remain visible | KI/MK/MR dependency and normalization ledger |
| H | Nonduplication | A reusable theorem and consumer surface exists | None | At most distinct bound, attainment, and asymptotic APIs survive | Registry, campaign, memory, and package collision search |

## Selection Criteria and Blinding

Selection is ordered by accepted dependency closure; explicit action, density,
target measure, orientation, potential, regularity, and degree conventions;
agreement of square-completion and AM-GM routes; separation of lower bound,
equality, sectorwise attainment, and interpretation; dimensions, signs,
absolute-degree behavior, and counterexamples; controlled remainder algebra;
assumption economy; nonduplication; and downstream convention closure.

No comparator gate remains blinded because the queue and prior audits expose
the mathematical and narrative surfaces. Those exposed conclusions cannot be
used as verifier inputs or tolerances. P107 freezes its structural gates before
opening E4's implementation.

## Proposed Claim Delta

P107 reserves three claims after collision search found no accepted or
historically reserved match. Each may be promoted only at its exact verified
ceiling and may be rejected or narrowed individually without promoting the
rest of E4.

`C-BPS-001` may state the exact conditional Bogomolny decomposition and bound.
For nonzero signed degree, equality must be equivalent to
`lambda*pi^2*B0=sign(B)*mu*sqrt(V(U))` almost everywhere. The claim imports the
oriented degree theorem and does not assert existence, sector minimization,
physical baryon number, or a selected potential or coupling.

`C-BPS-002` may state that if the degree-sector energy is defined as an
infimum and an equality configuration exists in each specified positive-degree
sector, then the sector energy equals `K*B`, with
`K=2*lambda*mu*pi^2*W`, and `n*M(A)-M(n*A)=0`. It must explicitly deny that
linearity of the lower bound alone proves attainment.

`C-BPS-003` may state that for a controlled expansion
`M_epsilon(B)=K*B+epsilon*Delta_B+r_B(epsilon)`, the signed combination is
`epsilon*(n*Delta_A-Delta_(nA))+n*r_A-r_(nA)`. An `o(epsilon)` or
`O(epsilon^2)` remainder gives the corresponding `O(epsilon)` conclusion, but
neither the coefficient nor its sign, numerical size, or physical state map is
derived. Candidate H must reject this claim if it is only ceremonial
restatement of C-RDIFF-001 with no distinct asymptotic contract or consumer.

C-DIM-002 and C-RDIFF-001/002 are reused but not challenged or superseded.
No E2/E3 physical action, M1 mass sector, later coupling derivation, empirical
coefficient, nucleus, reaction, overbinding resolution, or yield may enter the
accepted delta.

## Implementation and Oracle Plan

SymPy and exact direct algebra are the strongest practical oracles for the
square identity, sign branches, degree-normalized cross term, equality
condition, dimensions, sector cancellation, perturbative expansion, and
mutations. The standard degree theorem is inspected as an explicit import;
an independent AM-GM route checks the normalization without importing the
primary square-completion helper. Exact counterexamples separate a valid lower
bound from universal saturation.

A minimal pure package module may own target-average normalization, bound
coefficient, square decomposition residuals, conditional attained-sector
energy, zero difference, and controlled perturbative combination. It must not
claim to solve the saturation PDE, select a potential or couplings, identify a
degree sector physically, or encode expected answers as booleans. Tests will
mutate the `pi^2` normalization, density sign, degree orientation, equality
branch, multiplicity, correction coefficient, and remainder order.

Post-freeze work executes the pinned E4 source, inventories imports and checks,
and audits every source predicate. The consumer replay examines KI1--KI5,
MK1--MK6, and MR1--MR6 only as hash-pinned noncanonical evidence, especially
the later `lambda` convention dispute. Targeted exact checks, repository
schema, generated queue and memory checks, one full workflow at the terminal
promotion boundary, and `git diff --check` close the campaign.

## Attempts and Continuation

Every source reproduction, symbolic identity, topological normalization,
equality, counterexample, asymptotic, consumer, nonduplication, or verifier
failure is preserved append-only with command, environment, output, mechanism,
and next materially different route. A failed universal-existence candidate
does not end the exact bound, conditional attainment, or asymptotic work.

## Debt Ledger

P107 tracks source hash and execution, every predicate, energy and current
normalization, target volume, orientation, degree convention, potential domain,
regularity and boundary data, degree-theorem import, equality condition,
existence and attainment, sector infimum, coupling dimensions and provenance,
near-BPS parameter and remainder, correction coefficient, physical state and
reaction maps, downstream convention consumers, disposition, generated state,
and parent continuation. Every item must be derived, declared, rejected, or
excluded before closure.

## Review and Promotion Plan

The primary square-completion route, independent AM-GM derivation, source and
predicate audit, exact counterexamples, asymptotic ledger, dependency and
consumer audits, candidate comparison, and impact analysis must agree. Each
surviving claim receives its own four-axis review and importable implementation.
E4 then receives a terminal disposition with durable evidence. Generated queue,
docs, registry, release, and memory are synchronized, followed by one unchanged
integrated gate. A final attempt begins in progress and is finalized afterward
with only record-sensitive checks repeated.

## Done Gate

P107 closes only when the exact bound and normalization, equality condition,
attainment ceiling, zero-difference theorem, controlled near-BPS algebra, all
E4 predicates, every downstream convention dependency, nonduplication result,
canonical records, and empty debt ledger agree. A square completion, claimed
universal saturation, formal `O(epsilon)`, or physical small-binding story is
not sufficient by itself.

## Cross-References

This campaign cross-references E2 through E5, M1, KI1 through KI5, MK1 through
MK6, MR1 through MR6, C-DIM-002, C-RDIFF-001, C-RDIFF-002, P105, P106, and the
framework-migration effort.

## Terminal Adjudication

P107 promotes C-BPS-001 as the exact two-orientation conditional topological
bound with explicit target normalization and equality equation. It promotes
C-BPS-002 as the sector-attainment theorem: zero signed binding follows only
when the compared degree-sector infima actually attain that bound. It promotes
C-BPS-003 as the controlled near-BPS difference expansion with its coefficient
and remainder visible.

The primary route passes 35 checks and the independent AM-GM route passes 21.
The latter rederives the standard-potential compacton and shows its naive L2
first-order correction diverges logarithmically, so E4's physical-smallness
application is not controlled. Exact convention audit gives
`lambda_A=pi^2*lambda_B`; E4's bound is correct in convention B, while later
mixed use creates one spurious `pi^2`.

E4 is qualified. Its square and conditional algebra survive, but universal
saturation, an accepted physical action or state map, numerical couplings,
interpolation, reaction, overbinding resolution, empirical coefficient, and
yield do not. The P107 debt ledger is empty and the corpus migration continues
with E5.
