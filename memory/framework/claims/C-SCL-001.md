---
description: Accepted framework claim C-SCL-001
author: framework-registry
created: '2026-08-02T21:00:00Z'
updated: '2026-08-02T21:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SCL-001
category: claims
confidence: established
status: active
---
# C-SCL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let lambda, nu, S, E0, and epsilon0 be positive, with lambda a dimensionless classical Hessian eigenvalue, nu an inverse-time scale, S an action scale, and E0*epsilon0 a background energy. Conditional on a separately declared one-quantum harmonic interpretation, the dimensionless frequency is sqrt(lambda), the energy gap is S*nu*sqrt(lambda), and the gap-to-background ratio is S*nu*sqrt(lambda)/(E0*epsilon0). For every positive rho, replacing nu by rho*nu leaves the dimensionless Hessian problem unchanged while multiplying the gap and ratio by rho; analogous independent variation of S or E0 also changes the physical ratio. Thus a dimensionless squared classical frequency alone does not determine an excitation energy or mass ratio, and lambda itself cannot replace sqrt(lambda) in the harmonic gap. This exact conditional scale ledger supplies no quantization rule, value of S or nu, background normalization, spin, isospin, parity, particle or Roper dictionary, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-001. Assumptions: The five displayed inputs are positive and independently supplied in one dimensionally consistent convention; lambda is a squared dimensionless classical frequency., The one-quantum gap rule is an explicit conditional interpretation and is not derived by the classical Hessian or by C-DIM-001., Any identification of S with Planck's constant, E0*epsilon0 with a particle mass, or the mode with a named quantum state requires separately accepted premises.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.56.0` with provenance `campaigns/P062-pg3-roper-radial-mode/adjudication.yaml`.

- `campaigns/P062-pg3-roper-radial-mode/verify.py`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0003/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0005/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/reviews/independent_radial_review.py`
- `campaigns/P062-pg3-roper-radial-mode/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-SCL-001-review.md`
- `tests/test_radial_modes.py`
- `tests/test_action_scales.py`
