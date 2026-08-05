---
description: Accepted framework claim C-CMB-001
author: framework-registry
created: '2026-08-11T15:45:00Z'
updated: '2026-08-11T15:45:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CMB-001
category: claims
confidence: established
status: active
---
# C-CMB-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For every positive integer n, define q_n=1/(n!)^2. Then q_n is a positive exact rational, q_1=1, q_(n+1)/q_n=1/(n+1)^2, and the sequence is strictly decreasing. The positive exponential series gives e^n>n^n/n!, hence q_n<(e/n)^(2*n). For every fixed nonnegative integer p, if a_n=n^p*q_n then a_(n+1)/a_n=((n+1)/n)^p/(n+1)^2<=2^p/(n+1)^2; from n>=ceil(sqrt(2^(p+1)))-1 onward this ratio is at most one-half, so n^p*q_n tends to zero. Thus q_n decays faster than every fixed inverse power. The exact exponential-series bounds e<49/18<11/4 and integer comparison (11/4)^20<10^9 further imply that for every positive integer d, at n=10^d one has q_n<10^(-((20*d-9)*n/10)). In particular the exact exponent ceilings for d=7,9,11 are respectively -131000000, -17100000000, and -2110000000000. Applied to C-SG-019's exact zero-background one-high cosine coefficient with declared real amplitude A and coordinate scales a_H and a_L, the coefficient square is zero for even low order n and is A^2*a_H^2*a_L^(2*n)*q_n for odd n. The exact q_n remains positive at every positive integer even when a finite machine representation underflows or overflows. A classical coefficient square is not by itself a matrix element, transition rate, probability, branching weight, physical subdivision law, or material prediction.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-019. Assumptions: n is an exact positive integer, p is one separately fixed exact nonnegative integer, and d is an exact positive integer; the theorem makes no uniform-in-p convergence-rate claim., Factorial, the real exponential series, positive nth roots, and reciprocal order use their standard exact positive-real meanings., The decade ceiling is a conservative exact bound at the supplied mathematical order n=10^d. A selected d or n is not thereby a physical subdivision count or energy band., The cosine application inherits C-SG-019's independent real formal coordinates, exact real amplitude and scales, zero-background specialization, coefficient-versus-derivative convention, and parity ceiling., Changing background or coordinate normalization changes the supported coefficient or its magnitude; the unit specialization is not invariant under those changes., Machine zero, overflow, or underflow is representation evidence only and does not change the exact rational sequence., A Golden-rule rate would additionally require normalized quantum states, a complete interaction matrix element, an on-shell final-state measure or spectral density, energy and normalization conventions, and validity assumptions; none is imported here., PN2, WN2 through WN7, and MD1 through MD6 supply no accepted physical premise to this theorem and remain separately governed.. Comparators: WN1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its unit coefficient square, selected exact values, arbitrary-precision decade exponents, underflow demonstration, and rate wording were exposed before P189, while normalization, universal, exact-bound, mutation, and consumer criteria were frozen before implementation.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.140.0` with provenance `campaigns/P189-wn1-factorial-suppression-audit/adjudication.yaml`.

- `campaigns/P189-wn1-factorial-suppression-audit/verify.py`
- `campaigns/P189-wn1-factorial-suppression-audit/reviews/independent_factorial_review.py`
- `campaigns/P189-wn1-factorial-suppression-audit/reviews/replay_source_graph.py`
- `campaigns/P189-wn1-factorial-suppression-audit/reviews/C-CMB-001-claim-review.md`
- `campaigns/P189-wn1-factorial-suppression-audit/reviews/source_adjudication.md`
- `campaigns/P189-wn1-factorial-suppression-audit/reviews/impact_analysis.md`
- `campaigns/P189-wn1-factorial-suppression-audit/attempts/0003/result.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/attempts/0004/result.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/attempts/0005/result.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/formula-freeze.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/input-provenance.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/dependency-audit.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/consumer-audit.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/candidate-comparison.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/implementation-audit.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/primary-provenance.yaml`
- `campaigns/P189-wn1-factorial-suppression-audit/evidence/independent-provenance.yaml`
- `memory/vantasner/decisions/C-CMB-001-review.md`
- `memory/vantasner/decisions/WN1-qualified-review.md`
- `src/substrate_framework/factorial_suppression.py`
- `tests/test_factorial_suppression.py`
