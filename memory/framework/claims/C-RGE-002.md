---
description: Accepted framework claim C-RGE-002
author: framework-registry
created: '2026-08-01T15:07:43Z'
updated: '2026-08-01T15:07:43Z'
tags:
- substrate-framework
- accepted-claim
- C-RGE-002
category: claims
confidence: established
status: active
---
# C-RGE-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-LIE-001, a nonnegative integer flavor count n_f, and the declared four-dimensional one-loop formula b0=(11/3)*C_A-(4/3)*T_F*n_f for a gauge-plus-ghost term and Dirac fundamentals, exact substitution gives b0=11-(2/3)*n_f. Its zero is n_f=33/2; b0 is positive for integer 0<=n_f<=16 and negative for integer n_f>=17, with b0=7 at declared n_f=6. Combined with C-RGE-001, a positive b0 gives decreasing one-loop ultraviolet running with zero infinite-scale limit. The loop weights, field content, flavor count, perturbative regime, and physical gauge-sector identification are premises; the claim proves neither a substrate/QCD identity, unique SU(3) selection, nor confinement.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001, C-RGE-001. Assumptions: The weights 11/3 and 4/3 and their gauge-plus-ghost and Dirac-matter meanings are declared one-loop premises., The matter fields are counted by a nonnegative integer n_f in the fundamental representation., The one-loop running equation is used only in its declared perturbative regime., Removing the gauge term is an algebraic guard, not a complete derivation of a physical abelian theory.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.21.0` with provenance `campaigns/P024-su3-one-loop-coefficient/adjudication.yaml`.

- `campaigns/P024-su3-one-loop-coefficient/verify.py`
- `campaigns/P024-su3-one-loop-coefficient/attempts/0001/result.yaml`
- `campaigns/P024-su3-one-loop-coefficient/reviews/independent_completeness_review.py`
- `campaigns/P024-su3-one-loop-coefficient/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RGE-002-review.md`
- `tests/test_su3.py`
- `tests/test_renormalization.py`
