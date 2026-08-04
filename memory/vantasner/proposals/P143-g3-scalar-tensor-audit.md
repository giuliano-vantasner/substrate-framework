---
description: Audit G3's canonical scalar-tensor breather-sourcing claim
author: vantasner
created: '2026-08-09T15:40:00Z'
updated: '2026-08-09T16:50:00Z'
tags:
- substrate-framework
- campaign-proposal
- scalar-tensor
- einstein-scalar
- migration-G3
category: proposals
confidence: exploratory
status: archived
---
# P143 G3 Scalar-Tensor Audit

## Question and Positive Deliverable

P143 must reproduce and adjudicate G3's claim that a minimally coupled
canonical scalar and a free three-plus-one metric supply a nontrivial
breather-sourced dynamical route around the fixed optical-family obstruction.
The positive deliverable is an importable exact action-to-equations theorem,
including stress, conservation, constraints, limits, and at least one complete
solution or decisive ansatz countermodel. A nonzero stress, written action,
small residual, or no-go does not complete the campaign.

## Base Release and Provenance

The accepted base is v0.109.0 at scientific commit `63443d2`; parent checkpoint
`61ef5d9` records 144 accepted claims and 78 pending units. G3 is pinned to
`substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`, path
`merged-framework/bridges/phase-5/bridge_G3_horndeski_scalar_tensor.py`, SHA-256
`8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba`.
Its dossier is pinned at `merged-framework/bridges/phase-5/dossiers/G3-dossier.md`,
SHA-256 `4860923f422d5dfc24155a5b5d6788e9d3245e42cdfa1cc0ed982d430925faf6`.
The source checkout commit, queue record, current release, C-GOR-001,
C-RAD-001, C-SG-012, `gordon_metric.py`, and the canonical sine-Gordon stress
API were read before freeze. The G3 source and dossier bodies remain unopened.

## Invariants, Conventions, and Allowed Imports

P143 keeps effective analog geometry, a gravitational action, a matter stress,
constraint-compatible initial data, an actual solution, and physical gravity
as separate layers. C-GOR-001 supplies no source or Einstein dynamics.
C-SG-012 supplies only normalized one-plus-one stress and conservation.
C-RAD-001 supplies action and boundary discipline, not gravity. G4 is pending
and grants no authority. Mostly-plus signature and explicit covariant versus
contravariant indices are the provisional convention; any source convention
change must be mapped rather than mixed. Standard Einstein-Hilbert and
canonical real-scalar calculus may be imported only with coefficients,
boundary terms, potential, dimensions, and equation signs explicit.

## Candidate Preregistration

Six candidates cover literal replay, exact action variation, a full analytic
solution, source compatibility, countermodels, and governance.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Literal G3 reproduction | Hash-pinned source conventions | Source-declared | Evidence only | Clean tally plus predicate data-flow audit |
| B | Exact Einstein-canonical-scalar theorem | Declared mostly-plus action and boundary variation | Gravitational scale and potential | Native conditional object | Both Euler equations, stress divergence, Bianchi, signs, limits |
| C | Exact nonvacuum coupled solution | A tractable potential, symmetry ansatz, and complete data | Only action parameters | Native if every component closes | Scalar equation, all Einstein components, constraints, curvature, limits |
| D | Embedded breather source audit | Accepted one-plus-one field and explicit transverse prescription | Coupling and transverse data visible | Likely conditional or incompatible | Finite energy, conservation, scalar equation, all tensor components |
| E | Countermodel family | Same declared equations with vacuum, wrong sign, nonconserved source, or missing data | None hidden | Native rejection guards | Each load-bearing omission changes or destroys the verdict |
| F | Governance closure | Registry and source graph | None | Required | Claim review, graph, release, queue, docs, memory |

## Selection Criteria and Blinding

Selection is ordered by complete action convention, exact field equations,
Bianchi and stress closure, initial/boundary and gauge data, full componentwise
solution, hyperbolicity and energy sign, dimensions and limits, finite-energy
embedding, parameter economy, reusable API value, and dependency closure. The
queue exposes only the headline, eleven-check tally, dependencies, and oracle
hints; it exposes no result excerpt. All source formulas, values, and dossier
details stay unopened until the committed freeze, and none may select the
concept or threshold afterward.

## Proposed Claim Delta

