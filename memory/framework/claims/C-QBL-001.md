---
description: Accepted framework claim C-QBL-001
author: framework-registry
created: '2026-08-01T16:37:00Z'
updated: '2026-08-01T16:37:00Z'
tags:
- substrate-framework
- accepted-claim
- C-QBL-001
category: claims
confidence: established
status: active
---
# C-QBL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on the dimensionless 1+1 stationary-profile equation f_xx=(1/2-omega^2-f^2/12)f, C-U1-001's stationary phase Psi=f*exp(-i*omega*t), and 0<omega<1/sqrt(2), let kappa=sqrt(1/2-omega^2). Then for every real center x0 the positive localized profile f=sqrt(24)*kappa*sech(kappa*(x-x0)) solves the equation exactly. Within a nonzero ansatz A*sech(k*(x-x0)), the independent sech powers force k^2=1/2-omega^2 and A^2=24*k^2. Its accepted U1 charge is Q=96*omega*sqrt(1/2-omega^2): Q tends to zero at both open endpoints, increases on (0,1/2), reaches its unique maximum 24 at omega=1/2, and decreases on (1/2,1/sqrt(2)). These derivative signs alone establish no VK, spectral, orbital, or nonlinear stability, forced complex ontology, electric charge, particle identity, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-U1-001. Assumptions: The quartic stationary ODE and its dimensionless coefficients are declared model premises rather than consequences of an accepted action., The complex stationary-phase ansatz and Noether-current sign are exactly those of C-U1-001., The coefficient-forcing statement is restricted to a positive-width nonzero sech ansatz; no broader existence or uniqueness theorem is claimed., A charge-slope sign is not a stability theorem without separately verified VK hypotheses and a fluctuation operator., No accepted claim identifies this conditional complex scalar with the real sine-Gordon breather, a physical charged particle, or the substrate.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.27.0` with provenance `campaigns/P031-em6-quartic-qball/adjudication.yaml`.

- `campaigns/P031-em6-quartic-qball/verify.py`
- `campaigns/P031-em6-quartic-qball/attempts/0001/result.yaml`
- `campaigns/P031-em6-quartic-qball/reviews/independent_first_integral_review.py`
- `campaigns/P031-em6-quartic-qball/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-QBL-001-review.md`
- `tests/test_quartic_qball.py`
- `tests/test_u1_charge.py`
