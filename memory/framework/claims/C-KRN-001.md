---
description: Accepted framework claim C-KRN-001
author: framework-registry
created: '2026-08-02T23:40:00Z'
updated: '2026-08-02T23:40:00Z'
tags:
- substrate-framework
- accepted-claim
- C-KRN-001
category: claims
confidence: established
status: active
---
# C-KRN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a supplied finite inverse kernel K(k2)=sum_j c_j*k2^s_j with k2 positive and exact positive real exponents, first combine equal exponents and remove coefficients that simplify exactly to zero. If every remaining coefficient is provably nonzero, the smallest remaining exponent s_star controls the infrared and the corresponding power of |k| is 2*s_star. Exact cancellation can expose a higher exponent, while any separately supplied lower fractional term remains leading over analytic integer-power corrections. An undecidable symbolic coefficient supplies only a condition and cannot be treated as nonzero. In the fixed convention G(x)=integral d^d k/(2*pi)^d exp(i*k.x)/[A*(k^2)^s], for r=|x|>0, A nonzero, and 0<s<d/2, the exact kernel away from contact terms is Gamma(d/2-s)*r^(2*s-d)/[A*4^s*pi^(d/2)*Gamma(s)]. The separately supplied specialization d=3,s=1,A=1 is 1/(4*pi*r), but the theorem does not select s, d, A, a source, boundary condition, force law, charge normalization, electromagnetic sector, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The inverse kernel, exact exponents, coefficients, and their zero or nonzero status are supplied in one convention; an unresolved coefficient condition must be discharged before assigning a unique leading exponent., The Fourier convention, nonzero inverse-kernel coefficient A, positive radius, spatial dimension, exponent, convergence domain 0<s<d/2, and exclusion of distributional contact terms are declared exactly as stated., The d=3,s=1 endpoint is a conditional specialization and not evidence that accepted U1 covariance, a mass gap, or a pending dimensional argument selects either input., No physical Coulomb comparator, Maxwell action, charge dictionary, 1+1-to-3-dimensional lift, or pending source claim enters the leading-power classification or Schwinger/Fourier derivation.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.58.0` with provenance `campaigns/P064-d3s-gap-locality-coulomb/adjudication.yaml`.

- `campaigns/P064-d3s-gap-locality-coulomb/verify.py`
- `campaigns/P064-d3s-gap-locality-coulomb/attempts/0001/result.yaml`
- `campaigns/P064-d3s-gap-locality-coulomb/attempts/0004/result.yaml`
- `campaigns/P064-d3s-gap-locality-coulomb/reviews/independent_kernel_review.py`
- `campaigns/P064-d3s-gap-locality-coulomb/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-KRN-001-review.md`
- `tests/test_momentum_kernels.py`
