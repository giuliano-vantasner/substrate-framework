---
description: Accepted framework claim C-GLS-001
author: framework-registry
created: '2026-08-03T00:50:00Z'
updated: '2026-08-03T00:50:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GLS-001
category: claims
confidence: established
status: active
---
# C-GLS-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a nonempty finite exact real design A of full column rank, an exact observation column b with row provenance, and a separately supplied exact symmetric positive-definite covariance Sigma with declared provenance, the unique generalized least-squares estimator is x_hat=(A^T*Sigma^-1*A)^-1*A^T*Sigma^-1*b. Its fitted column is A*x_hat, residual r=b-A*x_hat, residual projector P=I-A*(A^T*Sigma^-1*A)^-1*A^T*Sigma^-1, exact normal residual A^T*Sigma^-1*r=0, quadratic residual chi2=r^T*Sigma^-1*r, and residual degrees of freedom m-rank(A). P is idempotent and annihilates A. Changing a supplied off-diagonal covariance can change chi2 without changing the algebraic coefficient rank; a singular, indefinite, nonsymmetric, inexact, or dimension-mismatched covariance and a rank-deficient design do not satisfy this unique-estimator theorem. The exact chi2 ledger alone assigns no sampling distribution, p-value, source independence, model adequacy, physical observation, fitted scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIN-001. Assumptions: The design, observations, and covariance are finite exact real inputs in one declared log-coordinate convention, with row and covariance provenance retained., Sigma is symmetric positive definite and A has full column rank; rank-deficient estimation would require a separately specified generalized inverse or prior and is outside the claim., Chi2 is only the displayed quadratic residual unless a separately governed stochastic model supplies its distribution and interpretation., Shared inputs must be represented in the supplied covariance; labels or distinct narrative derivation routes do not establish statistical independence.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.59.0` with provenance `campaigns/P065-od-absolute-scale-identifiability/adjudication.yaml`.

- `campaigns/P065-od-absolute-scale-identifiability/verify.py`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0003/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0004/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0005/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/attempts/0006/result.yaml`
- `campaigns/P065-od-absolute-scale-identifiability/reviews/independent_scale_review.py`
- `campaigns/P065-od-absolute-scale-identifiability/evidence/primary-provenance.yaml`
- `memory/vantasner/decisions/C-GLS-001-review.md`
- `tests/test_scale_constraints.py`
