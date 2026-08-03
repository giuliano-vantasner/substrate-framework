---
description: Accepted framework claim C-DYN-001
author: framework-registry
created: '2026-08-04T09:15:00Z'
updated: '2026-08-04T09:15:00Z'
tags:
- substrate-framework
- accepted-claim
- C-DYN-001
category: claims
confidence: established
status: active
---
# C-DYN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For the declared real linearly damped oscillator q_tt+Gamma*q_t+omega_0^2*q=0 with omega_0>0 and Gamma>=0, the exact characteristic roots are -Gamma/2 +/- sqrt(Gamma^2-4*omega_0^2)/2. The oscillator is underdamped, critically damped, or overdamped according as Gamma is below, equal to, or above 2*omega_0. In the underdamped branch its angular frequency is omega_d=sqrt(omega_0^2-Gamma^2/4), its coordinate amplitude envelope is exp(-Gamma*t/2), and the square of that envelope is exp(-Gamma*t). Its instantaneous mechanical energy E=(q_t^2+omega_0^2*q^2)/2 instead satisfies the exact on-shell balance dE/dt=-Gamma*q_t^2, so it is not pointwise a single exponential. In a declared 1/Gamma quadratic-envelope window the actual oscillation count is omega_d/(2*pi*Gamma); omega_0/(2*pi*Gamma) is only a nominal natural-frequency convention. The actual count tends to zero at critical damping while the nominal count tends to 1/(4*pi). For the normalized damped sine-Gordon linearization psi_tt-psi_xx+psi=-Gamma*psi_t, a real Fourier mode k has omega_0(k)=sqrt(1+k^2)>=1 and critical damping 2*sqrt(1+k^2). A finite-amplitude breather frequency 0<omega_b<1 is therefore not a real linear-mode natural frequency; substituting it can reverse the damping classification. Separately, for positive uniform damping, sufficient regularity, and zero integrated boundary flux, the period-integrated exact energy balance excludes every nontrivial exactly time-periodic finite-energy field. Thus an abstract reduced-coordinate damping classification, a linear field-mode transient, exact nonlinear periodic existence, phase coherence, survival probability, population, and a material or spark/DBD threshold are distinct predicates. No latter interpretation follows without an independently derived coordinate, observable, finite-time classifier, and physical parameter map.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-011, C-SG-012. Assumptions: The abstract oscillator has constant real omega_0>0 and constant real Gamma>=0; underdamped solution and cycle formulas require Gamma<2*omega_0, and 1/Gamma envelope windows require Gamma>0., Coordinate amplitude, quadratic envelope, instantaneous mechanical energy, exact field periodicity, transient ringing, phase coherence, survival, and population retain their declared distinct meanings., The normalized field-mode statement uses C-SG-011's gap-one convention and real spatial wavenumber. It does not assert that a finite-amplitude nonlinear breather is a single Fourier mode., The period-integrated obstruction uses C-SG-012 with sufficient regularity, finite energy, positive uniform damping, exact time periodicity, and vanishing integrated boundary flux. Nonzero flux or drive can balance dissipation and is outside that theorem., Gamma, omega_0, omega_b, k, and time remain normalized variables. No material, collision, density, thermal, phase-noise, discharge, or physical-unit map is imported.. Comparators: LB2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its body had already been exposed during P091, while P092 froze structural criteria before execution, output, additional consumers, or physical comparator values.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.79.0` with provenance `campaigns/P092-lb2-coherence-threshold/adjudication.yaml`.

- `campaigns/P092-lb2-coherence-threshold/verify.py`
- `campaigns/P092-lb2-coherence-threshold/reviews/independent_oscillator_review.py`
- `campaigns/P092-lb2-coherence-threshold/evidence/source-reproduction.yaml`
- `campaigns/P092-lb2-coherence-threshold/evidence/source-audit.yaml`
- `campaigns/P092-lb2-coherence-threshold/evidence/consumer-audit.yaml`
- `campaigns/P092-lb2-coherence-threshold/evidence/candidate-comparison.yaml`
- `campaigns/P092-lb2-coherence-threshold/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-DYN-001-review.md`
- `tests/test_damped_oscillator.py`
