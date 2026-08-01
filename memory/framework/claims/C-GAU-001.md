---
description: Accepted framework claim C-GAU-001
author: framework-registry
created: '2026-08-01T16:27:00Z'
updated: '2026-08-01T16:27:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GAU-001
category: claims
confidence: established
status: active
---
# C-GAU-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-U1-001's smooth complex scalar, a positive coupling e, and a declared real local-U(1) connection A_mu, define D_mu=partial_mu-i*e*A_mu and transform Psi'=exp(i*e*chi)Psi, A_mu'=A_mu+partial_mu chi for arbitrary smooth real chi. Then D_mu Psi transforms covariantly, a phase-independent potential and (D_mu Psi)^*D^mu Psi are invariant, and in C-U1-001's current convention the kinetic expansion is the bare term plus e*A_mu*j^mu+e^2*A_mu*A^mu*|Psi|^2. The curvature F_mu_nu=partial_mu A_nu-partial_nu A_mu is invariant and [D_mu,D_nu]Psi=-i*e*F_mu_nu*Psi. Separately, conditional on nonzero asymptotic amplitude, integer phase winding N, and angular energy with logarithmic coefficient proportional to (N-e*A_theta*r)^2, finite energy forces flux 2*pi*N/e; its charge-e holonomy is +1. A minus-one holonomy requires a separately declared fractional flux. Local covariance leaves every F^2 coefficient unconstrained and establishes no gauge kinetic action, Maxwell equation, photon, force, physical electric charge, or substrate electromagnetic sector.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-U1-001. Assumptions: The complex scalar, its conjugate, the real connection, and gauge parameter are smooth and mixed partial derivatives commute., The metric signature and Noether-current sign are exactly those of C-U1-001., The local transformation law and positive coupling are declared model structure., The flux clause additionally assumes integer phase winding, nonzero asymptotic amplitude, the stated angular-energy coefficient, and a loop enclosing the winding., Fractional flux, gauge-field dynamics, kinetic normalization, and every physical electromagnetic interpretation require separate premises.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.26.0` with provenance `campaigns/P030-em2-local-u1/adjudication.yaml`.

- `campaigns/P030-em2-local-u1/verify.py`
- `campaigns/P030-em2-local-u1/attempts/0001/result.yaml`
- `campaigns/P030-em2-local-u1/reviews/independent_sign_commutator_review.py`
- `campaigns/P030-em2-local-u1/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-GAU-001-review.md`
- `tests/test_gauge_u1.py`
- `tests/test_u1_charge.py`
