---
description: Independent review of C-LIN-001
author: vantasner-review
created: '2026-08-01T14:37:44Z'
updated: '2026-08-01T14:37:44Z'
tags:
- substrate-framework
- claim-review
- linear-system-consistency
category: decisions
confidence: working
status: archived
---
# Review of C-LIN-001

## Claim Under Review
For a finite exact real system `M*x=b`, consistency holds exactly when
`rank(M)=rank([M|b])`. If consistent, solution dimension is
`columns(M)-rank(M)`; the solution is unique exactly when that dimension is
zero and underdetermined exactly when it is positive. Having more rows than
columns is only an equation-count property. Adding a duplicate nonzero row
leaves coefficient rank and nullity unchanged, while the duplicate pair is
consistent exactly when its right-hand sides agree.

## Sourced Inputs
The review read `v0.19.0`, P022, attempt `0001`, the package diagnostic and
tests, both derivations, hash-pinned EL5, its seven subprocess outcomes, and the
source adjudication. EL4's free `q`, the source `b(1)` estimate, `kappa_h`, and
all particle labels remain outside the claim.

## Independence
The main route uses the proposed diagnostic API across status classes. The
independent route imports no package diagnostic and instead compares pivot
columns of exact reduced row-echelon forms for coefficient and augmented
matrices.

## Verification Status
Exact ranks, row reductions, status counterexamples, and solution dimensions
support `symbolic_verified`. Twenty-one main and six independent checks exercise
the theorem's actual logical distinctions. The predecessor subprocesses are
classified as regression evidence only.

## Sensitivity and Counterexamples
Changing the duplicate row multiplier or either right-hand side breaks the
specialized baseline. The same tall coefficient matrix is shown both consistent
and inconsistent under different right-hand sides. EL5's restored-electron
matrix has three pivots and no free column, while its different OD-v1 matrix has
four pivots and one free column.

## Framework Compatibility
The claim is native reusable verifier machinery and introduces no physical
parameter. Its explicit `overdetermined_by_count` field prevents row count from
silently standing in for consistency or uniqueness. No prior scientific
invariant changes.

## Dependency and Consumer Replay
The claim has no accepted scientific dependencies. Consumers are the exact
diagnostic API, package tests, P022, EL5's qualified disposition, and future
OD/AS/EL audits. Focused linear-system and renormalization tests pass. The seven
source subprocess tallies are preserved separately and no debt remains.

## Competing Candidate Audit
The proposal preregistered generic promotion, duplicate-only evidence, physical
mass prediction, and consumer-pass promotion. The semantic status object and
counterexamples select Candidate A. Free-offset sensitivity and consumer scope
reject Candidates C and D without observed mass comparison.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: new exact verifier theorem and diagnostic

## Promotion Transaction
Promotion adds the pure diagnostic API/tests, P022 evidence, `C-LIN-001`,
qualified EL5 disposition, release manifest, and regenerated canonical records.
The terminal qualification cites exact counterexamples and the durable source
consumer report.

## Continuation if Not Accepted
A status-class or independent-pivot failure would reject the API. A physical
mass ratio would still require separately accepted values and object maps.

## Done Gate
The exact diagnostic, independent row reduction, mutations, status
counterexamples, source qualification, consumers, and debt closure are
complete.

## Cross-References
See P022, EL5, `C-DIM-005`, linear-system APIs/tests, and the parent migration
effort.
