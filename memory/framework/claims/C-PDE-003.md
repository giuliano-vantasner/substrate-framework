---
description: Accepted framework claim C-PDE-003
author: framework-registry
created: '2026-08-01T20:50:36Z'
updated: '2026-08-01T20:50:36Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-003
category: claims
confidence: established
status: active
---
# C-PDE-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the dimensionless 3+1 sine-Gordon model of C-PDE-001, let P(r,t) satisfy the radial equation and let Y=P2(cos(theta)) with Delta_Omega Y=-6*Y. The finite multiplicative ansatz u=P*(1+a*Y) has exact full-field residual sin(P*(1+a*Y))-(1+a*Y)*sin(P)+6*a*P*Y/r^2. Its coefficient at first order in a is Y*(P*cos(P)-sin(P)+6*P/r^2), so the ansatz is not a generic solution; moreover its l=2 coefficient is nonregular wherever P(0,t) is nonzero. The correct infinitesimal ansatz u=P+epsilon*psi(r,t)*Y obeys at first order psi_tt-psi_rr-2*psi_r/r+6*psi/r^2+cos(P)*psi=0, with psi=O(r^2) at the origin. For v=r*psi this is v_tt=v_rr-6*v/r^2-cos(P)*v with v=O(r^3). At second order the multiplicative ansatz contains P4 harmonic leakage because P2^2=P0/5+2*P2/7+18*P4/35. These are exact field-equation statements, not a nonlinear mode-existence, stability, periodicity, gravity, or radiation theorem.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-001. Assumptions: The full spherical-coordinate equation and dimensionless potential convention are exactly those of C-PDE-001., P is any sufficiently differentiable radial solution on r>0 with the accepted even origin regularity., P2 uses the z-axis convention (3*cos(theta)^2-1)/2, and epsilon denotes a formal infinitesimal expansion parameter.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.41.0` with provenance `campaigns/P046-p3d3-l2-perturbation-consistency/adjudication.yaml`.

- `campaigns/P046-p3d3-l2-perturbation-consistency/verify.py`
- `campaigns/P046-p3d3-l2-perturbation-consistency/attempts/0004/result.yaml`
- `campaigns/P046-p3d3-l2-perturbation-consistency/reviews/independent_transformed_mode_review.py`
- `campaigns/P046-p3d3-l2-perturbation-consistency/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-003-review.md`
- `tests/test_sine_gordon_l_modes.py`
