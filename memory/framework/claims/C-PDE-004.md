---
description: Accepted framework claim C-PDE-004
author: framework-registry
created: '2026-08-01T20:50:36Z'
updated: '2026-08-01T20:50:36Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-004
category: claims
confidence: established
status: active
---
# C-PDE-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Evolve the C-PDE-001 radial initial data P(r,0)=3*exp(-(r/4)^2), P_t(r,0)=0 together with the regular C-PDE-003 l=2 perturbation psi(r,0)=0.2*(r/4)^2*exp(-(r/4)^2), psi_t(r,0)=0. On the baseline closed domain 0<=r<=80 through 0<=t<=40, a velocity-Verlet evolution of P and v=r*psi with dr=0.1, dt=0.04, homogeneous outer Dirichlet data, and no sponge completes with finite values before boundary reflection. For u=P+epsilon*psi*P2, the first-order energy-density coefficient is h=P_t*psi_t+P_r*psi_r+sin(P)*psi; defining H=4*pi*integral r^4*h dr, exact angular integration gives the triple-STF coefficient Q/epsilon=diag(-H/5,-H/5,2*H/5). The baseline Qzz/epsilon trace has RMS 404.678 and maximum absolute value 680.589, while the final-to-initial mode norm ratio is 0.62297. Meshes dr=0.2, 0.1, and 0.05 give approximately second-order self-convergence of background, mode, Q trace, and closed-box energy error; timestep halving, a causally disconnected domain extension to 100, exact zero/half-amplitude mutations, an exact free spherical-Bessel l=2 box mode, and an independent transformed-variable DOP853 evolution preserve the finite-time nonzero-moment verdict. This is linearized, dimensionless, finite-grid and finite-time simulation evidence for the specified IVP, not a nonlinear stable or periodic l=2 mode, a frequency-doubling result, conserved gravitational source, radiation channel, absolute scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `simulation_evidence`; review is `accepted`; compatibility is `native`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-001, C-PDE-003, C-MOM-003. Assumptions: All fields, coordinates, energies, and moments use the dimensionless C-PDE-001 convention., The perturbation is interpreted only to first order in a formal epsilon; its declared profile amplitude 0.2 fixes the coefficient normalization rather than a finite nonlinear deformation., The homogeneous outer boundary is causally disconnected from the interpreted region over the accepted interval, and no asymptotic or infinite-time limit is inferred., The triple-STF convention and P2 angular normalization are those fixed by C-MOM-003.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.41.0` with provenance `campaigns/P046-p3d3-l2-perturbation-consistency/adjudication.yaml`.

- `campaigns/P046-p3d3-l2-perturbation-consistency/verify.py`
- `campaigns/P046-p3d3-l2-perturbation-consistency/attempts/0004/result.yaml`
- `campaigns/P046-p3d3-l2-perturbation-consistency/reviews/independent_transformed_mode_review.py`
- `campaigns/P046-p3d3-l2-perturbation-consistency/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-004-review.md`
- `tests/test_sine_gordon_l_modes.py`
- `tests/test_radial_sine_gordon.py`
- `tests/test_conserved_moments.py`
