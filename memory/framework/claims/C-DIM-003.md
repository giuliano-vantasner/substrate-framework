---
description: Accepted framework claim C-DIM-003
author: framework-registry
created: '2026-08-01T13:54:42Z'
updated: '2026-08-01T13:54:42Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-003
category: claims
confidence: established
status: active
---
# C-DIM-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Relative to C-DIM-002's declared positive speed c0, action S, and length a, the map from a positive mass m to N_m=m*c0*a/S is dimensionless and bijective, with inverse m=N_m*S/(c0*a). For two masses represented using the same primitive values, m_1/m_2=N_1/N_2. This is a lossless change of coordinates: N_m remains one free dimensionless physics input, so the map predicts no mass or ratio, selects no primitive value, and does not turn a physical import into a derived quantity.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-002. Assumptions: The mass, speed, action, length, and dimensionless coordinate are positive., The speed, action, and length use the same declared primitive basis as C-DIM-002., The coordinate map is a reparameterization and supplies no equation fixing N_m or any primitive value., A ratio cancels shared dimensionful scales but still depends on the corresponding dimensionless coordinates.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.16.0` with provenance `campaigns/P018-imported-mass-coordinate/adjudication.yaml`.

- `campaigns/P018-imported-mass-coordinate/verify.py`
- `campaigns/P018-imported-mass-coordinate/attempts/0001/result.yaml`
- `campaigns/P018-imported-mass-coordinate/reviews/independent_exponent_review.py`
- `campaigns/P018-imported-mass-coordinate/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-DIM-003-review.md`
- `tests/test_action_scales.py`
