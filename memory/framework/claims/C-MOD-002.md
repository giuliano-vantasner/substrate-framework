---
description: Accepted framework claim C-MOD-002
author: framework-registry
created: '2026-08-02T21:00:00Z'
updated: '2026-08-02T21:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MOD-002
category: claims
confidence: established
status: active
---
# C-MOD-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-MOD-001's declared massless radial model, two independent float64 routes give resolution-bounded evidence for the same nontrivial stationary branch and for a finite-box continuum ladder of its complete self-adjoint Hessian. DOP853 shooting from r=10^-4 with r*f'(R)+2*f(R)=0, rtol=10^-10, atol=10^-12, max step 0.02, walls R=12,18,24, and 801,1201,1601 uniform samples gives fitted origin slopes 2.007528281, 2.007528220, 2.007528217 and energy coefficients 1.230872939, 1.231275966, 1.231374077; the relative E2/E4 imbalance falls from 4.65e-4 to 5.81e-5, and independently finite-differenced EOM residuals fall by approximately four under each spacing halving. A consistent-mass linear-FEM generalized eigensolve with tolerance 10^-10 gives lowest squared box frequencies 0.131132401, 0.061072240, and 0.034754127 at those walls, maximum relative algebraic residual below 3e-9, and node counts 0,1,2,3 for the first four modes. An independent solve_bvp collocation route with tolerance 2e-8, Simpson quadrature, and a mass-lumped finite-volume tridiagonal eigensolve agrees on the profiles and lowest levels within 0.07 percent. The positive lowest level decreases under domain growth while its product with R^2 stabilizes; none lies below C-MOD-001's exact zero continuum edge. This is conditional numeric evidence for a stationary profile and wall-quantized continuum, not an existence or uniqueness proof, a positive bound mode, a resonance, a physical Skyrmion, nucleon or Roper, a quantum state, an absolute mass, or a substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MOD-001. Assumptions: Every number is resolution-bounded float64 evidence for the exact declared model and stated solver settings; decimal agreement does not upgrade the result to an analytic half-line existence, uniqueness, or spectral theorem., The shooting branch uses origin data f(epsilon)=pi-C*epsilon and f'(epsilon)=-C plus the massless two-power Robin tail, while the independent collocation route fits the same branch with separately assembled boundary data., The finite-element and finite-volume spectra impose finite-box Dirichlet mode data and are classified only after comparison with C-MOD-001's independently derived half-line continuum edge., No physical comparator, PG3 target eigenvalue, pending B1/E2/E4/S2 unit, quantization rule, or particle dictionary enters branch selection, tolerances, or verdict thresholds.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.56.0` with provenance `campaigns/P062-pg3-roper-radial-mode/adjudication.yaml`.

- `campaigns/P062-pg3-roper-radial-mode/verify.py`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0002/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0003/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0004/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0005/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/reviews/independent_radial_review.py`
- `campaigns/P062-pg3-roper-radial-mode/evidence/source-audit.yaml`
- `memory/vantasner/decisions/C-MOD-002-review.md`
- `tests/test_radial_modes.py`
