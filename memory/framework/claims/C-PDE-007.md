---
description: Accepted framework claim C-PDE-007
author: framework-registry
created: '2026-08-02T08:45:00Z'
updated: '2026-08-02T08:45:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-007
category: claims
confidence: established
status: active
---
# C-PDE-007

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the dimensionless radial sine-Gordon convention of C-PDE-005, let H be a finite set of positive odd integers and let u(r,tau)=sum_(n in H) a_n(r)*cos(n*tau), where tau=omega*t. Then u, u_t, and u_r reverse sign under tau->tau+pi, while the canonical energy density T00=(u_t^2+u_r^2)/2+1-cos(u) is invariant. Therefore T00 has half the field period and every odd temporal Fourier coefficient of T00, and of any defined time-independent radial linear functional of T00, vanishes exactly. This selection rule permits only DC and even harmonics; it does not require any allowed coefficient to be nonzero, lowest, or dominant. In particular, for the local single-mode field u=a(r)*cos(tau), the cos(2*tau) coefficient is a_r^2/4-omega^2*a^2/4+2*J_2(a), so the gradient, kinetic, and potential terms can cancel while a higher even coefficient remains nonzero. For every radial energy density with finite second moment, C-MOM-003 gives I_ij=(delta_ij/3)*4*pi*integral r^4*T00 dr and identically zero STF part at each phase. These exact kinematic and Fourier statements do not establish that the ansatz solves the full PDE, a nonzero STF source, physical radiation, gravity, waveform, flux, absolute scale, particle identity, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-005, C-MOM-003. Assumptions: The finite odd-cosine ansatz, common phase origin, physical time derivative, canonical potential convention, and radial regularity are those of C-PDE-005 and its dependency closure., The amplitudes and radial functionals are sufficiently differentiable and integrable for every displayed derivative, Fourier coefficient, and moment to exist., The spherical STF conclusion uses the normalized moment convention of C-MOM-003; a nonzero anisotropic source would be different input data., Half-period selection is kinematic and applies even to an odd-harmonic non-solution, so it is not an equation-residual or existence oracle.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.47.0` with provenance `campaigns/P053-qb2-even-harmonic-energy-spectrum/adjudication.yaml`.

- `campaigns/P053-qb2-even-harmonic-energy-spectrum/verify.py`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/attempts/0007/result.yaml`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/attempts/0006/result.yaml`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/reviews/independent_energy_spectrum_review.py`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-007-review.md`
- `tests/test_radial_harmonic_observables.py`