P143 provisionally reserves C-STG-001 for a distinct exact conditional
Einstein-canonical-scalar theorem if nonduplication, full action variation, and
solution or countermodel closure pass. It has no provisional accepted
dependency beyond any exact framework claims actually used. G3 has twelve
direct reverse consumers: T1E, NC4, WZ4, OD, EM3, SC1, SC2, G1, G4, G5, QCD1,
and SM1. No consumer gains authority from chronology or source pass status.

## Implementation and Oracle Plan

The selected reusable surface will live under `src/substrate_framework/`,
provisionally `einstein_scalar.py`, with pure exact APIs for the declared action
ledger, stress, equations, and any analytic solution. SymPy is the primary
oracle for exact variation identities, tensor components, Bianchi reduction,
limits, and solution substitution. A fresh independent route will reconstruct
the load-bearing equations without importing the claim module. Mutations flip
metric signature, scalar kinetic sign, Einstein normalization, potential sign,
index raising, coupling, conservation, and boundary or constraint data.
Countermodels cover constant scalar vacuum, flat metric with nonzero stress,
nonconserved prescribed stress, infinite transverse embedding, and equation-
only data without a solved geometry.

Any source numerical leg is regression evidence until source inspection
identifies its actual equation, domain, data, method, tolerances, solver status,
error norm, and comparator independence. Before a fresh ODE, BVP, or PDE run,
an append-only attempt must freeze those items, refinement, an independent
method or soluble limit, and load-bearing mutations; otherwise it cannot
promote a claim. Campaign code will use `src/substrate_framework/numerics.py`
where applicable. Compatibility preflight audits direct, imported, dynamic,
and eager-fallback legacy integration syntax. Mutable code uses
`np.trapezoid` or `trapezoid_integral`; immutable source receives only a
recorded alias backed by `np.trapezoid` if needed, without scientific effect.

## Attempts and Continuation

Attempt 0001 freezes this contract before G3 execution or source and dossier
body inspection. Later failures are append-only and identify implementation,
representation, action, source, solution, target, or foundation mechanisms.
Failure of the breather-gravity headline advances Candidates B through F and
does not close the positive action or solution object.

## Debt Ledger

The campaign ledger tracks source predicates, action and boundary terms,
metric and curvature conventions, scalar sign and potential, stress and
conservation, constraints and gauge, index map, initial and boundary data,
hyperbolicity, finite transverse energy, coupling, compatibility, dependencies,
consumers, novelty, and generated state until every item is discharged.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| G3 executable and exact checks are unopened | Hash, compatibility preflight, replay, AST/data-flow audit, and all eleven predicates | discharged |
| Action variation and signs may be asserted | Exact boundary-aware metric and scalar Euler equations with mutations | discharged |
| Nonzero stress may substitute for a solution | Every Einstein and scalar component, constraints, conservation, and complete data | discharged |
| One-plus-one breather embedding may be infinite or inconsistent | Explicit transverse prescription, finite-energy ceiling, and source compatibility | discharged |
| Numeric evidence may be target-regression or under-specified | Solver status, refinement, independent limit, mutations, and comparator audit | discharged |
| Dependencies consumers and novelty are incomplete | G2 G4, twelve reverse consumers, cycles, graph, and nonduplication audit | discharged |
| Registry disposition release docs queue and memory are unsynchronized | Individual review and one governed terminal transaction | discharged |

## Review and Promotion Plan

Any C-STG-001 candidate receives a fresh independent derivation and individual
claim review. G3 receives a terminal predicate-level disposition whether or not
a claim is promoted. A mixed source maps only accepted surfaces and records
every rejected source, solution, gravity, material, physical, or substrate
clause. Release, queue, docs, accepted memory, proposal memory, and parent
effort change only at actual boundaries. The final attempt is prepared in
progress before one integrated gate and finalized afterward with
record-sensitive checks only.

## Done Gate

P143 closes only with a complete positive exact or controlled Einstein-scalar
object, sensitive primary and independent evidence, individual claim review,
terminal G3 disposition, closed dependencies and consumers, synchronized
governed state, and an empty ledger. An action, clean tally, nonzero stress,
small residual, or no-go label does not complete the campaign.

## Cross-References

The governing references are P049, P132, P141, P142, G2, G3, G4, C-SG-001,
C-SG-002, C-SG-008, C-SG-012, C-RAD-001, C-GOR-001, provisional C-STG-001,
v0.109.0, and the parent migration effort.
