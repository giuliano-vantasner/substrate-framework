---
description: Accepted framework claim C-OVL-005
author: framework-registry
created: '2026-08-06T08:24:51Z'
updated: '2026-08-06T08:24:51Z'
tags:
- substrate-framework
- accepted-claim
- C-OVL-005
category: claims
confidence: established
status: active
---
# C-OVL-005

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let n>=1, let psi be a complex L2(R) mode normalized by integral_R |psi|^2 dx=1, and let phi be a bounded real continuous multiplier that vanishes at spatial infinity. For each separation parameter t, let R_1(t),...,R_n(t) be real centers whose minimum pairwise distance tends to infinity, define psi_a(x)=psi(x-R_a(t)) and phi_c(x)=phi(x-R_c(t)), choose fixed real phases theta_c, and set Y_ab(t)=sum_c exp(i*theta_c)*integral_R conjugate(psi_a)*psi_b*phi_c dx. If the common matched self-overlap alpha=integral_R |psi|^2*phi dx is positive, then Y(t) tends in every finite matrix norm to alpha*diag(exp(i*theta_1),...,exp(i*theta_n)). Consequently every singular value tends to alpha. More sharply, whenever epsilon(t)=||Y(t)-alpha*diag(exp(i*theta_c))||_2 is less than alpha, every singular value lies in [alpha-epsilon,alpha+epsilon] and the spectral condition number is at most (alpha+epsilon)/(alpha-epsilon). The limit follows because matched self-overlaps are translation invariant, displaced density-multiplier convolutions vanish, and off-diagonal translated L2 correlations vanish. Unequal profiles, amplitudes, widths, nonunit weights, nonseparating centers, or a nondecaying multiplier change the conclusion. This theorem establishes no Yukawa interaction, physical mass or hierarchy, field species, role, generation, selected center or count, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-OVL-001. Assumptions: The mode is one fixed normalized L2 whole-line shape and every psi_a is its exact translate; the multiplier profiles are exact translates of one bounded real C0 shape., The number of centers is finite and fixed while every distinct pair separates; phases are fixed real scalars with unit-magnitude weights., The common self-overlap alpha is strictly positive. The finite condition-number bound additionally requires the operator-norm residual to be strictly smaller than alpha., Matrix entries use the standard complex L2 inner product and Cartesian whole-line measure. No radial Jacobian or finite-wall truncation is included., The theorem selects no mode shape center spacing amplitude field label or physical interpretation.. Comparators: GC5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its four sampled identical-family ratios are regression evidence for the exact limit, An independently completed normalized Gaussian triple-overlap family reaches the exact phase-weighted diagonal limit, Unequal limiting self-overlaps and residuals at the self-overlap threshold break the degeneracy and condition bound.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.154.0` with provenance `campaigns/P212-gc5-two-role-count-audit/adjudication.yaml`.

- `campaigns/P212-gc5-two-role-count-audit/verify.py`
- `campaigns/P212-gc5-two-role-count-audit/reviews/independent_two_role_review.py`
- `campaigns/P212-gc5-two-role-count-audit/reviews/C-OVL-005-claim-review.md`
- `campaigns/P212-gc5-two-role-count-audit/reviews/source_adjudication.md`
- `campaigns/P212-gc5-two-role-count-audit/evidence/formula-freeze.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/dependency-audit.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/primary-provenance.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/independent-provenance.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/compatibility-audit.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/impact-analysis.yaml`
- `campaigns/P212-gc5-two-role-count-audit/attempts/0004/result.yaml`
- `campaigns/P212-gc5-two-role-count-audit/attempts/0005/result.yaml`
- `src/substrate_framework/translated_overlap_matrices.py`
- `tests/test_translated_overlap_matrices.py`
