---
description: Accepted framework claim C-LAT-001
author: framework-registry
created: '2026-08-03T05:00:00Z'
updated: '2026-08-03T05:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-LAT-001
category: claims
confidence: established
status: active
---
# C-LAT-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N>=2, L>0, a=L/N, and let dimensionless real fields phi_j(t) live on a one-dimensional periodic uniform lattice. The Riemann-normalized nearest-neighbour sine-Gordon action has instantaneous Lagrangian a*sum_j[(dot(phi_j)^2)/2-((phi_(j+1)-phi_j)/a)^2/2 -m^2*(1-cos(phi_j))]. Its exact sitewise Euler-Lagrange equation is ddot(phi_j)-(phi_(j+1)-2*phi_j+phi_(j-1))/a^2+m^2*sin(phi_j)=0. The centered spatial operator has exact Fourier symbol -4*sin(k*a/2)^2/a^2, which is even and reciprocal-lattice periodic; on a declared first Brillouin zone its linearization has omega^2=m^2+4*sin(k*a/2)^2/a^2. At fixed k as a tends to zero this is m^2+k^2-a^2*k^4/12+a^4*k^6/360+O(a^6), while the exact zone-edge spatial value is 4/a^2 rather than pi^2/a^2. For a smooth field, the centered stencil derived from both neighbour jets is phi_xx+a^2*phi_xxxx/12+a^4*phi_6/360 plus a remainder bounded by M8*a^6/20160 when the eighth derivative is bounded by M8 on the local stencil interval. If an L-periodic sampled field on a fixed time interval T has uniform bounds Mx, Mxx, Mt, and Mtx on the absolute values of phi_x, phi_xx, phi_t, and phi_tx, then the absolute difference between the sampled discrete action and continuum action is at most T*L*(a*Mt*Mtx/2+a*m^2*Mx/2+a*Mx*Mxx+a^2*Mxx^2/8), and therefore tends to zero with a for fixed bounds. Removing the global factor a at one fixed spacing preserves the site equations under C-VAR-001 but destroys this action-value normalization across refinement. These exact conditional results derive no lattice existence, spacing value, hydrogen medium, EFT termination scale, nonlinear solution convergence, nonabelian sector, material realization, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-001, C-VAR-001. Assumptions: The lattice is one-dimensional, periodic, uniform, and declared with N>=2, L>0, a=L/N; no lattice origin or spacing-selection mechanism is inferred., The field is dimensionless in the normalized C-SG-001 convention, m is nonnegative, and the Fourier wave number uses a chosen first-Brillouin-zone representative., The Taylor statement assumes the displayed derivative exists locally and the eighth derivative has the declared uniform bound on each stencil interval., The action bound assumes an L-periodic continuum field with the four displayed uniform space-time derivative bounds and left-endpoint sampling over a fixed finite time interval., Action convergence, pointwise stencil convergence, and fixed-mode dispersion convergence do not assert convergence or stability of arbitrary nonlinear lattice solutions.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.63.0` with provenance `campaigns/P069-me3-lattice-continuum/adjudication.yaml`.

- `campaigns/P069-me3-lattice-continuum/verify.py`
- `campaigns/P069-me3-lattice-continuum/attempts/0001/result.yaml`
- `campaigns/P069-me3-lattice-continuum/attempts/0002/result.yaml`
- `campaigns/P069-me3-lattice-continuum/attempts/0003/result.yaml`
- `campaigns/P069-me3-lattice-continuum/reviews/independent_lattice_review.py`
- `campaigns/P069-me3-lattice-continuum/evidence/primary-provenance.yaml`
- `campaigns/P069-me3-lattice-continuum/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-LAT-001-review.md`
- `tests/test_lattice_scalar.py`
