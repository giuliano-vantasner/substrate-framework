---
description: Accepted framework claim C-RMOM-001
author: framework-registry
created: '2026-08-11T07:43:00Z'
updated: '2026-08-11T07:43:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RMOM-001
category: claims
confidence: established
status: active
---
# C-RMOM-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

On the oriented unit sphere and conformal-Jacobian convention of C-RMAP-001, declare the conditional angular-resolved density epsilon=f_prime^2+2*sin(f)^2*(1+f_prime^2)*J/r^2 +sin(f)^4*J^2/r^4 for an exact real radial profile f. If the declared map has normalized sphere averages <J>=B and <J^2>=I, exact sphere integration of r^2*epsilon gives precisely C-RPROF-001's radial density r^2*f_prime^2+2*B*sin(f)^2*(1+f_prime^2) +I*sin(f)^4/r^2. Its normalized second STF moment factorizes as I_STF=H1*A1+H2*A2, where H1=integral_0^infinity 2*r^2*sin(f)^2*(1+f_prime^2) dr, H2=integral_0^infinity sin(f)^4 dr, and Ak=integral_S2 J^k*(n*n^T-delta/3) dOmega. The isotropic radial term contributes no STF part. For R(z)=z, J=1 and A1=A2=0 exactly. For the axial map R(z)=z^2, writing u=cos(theta) gives J=4*(1-u^2)/(1+u^2)^2, <J>=2, and <J^2>=pi+8/3. Both angular tensors are diagonal with A_xx=A_yy=-A_zz/2 and exact axial coefficients A1_zz=8*pi*(3*pi-10)/3<0 and A2_zz=8*pi*(3*pi-16)/9<0. Hence every nontrivial integrable declared profile with positive H1 or H2 has I_STF=diag(q,q,-2*q) with q>0. In the C-MOM-001 convention the source quadrupole is Q=3*I_STF. These are exact conditional reduced-ansatz moment identities. I_STF/M has radial-coordinate-squared units and is not a scale-free physical observable. The result establishes no full three-dimensional field solution, local conserved physical stress, stationary-profile existence or minimum, physical baryon or nucleus, absolute scale, rotation, gravity, waveform, radiation, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RMAP-001, C-RPROF-001, C-MOM-001. Assumptions: The domain and target sphere, orientation, stereographic coordinate, conformal Jacobian, normalized sphere average, and axial map conventions are exactly those of C-RMAP-001., The angular-resolved density is a separately declared conditional local density whose exact sphere average matches C-RPROF-001; neither accepted predecessor claim derives it from a physical Skyrme action or full field., The radial profile is exact, real, differentiable, and integrable enough for the displayed monopole and second-moment integrals. The strict sign requires H1 or H2 to be positive, as for every nonvacuum real profile not identically at a sine vacuum., Cartesian moments use the normalized I_STF and triple Q conventions of C-MOM-001. Calling the normalized tensor Q without the factor three is a convention error., A static nonzero STF tensor has zero positive-order time derivatives and supplies no radiation verdict without separately accepted dynamics and coupling., Map degree, a conditional radial branch, a full three-dimensional solution, a physical baryon or nucleus, and an observed source are distinct objects.. Comparators: TX1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its nine native checks pass, while P180 derives the exact local-density closure and B2 angular coefficients independently and corrects its tensor normalization, tail formula, solver semantics, B4 scope, and physical prose.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.132.0` with provenance `campaigns/P180-tx1-intrinsic-quadrupole-audit/adjudication.yaml`.

- `campaigns/P180-tx1-intrinsic-quadrupole-audit/verify.py`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/reviews/independent_moment_review.py`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/reviews/C-RMOM-001-claim-review.md`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/reviews/source_adjudication.md`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/attempts/0004/result.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/attempts/0005/result.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/attempts/0006/result.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/source-audit.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/check-adjudication.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/input-provenance.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/dependency-audit.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/candidate-comparison.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/primary-provenance.yaml`
- `memory/vantasner/decisions/C-RMOM-001-review.md`
- `memory/vantasner/decisions/TX1-qualified-review.md`
- `src/substrate_framework/rational_map_moments.py`
- `tests/test_rational_map_moments.py`
