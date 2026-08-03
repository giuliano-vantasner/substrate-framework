---
description: Accepted framework claim C-MED-004
author: framework-registry
created: '2026-08-04T16:00:00Z'
updated: '2026-08-04T16:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MED-004
category: claims
confidence: established
status: active
---
# C-MED-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on a dimensionless real field theta, a physical length coordinate z, a physical time coordinate tau, and an exact positive coefficient g with dimensions 1/(length*time), the mixed-coordinate equation theta_z_tau=g*sin(theta) linearizes at a vacuum to theta_z_tau=g*theta. A plane wave exp(i*(k*z-Omega*tau)) therefore has characteristic k*Omega=g; for positive k its branch Omega=g/k has phase velocity g/k^2, group velocity -g/k^2, tends to infinity as k->0+, and tends to zero as k->infinity, so it has no finite k-independent laboratory angular-frequency floor. With xi=z/L and eta=tau/T, the normalized coefficient is g*L*T. Imposing g*L*T=1 leaves the exact positive family T=1/(g*L) for arbitrary L; its logarithmic scale Jacobian with respect to (L,T) is [1,1], with reciprocal null direction (-1,1). The map X=xi+eta and S=xi-eta sends the equation exactly to theta_SS-theta_XX+sin(theta)=0. Under rows (length,time), the columns (g,alpha,rate,Omega_squared) are (-1,-1), (-1,0), (0,-1), and (0,-2): an inverse-length absorption alpha is neither g nor a laboratory frequency squared and requires a separately supplied inverse-time rate and dimensionless prefactor even to form g. The normalized static kink is a coordinate-map cross-check only. These exact conditional results derive no Maxwell-Bloch reduction, self-induced-transparency regime, optical coefficient, gas or isotope map, material, nonlinear pulse existence, laboratory gap, damping, or absolute scale.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-001, C-DIM-002. Assumptions: Theta is dimensionless, z is a physical length, tau is a physical time, and g is exact, real, constant, strictly positive, and has inverse-length-time dimension., The mixed-coordinate equation is a declared conditional model. No Maxwell-Bloch variables, rotating-wave or sharp-line approximation, absorption formula, damping law, or material is imported by naming tau retarded time., The plane-wave statement uses positive real k and the displayed exp(i*(k*z-Omega*tau)) convention. It is a mixed-coordinate characteristic, not C-SG-018's laboratory Klein-Gordon dispersion., L and T are exact positive coordinate scales. The hyperbolic map uses the displayed orientation; alternative half-scaled light-cone conventions move exact factors and must be transformed explicitly., An absorption coefficient and inverse-time rate, if supplied, remain independent physical imports; dimensional completion alone does not derive their value or optical interpretation.. Comparators: MC3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64 and the cited McCall-Hahn primary records; P097 opened the literature only after freezing coordinate, unit, and interpretation criteria.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.83.0` with provenance `campaigns/P097-mc3-medium-gap-maps/adjudication.yaml`.

- `campaigns/P097-mc3-medium-gap-maps/verify.py`
- `campaigns/P097-mc3-medium-gap-maps/reviews/independent_medium_gap_review.py`
- `campaigns/P097-mc3-medium-gap-maps/evidence/source-reproduction.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/source-audit.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/literature-audit.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/check-adjudication.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/consumer-audit.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/candidate-comparison.yaml`
- `campaigns/P097-mc3-medium-gap-maps/reviews/source_adjudication.md`
- `campaigns/P097-mc3-medium-gap-maps/evidence/primary-provenance.yaml`
- `memory/vantasner/decisions/C-MED-004-review.md`
- `tests/test_mixed_sine_gordon.py`
