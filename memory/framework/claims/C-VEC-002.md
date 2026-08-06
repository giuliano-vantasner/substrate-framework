---
description: Accepted framework claim C-VEC-002
author: framework-registry
created: '2026-08-06T10:22:22Z'
updated: '2026-08-06T10:22:22Z'
tags:
- substrate-framework
- accepted-claim
- C-VEC-002
category: claims
confidence: established
status: active
---
# C-VEC-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the Hermitian Pauli-half basis T_0=I_2/2 and T_a=sigma_a/2 for a=1,2,3, every real symmetric Ad(U(2))-invariant bilinear form Q on u(2) has component Gram matrix diag(beta,alpha,alpha,alpha), equivalently Q(X,Y)=2*alpha*Tr(X*Y)+(beta-alpha)*Tr(X)*Tr(Y). It is positive definite exactly when alpha and beta are positive. The fundamental single-trace specialization and singlet-triplet degeneracy occur exactly at alpha=beta; U(2) invariance alone does not force that equality. Separately, for positive exact m and g, a supplied real current B, and the declared algebraic action L=m^2*w^2/2+g*w*B, stationary elimination gives w=-g*B/m^2 and L_eff=-g^2*B^2/(2*m^2). Thus the convention L6=-lambda_A^2*B^2 has lambda_A=g/(sqrt(2)*m), while C-BPS-001's convention L6=-lambda_BPS^2*pi^4*B^2 has lambda_BPS=lambda_A/pi^2. Restoring a vector kinetic differential operator replaces m^2 by a nonlocal kernel, so the displayed local term is only a leading low-momentum specialization under separately supplied power counting. This exact classification and conditional elimination derive no HLS field content, physical omega rho pion or baryon current, WZW or anomaly coefficient, N_c, universality, KSRF relation, mass, coupling value, decay scale, medium response, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-EFT-001, C-BPS-001, C-CHI-001. Assumptions: The basis is exactly T_0=I_2/2 and T_a=sigma_a/2 with Hermitian Pauli matrices and the ordinary fundamental trace; changing the central-generator normalization changes component coefficients., The invariant-form classification is over real symmetric bilinear forms under the adjoint U(2) action. Positivity requires independently positive triplet coefficient alpha and singlet coefficient beta., The vector-current action uses the displayed plus-source and one-half mass conventions with positive exact m and g, a real supplied current independent of w, and one common contraction convention., The algebraic elimination is exact only for the declared local mass kernel. A kinetic vector requires a separately supplied differential kernel, conserved-current and gauge constraints as applicable, boundary conditions, low-momentum counting, and remainder control., The lambda_A and lambda_BPS comparison uses the same normalized current B. Rescaling the current, generator, source, or BPS density changes the coefficient map and must be reviewed explicitly., No accepted claim identifies these declared objects with a physical HLS multiplet, singlet omega, triplet rho, pion, baryon, quark-number current, color count, decay constant, or substrate medium.. Comparators: MK2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact single-trace and algebraic-elimination specializations survive while its forced-degeneracy and physical closure are corrected, The exact positive invariant metric diag(5,2,2,2) refutes singlet-triplet degeneracy from U(2) invariance alone, Fixed-ratio different-mass-and-coupling families prove that the conditional sextic match does not determine m and g separately.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.156.0` with provenance `campaigns/P215-mk2-vector-sextic-matching-audit/adjudication.yaml`.

- `campaigns/P215-mk2-vector-sextic-matching-audit/verify.py`
- `campaigns/P215-mk2-vector-sextic-matching-audit/reviews/independent_vector_metric_review.py`
- `campaigns/P215-mk2-vector-sextic-matching-audit/reviews/C-VEC-002-claim-review.md`
- `campaigns/P215-mk2-vector-sextic-matching-audit/reviews/source_adjudication.md`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/formula-freeze.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/dependency-audit.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/primary-provenance.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/independent-provenance.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/compatibility-audit.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/evidence/impact-analysis.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/attempts/0004/result.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/attempts/0005/result.yaml`
- `campaigns/P215-mk2-vector-sextic-matching-audit/attempts/0006/result.yaml`
- `src/substrate_framework/hls_reduction.py`
- `tests/test_hls_reduction.py`
