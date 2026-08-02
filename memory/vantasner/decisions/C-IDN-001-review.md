---
description: Independent review of C-IDN-001 exact scale-coordinate identifiability
author: vantasner-review
created: '2026-08-03T00:35:00Z'
updated: '2026-08-03T00:35:00Z'
tags:
- substrate-framework
- claim-review
- scale-identifiability
category: decisions
confidence: established
status: archived
---
# C-IDN-001 Claim Review

## Claim Under Review

C-IDN-001 converts supplied positive dimensionless monomial ratios into an
exact log-linear system, composes C-LIN-001 with a coordinate-level nullspace
criterion, derives left-null compatibility and ordered coefficient/augmented
rank ledgers, proves reference-shift covariance, and classifies exact
one-coordinate interval intersections. It explicitly does not derive the
rows, values, references, covariance, source independence, or a physical scale.

## Sourced Inputs

The review reads release `v0.58.0`, C-DIM-001 through C-DIM-005 and C-DIM-007,
C-LIN-001, the frozen P065 candidate contract, hash-pinned OD and AS4, attempts
0001 through 0005, source audit and adjudication, primary provenance, canonical
module and tests, both exact verifiers, and the impact boundary. Pending AS1,
AS3, AS4, B1, G1-G3, G5, M1, and QCD5 supply no premise.

## Independence

The independent review imports no P065 scale-constraint API. It tests
coordinate covectors directly against the coefficient row space, rebuilds
right and left nullspaces, derives AS4's compatibility conditions, reconstructs
the altered free-length rank, takes interval endpoint order statistics, and
proves left-null residual invariance under a reference shift.

## Verification Status

The maximum verdict is `symbolic_verified`. Matrices, ranks, nullspaces,
residuals, shifts, and interval endpoints are exact. Canonical entry points
reject floating inputs and undecidable interval orderings rather than silently
introducing a tolerance. C-LIN-001 remains the owner of general consistency and
solution-dimension semantics; P065 adds the nonduplicate coordinate,
compatibility, provenance, and interval layers.

## Sensitivity and Counterexamples

OD's exact null vector is `(-1,1,1,1,1)`, making all five coordinates
unidentifiable and refuting its pure-`ln(a)` description. A 2x3 system can
identify two coordinates while remaining globally nonunique and not tall.
Rescaling a row adds no coefficient rank; changing only its offset raises
augmented rank and creates a left-null residual. AS4's four rows add directions
only in positions one and three. Its source free-length matrix has rank three
and nullity zero; changing the last extra-length coefficient from one to two is
what actually produces a null direction. Separated interval mutations turn
feasibility into contradiction.

## Framework Compatibility

The claim is a native composition with C-LIN-001 and preserves all accepted
dimensional ceilings. Positive log arguments are dimensionless ratios to
declared references, every row and interval has provenance, and a coordinate
verdict is unavailable for an inconsistent system. Neither a rank nor a
compatibility residual establishes a physical equation or statistical
independence.

## Dependency and Consumer Replay

The sole accepted dependency is C-LIN-001. Consumers are the new pure module,
focused tests, P065 verifiers, governance, generated docs and memory, the OD
disposition, and future scale audits. Post-change graph detection reports four
newly introduced internal flows and no affected pre-existing process. The full
promotion workflow passes all 501 repository tests; no pre-existing canonical
API is modified.

## Competing Candidate Audit

Candidates B, C, and E are selected because together they retain the exact
unknown set, distinguish coefficient information from compatibility, preserve
reference covariance and provenance, and handle deterministic uncertainty.
Candidate A is rejected as a physical derivation because its rows and
independence are assigned and its guards do not test their headlines. No
historical or AS4 verdict selected the theorem.

## Four-Axis Decision

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: new conditional theorem depending on C-LIN-001

## Promotion Transaction

Promotion adds C-IDN-001 to release `v0.59.0`, qualifies OD, and synchronizes
the implementation, tests, registry, release, queue, generated docs, and
memory. The exact routes, graph audit, one full workflow gate, and diff checks
must pass before the transaction is committed.

## Continuation if Not Accepted

This clause is inactive after the promotion gate. A future physical
absolute-scale claim must derive each dimensionless row and coefficient from
accepted dependencies, declare actual observations and references, discharge
every compatibility residual, and preserve shared-input provenance.

## Done Gate

The claim-level debt is empty only after canonical synchronization and the
promotion replay. The parent corpus migration remains active while queue units
remain pending.

## Cross-References

See P065, OD, AS4, C-LIN-001, `scale_constraints.py`,
`test_scale_constraints.py`, release `v0.59.0`, and the parent migration effort.
