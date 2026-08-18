---
description: Accepted framework claim C-OVL-002
author: framework-registry
created: '2026-08-03T07:10:00Z'
updated: '2026-08-03T07:10:00Z'
tags:
- substrate-framework
- accepted-claim
- C-OVL-002
category: claims
confidence: established
status: active
---
# C-OVL-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let p,r,kappa be positive, A real, R real, and let an L2-normalized whole-line Cartesian mode be proportional to sech(kappa*(x-R))^p while the supplied core multiplier is A*sech(kappa*x)^r. With a=kappa*abs(R), alpha=2*p, and ell=(alpha+r)/2, its exact expectation is A/J_alpha times 2^(alpha+r-1)*exp(-alpha*a)*B(ell,ell) *2F1(alpha,ell;2*ell;1-exp(-2*a)), where J_alpha=sqrt(pi)*Gamma(p)/Gamma(p+1/2). It is even in R and reduces to C-OVL-001's matched-width gamma ratio at R=0. For nonzero A and large a, unequal alpha and r give the exact leading class A*2^(alpha+r-1)*B(abs(alpha-r)/2,ell)/J_alpha times exp(-min(alpha,r)*a); equal alpha=r instead gives A*2^(2*alpha)/J_alpha times a*exp(-alpha*a). Thus the slower density or profile tail sets the exponential rate, and equal rates are not a pure geometric law. Separately, for V0,w>0 the whole-line Hamiltonian H_R=-d_x^2-V0*sech((x-R)/w)^2 has exact normalized ground state N*sech((x-R)/w)^s, with s=(sqrt(1+4*V0*w^2)-1)/2, N^2=Gamma(s+1/2)/(w*sqrt(pi)*Gamma(s)), eigenvalue -s^2/w^2, and density-tail rate 2*s/w. Translation changes R but not its spectrum. Against A*sech(kappa*x), the slower of 2*s/w and kappa controls the overlap; the exact unequal-rate beta prefactors and equal-rate linear-R prefactor are retained by the canonical ledger. A declared linear center ladder R_n=R_0+n*d therefore has limiting log overlap ratio -min(2*s/w,kappa)*d, but d is a free input and reciprocal rate/spacing rescaling leaves this product invariant. An exact Gaussian localized countermodel attenuates as exp(-c*R^2), proving localization does not uniquely select a geometric displaced-sech mechanism. These exact conditional results derive no half-line radial operator, common multi-rung spectrum, well centers or spacing, generation count or identity, Yukawa interaction, observed hierarchy, mixing, absolute mass, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-OVL-001. Assumptions: The hypergeometric overlap uses Cartesian whole-line dx, positive powers and shared positive inverse width; amplitude and displacement are separately supplied and no radial measure is implied., The asymptotic equivalences require nonzero amplitude and the displayed exact sech tails; the equal-rate polynomial factor and all beta-function convergence conditions are part of the statement., Each Pöschl-Teller center labels a translated copy of one declared external well Hamiltonian; it is not an additional eigenlevel of one fixed operator or a generated center., The Pöschl/core tail ledger uses normalized whole-line density, positive well depth and width, positive core inverse width, and a separately supplied real core amplitude., The ladder spacing and every amplitude, width, center, external mass-map scale, and physical label remain inputs; asymptotic attenuation alone is not a hierarchy prediction.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.65.0` with provenance `campaigns/P071-mh2-translated-localization/adjudication.yaml`.

- `campaigns/P071-mh2-translated-localization/verify.py`
- `campaigns/P071-mh2-translated-localization/attempts/0001/result.yaml`
- `campaigns/P071-mh2-translated-localization/attempts/0002/result.yaml`
- `campaigns/P071-mh2-translated-localization/attempts/0003/result.yaml`
- `campaigns/P071-mh2-translated-localization/attempts/0004/result.yaml`
- `campaigns/P071-mh2-translated-localization/attempts/0005/result.yaml`
- `campaigns/P071-mh2-translated-localization/reviews/independent_translation_review.py`
- `campaigns/P071-mh2-translated-localization/evidence/primary-provenance.yaml`
- `campaigns/P071-mh2-translated-localization/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-OVL-002-review.md`
- `tests/test_translated_localization.py`
