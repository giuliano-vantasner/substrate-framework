---
description: Accepted framework claim C-DIM-002
author: framework-registry
created: '2026-08-01T13:33:52Z'
updated: '2026-08-01T13:33:52Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-002
category: claims
confidence: established
status: active
---
# C-DIM-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Over base-dimension rows (M,L,T), the declared primitive columns for a speed c0=(0,1,-1), action S=(1,2,-1), and length a=(0,1,0) form the matrix [[0,1,0],[1,2,1],[-1,-1,0]], which has determinant -1, rank three, and zero kernel. Every target dimension therefore has unique monomial exponents relative to this set. In particular mass, energy, time, density, and stiffness are represented by S/(c0*a), S*c0/a, a/c0, S/(c0*a^4), and S*c0/a^4. Speed and length alone cannot span mass. These statements are local to the declared primitive set and determine neither dimensionless coefficients nor which primitives or values a physical model must select.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-001. Assumptions: Base-dimension rows are ordered as mass, length, and time, and primitive columns as speed, action, and length., Monomial exponent uniqueness is asserted only relative to the declared primitive set., Dimensionless multiplicative coefficients and the physical selection or values of primitives remain unconstrained.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.15.0` with provenance `campaigns/P016-primitive-unit-reduction/adjudication.yaml`.

- `campaigns/P016-primitive-unit-reduction/verify.py`
- `campaigns/P016-primitive-unit-reduction/attempts/0001/result.yaml`
- `campaigns/P016-primitive-unit-reduction/reviews/independent_elimination_review.py`
- `campaigns/P016-primitive-unit-reduction/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-DIM-002-review.md`
- `tests/test_action_scales.py`
