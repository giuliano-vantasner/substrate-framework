---
description: Accepted framework claim C-ACT-001
author: framework-registry
created: '2026-08-01T12:53:41Z'
updated: '2026-08-01T12:53:41Z'
tags:
- substrate-framework
- accepted-claim
- C-ACT-001
category: claims
confidence: established
status: active
---
# C-ACT-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

On any connected interval with normalized canonical action J>0, differentiable positive energy E(J), and positive frequency omega=dE/dJ, the identity E/omega=J throughout the interval holds if and only if E(J)=C*J for a positive constant C. Thus a linear harmonic energy law has secant action equal to canonical action. For a rigid rotor with normalized action J=I*omega and energy E=I*omega^2/2=J^2/(2I), E/omega=J/2 instead.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Canonical action uses the normalized convention (1/(2*pi))*closed_integral(p dq)., The action interval is connected and E and dE/dJ are positive there.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.13.0` with provenance `campaigns/P013-action-scale-dimensions/adjudication.yaml`.

- `campaigns/P013-action-scale-dimensions/verify.py`
- `campaigns/P013-action-scale-dimensions/attempts/0001/result.yaml`
- `campaigns/P013-action-scale-dimensions/reviews/independent_equation_review.py`
- `memory/vantasner/decisions/C-ACT-001-review.md`
- `tests/test_action_scales.py`
