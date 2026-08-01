---
description: Accepted framework claim C-LIE-002
author: framework-registry
created: '2026-08-01T16:01:23Z'
updated: '2026-08-01T16:01:23Z'
tags:
- substrate-framework
- accepted-claim
- C-LIE-002
category: claims
confidence: established
status: active
---
# C-LIE-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the standard explicit fundamental SU(3) representation of C-LIE-001, the exact complex 3-by-3 commutant of all eight generators consists only of scalar matrices. Intersecting that commutant with unitary determinant-one matrices gives exactly {omega^k*I_3 | k=0,1,2}, where omega=-1/2+i*sqrt(3)/2, an order-three cyclic group isomorphic to Z_3. A fundamental vector has center phase omega^k, center conjugation on any 3-by-3 matrix and hence the adjoint matrix representation is trivial, and abstract integer trialities compose additively modulo three. This theorem establishes no substrate field assignment, quark or gluon identity, screening dynamics, Wilson law, string tension, or confinement.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001. Assumptions: The fundamental generators and their normalization are exactly those of C-LIE-001., SU(3) group elements are complex unitary 3-by-3 matrices with determinant one., Triality denotes only the abstract center character unless a physical representation map is separately accepted.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.25.0` with provenance `campaigns/P028-su3-center-wilson/adjudication.yaml`.

- `campaigns/P028-su3-center-wilson/verify.py`
- `campaigns/P028-su3-center-wilson/attempts/0001/result.yaml`
- `campaigns/P028-su3-center-wilson/reviews/independent_center_wilson_review.py`
- `campaigns/P028-su3-center-wilson/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-LIE-002-review.md`
- `tests/test_su3.py`
