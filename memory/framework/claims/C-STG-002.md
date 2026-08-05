---
description: Accepted framework claim C-STG-002
author: framework-registry
created: '2026-08-11T07:12:00Z'
updated: '2026-08-11T07:12:00Z'
tags:
- substrate-framework
- accepted-claim
- C-STG-002
category: claims
confidence: established
status: active
---
# C-STG-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let the canonical C-STG-001 scalar be phi=F*u with exact positive field scale F, exact positive mass scale mu, and potential V(phi)=mu^2*F^2*(1-cos(u)); let kappa be exact and positive. Define x=mu*r, tau=mu*t, m=mu*M_geo, and alpha=kappa*F^2. On a domain with x>0, N=exp(Phi)>0, and f=1-2m/x>0, use the dimensionless static areal metric ds^2=-N(x)^2*d tau^2+dx^2/f(x)+x^2*d Omega_2^2 and the real single-harmonic ansatz u=a(x)*cos(Omega*tau), with exact positive frequency Omega. Exact phase averaging gives rho=Omega^2*a^2/(4*N^2)+f*a_x^2/4+1-J_0(a), p_r=f*a_x^2/4+Omega^2*a^2/(4*N^2)-(1-J_0(a)), and p_t=Omega^2*a^2/(4*N^2)-f*a_x^2/4-(1-J_0(a)). The reduced Einstein and fundamental-projected scalar equations are m_x=alpha*x^2*rho/2, Phi_x=[m+alpha*x^3*p_r/2]/[x*(x-2m)], and a_xx+[Phi_x+f_x/(2f)+2/x]*a_x+ [Omega^2*a/N^2-2*J_1(a)]/f=0. Identically, (p_r)_x+(rho+p_r)*Phi_x+2*(p_r-p_t)/x equals f*a_x/2 times the displayed scalar residual; this is an induced averaged conservation identity, not an independent pointwise equation. At a regular origin with a(0)=A and Phi(0)=Phi_0, let rho_0 and p_r0 be the displayed stress with a_x=0. Then a_xx(0)=[2J_1(A)-Omega^2*A*exp(-2Phi_0)]/3, m=alpha*rho_0*x^3/6+O(x^5), and Phi_xx(0)=alpha*(rho_0/6+p_r0/2). The flat alpha=0, m=Phi=0 limit is exactly the C-PDE-005 single-harmonic radial equation, and A=0 is the vacuum limit. The first discarded scalar harmonic in the same residual convention is 2J_3(a) cos(3Omega*tau), with coefficient a^3/24+O(a^5), while the pointwise energy density generally retains the cos(2Omega*tau) coefficient -Omega^2*a^2/(4N^2)+f*a_x^2/4+2J_2(a). Therefore this exact object is a scaled phase-averaged single-harmonic reduction and is not generally a pointwise solution of the full time-dependent Einstein-scalar PDE. It establishes no solution existence or uniqueness, exact half-line breather, full oscillaton, nonminimal Horndeski or Gordon dynamics, selected physical kappa, F, or mu, observation, material model, gravity realization, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-STG-001, C-PDE-005, C-PDE-009. Assumptions: The action, mostly-plus signature, Einstein-Hilbert normalization, canonical healthy scalar sign, curvature convention, and natural units are exactly those of C-STG-001., Kappa, F, mu, and Omega are exact and positive; u, a, m, and Phi are exact real quantities with sufficient differentiability. Floating inputs are outside the exact API., M_geo is the length-valued areal mass in 1-2M_geo/r, so m=mu*M_geo is dimensionless; alpha is a free dimensionless coupling rather than a selected physical constant., The exact reduction assumes a static spherical areal metric, one cosine scalar harmonic, and phase averaging over a complete period on a domain with f>0., The averaged conservation factorization uses the same projected scalar equation and is a consistency identity rather than an independent full-PDE oracle., The displayed discarded harmonics are equation-level counterterms to pointwise equivalence; they do not rule out a separately solved full oscillaton or Floquet construction with additional harmonics., No accepted claim identifies this scalar with a Gordon index, a material medium, observed gravity, or a substrate field.. Comparators: SC2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its seven native predicates pass and its averaged equations survive after scale completion, while its full-system, independent-angular-equation, Horndeski, exact-breather, physical-gravity, and substrate readings are rejected or qualified.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.131.0` with provenance `campaigns/P179-sc2-static-einstein-scalar-audit/adjudication.yaml`.

- `campaigns/P179-sc2-static-einstein-scalar-audit/verify.py`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/independent_einstein_scalar_review.py`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/replay_source_graph.py`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/C-STG-002-claim-review.md`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/source_adjudication.md`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0004/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0006/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0008/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0010/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/source-reproduction.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/source-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/check-adjudication.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/input-provenance.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/dependency-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/consumer-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/candidate-comparison.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/accepted-evidence-reuse.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/compatibility-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/primary-provenance.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/literature-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-STG-002-review.md`
- `memory/vantasner/decisions/SC2-qualified-review.md`
- `src/substrate_framework/spherical_einstein_scalar.py`
- `tests/test_spherical_einstein_scalar.py`
