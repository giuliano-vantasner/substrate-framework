---
description: Accepted framework claim C-QBL-004
author: framework-registry
created: '2026-08-05T20:34:00Z'
updated: '2026-08-05T20:34:00Z'
tags:
- substrate-framework
- accepted-claim
- C-QBL-004
category: claims
confidence: established
status: active
---
# C-QBL-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Declare on flat 3+1 spacetime with signature (+---) a dimensionless smooth complex scalar Psi, rho=conjugate(Psi)*Psi, and action density partial_mu(conjugate(Psi))*partial^mu(Psi)-U(rho), where U(rho)=1-cos(sqrt(rho)) is defined by its analytic rho-series at zero. The Euler-Lagrange equation is box Psi+(dU/drho)*Psi=0. For the real nonnegative stationary radial ansatz Psi(t,r)=f(r)*exp(-i*omega*t), f''+2*f'/r=sin(f)/2-omega^2*f, with f'(0)=0 and f tending to zero. A localized tail requires 0<omega<1/sqrt(2) and has inverse length kappa=sqrt(1/2-omega^2), with f asymptotic to C*exp(-kappa*r)/r. In the C-U1-001 current convention, I=4*pi*integral_0^infinity r^2*f^2 dr, Q=2*omega*I, T=4*pi*integral r^2*f'^2 dr, V=4*pi*integral r^2*(1-cos(f)) dr, and E=T+omega^2*I+V. Every sufficiently regular finite-energy stationary profile obeys the exact scaling identity T+3*(V-omega^2*I)=0. At the single declared branch coordinate omega=1/2, adaptive collocation on outer radii 20, 30, and 40 with tolerances through 1e-8, direct origin-series DOP853 shooting, and an independent transformed h=r*f DOP853 shooting route provide convergent numerical evidence for a nontrivial nodeless monotone finite-energy radial branch. The fine collocation values are f(0)=6.1066779651, E=2990.2501002, and Q=4721.0197236 in the declared normalization; radius-30-to-40 relative energy and charge changes are below 6e-11, the normalized Pohozaev residual is below 5e-12, and the fitted tail rate is 0.4999492 versus analytic 0.5. These values are resolution-bounded evidence, not an exact global existence interval, uniqueness theorem, or stability result. Omega is a separately selected branch coordinate. The declared action is a compatible conditional extension and is not derived as the matter field of C-VAC-002 or C-VAC-003. No quantization, asymptotic particle, propagator mass, determinant insertion, physical electric charge, material scale, observation, or substrate realization follows.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-U1-001. Assumptions: The complex scalar action and dimensionless normalization are declared model data rather than consequences of an accepted substrate medium or determinant calculation., The stationary ansatz uses a real nonnegative radial amplitude and the displayed phase sign. C-U1-001 fixes the corresponding Noether-current convention., Omega is separately chosen in the open localization interval. The numerical branch evidence and quoted values concern omega=1/2 only and do not establish an entire branch family., The infinite-domain statement is resolution-bounded numerical evidence from explicit wall extension, tail fitting, observable convergence, Pohozaev closure, and independent shooting; it is not an analytic existence proof., Nodelessness and monotonicity are numerically checked on the resolved profiles. No uniqueness, linear spectrum, Vakhitov-Kolokolov criterion, nonlinear evolution, or stability theorem is imported., The charge and energy integrals use the displayed action normalization. No dimensionful scale, physical electric-charge unit, rest-mass conversion, or measured parameter is supplied., A classical localized Noether-charged configuration is not by itself a quantized asymptotic particle, free determinant field, loop insertion, or physical matter species., C-QBL-001 through C-QBL-003 and C-PDE-001 remain context with their accepted dimensional and model ceilings; none supplies a hidden lift into this claim.. Comparators: GK3D5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its native finite-domain trace is retained after the committed P202 formula and numeric freeze but does not select the candidate, C-QBL-002 supplies a distinct one-dimensional implicit full-sine stationary branch and no three-dimensional lift or stability theorem, C-PDE-001 supplies a distinct real three-dimensional radial initial-value model and finite-time oscillon evidence rather than a complex stationary charged branch, Removing radial geometry, changing the potential force, erasing omega, accepting the zero branch, reversing the tail sign, or truncating at radius eight rejects the corresponding P202 verdict.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.150.0` with provenance `campaigns/P202-gk3d5-radial-charged-excitation-audit/adjudication.yaml`.

- `campaigns/P202-gk3d5-radial-charged-excitation-audit/verify.py`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/reviews/independent_transformed_review.py`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/reviews/replay_source_graph.py`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/reviews/C-QBL-004-claim-review.md`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/reviews/GK3D5-disposition-review.md`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/reviews/source_adjudication.md`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/reviews/impact_analysis.md`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/attempts/0001/result.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/attempts/0002/result.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/attempts/0003/result.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/attempts/0004/result.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/attempts/0005/result.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/formula-freeze.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/input-provenance.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/dependency-audit.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/consumer-audit.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/candidate-comparison.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/numerical-construction.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/implementation-audit.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/impact-analysis.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/primary-provenance.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/independent-provenance.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/source-reproduction.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/compatibility-audit.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/source-audit.yaml`
- `campaigns/P202-gk3d5-radial-charged-excitation-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-QBL-004-review.md`
- `memory/vantasner/decisions/GK3D5-qualified-review.md`
- `src/substrate_framework/radial_qball.py`
- `tests/test_radial_qball.py`
