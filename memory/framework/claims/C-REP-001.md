---
description: Accepted framework claim C-REP-001
author: framework-registry
created: '2026-08-03T18:00:00Z'
updated: '2026-08-03T18:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-REP-001
category: claims
confidence: established
status: active
---
# C-REP-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a separately supplied nonempty finite table of positive integer multiplicities m_i and exact real generator eigenvalues t_i,y_i, and an exact real coefficient c, define Q_i=t_i+c*y_i and the weighted traces T_2=sum_i m_i*t_i^2, T_Y=sum_i m_i*y_i^2, T_X=sum_i m_i*t_i*y_i, and T_Q=sum_i m_i*Q_i^2. Then exactly T_Q=T_2+2*c*T_X+c^2*T_Y, and T_2/T_Q is a conditional table ratio when T_Q is provably nonzero. For every separately supplied positive rho and positive Abelian coupling g_Y, the coordinate change y_i'=rho*y_i, c'=c/rho, and g_Y'=g_Y/rho preserves every Q_i, every product g_Y*y_i, T_Q, T_2/T_Q, and g_Y^2*T_Y. Holding c fixed instead generally changes Q and the quotient. Every homogeneous Abelian moment H_p=sum_i m_i*y_i^p scales as rho^p, so H_p=0 cannot select the positive overall generator normalization. Separately, for positive supplied traces S_2,S_Y and couplings g_2,g_Y, the coupling coordinate A_g=g_Y^2/(g_2^2+g_Y^2) equals the trace coordinate A_T=S_2/(S_2+S_Y) if and only if g_Y^2/g_2^2=S_2/S_Y, equivalently the two inverse-trace coefficients 1/(g_i^2*S_i) are equal. Thus a common law 1/g_i^2=C*S_i is a sufficient separately supplied premise, not a consequence of the finite table. Applied only to WM1's declared fifteen-state table and Q=T3+Y, the exact table values are T_2=2, T_Y=10/3, T_X=0, T_Q=16/3, and T_2/T_Q=3/8; equality with a coupling angle additionally requires g_Y^2/g_2^2=3/5. These results establish no physical representation, anomaly derivation, gauge action, kinetic normalization, common induction mechanism, simple unification, boundary or running scale, weak mixing angle, observed value, Standard Model, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The finite table is supplied rather than derived; labels are unique provenance keys, multiplicities are positive integers, and generator values and electric coefficient are exact real expressions., A trace quotient is reported only when its denominator is provably nonzero; no unresolved symbolic nonzero condition is silently assumed., Generator rescaling and the inverse coupling and electric-coefficient transformations are declared coordinate changes with rho positive., Coupling-angle statements require positive supplied traces and couplings; the common inverse-trace coefficient law is an additional premise., Homogeneous-moment algebra alone carries no anomaly, chirality, completeness, or physical matter-content interpretation., The WM1 specialization imports only its hash-pinned table as noncanonical evidence and does not promote its field labels, cited unified-group premises, or physical angle interpretation.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.73.0` with provenance `campaigns/P081-wm1-charge-trace-audit/adjudication.yaml`.

- `campaigns/P081-wm1-charge-trace-audit/verify.py`
- `campaigns/P081-wm1-charge-trace-audit/attempts/0001/result.yaml`
- `campaigns/P081-wm1-charge-trace-audit/attempts/0002/result.yaml`
- `campaigns/P081-wm1-charge-trace-audit/attempts/0003/result.yaml`
- `campaigns/P081-wm1-charge-trace-audit/attempts/0004/result.yaml`
- `campaigns/P081-wm1-charge-trace-audit/reviews/independent_charge_trace_review.py`
- `campaigns/P081-wm1-charge-trace-audit/evidence/source-reproduction.yaml`
- `campaigns/P081-wm1-charge-trace-audit/evidence/source-audit.yaml`
- `campaigns/P081-wm1-charge-trace-audit/evidence/literature-audit.yaml`
- `campaigns/P081-wm1-charge-trace-audit/evidence/candidate-comparison.yaml`
- `campaigns/P081-wm1-charge-trace-audit/evidence/primary-provenance.yaml`
- `campaigns/P081-wm1-charge-trace-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-REP-001-review.md`
- `tests/test_charge_traces.py`
- `formal/SubstrateFramework/Ingested/Phase23EW_Sin2ThetaW.lean`
