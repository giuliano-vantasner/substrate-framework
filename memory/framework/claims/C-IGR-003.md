---
description: Accepted framework claim C-IGR-003
author: framework-registry
created: '2026-08-18T12:01:47+02:00'
updated: '2026-08-18T12:01:47+02:00'
tags:
- substrate-framework
- accepted-claim
- C-IGR-003
category: claims
confidence: established
status: active
---
# C-IGR-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Under C-IGR-001's declared operator, determinant, local-coefficient, matching, constant-mass, and baseline assumptions, declare instead the power-subtracted sharp-cutoff finite-part prescription at a positive scale mu. For constant m2>=0 its exact continuously extended coefficient family is I2=m2*(log(m2/mu^2)+EulerGamma-1) and I3=-(m2^2/2)*(log(m2/mu^2)+EulerGamma-3/2). These are the finite limits after the P230-frozen power and logarithmic subtractions, obey dI3/dm2=-I2, mu*dI2/dmu=-2*m2, and mu*dI3/dmu=m2^2, and vanish continuously at m2=0. The conditional additive shifts use the same typed factors as C-IGR-001. At unit scale and cutoff with m2=0, the sharp, smooth, and power-subtracted I3 values are exactly 1/2, 1, and 0; moreover the finite-part I2 can change sign with m2/mu^2. Therefore P230 derives exact scheme and scale dependence, not a regulator-free coefficient, selected subtraction, finite counterterm, total Newton constant, or physical normalization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GRV-001, C-IGR-001, C-IGR-002. Assumptions: Every operator, mass, determinant, local-truncation, infrared, matching, and additive-baseline assumption of C-IGR-001 remains in force., The displayed power and logarithmic subtraction and positive scale mu define this finite-part scheme; changing a finite subtraction defines a different scheme., Zero mass means the one-sided continuous limit of m2*log(m2), not literal substitution into log(0)., No accepted claim chooses mu, a finite counterterm, a physical regulator, a cutoff identification, field spectrum, or additive baseline.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.161.0` with provenance `campaigns/P230-exact-mass-regulator-rung/adjudication.yaml`.

- `campaigns/P230-exact-mass-regulator-rung/verify.py`
- `campaigns/P230-exact-mass-regulator-rung/reviews/independent_exact_mass_review.py`
- `campaigns/P230-exact-mass-regulator-rung/reviews/C-IGR-003-claim-review.md`
- `campaigns/P230-exact-mass-regulator-rung/evidence/formula-freeze.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/literature-audit.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/candidate-comparison.yaml`
- `campaigns/P230-exact-mass-regulator-rung/evidence/dependency-audit.yaml`
- `campaigns/P230-exact-mass-regulator-rung/attempts/0003/result.yaml`
- `src/substrate_framework/scalar_one_loop_mass.py`
- `tests/test_scalar_one_loop_mass.py`
