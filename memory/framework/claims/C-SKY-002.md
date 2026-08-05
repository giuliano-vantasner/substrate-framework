---
description: Accepted framework claim C-SKY-002
author: framework-registry
created: '2026-08-11T11:20:00Z'
updated: '2026-08-11T11:20:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SKY-002
category: claims
confidence: established
status: active
---
# C-SKY-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let G be an exact real 3-by-4 matrix with rows g_i, let D=G*G^T, and declare the pointwise quadratic and quartic static densities e2=tr(D) and e4=((tr(D))^2-tr(D^2))/2. Then e2 is the sum of the twelve squared gradient components and e4 is exactly the sum over i<j and a<b of (g_i,a*g_j,b-g_i,b*g_j,a)^2, so e2+e4 is nonnegative. Separately, declare the exact real symmetric four-component kinetic mass operator M=2*((1+tr(D))*I_4-G^T*G). For every exact real tangent w, w^T*(M-2*I_4)*w is exactly twice the sum over i and a<b of (w_a*g_i,b-w_b*g_i,a)^2. Hence M>=2*I_4, and the coefficient two is sharp because gradients and tangent parallel to one component saturate it. For positive integrated two- and four-derivative energies, the declared full-space scale family phi_alpha(x)=phi(x/alpha) has E(alpha)=alpha*E2+E4/alpha, slope E2-E4 and curvature 2*E4 at alpha=1; positive scale curvature does not supply the separate stationarity equation E2=E4. These are exact conditional pointwise and scaling identities. They do not derive a physical Skyrme action or normalization, a unit-vector constraint consequence, topology or boundary conditions, a stationary finite or continuum field, static Hessian positivity, a strict local minimum, a rotating relative equilibrium, gyroscopic terms, linear or nonlinear stability, fission, gravity, radiation, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: G and w have exactly the displayed finite shapes and exact explicitly real entries; floating-point inputs require a separate error analysis., The formulas for e2, e4, and M are declared algebraic data. The claim does not derive them from an accepted action, field normalization, constraint, or spacetime convention., Square nonnegativity uses the ordinary real Euclidean component metric. Indefinite, complex, curved-target, or weighted metrics define different identities., The mass bound concerns the declared pointwise kinetic quadratic form only. It neither proves positivity of a static energy Hessian nor removes constraints, gyroscopic terms, or non-self-adjoint effects from a rotating linearization., The Derrick statement assumes positive finite integrated E2 and E4 and the exact full-space scaling law. Finite boxes, lattice interpolation, boundaries, and nonstationary fields require separate residual and convergence analysis., Applying the theorem to TX5 retains only its displayed algebraic density and mass formulas; TX5's source field fails its own stationarity prerequisite and has no complete constrained Hessian.. Comparators: TX5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64, whose pointwise mass formula and Derrick identity survive while its six-random-direction full-field minimum and dynamic-stability conclusions are refuted by P184, C-SYM-001 independently states that a positive kinetic metric preserves but does not create Hessian zero modes and requires stationarity before symmetry tangents become Hessian zeros.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.136.0` with provenance `campaigns/P184-tx5-full-field-stability-audit/adjudication.yaml`.

- `campaigns/P184-tx5-full-field-stability-audit/verify.py`
- `campaigns/P184-tx5-full-field-stability-audit/reviews/independent_skyrme_o4_review.py`
- `campaigns/P184-tx5-full-field-stability-audit/reviews/replay_source_graph.py`
- `campaigns/P184-tx5-full-field-stability-audit/reviews/C-SKY-002-claim-review.md`
- `campaigns/P184-tx5-full-field-stability-audit/reviews/source_adjudication.md`
- `campaigns/P184-tx5-full-field-stability-audit/attempts/0004/diagnose_declared_resolution_descent.py`
- `campaigns/P184-tx5-full-field-stability-audit/attempts/0004/result.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/attempts/0005/result.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/attempts/0007/result.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/attempts/0008/result.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/evidence/input-provenance.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/evidence/dependency-audit.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/evidence/consumer-audit.yaml`
- `campaigns/P184-tx5-full-field-stability-audit/evidence/primary-provenance.yaml`
- `src/substrate_framework/skyrme_o4.py`
- `tests/test_skyrme_o4.py`
