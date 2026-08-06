---
description: Accepted framework claim C-VAR-003
author: framework-registry
created: '2026-08-06T13:03:40Z'
updated: '2026-08-06T13:03:40Z'
tags:
- substrate-framework
- accepted-claim
- C-VAR-003
category: claims
confidence: established
status: active
---
# C-VAR-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let X be a nonempty set and let A, P, and Q be real-valued functionals on X such that the infima m_A=inf_X A, m_AP=inf_X(A+P), m_AQ=inf_X(A+Q), and m_APQ=inf_X(A+P+Q) are finite real numbers. Define the mixed variational interaction I=m_APQ+m_A-m_AP-m_AQ, equivalently the joint increment above A minus the two separate increments. The corresponding pointwise expression (A+P+Q)+A-(A+P)-(A+Q) vanishes identically, so I is entirely an effect of the four separate optimizations. It is symmetric under P and Q and invariant under consistent additive constants in A, P, or Q. It has no universal sign: even continuous nonnegative coercive quadratics on the real line realize positive, negative, and zero values, and positive scaling realizes every real value. A common minimizer of A, P, and Q implies I=0, but I=0 does not imply such a common minimizer. This theorem infers no infimum, existence, attainment, or interaction for a particular field model and supplies no physical decomposition, coefficient, state, sector mass, binding energy, double-counting diagnosis, observation, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: X is one common nonempty admissible set and A, P, and Q take finite real values on X., Each of m_A, m_AP, m_AQ, and m_APQ is the actual finite real infimum of the displayed functional on that same X; a supplied lower bound or stationary value is not interchangeable with an infimum., The common-minimizer sufficient condition means one point minimizes A, P, and Q individually; no existence theorem for such a point is inferred., The arbitrary-real construction uses positive rescaling of explicit nonnegative coercive quadratic examples, preserving their regularity and coercivity., Any physical application requires separately accepted functionals, coefficients, common boundary data, minimizer evidence, observable definition, and state interpretation.. Comparators: A=x^2, P=(x-1)^2, Q=(x+1)^2 gives I=1, A=x^2 and P=Q=(x-1)^2 gives I=-1/3, A=x^2, P=(x-1)^2, Q=(x-(2+sqrt(3)))^2 gives I=0 without a common minimizer, MR3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64 reports one positive unrefined stationary-branch surrogate and is not a sign or physical oracle for this claim.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.159.0` with provenance `campaigns/P221-mr3-no-double-counting-audit/adjudication.yaml`.

- `campaigns/P221-mr3-no-double-counting-audit/verify.py`
- `campaigns/P221-mr3-no-double-counting-audit/reviews/independent_variational_interaction_review.py`
- `campaigns/P221-mr3-no-double-counting-audit/reviews/C-VAR-003-claim-review.md`
- `campaigns/P221-mr3-no-double-counting-audit/reviews/source_adjudication.md`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/candidate-claim.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/dependency-audit.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/implementation-audit.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/primary-provenance.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/independent-provenance.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/consumer-audit.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/evidence/compatibility-audit.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/reviews/impact_analysis.md`
- `campaigns/P221-mr3-no-double-counting-audit/attempts/0005/result.yaml`
- `campaigns/P221-mr3-no-double-counting-audit/attempts/0007/result.yaml`
- `src/substrate_framework/variational.py`
- `tests/test_variational.py`
