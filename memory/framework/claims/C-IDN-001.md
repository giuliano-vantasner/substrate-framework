---
description: Accepted framework claim C-IDN-001
author: framework-registry
created: '2026-08-03T00:50:00Z'
updated: '2026-08-03T00:50:00Z'
tags:
- substrate-framework
- accepted-claim
- C-IDN-001
category: claims
confidence: established
status: active
---
# C-IDN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let A be a nonempty finite exact real m-by-n matrix with provenance for every row, and let b be an exact column. Conditional on separately supplied positive dimensionless ratios satisfying y_i=c_i*product_j(s_j/s_ref_j)^A_ij, taking logs gives A*x=b with x_j=log(s_j/s_ref_j) and b_i=log(y_i/c_i). Composing C-LIN-001, a consistent system identifies coordinate j exactly when every vector in null(A) has zero j component, equivalently when the jth coordinate covector lies in row(A); this can hold without global uniqueness or more rows than columns. Every left-null vector ell supplies the exact scale-free compatibility condition ell^T*b=0. Ordered prefix ranks of A and [A|b] distinguish a new coefficient direction, a consistent dependent row, and a conflicting dependent datum, but do not establish physical or statistical independence. A reference change x'=x-delta, b'=b-A*delta preserves nullspace, coordinate identifiability, and every left-null residual. For separately supplied exact closed intervals on one log coordinate, their intersection is [max lower_i,min upper_i]: a strict interval is a feasible range, equal endpoints identify one point, and reversed endpoints are a contradiction. These exact conditional ledgers derive no physical row, reference scale, observable, coefficient, covariance, independence premise, fitted constant, or substrate scale.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIN-001. Assumptions: Every matrix entry, right-hand side, reference shift, and interval endpoint is exact and real; interval endpoint ordering is decidable., Monomial observables, coefficients, and scale coordinates are positive dimensionless ratios to declared references, and every supplied row or interval retains its provenance., Coordinate identifiability is asserted only for a consistent supplied system; left-null compatibility does not certify the origin, independence, or correctness of a row., OD and AS4 are noncanonical evidence only; no pending dependency or absolute observed value supplies a physical constraint.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.59.0` with provenance `campaigns/P065-od-absolute-scale-identifiability/adjudication.yaml`.

- `campaigns/P065-od-absolute-scale-identifiability/verify.py`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0001/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0004/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0005/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0006/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/reviews/independent_scale_review.py`
- `campaigns/P065-od-absolute-scale-identifiability/evidence/primary-provenance.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-IDN-001-review.md`
- `tests/test_scale_constraints.py`
- `tests/test_linear_systems.py`
