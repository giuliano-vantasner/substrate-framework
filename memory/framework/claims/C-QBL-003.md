---
description: Accepted framework claim C-QBL-003
author: framework-registry
created: '2026-08-01T17:01:00Z'
updated: '2026-08-01T17:01:00Z'
tags:
- substrate-framework
- accepted-claim
- C-QBL-003
category: claims
confidence: established
status: active
---
# C-QBL-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-QBL-001 and the declared whole-line scalar energy E[f]=integral dx*[f_x^2/2+kappa^2*f^2/2-f^4/48], its positive quartic profile has unconstrained scalar Hessian L=-d_x^2+kappa^2-6*kappa^2*sech^2(kappa*(x-x0)). On L2(R), the complete discrete spectrum below the continuum threshold kappa^2 consists of exactly two simple levels: lambda_0=-3*kappa^2 with even nodeless mode proportional to sech^2(kappa*(x-x0)), and lambda_1=0 with odd one-node mode proportional to sech(kappa*(x-x0))*tanh(kappa*(x-x0)). The zero mode is exactly the translation tangent of the background. A terminating s=2 to s=1 to free partner factorization proves completeness, and the essential continuum begins at kappa^2. The negative and zero Hessian levels are not positive particle masses or generations; this scalar operator alone establishes no fixed-charge, spectral, orbital, or nonlinear Q-ball stability, exact-sine spectrum, Standard-Model quantum numbers, flavor tower, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-QBL-001. Assumptions: The quartic whole-line scalar energy functional is a declared model premise consistent with C-QBL-001's profile equation., Perturbations are real scalar L2 functions on the whole line and the operator uses its standard self-adjoint domain., Kappa is positive because the frequency remains in C-QBL-001's open domain., Completeness concerns this one unconstrained scalar Hessian only, not the coupled complex phase and fixed-charge perturbation problem., No mass, quantization, particle-family, flavor, or Standard-Model quantum-number dictionary is implied by a Hessian eigenvalue.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.29.0` with provenance `campaigns/P033-fg2-quartic-fluctuation-spectrum/adjudication.yaml`.

- `campaigns/P033-fg2-quartic-fluctuation-spectrum/verify.py`
- `campaigns/P033-fg2-quartic-fluctuation-spectrum/attempts/0001/result.yaml`
- `campaigns/P033-fg2-quartic-fluctuation-spectrum/reviews/independent_factorization_review.py`
- `campaigns/P033-fg2-quartic-fluctuation-spectrum/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-QBL-003-review.md`
- `tests/test_qball_fluctuations.py`
- `tests/test_quartic_qball.py`
