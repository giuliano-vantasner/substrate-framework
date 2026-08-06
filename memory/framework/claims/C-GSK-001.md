---
description: Accepted framework claim C-GSK-001
author: framework-registry
created: '2026-08-06T11:41:41Z'
updated: '2026-08-06T11:41:41Z'
tags:
- substrate-framework
- accepted-claim
- C-GSK-001
category: claims
confidence: established
status: active
---
# C-GSK-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let B be a positive integer, let I be a separately supplied positive rational-map angular integral, let c6 and c0 be separately supplied nonnegative dimensionless coefficients, and let f(r) be a real radial profile for r>0. Declare E=4*pi*integral_0^infinity L dr with L=r^2*f'^2+2*B*sin(f)^2*(1+f'^2)+I*sin(f)^4/r^2 +c6*I*sin(f)^4*f'^2/r^2+c0*r^2*(1-cos(f)). Every term is nonnegative. One half of d/dr(dL/df')-dL/df is exactly K*f''+(2*r-2*c6*I*sin(f)^4/r^3)*f' +B*sin(2*f)*(f'^2-1) +c6*I*sin(f)^2*sin(2*f)*f'^2/r^2 -I*sin(f)^2*sin(2*f)/r^2-c0*r^2*sin(f)/2, where K=r^2+2*B*sin(f)^2+c6*I*sin(f)^4/r^2. For f_s(r)=f(r/s), E(s)=s*E2+s^-1*E4+s^-3*E6+s^3*E0, so a stationary scale satisfies E2-E4-3*E6+3*E0=0. At c6=c0=0 the density and equation reduce exactly to C-RPROF-001. Linearization gives origin exponent (sqrt(1+8*B)-1)/2; when c0>0 the decaying tail is proportional to r^-1/2*K_nu(sqrt(c0/2)*r), with nu=sqrt(1/4+2*B), while c0=0 recovers the massless power tail. Conditional on separately supplied positive lambda_BPS, mu, e, and F in the accepted conventions, the reduced coefficients are c6=lambda_BPS^2*e^4*F^2/8 and c0=32*mu^2/(e^2*F^4); equivalently c6=lambda_A^2*e^4*F^2/(8*pi^4) when lambda_A=pi^2*lambda_BPS. This exact conditional reduced model derives no coefficient value, physical action, rational map, existence or uniqueness theorem, minimizer, full three-dimensional field, particle, nucleus, binding energy, observation, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RMAP-001, C-RPROF-001, C-BPS-001, C-VEC-002. Assumptions: B and I are independently supplied typed rational-map data; the reduced radial declaration neither constructs a rational map nor identifies B with a physical baryon number., c6 and c0 are independently supplied dimensionless coefficients. Their displayed dimensional reduction is conditional on the exact accepted lambda convention and on separately supplied positive inputs., The profile and its derivatives have the regularity and decay needed for the displayed variation, scaling, and integrations; endpoint linearization is local asymptotic information, not an existence theorem., The massive-tail formula applies for c0>0 and the massless branch must be handled separately., No accepted MK1 through MK4 claim supplies the physical coefficients or identifies this declaration with a physical generalized-Skyrme action.. Comparators: MK5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its conditional density survives while its physical coefficient closure does not, C-RPROF-001 is recovered exactly when c6 and c0 vanish, Replacing I by B squared or omitting the pi-squared lambda conversion changes the declared model and its numerical consequences.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.157.0` with provenance `campaigns/P218-mk5-generalized-skyrme-solve-audit/adjudication.yaml`.

- `campaigns/P218-mk5-generalized-skyrme-solve-audit/verify.py`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/independent_generalized_skyrme_review.py`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/C-GSK-001-claim-review.md`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/source_adjudication.md`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/formula-freeze.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/candidate-claim.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/dependency-audit.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/primary-provenance.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/independent-provenance.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/compatibility-audit.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/impact_analysis.md`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/attempts/0003/result.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/attempts/0006/result.yaml`
- `src/substrate_framework/generalized_skyrme_radial.py`
- `tests/test_generalized_skyrme_radial.py`
