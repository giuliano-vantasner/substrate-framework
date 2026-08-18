---
description: Accepted framework claim C-MIX-002
author: framework-registry
created: '2026-08-01T17:32:26Z'
updated: '2026-08-01T17:32:26Z'
tags:
- substrate-framework
- accepted-claim
- C-MIX-002
category: claims
confidence: established
status: active
---
# C-MIX-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on the abstract N-by-N unitary relative-basis matrices of C-MIX-001, let the left/right diagonal phase action be V -> D_L*V*D_R^dagger. For a unitary V whose bipartite nonzero-support graph has c connected components, the diagonal-action stabilizer has real dimension c and its orbit has dimension 2*N-c. On the generic connected-support stratum c=1, so the effective orbit dimension is 2*N-1 and the quotient of U(N) has dimension (N-1)^2. Separating the N*(N-1)/2 real-orthogonal angle dimensions leaves (N-1)*(N-2)/2 irreducible complex-phase dimensions; these are zero for N=2 and one for N=3. Every U(2) matrix is diagonal-rephasing-equivalent to a real orthogonal matrix, and every two-row/two-column quartet has zero imaginary part. For any indices, the quartet Q_ik;jl=V_ij*V_kl*conjugate(V_il)*conjugate(V_kj) is invariant under the declared diagonal action and its imaginary part reverses sign under entrywise complex conjugation. For the declared unitary chart V=R23*R13(delta)*R12, Im(Q_01;12) equals cos(t12)*cos(t23)*cos(t13)^2*sin(t12)*sin(t23)*sin(t13)*sin(delta). Disconnected zero patterns and degenerate singular spectra have enlarged basis freedoms and require their own stabilizer audit. These statements establish no quark or generation map, physical CKM matrix, Cabibbo or KM mechanism, physical CP operation or violation, observed family count, charged current, GIM or anomaly result, measured angle or phase, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MIX-001. Assumptions: N is a positive integer and the low-dimensional phase-count discussion concerns N at least two., The action is restricted to diagonal unitary changes in the two ordered bases; larger transformations allowed by degeneracy are outside the generic quotient., Numerical support is defined relative to an explicit tolerance, while the exact support-graph theorem uses mathematically nonzero entries., The three-angle matrix is a declared coordinate chart and its parameters are neither derived nor empirically selected., Complex conjugation is only an algebraic involution unless a physical CP action and interaction are separately accepted.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.31.0` with provenance `campaigns/P035-fg4-unitary-rephasing/adjudication.yaml`.

- `campaigns/P035-fg4-unitary-rephasing/verify.py`
- `campaigns/P035-fg4-unitary-rephasing/attempts/0001/result.yaml`
- `campaigns/P035-fg4-unitary-rephasing/reviews/independent_support_invariant_review.py`
- `campaigns/P035-fg4-unitary-rephasing/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MIX-002-review.md`
- `tests/test_unitary_rephasing.py`
- `tests/test_matrix_decompositions.py`
- `formal/SubstrateFramework/Ingested/Phase11Flavor_CPPhaseCount.lean`
