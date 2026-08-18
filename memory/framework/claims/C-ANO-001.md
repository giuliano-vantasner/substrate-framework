---
description: Accepted framework claim C-ANO-001
author: framework-registry
created: '2026-08-10T21:18:00Z'
updated: '2026-08-10T21:18:00Z'
tags:
- substrate-framework
- accepted-claim
- C-ANO-001
category: claims
confidence: established
status: active
---
# C-ANO-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a separately supplied nonempty finite table of uniquely named left-handed rows of G_a times SU(2) times U(1), let row r have positive integer factor dimensions d_ar and d_2r, exact real Abelian charge y_r, exact nonnegative quadratic indices T_ar and T_2r, an exact signed G_a cubic anomaly coefficient A_ar, and a supplied indicator that is true exactly for each fundamental SU(2) doublet in the scoped table. Under the explicitly imported four-dimensional chiral-anomaly criteria, the exact coefficients are sum_r d_2r*T_ar*y_r for G_a^2 U(1), sum_r d_ar*T_2r*y_r for SU(2)^2 U(1), sum_r d_ar*d_2r*y_r^3 for U(1)^3, sum_r d_ar*d_2r*y_r for gravity^2 U(1), and sum_r d_2r*A_ar for G_a^3. The supplied fundamental-doublet count is sum_r d_ar over marked rows; Witten's imported fundamental-doublet criterion requires this count to be even. Charge conjugation negates y_r and A_ar, preserves dimensions and quadratic indices, and reverses every odd local coefficient while preserving the doublet count. For the separately supplied five-row carrier (Q_L,u_R^c,d_R^c,L,e_R^c) with standard fundamental SU3 and SU2 indices, write its Abelian charges as (q,u,d,l,e). The four charge-dependent local zero conditions are equivalently 2q+u+d=0, 3q+l=0, 6q+3u+3d+2l+e=0, and 6q^3+3u^3+3d^3+2l^3+e^3=0. Their complete real affine zero set is the union of the three lines t*(1,-4,2,-3,6), t*(1,2,-4,-3,6), and t*(0,1,-1,0,0). The displayed SM3 values are the first line at t=1/6; the row-exchanged and vectorlike lines prove that anomaly freedom alone does not uniquely select those ratios up to scale. The fixed carrier's G_a^3 coefficient is zero and its fundamental-doublet count is four on every charge branch, so those charge-independent conditions select none of the three lines. This exact conditional theorem does not derive the carrier, physical row identities, observed charges, a unique hypercharge table, Yukawa or scalar constraints, completeness, higher- representation SU2 global-anomaly classification, a global U1 period or charge lattice, a global gauge group, an action, renormalizability, unitarity, general covariance, a Standard Model generation, a coupling normalization, running, observation, or a substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-REP-001, C-REP-002, C-REP-003, C-LIE-001. Assumptions: The quantum anomaly criteria are explicit external theory; P165 verifies their exact supplied coefficient arithmetic and solution variety rather than deriving the quantum theorem., Every row is left-handed in one fixed convention. Factor dimensions, quadratic indices, signed cubic coefficients, Abelian charges, and fundamental-doublet indicators are supplied exact data rather than inferred from labels or dimensions., The second non-Abelian factor is SU2. A row marked as a fundamental doublet has dimension two, and the parity verdict is complete only when all relevant SU2 global-anomaly content is represented by the supplied fundamental-doublet indicators., The five-row specialization fixes the representation carrier and standard C-LIE-001 and C-REP-002 fundamental normalizations before varying only its five Abelian coordinates., The complete local solution statement is an affine real zero-set theorem. It retains the q=0 component and makes no projective division by q., C-REP-001 and C-REP-003 supply finite-table normalization, conjugation, and completeness boundaries; they do not select the carrier or charges., No Yukawa operator, scalar row, mass term, target electric charge, generation completeness, global group, physical observation, or substrate dictionary is imported.. Comparators: SM3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all eight predicates and correctly evaluates six supplied anomaly conditions, two coordinate mutations, and common scaling, but it never solves the anomaly ideal and its claimed unique ratio up to scale is exactly refuted by a row-exchanged line and a zero-q vectorlike line.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.127.0` with provenance `campaigns/P165-sm3-anomaly-cancellation-audit/adjudication.yaml`.

- `campaigns/P165-sm3-anomaly-cancellation-audit/verify.py`
- `campaigns/P165-sm3-anomaly-cancellation-audit/reviews/independent_anomaly_review.py`
- `campaigns/P165-sm3-anomaly-cancellation-audit/reviews/replay_source_graph.py`
- `campaigns/P165-sm3-anomaly-cancellation-audit/attempts/0010/result.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/attempts/0012/result.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/attempts/0014/result.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/attempts/0015/result.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/attempts/0016/result.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/source-reproduction.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/source-audit.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/check-adjudication.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/input-provenance.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/dependency-audit.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/consumer-audit.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/candidate-comparison.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/primary-provenance.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/evidence/literature-audit.yaml`
- `campaigns/P165-sm3-anomaly-cancellation-audit/reviews/source_adjudication.md`
- `campaigns/P165-sm3-anomaly-cancellation-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-ANO-001-review.md`
- `memory/vantasner/decisions/SM3-qualified-review.md`
- `src/substrate_framework/chiral_anomalies.py`
- `tests/test_chiral_anomalies.py`
- `formal/SubstrateFramework/Ingested/Phase9SM_AnomalyCancellation.lean`
