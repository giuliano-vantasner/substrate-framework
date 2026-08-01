---
description: Accepted framework claim C-DIM-004
author: framework-registry
created: '2026-08-01T14:12:01Z'
updated: '2026-08-01T14:12:01Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-004
category: claims
confidence: established
status: active
---
# C-DIM-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on positive quantities satisfying the declared equations U*L=S*c0/(2*e^2) and U=4*pi*m*c0^2, exact elimination gives m=S/(8*pi*e^2*L*c0). Relative to C-DIM-003 with basis length L, the mass coordinate is N_m=1/(8*pi*e^2), equivalently S/(m*c0)=8*pi*e^2*L. The coupling e and both equations are premises. The relation predicts no mass, length, coupling, or particle identity and does not eliminate independent information unless those premises are established separately.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-003. Assumptions: U, L, S, c0, e, and m are positive., The unit-product coefficient one-half and mass-energy coefficient 4*pi are declared model premises., The dimensionless coupling e remains free and is not selected by dimensional analysis., No Skyrme, soliton, medium, Compton, or electron interpretation is part of the algebraic claim.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.18.0` with provenance `campaigns/P020-conditional-mass-length-coordinate/adjudication.yaml`.

- `campaigns/P020-conditional-mass-length-coordinate/verify.py`
- `campaigns/P020-conditional-mass-length-coordinate/attempts/0001/result.yaml`
- `campaigns/P020-conditional-mass-length-coordinate/reviews/independent_unit_elimination_review.py`
- `campaigns/P020-conditional-mass-length-coordinate/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-DIM-004-review.md`
- `tests/test_action_scales.py`
