---
description: Accepted framework claim C-BPS-003
author: framework-registry
created: '2026-08-07T18:00:00Z'
updated: '2026-08-07T18:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BPS-003
category: claims
confidence: established
status: active
---
# C-BPS-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let A and n be positive integers and epsilon a positive dimensionless parameter tending to zero. Suppose the same positive-degree sectors used in C-BPS-002 have controlled expansions at D=A and D=n*A of the form M_epsilon(D)=K*D+epsilon*Delta_D+r_D(epsilon), with finite fixed-degree coefficients Delta_D. Then exactly n*M_epsilon(A)-M_epsilon(n*A) =epsilon*(n*Delta_A-Delta_(n*A)) +n*r_A(epsilon)-r_(n*A)(epsilon). If both remainders are o(epsilon), this is epsilon*(n*Delta_A-Delta_(n*A))+o(epsilon); if both are O(epsilon^2), the residual is O(epsilon^2). The first-order coefficient may be positive, zero, or negative. This theorem does not establish that a proposed deformation admits the expansion, derive the corrections or their sign, provide a global interpolation, or make epsilon or a physical binding coefficient numerically small.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-BPS-002, C-RDIFF-001. Assumptions: C-BPS-002 supplies the common degree-linear leading coefficient K only in the relevant attained positive-degree sectors., Epsilon is dimensionless and tends to zero from above while A and n remain fixed; Delta_A and Delta_(n*A) are finite coefficients in the same energy convention., Each little-o or big-O conclusion requires the separately stated remainder control. Naming an uninterpreted correction or omitting a remainder does not establish that control., Degree balance n*A is load bearing. A different final degree leaves a nonzero leading BPS contribution., For the standard V=1-cos(chi) compacton, P107 independently finds a logarithmically divergent naive L2 first-order correction; the general conditional theorem does not validate that application., No interpolation monotonicity range coupling value physical state reaction empirical coefficient or yield follows from the asymptotic order.. Comparators: E4's formal exact-linear epsilon ansatz and claimed O(1) physical coefficient; the algebraic cancellation survives only at the controlled conditional ceiling, while the numerical and physical inference is rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.91.0` with provenance `campaigns/P107-e4-bps-zero-binding-audit/adjudication.yaml`.

- `campaigns/P107-e4-bps-zero-binding-audit/verify.py`
- `campaigns/P107-e4-bps-zero-binding-audit/reviews/independent_bps_review.py`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0001/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0004/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0005/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/source-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/check-adjudication.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/dependency-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/consumer-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/candidate-comparison.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-BPS-003-review.md`
- `tests/test_bps_energy.py`
