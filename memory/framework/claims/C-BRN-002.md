---
description: Accepted framework claim C-BRN-002
author: framework-registry
created: '2026-08-05T19:25:00Z'
updated: '2026-08-05T19:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BRN-002
category: claims
confidence: established
status: active
---
# C-BRN-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N>0 be a continuous population parameter, let rho>0 be a declared dimensionless ratio of two common-dimension positive rate normalizations, and let w(N)>0 be a differentiable dimensionless weight. For the comparison fraction B_c(N)=rho/(N*w(N)+rho), the exact total derivative is B_c'(N)=-rho*(w(N)+N*w'(N))/(N*w(N)+rho)^2. Consequently B_c is locally decreasing, stationary, or increasing exactly as w+N*w' is positive, zero, or negative. A constant positive weight recovers C-BRN-001's strictly decreasing specialization. Positive weight alone is insufficient: w=N^(-1/2), w=N^(-1), and w=N^(-2) realize the three respective verdicts. The theorem concerns a declared differentiable continuation. For integer-only counts, discrete monotonicity instead follows from adjacent values of N*w(N); no derivative is silently imported. The weight law, common rate dimensions, exhaustive channel set, and physical meaning of the inputs remain separate premises. No material population law, state preparation, interaction, isotope map, reaction, branching observable, rate, yield, heat, or substrate realization follows.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-BRN-001. Assumptions: N, rho, and w(N) are exact positive real quantities on the local domain considered, and w is differentiable there., The weighted input N*w(N) and comparison input rho arise from separately declared common-dimension positive rate normalizations as in C-BRN-001., The derivative is a total derivative on a declared positive continuous extension. Integer-only population monotonicity requires the adjacent ordering of N*w(N)., The sign verdict requires w+N*w' to have an explicitly established sign. Positive w alone does not supply that sign., The caller derives the weight law and its derivative independently; symbol absence in a selected formula is not a material-independence proof., C-CMB-003 supplies static factorial-one mass arithmetic only and is not a dependency of the derivative theorem., A physical branching interpretation requires separately accepted states, exhaustive channels, interactions, final-state measures, rate normalization, kinetics, and parameter provenance.. Comparators: MD5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its 63-check result was exposed before P200 froze the derivative criterion imports mutations and physical ceilings, C-BRN-001 supplies the exact constant-weight allocation and positive continuous partial derivative but not the total derivative for w of N, P193 previously rejected a different order-resolved C-BRN-002 proposal as duplicate accepted composition; that identifier never entered the accepted registry, Positive weights N^(-1/2), N^(-1), and N^(-2) distinguish decreasing stationary and increasing comparison fractions.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.149.0` with provenance `campaigns/P200-md5-branching-handshake-audit/adjudication.yaml`.

- `campaigns/P200-md5-branching-handshake-audit/verify.py`
- `campaigns/P200-md5-branching-handshake-audit/reviews/independent_weight_review.py`
- `campaigns/P200-md5-branching-handshake-audit/reviews/replay_source_graph.py`
- `campaigns/P200-md5-branching-handshake-audit/reviews/C-BRN-002-claim-review.md`
- `campaigns/P200-md5-branching-handshake-audit/reviews/MD5-disposition-review.md`
- `campaigns/P200-md5-branching-handshake-audit/reviews/source_adjudication.md`
- `campaigns/P200-md5-branching-handshake-audit/reviews/impact_analysis.md`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0001/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0002/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0003/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0004/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0005/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0006/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0007/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/attempts/0008/result.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/formula-freeze.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/input-provenance.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/dependency-audit.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/consumer-audit.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/candidate-comparison.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/implementation-audit.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/primary-provenance.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/independent-provenance.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/source-reproduction.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/consumer-reproduction.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/compatibility-audit.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/source-audit.yaml`
- `campaigns/P200-md5-branching-handshake-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-BRN-002-review.md`
- `memory/vantasner/decisions/MD5-qualified-review.md`
- `src/substrate_framework/branching.py`
- `tests/test_branching.py`
