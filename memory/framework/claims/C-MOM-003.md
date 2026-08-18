---
description: Accepted framework claim C-MOM-003
author: framework-registry
created: '2026-08-01T20:21:47Z'
updated: '2026-08-01T20:21:47Z'
tags:
- substrate-framework
- accepted-claim
- C-MOM-003
category: claims
confidence: established
status: active
---
# C-MOM-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let rho(r) be any radial density for which J=integral_R3 rho(r)*r^2 d^3x exists, and define I_ij=integral_R3 rho(r)*x_i*x_j d^3x. Exact sphere integration gives integral_S2 n_i*n_j dOmega=(4*pi/3)*delta_ij and hence I_ij=(J/3)*delta_ij. Therefore Tr(I)=J, the normalized tensor I_STF=I-delta*Tr(I)/3 is identically zero, and the triple convention Q=3*I_STF is identically zero. For the axisymmetric deformation rho=f(r)*(1+a*P2(cos(theta))) with the same scalar J, the exact guard is I_STF=diag(-a*J/15,-a*J/15,2*a*J/15) and Q=diag(-a*J/5,-a*J/5,2*a*J/5), which is nonzero when a*J is nonzero and returns to the spherical null at a=0. These are moment-kinematic identities. They define no gravitational dynamics and do not by themselves establish physical radiation, non-radiation, or a required dynamical l=2 channel.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MOM-001. Assumptions: The radial density has a finite scalar second radial moment J; positivity is not required for the angular identity., The z axis defines the P2 deformation convention, and P2(mu)=(3*mu^2-1)/2., The normalized and triple STF conventions are those fixed by C-MOM-001.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.40.0` with provenance `campaigns/P045-p3d2-spherical-stf-null/adjudication.yaml`.

- `campaigns/P045-p3d2-spherical-stf-null/verify.py`
- `campaigns/P045-p3d2-spherical-stf-null/attempts/0003/result.yaml`
- `campaigns/P045-p3d2-spherical-stf-null/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MOM-003-review.md`
- `tests/test_conserved_moments.py`
