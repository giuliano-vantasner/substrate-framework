---
description: Accepted framework claim C-NVP-001
author: framework-registry
created: '2026-08-10T14:25:00Z'
updated: '2026-08-10T14:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-NVP-001
category: claims
confidence: established
status: active
---
# C-NVP-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let Q>0, m>0, and g>0 be exact, let N_s be a positive integer, and let T_1,T_2,T_3 be same-size finite exact Hermitian matrices satisfying [T_1,T_2]=i*T_3 and cyclic permutations with tr_R(T_a*T_b)=T(R)*delta_ab for exact T(R)>0. Separately declare N_s identical massive complex-scalar multiplets in representation R on flat two-dimensional Euclidean space, with D_mu=partial_mu-i*g*W_mu^a*T_a, operator -D^2+m^2, the complex-scalar one-loop determinant, and a translation- and background-gauge-preserving regulator. In the convention Gamma^(2)=W_mu^a*Pi_mu_nu^ab*W_nu^b/2 and Pi_mu_nu^ab=P_mu_nu*Pi_hat^ab at nonzero momentum, define z=sqrt(Q)/sqrt(Q+4*m^2). Then Pi_hat^ab(Q)=delta_ab*N_s*T(R)*g^2/pi*(atanh(z)/z-1), equivalently the color transverse form factor is Pi_hat^ab/Q. Before transverse decomposition, contraction of the scalar bubble and seagull gives respectively +2*N_s*g^2*T(R)*delta_ab and -2*N_s*g^2*T(R)*delta_ab times the common tadpole and q_nu, so their sum vanishes. The projector coefficient vanishes as Q tends to zero and as m tends to infinity, while at fixed Q>0 it diverges as m tends to zero. Its leading low-momentum local Euclidean density is N_s*g^2*T(R)/(48*pi*m^2)*sum_a F_mu_nu^a*F_mu_nu^a, equivalently N_s*g^2/(48*pi*m^2)*tr_R(F_mu_nu*F_mu_nu). The independent background-field proper-time factors (4*pi)^(-1), 1/12, and integral_0^infinity exp(-m^2*s) ds=1/m^2 give the same trace-density coefficient and hence complete this leading term with the full non-Abelian curvature, including its connection-commutator pieces. This loop term is additive to separately declared bare and counterterm coefficients. These are exact conditional one-loop identities. They supply no unique total gauge coupling, massless Schwinger pole, propagating W sector, scalar-to-kink dictionary, weak matter content, dimensional lift, observation, or substrate gauge mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-NAG-001, C-VAC-001. Assumptions: Flat two-dimensional Euclidean space, positive exact Q m and g, a positive integer multiplicity, and the stated quadratic effective-action convention are declared together., The three generators are finite same-size exact Hermitian matrices satisfying the fixed SU2 cyclic commutators and a positive trace metric T(R)*delta_ab; changing generator coordinates requires a separately reviewed coupling and structure-constant convention map., The quantum fields are N_s identical massive complex scalars in that representation, so their determinant has no real-scalar one-half prefactor; no accepted classical field is silently quantized or identified with this multiplet., The regulator and subtraction preserve background gauge invariance and translation shifts, and the bubble and seagull belong to the same minimally coupled scalar action., The leading local curvature statement is a low-momentum inverse-mass expansion for m>0; it includes the full curvature inside tr_R(F^2) but does not claim that higher-derivative and higher-curvature terms vanish., Component-density and trace-density coefficients remain separately typed by tr_R(T_a*T_b)=T(R)*delta_ab., Bare and counterterm coefficients, field normalization, matching scale, state, physical matter representation, dimension lift, observation, and substrate dictionary are not imported.. Comparators: YM1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all nine predicates without a NumPy compatibility event, while it declares no quantum action determinant regulator bubble seagull or counterterm, imposes transversality before checking it, uses the wrong complex-scalar numerator, drops the momentum factor and full background completion, changes normalization in its Abelian guard, and does not derive a unique gauge coupling pole weak sector dimensional lift or substrate mechanism.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.123.0` with provenance `campaigns/P158-ym1-yang-mills-induction-audit/adjudication.yaml`.

- `campaigns/P158-ym1-yang-mills-induction-audit/verify.py`
- `campaigns/P158-ym1-yang-mills-induction-audit/reviews/independent_nonabelian_scalar_review.py`
- `campaigns/P158-ym1-yang-mills-induction-audit/reviews/replay_source_graph.py`
- `campaigns/P158-ym1-yang-mills-induction-audit/attempts/0009/result.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/attempts/0015/result.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/source-reproduction.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/source-audit.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/check-adjudication.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/input-provenance.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/dependency-audit.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/consumer-audit.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/candidate-comparison.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/primary-provenance.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/compatibility-audit.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/evidence/literature-audit.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/reviews/source_adjudication.md`
- `campaigns/P158-ym1-yang-mills-induction-audit/reviews/impact_analysis.md`
- `campaigns/P158-ym1-yang-mills-induction-audit/attempts/0017/result.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/attempts/0018/result.yaml`
- `campaigns/P158-ym1-yang-mills-induction-audit/attempts/0019/result.yaml`
- `memory/vantasner/decisions/C-NVP-001-review.md`
- `memory/vantasner/decisions/YM1-qualified-review.md`
- `src/substrate_framework/nonabelian_vacuum_polarization.py`
- `tests/test_nonabelian_vacuum_polarization.py`
