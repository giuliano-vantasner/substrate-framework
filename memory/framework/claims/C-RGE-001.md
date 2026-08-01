---
description: Accepted framework claim C-RGE-001
author: framework-registry
created: '2026-08-01T14:24:53Z'
updated: '2026-08-01T14:24:53Z'
tags:
- substrate-framework
- accepted-claim
- C-RGE-001
category: claims
confidence: established
status: active
---
# C-RGE-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For positive b0, mu0, and g0, a positive coupling on an interval that satisfies the declared one-loop equation mu*dg/dmu=-b0*g^3/(16*pi^2) with g(mu0)=g0 obeys 1/g(mu)^2=1/g0^2+b0*log(mu/mu0)/(8*pi^2). The formal zero of this inverse coupling is Lambda=mu0*exp(-8*pi^2/(b0*g0^2)). Lambda has zero total logarithmic-scale derivative along the declared flow, whereas its partial derivative with respect to mu0 at fixed g0 is Lambda/mu0. For b0>0, 0<Lambda/mu0<1. This conditional theorem does not derive the beta function or b0 and establishes no physical QCD, confinement, or strong-coupling interpretation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The scale, reference scale, reference coupling, and beta coefficient are positive., The coupling is differentiable and satisfies the declared one-loop ODE on the interval considered., The formal inverse-coupling zero need not lie in a perturbatively controlled regime., RG invariance refers to the total derivative along the coupling flow, not a fixed-coupling partial derivative.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.19.0` with provenance `campaigns/P021-frontier-rg-coordinate/adjudication.yaml`.

- `campaigns/P021-frontier-rg-coordinate/verify.py`
- `campaigns/P021-frontier-rg-coordinate/attempts/0001/result.yaml`
- `campaigns/P021-frontier-rg-coordinate/reviews/independent_flow_review.py`
- `campaigns/P021-frontier-rg-coordinate/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RGE-001-review.md`
- `tests/test_renormalization.py`
