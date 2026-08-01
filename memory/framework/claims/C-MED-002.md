---
description: Accepted framework claim C-MED-002
author: framework-registry
created: '2026-08-01T13:33:52Z'
updated: '2026-08-01T13:33:52Z'
tags:
- substrate-framework
- accepted-claim
- C-MED-002
category: claims
confidence: established
status: active
---
# C-MED-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on positive action scale S, speed c, length a, and dimensionless ratio kappa, declare number density n=a^-3 and a Debye-like scale Theta=kappa*S*c/a. Composing these premises with C-MED-001's co-scaled laws gives epsilon=kappa*S/(a^4*c), mu_inverse=kappa*S*c/a^4, epsilon/mu_inverse=1/c^2, and local wave speed c. Under the additional declared dictionary rho_medium=epsilon/2, the mass density is rho_medium=kappa*S/(2*a^4*c). The Debye relation, kappa, the number-density law, and the one-half dictionary are premises; dimensions and response cancellation do not select them or establish a physical medium realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-002, C-MED-001. Assumptions: The Debye-like scale Theta=kappa*S*c/a and number density n=a^-3 are declared model premises., The co-scaled response laws retain C-MED-001's conditional status., The mass-density dictionary rho_medium=epsilon/2 is a separate declared conversion and its coefficient is load-bearing., No absolute scale, observed action value, sound-speed ratio, temperature, or continuum realization is derived.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.15.0` with provenance `campaigns/P016-primitive-unit-reduction/adjudication.yaml`.

- `campaigns/P016-primitive-unit-reduction/verify.py`
- `campaigns/P016-primitive-unit-reduction/attempts/0001/result.yaml`
- `campaigns/P016-primitive-unit-reduction/reviews/independent_elimination_review.py`
- `campaigns/P016-primitive-unit-reduction/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MED-002-review.md`
- `tests/test_constitutive.py`
