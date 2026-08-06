---
description: Accepted framework claim C-MIX-003
author: framework-registry
created: '2026-08-06T07:02:59Z'
updated: '2026-08-06T07:02:59Z'
tags:
- substrate-framework
- accepted-claim
- C-MIX-003
category: claims
confidence: established
status: active
---
# C-MIX-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let R_a be finite real matrices with a common row dimension N, let theta_a be real scalars, and set Y_a=exp(i*theta_a)*R_a for a=1,2. Each left Gram is H_a=Y_a*Y_a^dagger=R_a*R_a^T and each right Gram is Y_a^dagger*Y_a=R_a^T*R_a; both are real symmetric positive semidefinite and independent of the phases. Real orthogonal matrices O_a may be chosen to diagonalize the left Grams, so V=O_1^T*O_2 is real orthogonal and every quartet V_ij*V_kl*conjugate(V_il)*conjugate(V_kj) has zero imaginary part. The commutator [H_1,H_2] is real antisymmetric, every odd-power trace vanishes, and its determinant vanishes when N is odd. Repeated Gram eigenvalues retain enlarged unitary basis freedom: arbitrary complex bases inside degenerate subspaces can display nonzero coordinate quartets even though a real representative and the commutator null identities remain. The hypothesis is the globally phased real matrix form itself; a scalar field or condensate label does not enforce real coupling matrices, real modes, or a spatially constant phase. These statements establish no Yukawa interaction, CKM matrix, physical CP operation or violation, condensate ontology, generation count, observed phase, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MIX-001, C-MIX-002. Assumptions: The matrices are finite and exactly real before their independent scalar global phases are attached, and pairs compared through left Grams have the same positive row dimension., Matrix products use the standard Hermitian inner product; the real eigenbases are existence representatives and are noncanonical in repeated eigenspaces., Quartet nullity concerns the chosen real representative and the diagonal-rephasing invariant of C-MIX-002; larger degenerate-subspace transformations require the stated commutator audit., A source-count coordinate K and the relative-matrix dimension N are independent inputs; neither is selected by this theorem., NumPy double-precision APIs are regression consumers of the exact theorem and scale odd-trace residuals relative to a declared matrix norm power.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.152.0` with provenance `campaigns/P210-gc3-common-phase-cp-audit/adjudication.yaml`.

- `campaigns/P210-gc3-common-phase-cp-audit/verify.py`
- `campaigns/P210-gc3-common-phase-cp-audit/reviews/independent_common_phase_review.py`
- `campaigns/P210-gc3-common-phase-cp-audit/reviews/C-MIX-003-claim-review.md`
- `campaigns/P210-gc3-common-phase-cp-audit/reviews/source_adjudication.md`
- `campaigns/P210-gc3-common-phase-cp-audit/evidence/primary-provenance.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/evidence/independent-provenance.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/evidence/compatibility-audit.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/evidence/impact-analysis.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/attempts/0003/result.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/attempts/0004/result.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/attempts/0005/result.yaml`
- `campaigns/P210-gc3-common-phase-cp-audit/attempts/0006/result.yaml`
- `tests/test_common_phase_matrices.py`
