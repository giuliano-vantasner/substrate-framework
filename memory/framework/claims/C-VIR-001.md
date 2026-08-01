---
description: Accepted framework claim C-VIR-001
author: framework-registry
created: '2026-08-01T11:55:53Z'
updated: '2026-08-01T11:55:53Z'
tags:
- substrate-framework
- accepted-claim
- C-VIR-001
category: claims
confidence: established
status: active
---
# C-VIR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on the real virial slope formulas width_slope=(a-b)/2 and energy_slope=-(a+b)/2, both slopes equal -1/2 if and only if (a,b)=(0,1). The alternatives (1,0) and (1,1) give slopes (1/2,-1/2) and (0,-1), respectively, and fail the simultaneous target.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The two virial slope formulas are approved conditional inputs; their physical derivation and fitted predecessor slopes are not part of this claim., Parameters a and b are real.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.7.0` with provenance `campaigns/P007-variational-scale/adjudication.yaml`.

- `campaigns/P007-variational-scale/verify.py`
- `campaigns/P007-variational-scale/attempts/0001/result.yaml`
- `campaigns/P007-variational-scale/reviews/independent_geometry_review.py`
- `memory/vantasner/decisions/C-VIR-001-review.md`
- `tests/test_collective_dynamics.py`
