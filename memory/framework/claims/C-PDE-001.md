---
description: Accepted framework claim C-PDE-001
author: framework-registry
created: '2026-08-01T19:57:49Z'
updated: '2026-08-01T19:57:49Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-001
category: claims
confidence: established
status: active
---
# C-PDE-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Adopt the C-SG-001 normalized sine-Gordon potential as a declared dimensionless 3+1 flat-space radial model with action S=4*pi*integral dt dr r^2[u_t^2/2-u_r^2/2-(1-cos(u))]. Its equation is u_tt-u_rr-2*u_r/r+sin(u)=0, with even regularity u_r(0,t)=0. For initial data u(r,0)=3*exp(-(r/4)^2), u_t(r,0)=0, a direct-radial centered leapfrog on 0<=r<=200 and 0<=t<=450 with dr=0.05, dt=0.02, outer Dirichlet data, and a quadratic velocity sponge over 150<r<=200 gives finite-time simulation evidence for a localized oscillatory core. The mean energy inside r<=30 over 360<=t<=430 is more than 0.9318 of its mean over 120<=t<=180, and the late center half-range is greater than 4.34. Hann-FFT and rising-crossing estimates on windows beginning at t=220 and t=300 all give 0.90<omega<0.94, below the linear threshold one. Center traces on dr=0.1, 0.05, and 0.025 self-converge at approximately second order; closed-box total-energy relative ranges decrease from 1.179e-3 to 2.940e-4 to 7.344e-5. Timestep halving, domains 160/200/240, core-radius diagnostics, a regular soluble linear mode, and an independent DOP853 evolution of v=r*u with Simpson energy preserve the verdict. Changing the radial geometric coefficient or using the A=4, width-three dispersive seed breaks the relevant verdict. This is resolution-bounded evidence for the specified finite-time IVP, not an exact or eternal breather, exponential lifetime law, family-wide stability result, gravitational source or radiation statement, absolute-scale prediction, particle model, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `simulation_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-001. Assumptions: The 3+1 radial action is a declared compatible extension of the normalized C-SG-001 potential convention; the exact 1+1 breather solution is not lifted into three dimensions., Coordinates, field, energy, and frequency are dimensionless with linear mass threshold one; no absolute unit conversion is supplied., The sponge is a numerical outer-boundary device and energy conservation is assessed separately in a causally quiet closed box., The quoted frequency and localization bounds are resolution-bounded metrics of this initial-data branch and finite time interval.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.39.0` with provenance `campaigns/P044-p3d1-radial-sine-gordon-oscillon/adjudication.yaml`.

- `campaigns/P044-p3d1-radial-sine-gordon-oscillon/verify.py`
- `campaigns/P044-p3d1-radial-sine-gordon-oscillon/attempts/0001/result.yaml`
- `campaigns/P044-p3d1-radial-sine-gordon-oscillon/reviews/independent_transformed_field_review.py`
- `campaigns/P044-p3d1-radial-sine-gordon-oscillon/reviews/source_adjudication.md`
- `campaigns/P044-p3d1-radial-sine-gordon-oscillon/evidence/source-reproduction.yaml`
- `memory/vantasner/decisions/C-PDE-001-review.md`
- `tests/test_radial_sine_gordon.py`
- `tests/test_numerics.py`
