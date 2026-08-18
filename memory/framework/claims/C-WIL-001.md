---
description: Accepted framework claim C-WIL-001
author: framework-registry
created: '2026-08-01T16:01:23Z'
updated: '2026-08-01T16:01:23Z'
tags:
- substrate-framework
- accepted-claim
- C-WIL-001
category: claims
confidence: established
status: active
---
# C-WIL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For positive separation R, Euclidean duration T, and coefficient sigma, conditional on the separately declared rectangular loop expectation W_A(R,T)=exp(-sigma*R*T), the extraction V(R)=-lim_{T->infinity} log(W_A)/T gives V(R)=sigma*R, with derivative sigma and zero second derivative. Separately, for positive rho, the declared perimeter law W_P(R,T)=exp(-2*rho*(R+T)) gives V(R)=2*rho and zero separation derivative. These exact implications derive neither loop law, do not select the area law from center algebra, and establish no physical string tension, gauge phase, or confinement mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: R, T, sigma, and rho are positive real quantities in one consistent convention., The logarithmic large-Euclidean-time extraction rule is declared., The area and perimeter expectation values are independent premises rather than outputs of this claim., No accepted claim maps either ansatz to a physical substrate or gauge sector.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.25.0` with provenance `campaigns/P028-su3-center-wilson/adjudication.yaml`.

- `campaigns/P028-su3-center-wilson/verify.py`
- `campaigns/P028-su3-center-wilson/attempts/0001/result.yaml`
- `campaigns/P028-su3-center-wilson/reviews/independent_center_wilson_review.py`
- `campaigns/P028-su3-center-wilson/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-WIL-001-review.md`
- `tests/test_wilson_loops.py`
