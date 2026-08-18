---
description: Accepted framework claim C-BPS-002
author: framework-registry
created: '2026-08-07T18:00:00Z'
updated: '2026-08-07T18:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BPS-002
category: claims
confidence: established
status: active
---
# C-BPS-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Under C-BPS-001, define the energy M(B) of a nonzero degree sector as the infimum of the declared energy over a specified nonempty admissible class, and write K=2*lambda*mu*pi^2*W. Then M(B)>=K*abs(B). If an admissible configuration attains the C-BPS-001 equality in a specified sector, M(B)=K*abs(B) in that sector. Hence, for positive integers A and n with attainment in sectors A and n*A, n*M(A)-M(n*A)=0. If sectors 1 and B>0 attain, the declared binding B*M(1)-M(B) is zero. Linearity of the lower bound alone does not imply these conclusions: writing M(B)=K*abs(B)+s_B with unknown nonnegative sector slacks leaves n*M(A)-M(n*A)=n*s_A-s_(n*A), which can have either sign. This is a conditional attainment theorem, not an existence or physical zero-binding claim.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-BPS-001, C-RDIFF-001. Assumptions: All C-BPS-001 premises hold and each degree sector uses an explicitly specified nonempty admissible class for the same declared energy and conventions., The infimum exists as an extended-real quantity, and every sector asserted to be linear contains an admissible configuration that actually attains the C-BPS-001 equality., The zero signed difference uses positive A and n and the final degree n*A. The binding statement additionally requires attainment in degree one and degree B., Sector slacks are independent nonnegative quantities unless a separate theorem relates them; a linear lower bound cannot silently set them to zero., Map degree remains a mathematical sector label. A baryon, nucleus, particle mass, quantum correction, reaction, and observed binding require separately accepted maps and dynamics.. Comparators: E4's hard-coded M(B)=K*B regression; P107 replaces its universal-saturation premise with actual sectorwise attainment and exact slack counterexamples.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.91.0` with provenance `campaigns/P107-e4-bps-zero-binding-audit/adjudication.yaml`.

- `campaigns/P107-e4-bps-zero-binding-audit/verify.py`
- `campaigns/P107-e4-bps-zero-binding-audit/reviews/independent_bps_review.py`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0001/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0004/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0005/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/check-adjudication.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/dependency-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/consumer-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/candidate-comparison.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-BPS-002-review.md`
- `tests/test_bps_energy.py`
