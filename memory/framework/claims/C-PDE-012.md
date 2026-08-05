---
description: Accepted framework claim C-PDE-012
author: framework-registry
created: '2026-08-11T06:01:00Z'
updated: '2026-08-11T06:01:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-012
category: claims
confidence: established
status: active
---
# C-PDE-012

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let ell be a nonnegative integer and let a sufficiently differentiable real radial mode g on r>0 obey -g''-2*g'/r+ell*(ell+1)*g/r^2+V(r)*g=E*g. The substitution chi=r*g gives exactly -chi''+[ell*(ell+1)/r^2+V(r)]*chi=E*chi, preserves the real radial norm integral r^2*g^2 dr=integral chi^2 dr, and maps regular g=O(r^ell) to chi=O(r^(ell+1)). On a regular finite Dirichlet ball of radius R with constant vacuum potential mu^2, the radial modes are spherical Bessel j_ell(z_(ell,n)*r/R) and E_(ell,n)=mu^2+(z_(ell,n)/R)^2, where z_(ell,n) is a supplied positive zero of j_ell. Thus the vacuum wall gap scales exactly as R^-2 and its normalized radial shape scales with r/R; neither fact establishes a localized half-line mode. More generally, if W_ell=ell*(ell+1)/r^2+V-mu^2 is nonnegative almost everywhere and the self-adjoint boundary form vanishes, the quadratic form of H-mu^2 is nonnegative, so no eigenvalue lies below mu^2. This implication is exact conditional on the pointwise premise; finite sampling of W_ell does not prove it. An endpoint-decay predicate evaluated after the endpoint or outer tail has been imposed as zero is non-discriminating whenever the interior amplitude clears the predicate's floor. Applied to C-PDE-009, these statements type only the supplied time-averaged finite-wall operator and establish no averaged or Floquet mode, nonlinear deformation, all-channel nonexistence, gravity, radiation, absolute scale, particle identity, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-003, C-PDE-005, C-PDE-009. Assumptions: The radial coordinate is positive; ell is a nonnegative integer; g, chi, V, and their displayed derivatives are real and sufficiently regular on the declared domain., The norm identity uses the three-dimensional radial measure and real modes. Complex modes require the corresponding absolute-square convention., The vacuum-ball formula assumes constant V=mu^2, regular-origin data, a positive finite radius, homogeneous outer Dirichlet data, and a supplied positive spherical-Bessel zero., The threshold bound requires W_ell nonnegative almost everywhere, a self-adjoint domain, and boundary or decay data that cancel the Green boundary form. Sampled positivity is numeric evidence only., A finite-wall level at or above the half-line threshold, inverse-wall-square scaling, or a forced-zero endpoint value does not by itself establish half-line localization. An unforced endpoint test alone is also not claimed sufficient., The sine-Gordon application inherits C-PDE-009's exact separation between the time-averaged radial operator and the full periodic-coefficient perturbation equation.. Comparators: BX1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64, whose finite-wall result and selected values were exposed before freeze and did not select the theorem.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.129.0` with provenance `campaigns/P177-bx1-l2-box-artifact-audit/adjudication.yaml`.

- `campaigns/P177-bx1-l2-box-artifact-audit/verify.py`
- `campaigns/P177-bx1-l2-box-artifact-audit/attempts/0012/result.yaml`
- `campaigns/P177-bx1-l2-box-artifact-audit/attempts/0015/result.yaml`
- `campaigns/P177-bx1-l2-box-artifact-audit/reviews/independent_radial_spectral_review.py`
- `campaigns/P177-bx1-l2-box-artifact-audit/reviews/C-PDE-012-claim-review.md`
- `campaigns/P177-bx1-l2-box-artifact-audit/reviews/source_adjudication.md`
- `campaigns/P177-bx1-l2-box-artifact-audit/evidence/numerical-audit.yaml`
- `memory/vantasner/decisions/C-PDE-012-review.md`
- `src/substrate_framework/radial_spectral_classification.py`
- `tests/test_radial_spectral_classification.py`
