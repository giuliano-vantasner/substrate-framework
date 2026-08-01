---
description: Accepted framework claim C-TOP-001
author: framework-registry
created: '2026-08-01T14:03:06Z'
updated: '2026-08-01T14:03:06Z'
tags:
- substrate-framework
- accepted-claim
- C-TOP-001
category: claims
confidence: established
status: active
---
# C-TOP-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For integer winding under addition, p(w)=(-1)^w is a homomorphism from Z to the multiplicative signs {+1,-1}. Even winding has label +1 and odd winding has label -1. Adding any even winding, including zero, preserves the label; adding odd winding flips it. This is a mathematical winding character only. Without a separately accepted physical representation it determines no exchange statistics, spin, fermion or boson identity, baryon number, internal or electric charge, or existence of a composite.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Winding labels are integers composed by addition., The codomain signs compose by multiplication., Dressing invariance applies exactly when the added winding is even., Any physical spin-statistics, baryon, or charge interpretation requires an additional governed map.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.17.0` with provenance `campaigns/P019-winding-parity-labels/adjudication.yaml`.

- `campaigns/P019-winding-parity-labels/verify.py`
- `campaigns/P019-winding-parity-labels/attempts/0001/result.yaml`
- `campaigns/P019-winding-parity-labels/reviews/independent_quotient_review.py`
- `campaigns/P019-winding-parity-labels/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-TOP-001-review.md`
- `tests/test_topological_labels.py`
