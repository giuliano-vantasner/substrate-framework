---
description: Accepted framework claim C-MOM-002
author: framework-registry
created: '2026-08-01T19:03:00Z'
updated: '2026-08-01T19:03:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MOM-002
category: claims
confidence: established
status: active
---
# C-MOM-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let rho(x,y,z,t)=lambda(x,t)*g(y,z), where lambda is centered on the declared x axis with constant monopole M and longitudinal second moment mu(t), while g is a declared time-independent normalized centered axisymmetric transverse profile with per-axis variance sigma^2. Then the Cartesian second moment is diag(mu,M*sigma^2,M*sigma^2). Writing Delta=mu-M*sigma^2, the normalized trace-free moment is I_STF=diag(2*Delta/3,-Delta/3,-Delta/3), and the triple convention is Q=3*I_STF=diag(2*Delta,-Delta,-Delta). For every positive derivative order n, with M and sigma fixed, d^n I_STF/dt^n=diag(2*d^n mu/dt^n/3,-d^n mu/dt^n/3, -d^n mu/dt^n/3), whose Frobenius norm squared is 2*(d^n mu/dt^n)^2/3; the corresponding triple-tensor norm squared is 6*(d^n mu/dt^n)^2. The TT projection of this derivative tensor vanishes along the symmetry axis. Along a perpendicular declared z direction it is diag(d/2,-d/2,0), where d=d^n mu/dt^n, with normalized plus coordinate d/sqrt(2) and cross coordinate zero in the declared x-y basis. Pure trace additions are annihilated. C-SG-009 supplies an exact longitudinal specialization, but this conditional moment construction establishes no 3+1 field solution, momentum flux or spatial stress, local conservation, stability, gravitational action or coupling, retarded dynamics, radiation, detector observable, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-009, C-MOM-001, C-GW-002. Assumptions: The longitudinal and transverse factors are integrable with the stated finite moments, so the required product integrals may be factored., The coordinate origin, longitudinal x axis, and transverse x-y polarization basis for the perpendicular z viewing direction are declared conventions., The transverse variance is per Cartesian axis; its radial second moment is twice sigma^2., M, sigma, and the transverse profile are time-independent when the positive-order derivative formulas are used., The TT statements are algebraic projections under C-GW-002 and import no waveform, flux, gravity, or source-dynamics premise.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.37.0` with provenance `campaigns/P041-fs2-separable-density-stf/adjudication.yaml`.

- `campaigns/P041-fs2-separable-density-stf/verify.py`
- `campaigns/P041-fs2-separable-density-stf/attempts/0001/result.yaml`
- `campaigns/P041-fs2-separable-density-stf/reviews/independent_product_density_review.py`
- `campaigns/P041-fs2-separable-density-stf/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MOM-002-review.md`
- `tests/test_separable_moments.py`
