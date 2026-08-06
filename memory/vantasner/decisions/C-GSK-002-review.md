---
description: Accepted qualified review of C-GSK-002 stationary branches
author: vantasner-review
created: '2026-08-06T11:41:41Z'
updated: '2026-08-06T11:41:41Z'
tags:
- substrate-framework
- claim-review
- C-GSK-002
category: decisions
confidence: established
status: archived
---
# C-GSK-002 Review

## Decision

C-GSK-002 is accepted with `numeric_evidence` and `qualified` epistemic scope.
For supplied `(c6,c0)=(1/2,1/4)` and accepted B=1,2,4 angular inputs, checked
collocation on `[10^-4,20]` gives energy coefficients about 1.4326169552,
2.7988849886, and 5.1973886988 and signed difference 11.85481448.

## Numerical Ceiling

The record fixes binary64 precision, continuation, endpoint laws, solver and
output meshes, tolerances, residual norms, domain, cutoff, and quadrature
refinements. Independent vacuum-complement DOP853 shooting with Simpson
quadrature agrees on the like-for-like radius-14 problem. Angular and sextic
mutations materially move the result.

## Exclusions

The evidence proves no half-line existence, uniqueness, minimum, full
three-dimensional solution, physical coefficient, baryon, nucleus, binding
prediction, observation, or substrate mechanism. The signed difference is a
conditional reduced-model number, not a physical binding energy.
