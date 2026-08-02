---
description: Accepted framework claim C-PDE-009
author: framework-registry
created: '2026-08-02T11:30:00Z'
updated: '2026-08-02T11:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-009
category: claims
confidence: established
status: active
---
# C-PDE-009

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the dimensionless radial-background linearization of C-PDE-003, let n=(n_x,n_y,n_z) be a unit direction and use the unnormalized real l=2 angular basis P2(n_z), n_x^2-n_y^2, 2*n_x*n_y, 2*n_x*n_z, and 2*n_y*n_z. Every basis element obeys Delta_Omega Y=-6*Y. Consequently, for any sufficiently differentiable radial background P(r,t), every real m component has the same radial equation psi_tt-psi_rr-2*psi_r/r+6*psi/r^2+cos(P)*psi=0 and the same regular origin law psi=O(r^2); m-degeneracy does not supply a separated frequency, normalization, or mode existence. Replacing cos(P) by a time average Cbar(r) defines a different equation whose exact omitted term is (cos(P)-Cbar)*psi. For P=a(r)*cos(tau), Cbar=J_0(a) and cos(P)-Cbar=-2*J_2(a)*cos(2*tau)+2*J_4(a)*cos(4*tau)-..., with leading small-a term -a^2*cos(2*tau)/4. Thus an eigenfunction of the averaged radial operator is a solution of the full linearized equation only when the displayed pointwise defect vanishes or a separate Floquet argument supplies the missing time dependence. At a positive cutoff epsilon the regular leading series satisfies epsilon*psi_r-2*psi=O(epsilon^4), so zero value paired with nonzero derivative is not nontrivial regular l=2 data. These are exact angular, equation, and regularity statements. They establish no averaged or Floquet eigenmode, bound state, frequency, stability, nonlinear deformation, infinite-domain localization, gravity, radiation, absolute scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-PDE-003. Assumptions: The dimensionless field equation, radial-background regularity, and formal first-order perturbation meaning are exactly those of C-PDE-003., The five displayed real angular functions are deliberately unnormalized; any normalized spherical-harmonic convention requires explicit coefficient conversion., P, psi, and their derivatives and time averages exist on the declared domain, and the phase average for the harmonic example spans a full 2*pi interval., The pointwise averaging defect is an equation-equivalence test, not a general no-go theorem for Floquet solutions with independently solved time dependence.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.48.0` with provenance `campaigns/P054-qb3-triaxial-l2-polarizations/adjudication.yaml`.

- `campaigns/P054-qb3-triaxial-l2-polarizations/verify.py`
- `campaigns/P054-qb3-triaxial-l2-polarizations/attempts/0002/result.yaml`
- `campaigns/P054-qb3-triaxial-l2-polarizations/attempts/0005/result.yaml`
- `campaigns/P054-qb3-triaxial-l2-polarizations/reviews/independent_cartesian_review.py`
- `campaigns/P054-qb3-triaxial-l2-polarizations/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PDE-009-review.md`
- `tests/test_triaxial_l2.py`
- `tests/test_sine_gordon_l_modes.py`
