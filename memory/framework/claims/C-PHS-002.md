---
description: Accepted framework claim C-PHS-002
author: framework-registry
created: '2026-08-06T08:24:51Z'
updated: '2026-08-06T08:24:51Z'
tags:
- substrate-framework
- accepted-claim
- C-PHS-002
category: claims
confidence: established
status: active
---
# C-PHS-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

For N>=2 real scalar phases theta_1,...,theta_N, define the equal-weight complete-graph surrogate S=sum_{a<b} cos(theta_a-theta_b) and the phasor resultant Z=sum_a exp(i*theta_a). Exact expansion gives S=(|Z|^2-N)/2, hence S>=-N/2 with equality exactly when Z=0. A regular N-gon attains the minimum for every N>=2. For N=2 the relative phase at the minimum is pi, and for N=3 the zero-resultant unit phasors form the regular Z3 configuration up to global phase and permutation. For N=4 there is a continuous antipodal-pair family (0,pi,beta,beta+pi) of global minima; the square beta=pi/2 has every pairwise cosine nonpositive and worst cosine zero, while a generic member has a positive pair. Thus one numerically selected positive-pair four-phase minimum is not universal. The identity concerns a static equal-weight complete scalar-phase surrogate. It establishes no physical interaction energy, phase dynamics or relaxation, equilibrium, merger, stability, CP operation or violation, occupied condensate or generation count, multiplicity ratio, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PHS-001. Assumptions: Every phase is a scalar point modulo 2*pi and every unordered pair appears once with the same positive surrogate weight., The surrogate is declared algebraically and is not identified with C-QBL-006 or any other physical energy., Global phase and permutation do not change the resultant norm or pair sum; coincident phases are permitted unless separately excluded., A static minimizing configuration supplies neither dynamics nor selected occupancy.. Comparators: GC5's 400-start minimization is replaced by the exact resultant identity and complete minimum set, The four-phase square is a global-minimum counterexample to GC5's assertion that every four-phase minimum contains a positive pair, C-QBL-006 retains constant linear-cosine and cosine-squared finite pair terms and is not this surrogate.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.154.0` with provenance `campaigns/P212-gc5-two-role-count-audit/adjudication.yaml`.

- `campaigns/P212-gc5-two-role-count-audit/verify.py`
- `campaigns/P212-gc5-two-role-count-audit/reviews/independent_two_role_review.py`
- `campaigns/P212-gc5-two-role-count-audit/reviews/C-PHS-002-claim-review.md`
- `campaigns/P212-gc5-two-role-count-audit/reviews/source_adjudication.md`
- `campaigns/P212-gc5-two-role-count-audit/evidence/formula-freeze.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/dependency-audit.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/primary-provenance.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/independent-provenance.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/compatibility-audit.yaml`
- `campaigns/P212-gc5-two-role-count-audit/evidence/impact-analysis.yaml`
- `campaigns/P212-gc5-two-role-count-audit/attempts/0004/result.yaml`
- `campaigns/P212-gc5-two-role-count-audit/attempts/0008/result.yaml`
- `src/substrate_framework/phase_interactions.py`
- `tests/test_phase_interactions.py`
