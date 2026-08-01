---
description: Accepted framework claim C-VTX-002
author: framework-registry
created: '2026-08-01T15:41:27Z'
updated: '2026-08-01T15:41:27Z'
tags:
- substrate-framework
- accepted-claim
- C-VTX-002
category: claims
confidence: established
status: active
---
# C-VTX-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-VTX-001 with (v,n,lambda,g)=(1,1,2,1), there is resolution-bounded numerical evidence on truncated radial domains for a nontrivial monotone solution with f(epsilon)=a(epsilon)=0 and f(R)=a(R)=1 and finite positive tension approximately 4.21160. The reference collocation solve uses epsilon=1e-4, R=20, 120 initial points, tolerance 1e-8, at most 100000 nodes, maximum RMS residual below 1.1e-8, and uniform 20001-point trapezoidal energy quadrature. Tightening tolerance reduces tension error; R from 10 through 25 agrees within 1e-5; inner-cutoff error decreases from 1e-2 toward 1e-4; exponential and rational guesses converge to the same branch; matched dimensionless v=1 and v=2 domains give tension ratio four within 1e-5. Independent central finite differences at 101, 201, and 401 points give tensions 4.19212, 4.20658, and 4.21037. This is numeric evidence, not a continuum existence or uniqueness theorem, absolute tension, or physical confinement result.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-VTX-001. Assumptions: The parameter values, interval family, cutoff, Dirichlet data, solver, tolerances, maximum nodes, residual norm, and quadrature are exactly as stated., The reported branch is compared only within the declared positive-winding parameter family., Numerical agreement across the stated refinements does not prove continuum existence or uniqueness., The dimensionless demo tension is not an absolute physical string tension., Tail fits are regression checks against C-VTX-001's exact linearization, not independent derivations.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.23.0` with provenance `campaigns/P026-abelian-higgs-vortex/adjudication.yaml`.

- `campaigns/P026-abelian-higgs-vortex/verify.py`
- `campaigns/P026-abelian-higgs-vortex/attempts/0004/result.yaml`
- `campaigns/P026-abelian-higgs-vortex/reviews/independent_finite_difference_review.py`
- `campaigns/P026-abelian-higgs-vortex/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-VTX-002-review.md`
- `tests/test_abelian_higgs_vortex.py`
- `tests/test_numerics.py`
