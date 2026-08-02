---
description: Accepted framework claim C-BRK-001
author: framework-registry
created: '2026-08-02T20:00:00Z'
updated: '2026-08-02T20:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BRK-001
category: claims
confidence: established
status: active
---
# C-BRK-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let x be a real scalar coordinate, let A be real, and let F, q, and K be positive. For the declared periodic potential V(x)=A*(1-cos(q*x/F)) and scalar quadratic kinetic convention L_kin=K*(partial x)^2/2, x=0 is stationary, the period is 2*pi*F/q, the exact origin curvature and fourth derivative are A*q^2/F^2 and -A*q^4/F^4, and the generalized quadratic mass squared is A*q^2/(K*F^2). Its series through sixth order is A*q^2*x^2/(2*F^2)-A*q^4*x^4/(24*F^4) +A*q^6*x^6/(720*F^6). Separately, the periodic potential h*F^2*(1-cos(x/F)) and quadratic potential h*x^2/2 have the same origin Hessian h, but only the first is periodic and their origin fourth derivatives differ by -h/F^2. Thus local quadratic curvature does not select a global explicit-breaking potential. These are exact declared- coordinate identities. They derive no field ontology, symmetry-breaking source, physical mass, coefficient, absolute scale, or substrate map.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The coordinate is real; F, q, and the scalar kinetic coefficient K are positive; and the displayed potential and kinetic convention are declared model data., Generalized quadratic mass means the one-coordinate operator K^-1 times the potential Hessian in the same coordinate convention., The matched-curvature comparison assumes positive F and uses the exact global functions displayed; equality of one Hessian is not action or ontology equivalence., No accepted physical map identifies A, F, q, K, or x with a chiral field, pion, decay constant, quark source, or substrate observable.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.55.0` with provenance `campaigns/P061-pg2-explicit-breaking/adjudication.yaml`.

- `campaigns/P061-pg2-explicit-breaking/verify.py`
- `campaigns/P061-pg2-explicit-breaking/attempts/0002/result.yaml`
- `campaigns/P061-pg2-explicit-breaking/attempts/0003/result.yaml`
- `campaigns/P061-pg2-explicit-breaking/reviews/independent_breaking_review.py`
- `campaigns/P061-pg2-explicit-breaking/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-BRK-001-review.md`
- `tests/test_explicit_breaking.py`
