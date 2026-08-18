---
description: Accepted framework claim C-XOV-001
author: framework-registry
created: '2026-08-08T06:30:00Z'
updated: '2026-08-08T06:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-XOV-001
category: claims
confidence: established
status: active
---
# C-XOV-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let f be a real continuous strictly increasing function on [0,infinity), let a=f(0), and suppose f has a finite limit b>a at infinity that it never attains at finite input. A horizontal level below a or above b has no crossing, level a has the unique crossing zero, every level strictly between a and b has exactly one finite positive crossing, and level b occurs only as an infinite-input limit. If S(E;E0)=1-exp(-E/E0) for real E>=0 and E0>0, then S has range [0,1) and its unique finite inverse for 0<=c<1 is E_x=-E0*log(1-c). On 0<c<1, partial_c E_x=E0/(1-c)>0, partial_c^2 E_x=E0/(1-c)^2>0, and partial_E0 E_x=-log(1-c)=E_x/E0>0; E_x tends to infinity as c tends to one from below. For C-SCR-001's shifted factor P(E,U,G)=exp(-sqrt(G/(E+U))), with G>0 and U>0 in the same energy unit, the attained lower value is p0=exp(-sqrt(G/U)), the unattained upper limit is one, and every p0<c<1 has the unique positive inverse E_x=G/log(c)^2-U. Its sensitivities are partial_c E_x=-2*G/(c*log(c)^3)>0, partial_G E_x=1/log(c)^2>0, and partial_U E_x=-1. At U=0 the lower endpoint is zero in the limiting convention and the inverse is G/log(c)^2. Common positive rescaling of all energy inputs rescales each crossover energy by the same factor. Continuity, strict monotonicity, and actual range are independently load bearing: a discontinuity can skip a level, a plateau can give repeated crossings, and a nonmonotone response can give multiple crossings. These are conditional dimensionless level-crossing identities. A free level, response scale, or physical normalization makes any selected positive crossing nonidentifying, and formal curve ordering alone establishes no common observable, state, interaction, coherent or tunnelling channel, transition rate, material crossover, predicted energy, yield, heat, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SCR-001. Assumptions: The general theorem uses a real continuous strictly increasing function on the full nonnegative half-line, an attained finite lower endpoint, and a finite strictly larger upper limit that is not attained at finite input., The exponential specialization requires E and E0 in one energy convention, E>=0, E0>0, and a dimensionless level c. A finite inverse exists exactly for 0<=c<1 and is positive exactly for 0<c<1., The shifted specialization imports exactly C-SCR-001's declared conditional factor. G>0 and U>=0 share E's energy dimension; for U>0 an interior positive crossing requires exp(-sqrt(G/U))<c<1., Logarithms are real natural logarithms of dimensionless positive levels. Sign, logarithmic power, response floor, and shift convention are load bearing., Scale covariance changes every dimensionful energy together. Holding a selected scale or shift fixed while rescaling other quantities is a different comparison., A mathematical comparison becomes a physical channel crossover only with separately accepted common states, observables, dimensions, normalizations, dynamics, parameter provenance, and measurement map.. Comparators: CM3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its structural range theorem and exponential inverse survive, while its sampled global proofs, zero-floor substitution for CM1, flat CM2 physical rate, channel dominance, predicted crossover, tunnelling sufficiency, material, yield, heat, and observation readings are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.97.0` with provenance `campaigns/P117-cm3-monotone-crossover-audit/adjudication.yaml`.

- `campaigns/P117-cm3-monotone-crossover-audit/verify.py`
- `campaigns/P117-cm3-monotone-crossover-audit/reviews/independent_crossover_review.py`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0001/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0002/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0003/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0004/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0005/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0006/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0007/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0008/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0009/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/attempts/0010/result.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/source-reproduction.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/source-audit.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/check-adjudication.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/input-provenance.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/dependency-audit.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/consumer-audit.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/candidate-comparison.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/evidence/primary-provenance.yaml`
- `campaigns/P117-cm3-monotone-crossover-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-XOV-001-review.md`
- `src/substrate_framework/crossovers.py`
- `tests/test_crossovers.py`
- `formal/SubstrateFramework/Ingested/Phase34KIKernel.lean`
