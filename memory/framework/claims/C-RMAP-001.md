---
description: Accepted framework claim C-RMAP-001
author: framework-registry
created: '2026-08-07T12:30:00Z'
updated: '2026-08-07T12:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RMAP-001
category: claims
confidence: established
status: active
---
# C-RMAP-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let S^2 carry its oriented unit round metric and normalized average <F>=(1/(4*pi))*integral_{S^2} F dOmega, with stereographic coordinate z=tan(theta/2)*exp(i*phi). For a declared nonconstant coprime holomorphic rational map R(z)=p(z)/q(z) of exact algebraic degree B>=1, define its conformal Jacobian J_R=((1+|z|^2)/(1+|R|^2)*|dR/dz|)^2, understood in a homogeneous polynomial representation at target poles. The pullback-area identity gives <J_R>=B. Hence the angular functional I[R]=<J_R^2> obeys I[R]>=B^2, with exact deficit I[R]-B^2=<(J_R-B)^2>. Polynomial degree is assigned only after exact common-factor cancellation. For the axial map R(z)=z^B, explicit radial substitution and Euler-beta integration give I_B=(B^3/3)*(1+Gamma(2-1/B)*Gamma(2+1/B)); in particular I_1=1 and I_2=pi+8/3 exactly. These conditional sphere-geometric results do not select a global fixed-degree minimizer, derive a physical Skyrme action or rational-map ansatz, solve a radial profile, identify map degree with a physical baryon or nucleus, or supply a mass, binding energy, reaction, yield, material, or observation map.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The domain and target are oriented unit round two-spheres with the displayed stereographic coordinate, measure, complex-derivative convention, and normalization., With u=cos(theta), sin(theta)*dtheta=-du; a positive u integral runs from -1 to 1 only after reversing the bounds transformed from theta in [0,pi]., The numerator and denominator are exact nonzero complex polynomials, have no common nonconstant factor after reduction, and define a nonconstant holomorphic map of positive integer degree. Antiholomorphic maps or other orientations require a separate sign convention., The pullback area/degree theorem, Euler beta/gamma identities, and nonnegativity of a real square are declared standard mathematical imports. No physical field theory is imported by using rational-map terminology., The axial formula evaluates the supplied family R=z^B. It is not a theorem that this family minimizes I among all maps of degree B., Compatibility at B=1 with C-MOD-001 concerns only the coefficient I=1 in a separately declared radial functional; it does not derive the general rational-map energy or physical action., Algebraic degree, topological degree, physical baryon number, nuclear species, and observed state are distinct unless an accepted model and state map explicitly connect them.. Comparators: E1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; values and map labels were exposed before source execution, while P104 froze exact transformations, methods, mutations, and interpretation ceilings before body inspection.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.88.0` with provenance `campaigns/P104-e1-rational-map-angular-audit/adjudication.yaml`.

- `campaigns/P104-e1-rational-map-angular-audit/verify.py`
- `campaigns/P104-e1-rational-map-angular-audit/reviews/independent_rational_map_review.py`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/source-reproduction.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/source-audit.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/check-adjudication.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/dependency-audit.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/consumer-audit.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/candidate-comparison.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/evidence/primary-provenance.yaml`
- `campaigns/P104-e1-rational-map-angular-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RMAP-001-review.md`
- `tests/test_rational_maps.py`
