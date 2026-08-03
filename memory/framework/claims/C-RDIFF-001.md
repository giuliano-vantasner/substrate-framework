---
description: Accepted framework claim C-RDIFF-001
author: framework-registry
created: '2026-08-07T17:00:00Z'
updated: '2026-08-07T17:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RDIFF-001
category: claims
confidence: established
status: active
---
# C-RDIFF-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let U and alpha be positive, let A and n be positive integers, and let b(A) and b(n*A) be real dimensionless coefficients. Conditional on the declared masses M(k)=alpha*b(k)*U and binding convention B_E(k)=k*M(1)-M(k), the signed difference satisfies exactly Q=n*M(A)-M(n*A)=B_E(n*A)-n*B_E(A) =alpha*U*(n*b(A)-b(n*A)). Hence kappa=Q/U has inverse b(n*A)=n*b(A)-kappa/alpha, and for positive alpha its sign is the sign of n*b(A)-b(n*A), with zero surface b(n*A)=n*b(A). If independent input intervals are b(A) in [l_A,u_A] and b(n*A) in [l_F,u_F], their sharp rectangular image is alpha*(n*l_A-u_F) <= kappa <= alpha*(n*u_A-l_F). Separate upper bounds on M(A) and M(n*A) do not in general bound their signed difference: their unknown nonnegative slacks enter with opposite signs. This is an exact conditional linear transformation. It derives no mass formula, scale, action, minimum, state identity, binding convention, reaction, yield, material, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-002. Assumptions: U and alpha are positive, A and n are positive integers, and both displayed coefficients are real and dimensionless., The mass normalization M(k)=alpha*b(k)*U and binding convention B_E(k)=k*M(1)-M(k) are explicit premises rather than framework predictions., The binding cancellation uses a final degree n*A and n identical initial-degree terms. Different multiplicities or state bookkeeping require a new declared ledger., The interval formula is the exact image of independent rectangular input intervals under a positive affine map; it is only as rigorous as those supplied intervals and encodes no statistical dependence or confidence level., An individual upper bound M(k)<=M_hat(k) supplies an unknown nonnegative slack. Without a relation between slacks, subtracting upper bounds gives neither an upper nor a lower bound on Q., C-DIM-002 supplies only the ceiling that dimensional consistency leaves dimensionless coefficients and physical primitive choices unconstrained.. Comparators: E3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its formula and physical comparator values were exposed before P106, while exact identities, mutations, interval tests, bound counterexamples, and physical ceilings were frozen before body execution.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.90.0` with provenance `campaigns/P106-e3-conditional-energy-difference-audit/adjudication.yaml`.

- `campaigns/P106-e3-conditional-energy-difference-audit/verify.py`
- `campaigns/P106-e3-conditional-energy-difference-audit/reviews/independent_difference_review.py`
- `campaigns/P106-e3-conditional-energy-difference-audit/attempts/0002/result.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/attempts/0004/result.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/source-reproduction.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/source-audit.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/check-adjudication.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/dependency-audit.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/consumer-audit.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/candidate-comparison.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/primary-provenance.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RDIFF-001-review.md`
- `tests/test_energy_differences.py`
