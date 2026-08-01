---
description: Accepted framework claim C-MED-001
author: framework-registry
created: '2026-08-01T12:07:29Z'
updated: '2026-08-01T12:07:29Z'
tags:
- substrate-framework
- accepted-claim
- C-MED-001
category: claims
confidence: established
status: active
---
# C-MED-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For positive density rho, thermal scale Theta, and reference speed c, the declared co-scaled response laws epsilon=rho*Theta/c^2 and mu_inverse=rho*Theta satisfy epsilon*mu=1/c^2 and give local wave speed sqrt(mu_inverse/epsilon)=c. Density and thermal variations therefore cannot create an index within this ansatz. More generally, the logarithmic sensitivities vanish exactly when the corresponding response exponents match.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The permittivity and inverse permeability response laws are declared constitutive premises with positive inputs., The conclusion is confined to common response scaling and does not derive a separate continuum coupling or physical medium realization.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.8.0` with provenance `campaigns/P008-constitutive-qualification/adjudication.yaml`.

- `campaigns/P008-constitutive-qualification/verify.py`
- `campaigns/P008-constitutive-qualification/attempts/0001/result.yaml`
- `campaigns/P008-constitutive-qualification/reviews/independent_algebra_review.py`
- `memory/vantasner/decisions/C-MED-001-review.md`
- `tests/test_constitutive.py`
