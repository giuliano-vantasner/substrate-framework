---
description: Accepted framework claim C-CMB-002
author: framework-registry
created: '2026-08-11T16:45:00Z'
updated: '2026-08-11T16:45:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CMB-002
category: claims
confidence: established
status: active
---
# C-CMB-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let z be an exact positive dimensionless real and let the positive integers carry counting measure. Define m_z(n)=1_odd(n)*z^(2*n)/(n!)^2, so the support is the positive odd integers. Its exact positive total is M(z)=sum_(n positive odd) m_z(n)=(I_0(2*z)-J_0(2*z))/2, and p_z(n)=m_z(n)/M(z) is a normalized mathematical mass function. For an exact positive rational z and positive odd cutoff K, put L_K=sum_(n odd,n<=K)m_z(n), f_K=m_z(K+2), and r_K=z^4/((K+3)^2*(K+4)^2). Whenever r_K<1, the monotone consecutive-odd ratio gives L_K<M(z)<=L_K+f_K/(1-r_K), with normalized tail above K at most f_K/((1-r_K)*L_K). At z=1 and K=9 the exact upper total is 9963487458886859459/9693548673177600000; consequently p_1(1)>972/1000 and p_1(1)+p_1(3)>9999/10000, and the odd masses have mode one. The mode is normalization-dependent: at z=4 the order-three to order-one ratio is 64/9 and the order-five to order-three ratio is 16/25, so the unique mode is three. This normalization declares a mathematical sample space and does not by itself derive occurrence probabilities, normalized quantum states, a complete interaction, transition rates, branching channels, a physical subdivision band, or a material prediction.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-CMB-001. Assumptions: n is an exact positive integer and z is one separately declared exact positive dimensionless real; the ambient sample space is the positive integers with counting measure and odd support., I_0 and J_0 use their standard exact power-series definitions. Parity filtering and termwise addition are applied to absolutely convergent positive-factorial series., The rational enclosure requires exact positive rational z, exact positive odd K, and r_K<1. It is an analytic tail certificate rather than a floating-point truncation estimate., The unit-activity concentration statements use the declared mathematical sample space. Changing activity or coordinate normalization changes the mass ratios and can change the mode., C-BRN-001 may consume a separately supplied positive odd mass through its weighted specialization or an even zero through its general allocation endpoint; this conditional composition is not a dependency and derives no physical rate., A physical probability or rate would additionally require normalized states, a complete interaction, common-dimension rate inputs, final-state measure or spectral density, energy conventions, and validity assumptions; none is imported here., PN2, WN3 through WN7, and MD1 through MD6 supply no accepted physical premise to this theorem and remain separately governed.. Comparators: WN2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its formulas, seventy-check tally, concentration thresholds, and physical conclusion prose were exposed during P189 before P190, while sample-space, normalization, API, mutation, nonduplication, and consumer criteria were frozen before implementation.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.141.0` with provenance `campaigns/P190-wn2-coefficient-weight-audit/adjudication.yaml`.

- `campaigns/P190-wn2-coefficient-weight-audit/verify.py`
- `campaigns/P190-wn2-coefficient-weight-audit/reviews/independent_odd_mass_review.py`
- `campaigns/P190-wn2-coefficient-weight-audit/reviews/replay_source_graph.py`
- `campaigns/P190-wn2-coefficient-weight-audit/reviews/C-CMB-002-claim-review.md`
- `campaigns/P190-wn2-coefficient-weight-audit/reviews/source_adjudication.md`
- `campaigns/P190-wn2-coefficient-weight-audit/reviews/impact_analysis.md`
- `campaigns/P190-wn2-coefficient-weight-audit/attempts/0003/result.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/attempts/0004/result.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/attempts/0005/result.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/attempts/0006/result.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/formula-freeze.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/input-provenance.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/dependency-audit.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/consumer-audit.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/candidate-comparison.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/implementation-audit.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/primary-provenance.yaml`
- `campaigns/P190-wn2-coefficient-weight-audit/evidence/independent-provenance.yaml`
- `memory/vantasner/decisions/C-CMB-002-review.md`
- `memory/vantasner/decisions/WN2-qualified-review.md`
- `src/substrate_framework/factorial_suppression.py`
- `tests/test_odd_factorial_mass.py`
