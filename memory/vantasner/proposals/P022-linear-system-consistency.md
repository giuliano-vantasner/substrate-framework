---
description: Audit EL5's over-determination instrument as an exact linear-system diagnostic
author: vantasner
created: '2026-08-01T14:33:34Z'
updated: '2026-08-01T14:37:44Z'
tags:
- substrate-framework
- campaign-proposal
- linear-system-consistency
- migration-EL5
category: proposals
confidence: exploratory
status: archived
---
# P022 Linear-System Consistency

## Question and Positive Deliverable
P022 must determine which EL5 conclusions follow from coefficient and augmented
matrix ranks without importing EL4's rejected electron closure. The positive
object is an importable exact diagnostic that distinguishes consistency,
uniqueness, underdetermination, redundant equations, and excess equation count.
A green predecessor consumer run or a failed mass prediction does not complete
the campaign.

## Base Release and Provenance
The accepted base is `v0.19.0` at commit `240b3ad`. Direct authority is
`C-DIM-003`, `C-RGE-001`, and `C-DIM-005`; in particular the mass-energy ratio
`q` remains free. The hash-pinned candidate is EL5 at
`merged-framework/bridges/phase-46/bridge_EL5_od_instrument_and_consumers.py`,
SHA-256 `5684f2aba979501c81dc12c1afcc51c29cbeb7eb676678b76208cfcd23f01d1f`.
Its listed AS4, MR1, NY, OD, OD3, and S5 dependencies are not authority unless
mapped separately to accepted claims. Memory search found only the parent
direction and prior rank reviews; all reused facts will be checked at source.

## Invariants, Conventions, and Allowed Imports
Matrices are finite exact SymPy matrices over the real numbers. Consistency is
decided by equality of coefficient and augmented ranks. For a consistent
system with `p` unknowns and coefficient rank `r`, solution-space dimension is
`p-r`; uniqueness requires `r=p`. The descriptive fact `n>p` is neither
consistency nor uniqueness. EL4's `q`, source soliton coefficient, hadronic
offset, and particle labels remain unavailable. Consumer execution establishes
only regression compatibility for the pinned files it actually runs.

## Candidate Preregistration
The candidates are frozen before EL5's full body and reported mass ratio are
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote a general exact coefficient/augmented-rank diagnostic and duplicate-row theorem | Finite exact linear system; nonzero duplicated row for the specialized iff | Matrix and right-hand side | Native reusable verification machinery | Compare ranks, solve examples in every status class, and mutate right-hand offsets |
| B | Classify EL5 as duplicate evidence for standard rank calls | Existing SymPy operations suffice and no distinct consumer benefits | None | Preferred if a package diagnostic adds no semantic guard | Inspect consumers and compare with existing framework APIs |
| C | Promote the source's electron/hadron mass-ratio prediction | Treat `b(1)`, `kappa_h`, and both object maps as fixed accepted inputs | Hidden prefactor and physical mappings | Conflicts with C-DIM-005's free-input ceiling | Vary `q` or the two offsets while holding the coefficient matrix fixed |
| D | Promote source consumer pass status as scientific verification | Hash-pinned scripts represent all semantic consumers | File set and environment | Evidence-only, not a scientific claim | Audit executed paths, return codes, and whether they test the headline theorem |

## Selection Criteria and Blinding
Selection is ordered by exact logical classification, premise closure, retained
free inputs, counterexample coverage, API distinctness, dependency economy, and
consumer reach. Candidate A must distinguish row-count overdetermination from
rank, consistency, and uniqueness. Candidate C fails if a free offset can make
the dependent-row constraint hold for arbitrary masses. Any observed mass
ratio and consumer tally remain blinded until equations, classifications,
mutations, and selection are frozen.

## Proposed Claim Delta
Provisional `C-LIN-001` states the Rouché-Capelli rank criterion for a finite
exact real system and its solution-space consequences. It also specializes to
two copies of a nonzero row: adding the duplicate leaves coefficient rank and
nullity unchanged, while the two-row subsystem is consistent exactly when its
right-hand sides agree. The statement assigns no physical meaning to rows or
offsets and does not promote any mass relation.

## Implementation and Oracle Plan
A pure linear-algebra module will return immutable diagnostics for a matrix and
right-hand side if the theorem has distinct framework value. SymPy exact ranks
and `linsolve` fit the obligation. The main verifier will cover unique,
underdetermined, inconsistent, redundant, tall-consistent, and tall-
inconsistent systems; mutate a duplicated row's right-hand side; and reproduce
EL5's coefficient matrices without importing its offsets. An independent route
will use row reduction and explicit solutions. Source consumer executions, if
audited, are regression evidence rather than independent proof.

## Attempts and Continuation
Attempt `0001` will reproduce the pinned EL5 source and compare every checked
predicate with the exact diagnostic. Technical failures are preserved. If the
API adds no semantic protection, Candidate B replaces promotion. If the
generic theorem survives but the physical offset closure fails, EL5 is
qualified with its consumer evidence preserved separately.

## Debt Ledger
The campaign tracks four logical and provenance debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Overdetermined may be used as a proxy for consistency or uniqueness | Encode and test the distinct predicates | discharged |
| Duplicate coefficient rows may hide inconsistent offsets | Mutate and rank the augmented matrix | discharged |
| EL4's free prefactor may be called a prediction | Retain it or exclude the physical specialization | discharged |
| Consumer runs may be treated as proof of the headline | Audit their scope and classify them as regression | discharged |

## Review and Promotion Plan
Review will independently row-reduce representative systems, audit EL5 check by
check, and inspect every claimed consumer execution. Promotion requires an
importable diagnostic and tests, individual claim review, terminal EL5
disposition, registry/release/generated-record synchronization, targeted
consumer replay, and one full repository gate at the unchanged boundary.

## Results and Promotion
EL5 reproduces all nine source checks and seven predecessor subprocess tallies.
The main audit passes 21 exact checks, independent row reduction passes six,
and 22 focused tests pass. `C-LIN-001` is selected because the status object
prevents repeated row-count/rank/consistency conflation. EL5 is qualified: its
actual restored-electron matrix has nullity zero, its ratio retains `b` and
`kappa_h`, and its subprocesses do not replay accepted package consumers.

## Done Gate
P022 is complete. The positive diagnostic exists, logical classes and mutations
are independently verified, EL5 is terminally qualified, consumers are scoped
correctly, and campaign debt is empty.
