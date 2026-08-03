---
description: Accepted framework claim C-LAT-002
author: framework-registry
created: '2026-08-04T16:00:00Z'
updated: '2026-08-04T16:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-LAT-002
category: claims
confidence: established
status: active
---
# C-LAT-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N>=2 and let dimensionless real phases u_j(t) live on a one-dimensional periodic nearest-neighbour chain with exact positive physical phase inertia I, coupling energy K, on-site energy V0, and spacing a. The per-site-energy Lagrangian sum_j[I*dot(u_j)^2/2-K*(u_(j+1)-u_j)^2/2 -V0*(1-cos(u_j))] has exact site equation I*ddot(u_j)-K*(u_(j+1)-2*u_j+u_(j-1))+V0*sin(u_j)=0. Linearization about a vacuum has first-zone dispersion Omega^2=(V0+4*K*sin(k*a/2)^2)/I, gap sqrt(V0/I), zone-edge frequency sqrt((V0+4*K)/I), and long-wave speed a*sqrt(K/I). Under base rows (mass,length,time), the columns (I,K,V0,a,m,b) are (1,2,0), (1,2,-2), (1,2,-2), (0,1,0), (1,0,0), and (0,1,0). If a physical displacement is declared by q=b*u, then I=m*b^2; if its neighbour stiffness is kappa, then K=kappa*b^2. Thus sqrt(V0/m) has speed rather than frequency units when m is a bare mass. For two declared hosts A and B, Omega_A(0)/Omega_B(0)=sqrt(V_A*I_B/(I_A*V_B)), or after displacement lifts sqrt(V_A*m_B*b_B^2/(V_B*m_A*b_A^2)). The H-over-D value sqrt(2) follows only if V_D=V_H, b_D=b_H, and m_D=2*m_H exactly; changing either curvature or phase scale can remove that shift. At fixed I, V0->0+ closes the linear gap. These exact conditional results derive no lattice or material realization, coefficient value, collective effective mass, exact isotope prediction, nonlinear discrete-breather existence, lifetime, radiation, or absolute frequency.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LAT-001, C-DIM-002. Assumptions: The chain is one-dimensional, periodic, uniform, and nearest-neighbour with N>=2; u is dimensionless and I, K, V0, and a are exact, real, constant, and strictly positive., The displayed Lagrangian is a per-site energy sum, so I has phase-inertia dimensions and K and V0 have energy dimensions; no Riemann continuum measure or material origin is inferred., The Fourier wave number uses a declared first-Brillouin-zone representative, and the gap and band statements concern the linearization about an exact cosine minimum., The displacement lift additionally assumes one exact positive coordinate scale b for each host and, when used, a displacement stiffness kappa; bare mass and phase inertia remain distinct., The sqrt(2) specialization requires exact equality of the two on-site energies and coordinate scales and an exact doubled effective mass. Atomic isotope labels, tabulated atomic masses, or Born-Oppenheimer wording do not establish these premises., Gap positivity, gap closure, and a supplied sub-gap frequency are not sufficient nonlinear-existence or host-selection criteria.. Comparators: MC3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its body was exposed during P096, while P097 froze units, alternatives, isotope premises, and criteria before source execution and imported self-tests.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.83.0` with provenance `campaigns/P097-mc3-medium-gap-maps/adjudication.yaml`.

- `campaigns/P097-mc3-medium-gap-maps/verify.py`
- `campaigns/P097-mc3-medium-gap-maps/reviews/independent_medium_gap_review.py`
- `campaigns/P097-mc3-medium-gap-maps/evidence/source-reproduction.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/source-audit.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/imported-source-audit.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/check-adjudication.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/consumer-audit.yaml`
- `campaigns/P097-mc3-medium-gap-maps/evidence/candidate-comparison.yaml`
- `campaigns/P097-mc3-medium-gap-maps/reviews/source_adjudication.md`
- `campaigns/P097-mc3-medium-gap-maps/evidence/primary-provenance.yaml`
- `memory/vantasner/decisions/C-LAT-002-review.md`
- `tests/test_lattice_scalar.py`
