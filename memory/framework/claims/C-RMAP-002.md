---
description: Accepted framework claim C-RMAP-002
author: framework-registry
created: '2026-08-07T12:30:00Z'
updated: '2026-08-07T12:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RMAP-002
category: claims
confidence: established
status: active
---
# C-RMAP-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RMAP-001 and on the exact declared rational map R_4(z)=(z^4+2*i*sqrt(3)*z^2+1)/(z^4-2*i*sqrt(3)*z^2+1), exact polynomial reduction makes the numerator and denominator coprime and the map degree four. Homogeneous-Wronskian tensor Gauss-Legendre cubature on u=cos(theta),phi at orders 16x32 through 64x128 gives normalized pullback area converging to four and angular functional converging to 20.6496264884189 in IEEE-754 binary64/complex128. An independent nested adaptive integration split between direct and reciprocal stereographic charts at relative and absolute tolerances 1e-7, 1e-9, and 1e-11 agrees within 2e-12 relative. Axis rotations preserve the two integrals, while changing the imaginary quadratic coefficient to 3.2*i preserves degree area and changes I to about 20.7744. This is resolution-bounded evidence for one declared map only; it proves neither full cubic symmetry nor global degree-four minimality and supplies no radial solution, physical state, baryon or nucleus identification, energy, mass, binding, reaction, yield, material, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RMAP-001. Assumptions: All C-RMAP-001 sphere, orientation, normalization, and mathematical-import assumptions hold., The numerator and denominator coefficients are exactly the displayed algebraic numbers; floating-point cubature receives their complex128 evaluation after exact coprimality and degree are established separately., Tensor orders, adaptive tolerances, direct/reciprocal chart split, homogeneous Wronskian, binary64 precision, finite solver outputs, degree-area error, and successive-value error are part of the evidence and bound its status., Agreement of two numerical methods and symmetry-preserving rotations is resolution-bounded verification, not an exact closed form for I[R_4]., The coefficient mutation and shifted-map comparator test load-bearing inputs but do not constitute a global fixed-degree variational search., Names such as cubic, alpha, or B=4 do not establish a full symmetry group, physical Skyrmion, baryon, nucleus, or nuclear reaction.. Comparators: E1's source value 20.63 and its cited literature neighborhood; P104's structural selection and tolerances were frozen before source execution, and the source value is rejected as a final accuracy oracle.

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
- `memory/vantasner/decisions/C-RMAP-002-review.md`
- `tests/test_rational_maps.py`
