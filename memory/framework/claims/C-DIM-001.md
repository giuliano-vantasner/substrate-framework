---
description: Accepted framework claim C-DIM-001
author: framework-registry
created: '2026-08-01T12:53:41Z'
updated: '2026-08-01T12:53:41Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-001
category: claims
confidence: established
status: active
---
# C-DIM-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Over base dimensions energy E and time T, primitives consisting of an energy and frequency have dimension matrix [[1,0],[0,-1]], rank two, and zero kernel, so they form no nontrivial dimensionless monomial. Adding an independent action primitive S gives matrix [[1,0,1],[0,-1,1]], rank two, with one-dimensional kernel spanned by (-1,1,1); up to powers its unique dimensionless monomial is S*omega/E. Both conclusions are local to the declared primitive set and do not prohibit groups after further independent primitives are added.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Dimension-matrix rows are ordered as energy and time and columns follow the stated primitive order., Buckingham monomials use real exponent vectors in the matrix kernel.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.13.0` with provenance `campaigns/P013-action-scale-dimensions/adjudication.yaml`.

- `campaigns/P013-action-scale-dimensions/verify.py`
- `campaigns/P013-action-scale-dimensions/attempts/0001/result.yaml`
- `campaigns/P013-action-scale-dimensions/reviews/independent_equation_review.py`
- `memory/vantasner/decisions/C-DIM-001-review.md`
- `tests/test_action_scales.py`
