---
description: Accepted framework claim C-VAR-002
author: framework-registry
created: '2026-08-06T12:12:00Z'
updated: '2026-08-06T12:12:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VAR-002
category: claims
confidence: established
status: active
---
# C-VAR-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let X be a nonempty set, let n be a positive integer, and let E_1,...,E_n be real-valued functionals on X whose component infima m_i=inf_{x in X} E_i(x) are finite real numbers. Then the joint functional has a finite infimum M=inf_{x in X} sum_i E_i(x) and M>=sum_i m_i. Equality holds if and only if, for every epsilon>0, there exists one common x_epsilon in X such that 0<=E_i(x_epsilon)-m_i<epsilon for every i. If the joint infimum is attained, equality holds if and only if a joint minimizer is simultaneously a minimizer of every component; under equality every joint minimizer has that property. Pointwise, the joint excess above the sum of separate infima is exactly sum_i(E_i(x)-m_i), a finite sum of nonnegative component excesses. Thus a sum of energy terms evaluated on one shared configuration does not generally equal a sum of separately minimized component energies; incompatible component minimizers can make the joint inequality strict. This exact order theorem proves no existence or attainment for a particular field model and derives no action, coefficient, state, sector mass, binding energy, double-counting diagnosis, observation, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The index family is finite and nonempty, all component functionals share exactly one nonempty admissible set X, and every pointwise component value is a finite real number., Each displayed m_i is the actual finite real infimum of its component on X. A supplied lower bound that is not the infimum changes the equality criterion., The common minimizing-sequence condition uses one configuration for all components at each epsilon; separately chosen component configurations do not satisfy it., The joint-attainment specialization additionally assumes that the infimum of the sum is achieved by an element of X. No topology compactness coercivity or lower semicontinuity is inferred., Applying the theorem to physical sectors requires a separately accepted common field space functional decomposition coefficients boundary data and state interpretation.. Comparators: Two quadratic components with a common minimizer saturate the inequality, The components (x-1)^2 and (x+1)^2 have separate infima zero but joint infimum two and refute unqualified additivity, MK6 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its shared generalized functional motivates the theorem while its physical double-counting diagnosis is rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.158.0` with provenance `campaigns/P219-mk6-confrontation-tension-audit/adjudication.yaml`.

- `campaigns/P219-mk6-confrontation-tension-audit/verify.py`
- `campaigns/P219-mk6-confrontation-tension-audit/reviews/independent_variational_composition_review.py`
- `campaigns/P219-mk6-confrontation-tension-audit/reviews/C-VAR-002-claim-review.md`
- `campaigns/P219-mk6-confrontation-tension-audit/reviews/source_adjudication.md`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/formula-freeze.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/candidate-claim.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/dependency-audit.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/primary-provenance.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/independent-provenance.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/evidence/compatibility-audit.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/reviews/impact_analysis.md`
- `campaigns/P219-mk6-confrontation-tension-audit/attempts/0003/result.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/attempts/0004/result.yaml`
- `campaigns/P219-mk6-confrontation-tension-audit/attempts/0005/result.yaml`
- `src/substrate_framework/variational.py`
- `tests/test_variational.py`
