---
description: Accepted framework claim C-WZW-002
author: framework-registry
created: '2026-08-02T16:00:00Z'
updated: '2026-08-02T16:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-WZW-002
category: claims
confidence: established
status: active
---
# C-WZW-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

In C-WZW-001's convention Omega_5=-i*Alt Tr(theta^5), orient the unit S^5 as the boundary of the unit ball in (Re z1,Im z1,Re z2,Im z2,Re z3,Im z3). The explicit Puttmann-Rigas map eta(z)=z*z^T+A(conjugate(z)), with A(conjugate(z)) the displayed complex cross-product matrix, obeys eta^dagger*eta=I and det eta=1 on |z|=1. The regular value (1,0,0) of its first-column projection has exactly the preimages +(1,0,0) and -(1,0,0), both with oriented real Jacobian determinant 8, so the projection has degree +2. By the audited U(n-1)->U(n)->S^(2n-1) generator criterion, eta is the positive generator of pi_5(SU(3))=Z. Equivariance makes eta^*Omega_5 an invariant top form on S^5. On the positive tangent frame at (1,0,0), exact evaluation gives Alt Tr(theta^5)=-480*i and Omega_5=-480; since Vol(S^5)=pi^3, the oriented primitive periods are -480*i*pi^3 for the raw trace and -480*pi^3 for Omega_5. Consequently a map in homotopy class n has real sphere period -480*pi^3*n. For two oriented five-ball fillings of a common S^4 boundary whose glued map has winding n, for real k the coefficient c=k/(240*pi^2) gives phase ratio exp(-2*pi*i*k*n)=1 for all integer n exactly when k is an integer; orientation reversal changes the period sign but not this lattice. This is a mathematical sphere-filling level theorem. It does not fix periods on arbitrary closed five-manifolds, identify k with N_c, or establish a WZW action from substrate dynamics, baryon number, representation selection, a gauge anomaly, descent, inflow, absolute scale, or any physical realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-WZW-001. Assumptions: The SU(3), anti-Hermitian trace, unnormalized alternating sum, and minus-i reality conventions are exactly those fixed by C-WZW-001 and C-LIE-001., The sphere and its tangent frames use the displayed boundary orientation; reversing the domain or glued-cycle orientation reverses the period sign., Puttmann-Rigas Lemma 1.1 and Theorem 2.1, including pi_5(SU(3))=Z and the degree-two column criterion, are approved primary-source topology imports whose algebraic and local-degree parts are independently reproduced here., Equivariance of eta, transitivity and orientation preservation of the connected SU(3) action on S^5, homotopy invariance of closed-form integrals, and Vol(S^5)=pi^3 are approved standard mathematical inputs., The coefficient-lattice conclusion concerns two smooth oriented five-ball fillings of a common S^4 boundary, so their gluing is an oriented S^5; it makes no claim for arbitrary closed five-manifold periods or additional bordism structures., The lattice parameter k is real; when integral it is a mathematical coefficient label only and has no accepted identification with N_c, baryon number, anomaly data, or a substrate observable.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.51.0` with provenance `campaigns/P057-wz2-pi5-period-level/adjudication.yaml`.

- `campaigns/P057-wz2-pi5-period-level/verify.py`
- `campaigns/P057-wz2-pi5-period-level/attempts/0002/result.yaml`
- `campaigns/P057-wz2-pi5-period-level/attempts/0003/result.yaml`
- `campaigns/P057-wz2-pi5-period-level/reviews/independent_period_review.py`
- `campaigns/P057-wz2-pi5-period-level/reviews/source_adjudication.md`
- `campaigns/P057-wz2-pi5-period-level/evidence/topology-provenance.yaml`
- `memory/vantasner/decisions/C-WZW-002-review.md`
- `tests/test_wzw.py`
