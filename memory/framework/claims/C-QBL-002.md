---
description: Accepted framework claim C-QBL-002
author: framework-registry
created: '2026-08-01T16:49:00Z'
updated: '2026-08-01T16:49:00Z'
tags:
- substrate-framework
- accepted-claim
- C-QBL-002
category: claims
confidence: established
status: active
---
# C-QBL-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on the dimensionless 1+1 stationary-profile equation f_xx=sin(f)/2-omega^2*f, C-U1-001's stationary phase, and 0<omega<1/sqrt(2), define G_omega(u)=1-cos(u)-omega^2*u^2. The ratio (1-cos(u))/u^2 decreases strictly from 1/2 to 0 on 0<u<2*pi, so there is a unique peak f0 in that interval with G_omega(f0)=0 and G_omega(u)>0 for 0<u<f0. Up to translation and reflection, the positive even localized branch is specified by x=integral_f(x)^f0 du/sqrt(G_omega(u)); it has f(0)=f0, f_x(0)=0, and tends to zero as |x| tends to infinity. Its accepted U1 charge is the finite exact quadrature Q=4*omega*integral_0^f0 u^2 du/sqrt(G_omega(u)). With kappa=sqrt(1/2-omega^2), the scaled field f(x)=kappa*F(z), z=kappa*x, obeys F_zz=F-F^3/12+O(kappa^2), f0/kappa tends to sqrt(24), and Q/(96*omega*kappa) tends to one as kappa tends to zero, recovering C-QBL-001 only in this controlled small-amplitude limit. The claim establishes no elementary closed form, finite-amplitude identity with EM1, VK or nonlinear stability, physical electric charge, particle identity, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-U1-001, C-QBL-001. Assumptions: The exact-sine stationary ODE and its dimensionless coefficients are declared model premises rather than consequences of an accepted action or potential., The complex stationary-phase ansatz and Noether-current sign are exactly those of C-U1-001., The branch is the positive nodeless first-root homoclinic; later roots and sign-changing profiles are outside the claim., The asymptotic statement scales both amplitude and coordinate as kappa tends to zero and does not assert equality at finite kappa., Numerical root and quadrature routines are implementation evidence for exact implicit formulas, not stability or empirical evidence., No accepted claim identifies the conditional complex field with the accepted real sine-Gordon breather or a physical substrate object.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.28.0` with provenance `campaigns/P032-fg1-exact-sine-qball/adjudication.yaml`.

- `campaigns/P032-fg1-exact-sine-qball/verify.py`
- `campaigns/P032-fg1-exact-sine-qball/attempts/0001/result.yaml`
- `campaigns/P032-fg1-exact-sine-qball/reviews/independent_energy_asymptotic_review.py`
- `campaigns/P032-fg1-exact-sine-qball/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-QBL-002-review.md`
- `tests/test_exact_sine_qball.py`
- `tests/test_quartic_qball.py`
- `tests/test_u1_charge.py`
