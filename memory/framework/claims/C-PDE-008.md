---
description: Accepted framework claim C-PDE-008
author: framework-registry
created: '2026-08-02T08:45:00Z'
updated: '2026-08-02T08:45:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-008
category: claims
confidence: established
status: active
---
# C-PDE-008

## Statement
The accepted statement is reproduced exactly from the claim registry.

On the accepted finite-box branch C-PDE-006, define the core radial second energy moment S_12(tau)=4*pi*integral_0.001^12 r^4*T00(r,tau) dr and the real series S_12=a_0+sum_k(a_k*cos(k*tau)+b_k*sin(k*tau)). With central fundamental 2.5, wall radius 40, IEEE float64 adaptive collocation initialized by 300 radial points, 256 projection phases, tolerance 1e-8, a separate 2401-point exact-cutoff radial audit grid, and 512 endpoint-excluded phases, the N=1, 3, 5, 7, and 9 values of a_2 are 666.330281099, 591.504983105, 591.470022142, 591.470478411, and 591.470484284. At N=9 the twice-frequency coefficient supplies 0.999865185 of the resolved even coefficient power, the exact C-PDE-007 rule removes odd coefficients, and the time-averaged core per-axis variance is 7.827021539. Temporal samples 256/512/1024, radial samples 1201/2401/4801, initial BVP meshes 200/300/400, and tolerance 1e-8 versus 1e-9 with 512 projection phases preserve a_2 within 0.008. Across the harmonic ladder, the full nonlinear core remainder falls from 0.105185 to 1.36601e-5 and the full-box energy relative range from 0.0581543 to 9.6871e-7. Independent Gauss-Legendre phase and Simpson radial integration gives a_2=591.468056462. Walls 30, 40, 50, and 60 give core coefficients 591.269664499, 591.470484284, 598.370080354, and 590.990332998 and expose a full-box scalar-variance resonance near wall 50. This is numeric evidence for one cutoff scalar moment on one finite-box, finite-harmonic family point. It establishes no wall- independent or infinite-domain line, exact full-PDE periodic solution, universal nonzero twice-frequency theorem, STF quadrupole, physical radiation, gravity, waveform, flux, absolute scale, particle identity, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-006, C-PDE-007. Assumptions: The finite-box branch, dimensionless convention, free central amplitude, origin cutoff, wall data, and harmonic meanings are exactly those of C-PDE-006., The core radius 12, radial second-moment weight, Fourier convention, audit grids, retained bins, and coefficient-power metric are declared diagnostic data., Exact odd-bin absence is inherited from C-PDE-007; all nonzero coefficient values and convergence bounds remain numeric evidence., Radiative-mode walls define standing-wave box data, so bounded core coefficients do not override the measured full-box resonance or establish an infinite-domain limit.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.47.0` with provenance `campaigns/P053-qb2-even-harmonic-energy-spectrum/adjudication.yaml`.

- `campaigns/P053-qb2-even-harmonic-energy-spectrum/verify.py`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/attempts/0007/result.yaml`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/attempts/0006/result.yaml`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/reviews/independent_energy_spectrum_review.py`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/evidence/numerical-audit.yaml`
- `campaigns/P053-qb2-even-harmonic-energy-spectrum/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-008-review.md`
- `tests/test_radial_harmonic_observables.py`
- `tests/test_radial_harmonic_balance.py`
