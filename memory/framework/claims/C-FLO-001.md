---
description: Accepted framework claim C-FLO-001
author: framework-registry
created: '2026-08-11T10:25:00Z'
updated: '2026-08-11T10:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-FLO-001
category: claims
confidence: established
status: active
---
# C-FLO-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let B and K be exact constant complex square matrices of equal finite dimension, let Q(t)=exp(t*K), and consider the declared laboratory linear system x_dot=Q(t)*B*Q(t)^(-1)*x. Under x=Q(t)*y, exact chain rule gives y_dot=(B-K)*y and the laboratory fundamental matrix Phi(t)=Q(t)*exp(t*(B-K)). If T is exact and positive with Q(T)=I, the laboratory and transformed monodromies both equal exp(T*(B-K)). For any exact finite monodromy M, its integer powers are bounded exactly when every eigenvalue lies in the closed unit disk and every eigenvalue on the unit circle is semisimple, equivalently its algebraic and geometric multiplicities agree there. Thus a time-independent transformed generator or unit-modulus multipliers alone does not prove stability: a nontrivial boundary Jordan block gives secularly unbounded powers. This is an exact conditional finite-dimensional linear theorem. It supplies no field action, periodic field solution, unbounded-operator domain, constraint or gauge slice, boundary data, complete field spectrum, nonlinear estimate, energy-momentum coercivity, physical source, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: B and K are exact constant finite square matrices of equal dimension; floating inputs and time-dependent generators require separate error or evolution analysis., T is exact and positive, and monodromy equality requires the displayed periodic-frame condition Q(T)=I., Boundedness concerns nonnegative integer powers of one finite matrix in any equivalent finite-dimensional norm; it is not nonlinear Lyapunov stability., Boundary eigenvalues require their full Jordan structure, not merely a numerical list of eigenvalue moduli., No accepted claim identifies the declared matrices with a Skyrme field operator, rotating soliton, collective model, physical source, or observation.. Comparators: TX4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its chain rule and unit multipliers survive while its static-generator and no-exponential-growth stability inference is corrected by the exact Jordan criterion.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.135.0` with provenance `campaigns/P183-tx4-floquet-stability-audit/adjudication.yaml`.

- `campaigns/P183-tx4-floquet-stability-audit/verify.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/independent_rotating_stability_review.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/replay_source_graph.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/C-FLO-001-claim-review.md`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/source_adjudication.md`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0011/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0017/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/dependency-audit.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/consumer-audit.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/primary-provenance.yaml`
- `src/substrate_framework/rotating_stability.py`
- `tests/test_rotating_stability.py`
