---
description: Accepted framework claim C-VTX-001
author: framework-registry
created: '2026-08-01T15:41:27Z'
updated: '2026-08-01T15:41:27Z'
tags:
- substrate-framework
- accepted-claim
- C-VTX-001
category: claims
confidence: established
status: active
---
# C-VTX-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For positive g, lambda, and v and positive integer n, declare the radial Abelian-Higgs convention phi=f(r)*exp(i*n*theta), A_theta=a(r)/(g*r), and energy per unit length 2*pi*integral r*dr*[f'^2/2+f^2*(n-a)^2/(2*r^2) +(a'/r)^2/(2*g^2)+lambda*(f^2-v^2)^2/4]. Exact variation gives f''+f'/r-f*(n-a)^2/r^2-lambda*f*(f^2-v^2)=0 and a''-a'/r+g^2*(n-a)*f^2=0. If f approaches v, finite angular energy uniquely requires a to approach n; the declared connection then has flux 2*pi*n/g, while the ungauged positive-winding profile has a logarithmic divergence. Vacuum linearization gives vector and scalar inverse lengths g*v and v*sqrt(2*lambda), both tending to zero as v tends to zero. This conditional model establishes no substrate, dual, chromoelectric, QCD, or confinement identity and no vortex existence.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The radial Abelian-Higgs functional and cylindrical ansatz are declared model premises., The convention A_theta=a/(g*r) and its gauge kinetic normalization are used consistently., Profiles are sufficiently smooth on positive radius and have the stated asymptotic limits., Finite-energy flux reasoning assumes positive vacuum amplitude and positive integer winding., No accepted physical map identifies this Abelian model with the substrate, QCD, or confinement.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.23.0` with provenance `campaigns/P026-abelian-higgs-vortex/adjudication.yaml`.

- `campaigns/P026-abelian-higgs-vortex/verify.py`
- `campaigns/P026-abelian-higgs-vortex/attempts/0004/result.yaml`
- `campaigns/P026-abelian-higgs-vortex/reviews/independent_finite_difference_review.py`
- `campaigns/P026-abelian-higgs-vortex/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-VTX-001-review.md`
- `tests/test_abelian_higgs_vortex.py`
