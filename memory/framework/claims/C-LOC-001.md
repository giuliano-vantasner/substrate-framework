---
description: Accepted framework claim C-LOC-001
author: framework-registry
created: '2026-08-02T23:40:00Z'
updated: '2026-08-02T23:40:00Z'
tags:
- substrate-framework
- accepted-claim
- C-LOC-001
category: claims
confidence: established
status: active
---
# C-LOC-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let Q2 be a Euclidean momentum-squared variable, m2 positive, and C a separately supplied coefficient. The declared kernel K(Q2)=C*integral_0^1[u*(1-u)*Q2/(m2+u*(1-u)*Q2)]du has the exact positive-Q2 closed form C*[1-4*m2*atanh(sqrt(Q2/(4*m2+Q2)))/sqrt(Q2*(4*m2+Q2))]. Its Q2^n coefficient for every integer n>=1 is C*(-1)^(n-1)*(n!)^2/[(2*n+1)!*m2^n], and its finite geometric remainder proves convergence for |Q2|<4*m2, with nearest continued threshold Q2=-4*m2. The Q2-to-zero limit is zero, while the m2-to-zero limit at fixed positive Q2 is C, so those iterated limits do not commute. More generally, for a separately declared spectral density rho(t) supported on t>=Delta>0, whenever the displayed inverse moments and remainder converge, integral[rho(t)*Q2/(t+Q2)]dt equals the order-N sum sum_(n=1)^N (-1)^(n-1)*Q2^n*integral[rho(t)/t^n]dt plus the exact remainder (-1)^N*Q2^(N+1)*integral[rho(t)/(t^N*(t+Q2))]dt. A positive support gap alone guarantees neither ultraviolet moment convergence nor a nonzero first moment. These exact conditional identities derive no charged field, loop vertex, regulator or subtraction, physical mass or coupling, gauge kinetic action, electromagnetic sector, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The Euclidean momentum convention, positive mass squared, overall coefficient, parameter numerator u*(1-u), and subtraction K(0)=0 are declared exactly as stated; no accepted sine-Gordon claim supplies their loop interpretation., The closed form uses the positive-Euclidean branch, while the convergence radius is located with a separate complex continuation variable; other numerators or thresholds require a new coefficient and singularity derivation., The general spectral identity is promoted only as a finite pointwise algebraic expansion conditional on convergence of every displayed improper integral; a support gap does not discharge ultraviolet, regulator, subtraction, positivity, or nonzero-moment premises., No pending EM3, EM5, EM7, QCD5, physical comparator, or dimensional lift enters the kernel definition, coefficient sequence, remainder, or verdict.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.58.0` with provenance `campaigns/P064-d3s-gap-locality-coulomb/adjudication.yaml`.

- `campaigns/P064-d3s-gap-locality-coulomb/verify.py`
- `campaigns/P064-d3s-gap-locality-coulomb/attempts/0001/result.yaml`
- `campaigns/P064-d3s-gap-locality-coulomb/attempts/0004/result.yaml`
- `campaigns/P064-d3s-gap-locality-coulomb/reviews/independent_kernel_review.py`
- `campaigns/P064-d3s-gap-locality-coulomb/evidence/primary-provenance.yaml`
- `campaigns/P064-d3s-gap-locality-coulomb/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-LOC-001-review.md`
- `tests/test_momentum_kernels.py`
