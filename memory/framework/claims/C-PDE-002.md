---
description: Accepted framework claim C-PDE-002
author: framework-registry
created: '2026-08-01T20:21:47Z'
updated: '2026-08-01T20:21:47Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-002
category: claims
confidence: established
status: active
---
# C-PDE-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

For the finite-time radial sine-Gordon branch of C-PDE-001, define the cutoff core energy-radius moment S_R(t)=4*pi*integral_0^R r^4*T00(r,t) dr. On the baseline domain 0<=r<=200, 0<=t<=450, dr=0.05, dt=0.02, and for each core cutoff R=20, 25, or 30, the detrended moment has a resolved dominant frequency near twice the contemporaneous center-field fundamental. On windows beginning at t=220 and t=300, detrended Hann/quadratic FFT and quadratically interpolated prominent-maximum estimates give moment to field frequency ratios between 1.995 and 2.005; the baseline R=30 moment frequencies lie between 1.83 and 1.85 and its relative half-range exceeds 0.25. Meshes dr=0.1, 0.05, 0.025, timestep halving, domains 160/200/240, and an independent dr=0.2 DOP853 method-of-lines route preserve the near-two verdict. The relation is cutoff- and resolution-bounded: at R=40 radiative-shell drift dominates the FFT, and the weak dispersive seed has no combined persistent-core verdict. This is a finite-time scalar diagnostic, not exact frequency doubling, a global moment theorem, conserved charge, gravitational quadrupole, radiation result, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `simulation_evidence`; review is `accepted`; compatibility is `native`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-001. Assumptions: The field equation, initial data, boundary treatment, dimensionless convention, and finite-time epistemic ceiling are exactly those of C-PDE-001., The core cutoff is part of the diagnostic and is restricted to 20 through 30; no R-to-infinity claim is made., Linear detrending removes only the fitted slow drift on each stated analysis window; both frequency estimators operate on the same centered timestamps.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.40.0` with provenance `campaigns/P045-p3d2-spherical-stf-null/adjudication.yaml`.

- `campaigns/P045-p3d2-spherical-stf-null/verify.py`
- `campaigns/P045-p3d2-spherical-stf-null/attempts/0003/result.yaml`
- `campaigns/P045-p3d2-spherical-stf-null/reviews/independent_moment_frequency_review.py`
- `campaigns/P045-p3d2-spherical-stf-null/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-002-review.md`
- `tests/test_radial_sine_gordon.py`
