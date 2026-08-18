---
description: Accepted framework claim C-IGR-001
author: framework-registry
created: '2026-08-18T12:01:47+02:00'
updated: '2026-08-18T12:01:47+02:00'
tags:
- substrate-framework
- accepted-claim
- C-IGR-001
category: claims
confidence: established
status: active
---
# C-IGR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GRV-001's independent additive inverse-coupling baseline ledger, separately declare a positive self-adjoint boundaryless four-dimensional Euclidean real-scalar Laplace-type operator D_E=-nabla_E^2+xi*R_E+m2 with spacetime-constant m2>=0, adequate infrared convergence or reference subtraction, Gamma_E=(1/2)*ln(det(D_E)), heat-kernel prefactor (4*pi)^-2, and Euclidean Einstein-Hilbert matching factor 16*pi. For a positive sharp proper-time cutoff Lambda with tau0=Lambda^-2 and z=m2/Lambda^2, the exact local curvature and vacuum coefficient integrals are I2=Lambda^2*(exp(-z)-z*E1(z)) and I3=Lambda^4*exp(-z)/2-m2*I2/2, continuously extended at m2=0. They obey dI3/dm2=-I2, have massless values Lambda^2 and Lambda^4/2, and decay in the large-mass limit. For positive integer N and exact xi, the declared conditional additive coefficients are Delta(1/G)=N*(1-6*xi)*I2/(12*pi) and Delta(rho)=-(N/2)*(4*pi)^-2*I3. These are exact local coefficient families, not a full or nonlocal determinant, varying-mass theorem, selected regulator, cutoff ontology, total Newton constant, attractive- gravity result, sourced geometry, or empirical prediction.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GRV-001. Assumptions: The operator, scalar statistics, determinant sign and weight, heat-kernel and Einstein-Hilbert conventions, and sharp regulator are declared conditional inputs rather than derived substrate physics., The mass-squared input is exact, nonnegative, and spacetime constant; an x-dependent V'' background cannot be factored into these integrals., The determinant reading requires a positive self-adjoint operator and adequate infrared convergence or an explicit reference subtraction., Only the displayed local coefficient classes are retained; tau^-1, higher heat-kernel, nonlocal, boundary, and full-spectrum terms remain outside the claim., C-GRV-001's independent baseline B remains free in 1/G_total=B+Delta(1/G), and no total sign or physical value follows.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.161.0` with provenance `campaigns/P230-exact-mass-regulator-rung/adjudication.yaml`.

- `campaigns/P230-exact-mass-regulator-rung/verify.py`
- `campaigns/P230-exact-mass-regulator-rung/reviews/independent_exact_mass_review.py`
- `campaigns/P230-exact-mass-regulator-rung/reviews/C-IGR-001-claim-review.md`
- `campaigns/P230-exact-mass-regulator-rung/evidence/formula-freeze.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/literature-audit.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/candidate-comparison.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/dependency-audit.yaml`
- `campaigns/P230-exact-mass-regulator-rung/attempts/0003/result.yaml`
- `src/substrate_framework/scalar_one_loop_mass.py`
- `tests/test_scalar_one_loop_mass.py`
