---
description: Accepted framework claim C-MED-003
author: framework-registry
created: '2026-08-04T14:00:00Z'
updated: '2026-08-04T14:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MED-003
category: claims
confidence: established
status: active
---
# C-MED-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on a dimensionless real field u, physical coordinates x and t, exact positive coefficients lambda, T, and mu, and the declared energy-per-length density L=lambda*u_t^2/2-T*u_x^2/2-mu*(1-cos(u)), the Euler-Lagrange equation is lambda*u_tt-T*u_xx+mu*sin(u)=0 and the positive scales are c=sqrt(T/lambda), omega_0=sqrt(mu/lambda), ell=sqrt(T/mu)=c/omega_0, E_scale=sqrt(T*mu), and J_scale=sqrt(lambda*T), with E_scale=omega_0*J_scale. Under base rows (energy,length,time), the coefficient columns (lambda,T,mu) are (1,-1,2), (1,1,0), and (1,-1,0), a full-rank matrix. The coordinate map X=x/ell and tau=omega_0*t sends the dimensional residual exactly to mu times U_tau_tau-U_XX+sin(U). The logarithmic map from coefficients to (c,omega_0,ell) has rank two and right nullspace spanned by (1,1,1): at fixed positive c and omega_0 the inverse coefficient family is (lambda,lambda*c^2,lambda*omega_0^2) for an arbitrary positive lambda. A common coefficient multiplier preserves c, omega_0, ell and the field solution set while multiplying physical energy and canonical action by that factor. This is a conditional continuum cosine model; dimensions, periodicity, ratio closure, or symbol absence does not derive a material, select coefficient values, or remove the common energy/action scale.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-VAR-001, C-DIM-002. Assumptions: The real field is dimensionless, x and t are physical coordinates, and the integrated Lagrangian has energy dimension, so the density has energy-per-length dimension., Lambda, T, and mu are exact, real, constant, and strictly positive. Spatial and temporal boundary terms are admissible for the stated variational and conserved-energy uses., The cosine density and 1+1 continuum description are declared model premises. No microscopic material, coefficient value, lattice cutoff, bath, source, damping, or experimental map is imported., Coordinate, energy, and canonical action scales retain their distinct dimensions; the common coefficient multiplier is not identified by the three kinematic ratios.. Comparators: MC1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64, opened and executed only after P095 froze candidates and structural criteria.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.81.0` with provenance `campaigns/P095-mc1-dimensional-sine-gordon/adjudication.yaml`.

- `campaigns/P095-mc1-dimensional-sine-gordon/verify.py`
- `campaigns/P095-mc1-dimensional-sine-gordon/reviews/independent_dimensional_review.py`
- `campaigns/P095-mc1-dimensional-sine-gordon/evidence/source-reproduction.yaml`
- `campaigns/P095-mc1-dimensional-sine-gordon/evidence/source-audit.yaml`
- `campaigns/P095-mc1-dimensional-sine-gordon/evidence/check-adjudication.yaml`
- `campaigns/P095-mc1-dimensional-sine-gordon/evidence/consumer-audit.yaml`
- `campaigns/P095-mc1-dimensional-sine-gordon/evidence/candidate-comparison.yaml`
- `campaigns/P095-mc1-dimensional-sine-gordon/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MED-003-review.md`
- `tests/test_dimensional_sine_gordon.py`
- `formal/SubstrateFramework/Ingested/Phase27MediumKernel.lean`
