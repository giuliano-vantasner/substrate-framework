---
description: Accepted framework claim C-BRN-001
author: framework-registry
created: '2026-08-08T11:30:00Z'
updated: '2026-08-08T11:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BRN-001
category: claims
confidence: established
status: active
---
# C-BRN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let A and B be exact nonnegative real quantities in one common dimension with A+B>0. Define q_A=A/(A+B) and q_B=B/(A+B). Then exactly 0<=q_A,q_B<=1, q_A+q_B=1, (A,B)=(0,B) gives (q_A,q_B)=(0,1), and (A,B)=(A,0) gives (1,0); the double-zero point is undefined. For A,B>0, q_A/q_B=A/B, partial_A q_A=B/(A+B)^2>0, and partial_B q_A=-A/(A+B)^2<0. At fixed B>0, q_A tends from zero to one as A runs from zero to infinity. Common positive scaling (A,B)->(s*A,s*B) leaves both fractions invariant, while independent channel scaling generally changes them. If positive common-dimension baselines r_w and r_c, a positive dimensionless weight w, and a positive integer N are separately declared, then A=r_w*w*N, B=r_c, and rho=r_c/r_w give q_A=w*N/(w*N+rho) and q_B=rho/(w*N+rho). On the positive continuous N extension, partial_N q_B=-rho*w/(w*N+rho)^2<0. Relative to the same positive baselines at population one and positive baseline weight w_1, the ratio of A/B odds is w*N/w_1. A common positive gate cancels, but unequal positive gates C_A and C_B change q_A by A*B*(C_A-C_B)/((A+B)*(C_A*A+C_B*B)). Every target 0<q<1 can be fitted by rho=w*N*(1-q)/q, so free baselines or weights do not predict a branching fraction. These are exact conditional normalization identities. They do not establish that the inputs are physical rates, that two channels exhaust a state, or derive states, interactions, final-state measures, kinetics, coherence, subdivision weights, nuclear transitions, material branching, enhancement magnitude, yield, heat, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: A and B are exact real nonnegative quantities in one common dimension and their sum is explicitly positive. The theorem retains either zero endpoint and excludes the undefined double-zero point., Physical bounds and derivative signs use the displayed nonnegative or positive domains. Odds and interior derivatives require both A and B positive; endpoint statements are evaluated separately., Common scaling multiplies both channels by the same positive factor. Unequal channel gates or independently changed normalizations define a different allocation., The weighted specialization requires positive common-dimension baselines, a positive dimensionless weight, and a positive integer population. The N derivative concerns the declared positive real extension of that integer formula., Relative-odds enhancement requires the same positive channel baselines in numerator and denominator and a positive nonzero baseline weight. It does not determine the weight law or population., A physical branching interpretation requires separately accepted states, an exhaustive channel set, interactions, final-state measures or spectral densities, kinetics, normalization, and parameter provenance.. Comparators: GB1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact fraction and relative-odds algebra survives, while its rho tautology, unused subdivision symbols, prose-only common factors, finite syntax scan, physical rate, exhaustive channel, weight law, material branching, enhancement, yield, heat, and observation readings are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.98.0` with provenance `campaigns/P122-gb1-channel-branching-audit/adjudication.yaml`.

- `campaigns/P122-gb1-channel-branching-audit/verify.py`
- `campaigns/P122-gb1-channel-branching-audit/reviews/independent_branching_review.py`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0001/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0002/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0003/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0004/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0005/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0006/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0007/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/attempts/0008/result.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/source-reproduction.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/source-audit.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/check-adjudication.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/input-provenance.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/dependency-audit.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/consumer-audit.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/candidate-comparison.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P122-gb1-channel-branching-audit/evidence/primary-provenance.yaml`
- `campaigns/P122-gb1-channel-branching-audit/reviews/source_adjudication.md`
- `campaigns/P122-gb1-channel-branching-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-BRN-001-review.md`
- `src/substrate_framework/branching.py`
- `tests/test_branching.py`
- `formal/SubstrateFramework/Ingested/Phase30PNKernel.lean`
- `formal/SubstrateFramework/Ingested/Phase31CMKernel.lean`
- `formal/SubstrateFramework/Ingested/Phase32GBKernel.lean`
- `formal/SubstrateFramework/Ingested/Phase38MDKernel.lean`
