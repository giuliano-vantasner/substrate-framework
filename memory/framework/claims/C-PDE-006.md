---
description: Accepted framework claim C-PDE-006
author: framework-registry
created: '2026-08-02T02:05:00Z'
updated: '2026-08-02T02:05:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-006
category: claims
confidence: established
status: active
---
# C-PDE-006

## Statement
The accepted statement is reproduced exactly from the claim registry.

On the C-PDE-005 odd-harmonic system, declare the free branch coordinate a_1(0)=2.5, origin cutoff 0.001, outer radius 40, a decaying Robin condition on the evanescent fundamental, and finite-box Dirichlet data on every radiative harmonic. SciPy adaptive collocation in IEEE float64, initialized with 300 radial points, periodic-DFT projection with 256 temporal samples, tolerance 1e-8, and a fitted frequency constrained to 0<omega<1 completes through retained sets N=1, 3, 5, 7, and 9. The frequencies are 0.976908657117, 0.976876828530, 0.976873949847, 0.976873921614, and 0.976873921394. On a uniform radial audit grid over r<=12 with 1024 temporal phases, the RMS full nonlinear projection remainder falls from 0.105422 to 0.0136221, 0.00145899, 0.000144585, and 1.37187e-5; the N=9 maximum collocation RMS residual is below 1e-8. Initial-mesh 200/300/400, temporal-sample 256/512, and tolerance 1e-8/1e-9 refinements preserve the branch. Walls at radii 30, 40, 50, and 60 keep the fitted frequency within 1e-4 but produce a nonmonotone more-than-twentyfold resonance in the outer third-harmonic r*a_3 RMS, exposing the standing-wave boundary dependence. Independent DOP853 shooting, Gauss-Legendre projected collocation, and second-order finite differences with a three-grid zero-spacing extrapolation reproduce the finite-box core branch and remainder trend. This is numeric evidence for one declared finite-radius, finite-harmonic family point. The central amplitude is not equation-derived, the P3D1 frequency is not an input, and the result establishes no unique eigenfrequency, exponentially localized infinite-domain state, exact or eternal quasibreather, lifetime law, gravity, particle identity, absolute scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-005. Assumptions: All fields, coordinates, frequencies, and residuals use the dimensionless C-PDE-001 convention and the exact projected system and channel meanings of C-PDE-005., The central fundamental amplitude, origin cutoff, finite wall, retained harmonics, temporal projection, and mixed outer conditions are explicit branch and numerical-model data., Core remainder means the RMS of the unretained time-dependent part of sin(u) over the declared r<=12 audit region and uniform temporal phases; it is not an infinite-domain norm., Radiative-mode Dirichlet data define finite-box standing waves, so frequency stability under wall motion does not override the independently observed tail resonance., The accepted C-PDE-001 IVP is only a post-selection comparator and is not identified with this harmonic-balance family point.. Comparators: C-PDE-001 finite-time Gaussian-IVP frequency interval, inspected only after the candidate equations and structural criteria were frozen and never used as a fit target.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.46.0` with provenance `campaigns/P052-qb1-radial-harmonic-balance/adjudication.yaml`.

- `campaigns/P052-qb1-radial-harmonic-balance/verify.py`
- `campaigns/P052-qb1-radial-harmonic-balance/attempts/0011/result.yaml`
- `campaigns/P052-qb1-radial-harmonic-balance/attempts/0010/result.yaml`
- `campaigns/P052-qb1-radial-harmonic-balance/reviews/independent_harmonic_review.py`
- `campaigns/P052-qb1-radial-harmonic-balance/evidence/numerical-audit.yaml`
- `campaigns/P052-qb1-radial-harmonic-balance/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-006-review.md`
- `tests/test_radial_harmonic_balance.py`
- `tests/test_numerics.py`
