---
description: Accepted framework claim C-MOD-001
author: framework-registry
created: '2026-08-02T21:00:00Z'
updated: '2026-08-02T21:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MOD-001
category: claims
confidence: established
status: active
---
# C-MOD-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For r>0, declare the dimensionless reduced energy E=4*pi*integral[(r^2+2*sin(f)^2)*f'^2+2*sin(f)^2 +sin(f)^4/r^2]dr. Its exact Euler--Lagrange equation is (r^2+2*sin(f)^2)*f''+2*r*f'+sin(2*f)*(f'^2-1) -sin(2*f)*sin(f)^2/r^2=0. For f+epsilon*eta, the coefficient of epsilon^2 before integration by parts is A*eta'^2+B*eta*eta'+D*eta^2, where A=r^2+2*sin(f)^2, B=4*sin(2*f)*f', and D=2*cos(2*f)+2*cos(2*f)*f'^2 +2*sin(f)^2*(3*cos(f)^2-sin(f)^2)/r^2. Under endpoint data that cancel the boundary term, the self-adjoint quadratic operator is H*eta=-(A*eta')'+C*eta with C=D-B'/2 and separately declared kinetic weight W=A; its Green boundary form is A*(u*v'-u'*v). For the scale family f(exp(s)*r), the tangent is r*f' and the declared two-/four- derivative energy scales as exp(-s)*E2+exp(s)*E4, so E2=E4 gives zero first derivative but positive curvature E2+E4 rather than a dilation zero mode. For a regular-origin half-line realization with the declared massless tail f,f' tending to zero sufficiently fast, A/W tends to one and C/W tends to 2/r^2 and then zero, so the continuum edge is Omega^2=0. A positive finite-Dirichlet-box eigenvalue is therefore not below that continuum edge. These are exact conditional reduced-model identities. They derive no physical Skyrme action, soliton or bound state, nucleon, Roper, spin or isospin, quantization, absolute scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The displayed dimensionless radial energy, positive radial coordinate, differentiability, kinetic mirror W=A, and endpoint or decay data are declared model premises rather than consequences of an accepted physical action., Integrations by parts require modes and coefficient functions regular enough that the displayed endpoint form vanishes; stationarity alone does not remove the mixed field/gradient Hessian term., The continuum-edge statement assumes the regular-origin half-line realization and the displayed massless coefficient limits; a different asymptotic potential, mass term, domain, or self-adjoint extension can change the edge., Derrick scaling concerns the explicitly declared family f(exp(s)*r); it is not a rigid translation and does not establish a spectral eigenfunction without a separate operator-domain test.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.56.0` with provenance `campaigns/P062-pg3-roper-radial-mode/adjudication.yaml`.

- `campaigns/P062-pg3-roper-radial-mode/verify.py`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0002/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0003/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/attempts/0005/result.yaml`
- `campaigns/P062-pg3-roper-radial-mode/reviews/independent_radial_review.py`
- `campaigns/P062-pg3-roper-radial-mode/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MOD-001-review.md`
- `tests/test_radial_modes.py`
