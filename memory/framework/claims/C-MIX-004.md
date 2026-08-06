---
description: Accepted framework claim C-MIX-004
author: framework-registry
created: '2026-08-06T09:14:06Z'
updated: '2026-08-06T09:14:06Z'
tags:
- substrate-framework
- accepted-claim
- C-MIX-004
category: claims
confidence: established
status: active
---
# C-MIX-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let a nonempty finite family Y_a of nonempty same-size square complex matrices and a same-length family of complex scalar weights v_a be separately supplied, and define M=sum_a v_a*Y_a. Let U_L and U_R be separately supplied unitary bases for which D=U_L^dagger*M*U_R is diagonal, and define Gamma_a=U_L^dagger*Y_a*U_R. Then exactly D=sum_a v_a*Gamma_a. A diagonal weighted sum does not force the individual Gamma_a to be diagonal: their off-diagonal entries can cancel, and a zero-weight matrix can remain off diagonal while absent from M. Conditional on a separately declared multi-scalar interaction that identifies this complete Gamma_a family as the neutral-scalar couplings in the fixed mass basis, all such couplings are flavor diagonal exactly when every Gamma_a is diagonal. If Y_a=c_a*Y for separately supplied complex c_a and C=sum_a v_a*c_a is nonzero, common alignment is sufficient and Gamma_a=c_a*D/C is diagonal. If C=0, then M=0 and alignment alone does not force individual diagonality in an arbitrary degenerate mass basis. For a complex-symmetric M with Takagi form M=U*D*U^T, the corresponding right basis is conjugate(U), so the mass-basis transform is U^dagger*Y_a*conjugate(U), not U^dagger*Y_a*U. Repeated singular values and null blocks retain the basis freedoms of C-MIX-001 and require a separate degeneracy audit. These exact finite-matrix identities derive no Yukawa interaction, scalar field content, vacuum expectation values, physical mass or generation map, localization geometry, flavor-changing rate or bound, natural flavor conservation, Standard-Model identity, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MIX-001. Assumptions: Every coupling matrix is finite nonempty square and exact, all matrices have one common dimension, and one complex scalar weight is supplied per matrix., The supplied left and right bases are exactly unitary and diagonalize the displayed weighted mass matrix. The theorem does not derive those bases or identify the matrix as a physical mass interaction., The no-off-diagonal-coupling interpretation is conditional on a separately declared interaction in which the complete transformed family gives the relevant neutral-scalar couplings in one fixed mass basis., Common alignment implies diagonality from the mass basis only when the combined coefficient C is nonzero. A zero mass matrix and repeated singular blocks retain arbitrary admissible basis choices., The Takagi specialization requires the displayed weighted mass matrix to be complex symmetric. Individual source matrices need not separately be symmetric unless another premise says so., No accepted claim maps GC6's overlap matrices profiles field labels counts spacings or thresholds to physical Yukawa matrices scalar doublets generations or experimental flavor bounds.. Comparators: GC6 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its left-basis-on-both-sides transform is replaced by the exact biunitary transform, An exact two-by-two Takagi countermodel is diagonal under the conjugate right basis while the source transform manufactures off-diagonal entries, Aligned matrices with zero combined coefficient and a degenerate-mass basis refute the unqualified alignment corollary, GC6's finite-box ratios remain conditional numeric model evidence and do not select or establish the exact theorem.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.155.0` with provenance `campaigns/P213-gc6-fcnc-consequence-audit/adjudication.yaml`.

- `campaigns/P213-gc6-fcnc-consequence-audit/verify.py`
- `campaigns/P213-gc6-fcnc-consequence-audit/reviews/independent_flavor_review.py`
- `campaigns/P213-gc6-fcnc-consequence-audit/reviews/C-MIX-004-claim-review.md`
- `campaigns/P213-gc6-fcnc-consequence-audit/reviews/source_adjudication.md`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/formula-freeze.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/claim-delta-revision-0003.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/dependency-audit.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/primary-provenance.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/independent-provenance.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/compatibility-audit.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/evidence/impact-analysis.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/attempts/0008/result.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/attempts/0009/result.yaml`
- `campaigns/P213-gc6-fcnc-consequence-audit/attempts/0010/result.yaml`
- `src/substrate_framework/multi_scalar_flavor.py`
- `tests/test_multi_scalar_flavor.py`
