---
description: Accepted framework claim C-RGE-005
author: framework-registry
created: '2026-08-08T20:30:00Z'
updated: '2026-08-08T20:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RGE-005
category: claims
confidence: established
status: active
---
# C-RGE-005

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let a finite nonempty ordered family of gauge factors contain at most one Abelian factor. Supply each factor a nonnegative exact real adjoint Casimir C_A(a), with zero for the Abelian factor, and supply each of a finite family of Weyl-fermion or complex-scalar multiplets a positive integer multiplicity m_r, nonnegative exact Dynkin indices S2_a(r) including spectator-factor degeneracies, and nonnegative exact quadratic Casimirs C2_a(r). Conditional on the imported modified-minimal- subtraction one- and two-loop gauge weights, define b_a=-(11/3)C_A(a)+(2/3)sum_F m_r*S2_a(r) +(1/3)sum_S m_r*S2_a(r), and define the gauge-only matrix B_ab=-(34/3)C_A(a)^2*delta_ab +sum_F m_r*S2_a(r)*((10/3)C_A(a)*delta_ab+2*C2_b(r)) +sum_S m_r*S2_a(r)*((2/3)C_A(a)*delta_ab+4*C2_b(r)). In the convention mu*dg_a/dmu=b_a*g_a^3/(16*pi^2) +g_a^3*sum_b(B_ab*g_b^2)/(16*pi^2)^2, row a belongs to beta(g_a) and column b multiplies g_b^2. Every coefficient is an exact sum with separately inspectable gauge, Weyl, and complex-scalar contributions. For an Abelian coordinate change T'=rho*T and g'=g/rho with rho>0, S2'=rho^2*S2 and C2'=rho^2*C2 imply b'_a=rho_a^2*b_a and B'_ab=rho_a^2*rho_b^2*B_ab, so beta'_a=beta_a/rho_a. Applied only to a separately supplied three-factor table with squared Abelian normalization 3/5, three copies of five declared Weyl multiplets, and one declared complex scalar doublet, the exact specialization is b=(41/10,-19/6,-7) and B=((199/50,27/10,44/5),(9/10,35/6,12),(11/10,9/2,-26)). This theorem imports the loop weights and supplied invariants. It excludes the same-order Yukawa contribution, multiple-Abelian kinetic mixing, thresholds, matching, boundary data, field-content or anomaly derivation, a preferred Abelian normalization, unification, Standard-Model identity, observed running, and substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001, C-REP-001, C-RGE-001, C-RGE-002, C-RGE-004. Assumptions: The factor order is fixed and nonempty, at most one factor is Abelian, its adjoint Casimir is zero, and all supplied invariants are exact real and nonnegative., Multiplet labels are provenance keys only. Every positive integer multiplicity, Weyl or complex-scalar classification, spectator degeneracy, Dynkin index, and quadratic Casimir is separately supplied rather than inferred by the theorem., The one- and two-loop weights are an approved external perturbative import in the modified-minimal-subtraction convention. Fermions are two-component Weyl fields and scalars are complex., The displayed matrix includes gauge-gauge terms only. Yukawa-dependent terms enter at the same formal loop order, and multiple Abelian factors require a separate kinetic-mixing treatment., The Abelian covariance result rescales generator, coupling, Dynkin indices, and quadratic Casimirs together. Holding any member of that coordinate change fixed defines a different comparison., The supplied specialization is exact arithmetic on a declared table. It does not derive physical representations, chirality, generation count, Higgs content, anomaly cancellation, a GUT embedding, or preferred normalization., Physical running additionally requires a perturbative domain, threshold and matching prescriptions, initial or boundary data, and parameter provenance.. Comparators: WM5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact supplied-table vector and gauge-only matrix survive, while its corpus-derived field content, SM4 upgrade, FULL two-loop Standard-Model, comparator-ordering, local-to-global running, unification, and substrate readings are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.99.0` with provenance `campaigns/P129-wm5-two-loop-coefficient-audit/adjudication.yaml`.

- `campaigns/P129-wm5-two-loop-coefficient-audit/verify.py`
- `campaigns/P129-wm5-two-loop-coefficient-audit/reviews/independent_coefficient_review.py`
- `campaigns/P129-wm5-two-loop-coefficient-audit/attempts/0001/result.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/attempts/0002/result.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/attempts/0003/result.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/source-reproduction.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/source-audit.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/check-adjudication.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/input-provenance.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/dependency-audit.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/consumer-audit.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/candidate-comparison.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/evidence/primary-provenance.yaml`
- `campaigns/P129-wm5-two-loop-coefficient-audit/reviews/source_adjudication.md`
- `campaigns/P129-wm5-two-loop-coefficient-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-RGE-005-review.md`
- `src/substrate_framework/gauge_beta.py`
- `tests/test_gauge_beta.py`
