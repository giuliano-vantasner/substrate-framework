---
description: Accepted framework claim C-VAR-001
author: framework-registry
created: '2026-08-01T11:55:53Z'
updated: '2026-08-01T11:55:53Z'
tags:
- substrate-framework
- accepted-claim
- C-VAR-001
category: claims
confidence: established
status: active
---
# C-VAR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For any differentiable one-coordinate Lagrangian L0 and any nonzero multiplier A that is independent of the path coordinate, velocity, and evolution parameter, the Euler-Lagrange operator satisfies EL[A*L0] = A*EL[L0]. The two Euler-Lagrange equations therefore have the same solution set. The result holds for every fixed nonzero uniform factor, not only a factor of degree one in a named energy scale.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The multiplier is nonzero and constant with respect to the path, velocity, and evolution parameter., The Lagrangian is differentiable enough for the stated Euler-Lagrange operator.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.7.0` with provenance `campaigns/P007-variational-scale/adjudication.yaml`.

- `campaigns/P007-variational-scale/verify.py`
- `campaigns/P007-variational-scale/attempts/0001/result.yaml`
- `campaigns/P007-variational-scale/reviews/independent_geometry_review.py`
- `memory/vantasner/decisions/C-VAR-001-review.md`
- `tests/test_variational.py`
