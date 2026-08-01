---
description: Accepted framework claim C-MIX-001
author: framework-registry
created: '2026-08-01T17:17:53Z'
updated: '2026-08-01T17:17:53Z'
tags:
- substrate-framework
- accepted-claim
- C-MIX-001
category: claims
confidence: established
status: active
---
# C-MIX-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For every finite complex m-by-n matrix M, there are square unitary column bases U and V and a same-shape rectangular diagonal Sigma with nonnegative entries such that U^dagger*M*V=Sigma and M=U*Sigma*V^dagger. The nonzero spectra of M*M^dagger and M^dagger*M are the squared singular values with the shape-required additional zeros. Individual bases are noncanonical: a repeated nonzero singular block permits the same unitary rotation on its paired left and right bases, while left and right null blocks permit independent unitary choices. For two same-size unitary column bases U_a,U_b, R=U_a^dagger*U_b is unitary and identical ordered bases give R=I. If row transforms A_i instead satisfy A_i*M_i*B_i^dagger=Sigma_i and map original coordinates to diagonal coordinates, the corresponding relative transform is A_a*A_b^dagger, not A_a^dagger*A_b. For a real symmetric matrix [[a,b],[b,d]], the proper rotation [[cos(theta),sin(theta)],[-sin(theta),cos(theta)]] with 2*theta=atan2(2*b,d-a) diagonalizes by R^T*M*R; a scalar identity block has arbitrary rotation and the numerical API chooses theta=0. These matrix facts establish no fermion mass matrix, Yukawa texture, flavor or family ontology, CKM identity, Cabibbo prediction, CP-phase count, charged-current or GIM mechanism, anomaly result, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Matrices are finite dimensional over the complex numbers with the standard Hermitian inner product., U and V denote column singular-vector bases; the separate A and B clause fixes the inverse row-transform convention explicitly., Singular-vector ordering and phases are conventional, and repeated or null subspaces have the stated unitary freedoms., The real symmetric rotation clause applies only to a real symmetric two-by-two matrix and does not by itself define a two-sector relative angle., NumPy double-precision implementations are regression consumers of the exact theorem and report no exact or physical evidence.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.30.0` with provenance `campaigns/P034-fg3-flavor-mixing/adjudication.yaml`.

- `campaigns/P034-fg3-flavor-mixing/verify.py`
- `campaigns/P034-fg3-flavor-mixing/attempts/0001/result.yaml`
- `campaigns/P034-fg3-flavor-mixing/reviews/independent_decomposition_review.py`
- `campaigns/P034-fg3-flavor-mixing/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MIX-001-review.md`
- `tests/test_matrix_decompositions.py`
