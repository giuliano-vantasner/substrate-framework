---
description: Accepted framework claim C-LIN-001
author: framework-registry
created: '2026-08-01T14:37:44Z'
updated: '2026-08-01T14:37:44Z'
tags:
- substrate-framework
- accepted-claim
- C-LIN-001
category: claims
confidence: established
status: active
---
# C-LIN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a finite exact real linear system M*x=b, the system is consistent if and only if rank(M)=rank([M|b]). When consistent, its solution-space dimension is columns(M)-rank(M); it is unique exactly when this dimension is zero and underdetermined exactly when it is positive. More equations than unknowns is only an equation-count property and implies neither consistency nor uniqueness. Adding an exact duplicate of a nonzero row leaves coefficient rank and nullity unchanged; the two-row duplicate subsystem is consistent exactly when the two right-hand sides agree.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The coefficient matrix and right-hand side define a finite exact real linear system., The right-hand side is a column with one entry per coefficient row., The duplicate-row specialization assumes the duplicated coefficient row is nonzero., Overdetermined_by_count records row count only and is not a consistency verdict.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.20.0` with provenance `campaigns/P022-linear-system-consistency/adjudication.yaml`.

- `campaigns/P022-linear-system-consistency/verify.py`
- `campaigns/P022-linear-system-consistency/attempts/0001/result.yaml`
- `campaigns/P022-linear-system-consistency/reviews/independent_row_reduction_review.py`
- `campaigns/P022-linear-system-consistency/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-LIN-001-review.md`
- `tests/test_linear_systems.py`
