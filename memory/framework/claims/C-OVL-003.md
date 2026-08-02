---
description: Accepted framework claim C-OVL-003
author: framework-registry
created: '2026-08-03T08:10:00Z'
updated: '2026-08-03T08:10:00Z'
tags:
- substrate-framework
- accepted-claim
- C-OVL-003
category: claims
confidence: established
status: active
---
# C-OVL-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let {eta_i}_{i=1}^N be one declared ordered orthonormal family in a complex L2 space with fixed domain and measure, and let Phi be a bounded real multiplication profile. The finite compression Y_ij=<eta_i,Phi*eta_j>, with complex conjugation in the first slot, is Hermitian. For psi=sum_i c_i*eta_i, c^dagger*Y*c=<psi,Phi*psi>; hence a normalized Rayleigh quotient and every eigenvalue of Y lie in Phi's supplied essential range. Under one common basis change eta'=eta*U, Y'=U^dagger*Y*U, so entries are basis dependent while the spectrum, trace, determinant, spectral multiplicities, and commonly transformed commutator data are invariant. If the two modes and multiplier have declared parities p_i,p_j,p_Phi in {+1,-1}, the whole-line entry vanishes when p_i*p_Phi*p_j=-1; in particular, changing only the width of a centered even profile cannot couple opposite parities. Two finite Hermitian compressions on one explicitly identified space admit a common unitary eigenbasis exactly when their commutator vanishes. Matrix inequality alone does not establish misalignment, and a relative eigenbasis additionally retains independent eigenvector phases, permutations, arbitrary U(m) rotations in m-fold degenerate subspaces, and any undeclared map between separately named spaces; its unitarity or nonidentity alone is not a physical observable. For C-QBL-003's actual normalized even sech(z)^2 and odd sech(z)*tanh(z) modes, z=kappa*x, compressing the separately supplied asymmetric profile A*sech(z)*(1+b*tanh(z)) gives exactly [[9*pi*A/32,sqrt(2)*A*b/5],[sqrt(2)*A*b/5,3*pi*A/16]]. The common positive kappa cancels, b=0 restores the parity-diagonal C-OVL-001 matrix, and the nonzero cross entry therefore requires the new free odd profile premise b rather than a width change. MH3's substituted sech even mode instead gives pi*A/16 times [[4,sqrt(3)*b],[sqrt(3)*b,3]], also independent of kappa; its two displayed textures differ because b is independently changed, not because their widths differ. These exact compression results derive no fermion or chirality, Yukawa or mass interaction, generation assignment, physical up/down sectors, charged-current operator, hierarchy, CKM or Cabibbo observable, CP quantity, absolute mass, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-QBL-003, C-MIX-001, C-MIX-002, C-OVL-001. Assumptions: The general compression uses one fixed complex Hilbert space, domain, measure, ordered orthonormal family, conjugation convention, and bounded real multiplier with separately proved essential-range bounds., Parity zeros require a reflection-symmetric whole-line domain and parity-definite modes and multiplier; an asymmetric or displaced profile is an additional premise., The simultaneous-diagonalization criterion compares Hermitian operators on one explicitly identified finite space; unrelated spaces cannot be compared without a supplied unitary identification., Eigenbasis entries retain phase and ordering conventions, and degeneracies add arbitrary rotations; only appropriately quotiented invariants may receive interpretation., The concrete matrix uses exactly C-QBL-003's two conditional scalar-Hessian shapes, Cartesian dx, common positive inverse width, real amplitude, and a separately supplied real odd-profile coefficient., Every physical field, interaction, sector map, current, mass scale, and flavor label remains absent and cannot be inferred from matrix algebra.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.66.0` with provenance `campaigns/P072-mh3-overlap-compression/adjudication.yaml`.

- `campaigns/P072-mh3-overlap-compression/verify.py`
- `campaigns/P072-mh3-overlap-compression/attempts/0001/result.yaml`
- `campaigns/P072-mh3-overlap-compression/attempts/0002/result.yaml`
- `campaigns/P072-mh3-overlap-compression/attempts/0003/result.yaml`
- `campaigns/P072-mh3-overlap-compression/reviews/independent_compression_review.py`
- `campaigns/P072-mh3-overlap-compression/evidence/source-reproduction.yaml`
- `campaigns/P072-mh3-overlap-compression/evidence/source-audit.yaml`
- `campaigns/P072-mh3-overlap-compression/evidence/candidate-comparison.yaml`
- `campaigns/P072-mh3-overlap-compression/evidence/primary-provenance.yaml`
- `campaigns/P072-mh3-overlap-compression/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-OVL-003-review.md`
- `tests/test_overlap_compressions.py`
