---
description: Accepted framework claim C-GSK-003
author: framework-registry
created: '2026-08-18T22:40:00+02:00'
updated: '2026-08-18T22:40:00+02:00'
tags:
- substrate-framework
- accepted-claim
- C-GSK-003
category: claims
confidence: established
status: active
---
# C-GSK-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Declare the generalized-Skyrme linearized quadratic weights Aw(x,s,c6,alpha)=x^2*(1+(1+alpha^2)*(s/x)^2+alpha^2*c6*(s/x)^4) and Kw(x,s,p,c6,alpha)=x^2*(1+(1-alpha^2)*p^2+(1+alpha^2)*(s/x)^2+alpha^2*c6*(s/x)^4+(1-alpha^2)*c6*p^2*(s/x)^2) for nonzero real x, real s, p, alpha, and nonnegative sextic coefficient c6. Then exactly Kw-Aw=(1-alpha^2)*p^2*(x^2+c6*s^2); Aw is strictly positive; Kw=Aw holds exactly when alpha^2=1 or p=0; and for |alpha|<1 with nonzero p the kinetic weight strictly exceeds the gradient weight, Aw<Kw. Consequently the declared refractive index n=sqrt(Kw/Aw) equals 1 exactly in the longitudinal case alpha^2=1 and strictly exceeds 1 whenever |alpha|<1 with p nonzero: transverse disturbances in the declared generalized-Skyrme medium propagate with index above one while longitudinal ones do not. This is a conditional weight-comparison theorem on the declared quadratic forms. It does not derive the generalized Skyrme action or its linearization, prove a medium exists, identify x, s, p with physical momentum components beyond the declared reading, or assert a physical refractive medium.

## Status Axes
The four governance axes remain independent.

Verification is `formal_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The weight formulas (the c6-sextic linearization bookkeeping) and the refractive-index reading sqrt(Kw/Aw) are declared inputs; the claim machine-checks the exact gap identity, positivity, and the longitudinal/transverse dichotomy of the declared forms.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.163.0` with provenance `campaigns/P233-lean-discrete-facts/adjudication.yaml`.

- `formal/SubstrateFramework/Ingested/Phase48CE_OperatorAndGap.lean`
- `campaigns/P233-lean-discrete-facts/attempts/0001/result.yaml`
- `campaigns/P232-lean-corpus-census/census.yaml`
