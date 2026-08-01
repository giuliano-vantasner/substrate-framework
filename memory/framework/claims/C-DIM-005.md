---
description: Accepted framework claim C-DIM-005
author: framework-registry
created: '2026-08-01T14:24:53Z'
updated: '2026-08-01T14:24:53Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-005
category: claims
confidence: established
status: active
---
# C-DIM-005

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RGE-001 and positive quantities satisfying mu0=S*c0/a, g0^2=beta^2, and m*c0^2=q*Lambda, the C-DIM-003 mass coordinate is N_m=m*c0*a/S=q*exp(-8*pi^2/(b0*beta^2)). The dimensionless inputs q, b0, and beta^2 all remain free and load-bearing. This composition predicts no mass, length, coupling, beta coefficient, prefactor, or particle identity; an unpinned q can reproduce any positive N_m.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-003, C-RGE-001. Assumptions: S, c0, a, beta^2, b0, q, Lambda, and m are positive., The reference-scale, coupling, and mass-energy identifications are declared premises., The mass-energy ratio q is independent unless another accepted claim fixes it., No soliton coefficient, hadronic offset, granularity scale, or electron interpretation is part of the claim.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.19.0` with provenance `campaigns/P021-frontier-rg-coordinate/adjudication.yaml`.

- `campaigns/P021-frontier-rg-coordinate/verify.py`
- `campaigns/P021-frontier-rg-coordinate/attempts/0001/result.yaml`
- `campaigns/P021-frontier-rg-coordinate/reviews/independent_flow_review.py`
- `campaigns/P021-frontier-rg-coordinate/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-DIM-005-review.md`
- `tests/test_renormalization.py`
