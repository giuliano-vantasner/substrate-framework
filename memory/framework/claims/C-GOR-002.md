---
description: Accepted framework claim C-GOR-002
author: framework-registry
created: '2026-08-11T06:49:00Z'
updated: '2026-08-11T06:49:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GOR-002
category: claims
confidence: established
status: active
---
# C-GOR-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let n(x) be an exact positive twice-differentiable refractive index on a connected interval, let the C-GOR-001 mostly-plus Gordon metric have a uniform exact real z velocity v with |v|<1, and let an exact real canonical C-STG-001 scalar U depend only on t and x, with exact real potential value V and exact positive coupling kappa. At each scalar jet, every covariant algebraic Einstein equation G_ab=kappa*T_ab holds if and only if U_t=0, U_x=0, V=0, and K=(n*n_xx-2*n_x^2)/n^2=0. For v nonzero, the source-ray equations for U_t^2, U_x^2, and V have rank three; in the exact parameterization v=r/sqrt(1+r^2), r real and nonzero, one numerator-normalized minor is 8*n^2*r^2*sqrt(1+r^2), hence nonzero. At v=0, the zero tt and xx equations are n^2*U_t^2+U_x^2+2*V=0 and n^2*U_t^2+U_x^2-2*V=0; real-square nonnegativity forces the same scalar vacuum, and the remaining yy and zz equations force K=0. Conversely those four zero conditions make both tensors zero. Exactly (1/n)_xx=-K/n, so K vanishes on the interval if and only if the positive reciprocal index is affine there. This is a local algebraic compatibility theorem. A full Einstein-scalar solution additionally requires the scalar Euler equation, including V'(U)=0 on the constant branch, and suitable global boundary data. It does not derive a sine-Gordon breather embedding, nonvacuum source, material medium, physical gravity, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GOR-001, C-STG-001, C-LIN-001. Assumptions: The metric signature, covariant component order, Gordon coefficient, Riemann sign, and canonical scalar-stress sign are exactly those of C-GOR-001 and C-STG-001., The velocity is spatially constant, exact, real, and provably subluminal. The scalar has no y or z derivative at the evaluated jet, and n depends only on x., The index, coupling, scalar derivatives, and potential value are exact real quantities with n and kappa positive; floating inputs are outside the exact API., The iff concerns local algebraic Einstein components. Scalar on-shell conservation additionally requires the C-STG-001 Euler equation, and a constant scalar branch requires V'(U)=0 as well as V(U)=0., The reciprocal-affine conclusion is interval-local; positivity restricts the interval so the affine reciprocal has no zero there., No accepted claim identifies U or n with a sine-Gordon breather, supplies transverse localization or boundary data, or turns the effective Gordon metric into physical gravity.. Comparators: SC1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all five predicates, but its copied Gordon sign, rejected five-sixths witness, opposite scalar-potential sign, omitted tx and rest branches, incomplete curvature closure, breather embedding, SC2 handoff, and physical readings are corrected, qualified, or rejected rather than imported.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.130.0` with provenance `campaigns/P178-sc1-gordon-source-compatibility-audit/adjudication.yaml`.

- `campaigns/P178-sc1-gordon-source-compatibility-audit/verify.py`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/attempts/0013/result.yaml`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/attempts/0014/result.yaml`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/attempts/0018/result.yaml`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/attempts/0020/result.yaml`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/reviews/independent_gordon_scalar_review.py`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/reviews/C-GOR-002-claim-review.md`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/reviews/source_adjudication.md`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/evidence/compatibility-audit.yaml`
- `campaigns/P178-sc1-gordon-source-compatibility-audit/evidence/numerical-audit.yaml`
- `memory/vantasner/decisions/C-GOR-002-review.md`
- `src/substrate_framework/gordon_scalar_compatibility.py`
- `src/substrate_framework/gordon_metric.py`
- `tests/test_gordon_scalar_compatibility.py`
- `tests/test_gordon_metric.py`
