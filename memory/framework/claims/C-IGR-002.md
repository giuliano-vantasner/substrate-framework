---
description: Accepted framework claim C-IGR-002
author: framework-registry
created: '2026-08-18T12:01:47+02:00'
updated: '2026-08-18T12:01:47+02:00'
tags:
- substrate-framework
- accepted-claim
- C-IGR-002
category: claims
confidence: established
status: active
---
# C-IGR-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Under C-IGR-001's declared operator, determinant, local-coefficient, matching, constant-mass, and baseline assumptions, replace the sharp cutoff by the explicitly declared smooth proper-time weight exp(-1/(Lambda^2*tau)). For positive Lambda, m2>=0, and z=m2/Lambda^2, the exact coefficient integrals are I2=2*Lambda^2*sqrt(z)*K1(2*sqrt(z)) and I3=2*Lambda^4*z*K2(2*sqrt(z)), continuously extended at m2=0. They obey dI3/dm2=-I2, have massless values Lambda^2 and Lambda^4, and decay for large mass. The conditional additive coefficients are the same typed compositions Delta(1/G)=N*(1-6*xi)*I2/(12*pi) and Delta(rho)=-(N/2)*(4*pi)^-2*I3. The exact massless I3 value is twice C-IGR-001's sharp value at the same Lambda, so this claim exposes rather than removes regulator dependence and establishes no physical regulator selection or total gravitational normalization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GRV-001, C-IGR-001. Assumptions: Every operator, mass, determinant, local-truncation, infrared, matching, and additive-baseline assumption of C-IGR-001 remains in force., The smooth essential-singularity weight and positive cutoff are explicit regulator data, not a derived or preferred physical scheme., The standard exact modified-Bessel integral representation is an approved mathematical import and numerical quadrature is corroboration only., The result selects no cutoff identification, renormalization condition, total Newton constant, sourced geometry, or empirical comparator.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.161.0` with provenance `campaigns/P230-exact-mass-regulator-rung/adjudication.yaml`.

- `campaigns/P230-exact-mass-regulator-rung/verify.py`
- `campaigns/P230-exact-mass-regulator-rung/reviews/independent_exact_mass_review.py`
- `campaigns/P230-exact-mass-regulator-rung/reviews/C-IGR-002-claim-review.md`
- `campaigns/P230-exact-mass-regulator-rung/evidence/formula-freeze.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/candidate-comparison.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/dependency-audit.yaml`
- `campaigns/P230-exact-mass-regulator-rung/attempts/0003/result.yaml`
- `src/substrate_framework/scalar_one_loop_mass.py`
- `tests/test_scalar_one_loop_mass.py`
