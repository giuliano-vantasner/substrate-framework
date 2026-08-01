---
description: Accepted framework claim C-FLX-001
author: framework-registry
created: '2026-08-01T15:50:39Z'
updated: '2026-08-01T15:50:39Z'
tags:
- substrate-framework
- accepted-claim
- C-FLX-001
category: claims
confidence: established
status: active
---
# C-FLX-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on positive flux Phi uniformly crossing a cross-section A that is fixed independently of positive length L, Gauss data give the constant field E=Phi/A. With declared field-energy density E^2/2, stored field energy is U(L)=Phi^2*L/(2A), linear with energy slope sigma_energy=Phi^2/(2A). Separately, for positive endpoint charge q and declared force F=qE, endpoint work is V(L)=q*Phi*L/A, linear with force slope sigma_force=q*Phi/A. The slopes agree if and only if q=Phi/2; for q=Phi the endpoint slope is twice the energy slope. Fixed area is load-bearing: A(L)=A0*(1+L/L0) gives logarithmic field energy, while spherical spreading gives an inverse-square field and curved Coulomb potential. Matching a supplied tension by A_eff=Phi^2/(2*sigma) defines an effective area and does not predict it. This theorem establishes no physical charge, flux tube, vortex-tension identity, QCD, area law, or confinement.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Flux, area, endpoint charge, and length are positive., The field is uniform across the cap and the cross-sectional area is fixed independently of length., Field-energy density is E^2/2 and endpoint force is qE in the declared units., Field energy and endpoint work remain distinct unless q=Phi/2 is separately established., No accepted physical map identifies these ideal variables with the substrate, quarks, QCD, or confinement.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.24.0` with provenance `campaigns/P027-fixed-flux-tube-linearity/adjudication.yaml`.

- `campaigns/P027-fixed-flux-tube-linearity/verify.py`
- `campaigns/P027-fixed-flux-tube-linearity/attempts/0001/result.yaml`
- `campaigns/P027-fixed-flux-tube-linearity/reviews/independent_work_energy_review.py`
- `campaigns/P027-fixed-flux-tube-linearity/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-FLX-001-review.md`
- `tests/test_flux_tube.py`
