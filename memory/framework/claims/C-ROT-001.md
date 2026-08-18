---
description: Accepted framework claim C-ROT-001
author: framework-registry
created: '2026-08-11T10:25:00Z'
updated: '2026-08-11T10:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-ROT-001
category: claims
confidence: established
status: active
---
# C-ROT-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Declare a free axisymmetric Euler top in body angular-velocity space with principal inertias diag(A,A,C), exact C>A>0, and exact Omega>0. The circle E_Omega={(Omega*cos(phi),Omega*sin(phi),0): phi real} consists of equilibria. At the member (Omega,0,0), the exact linearization is nonzero rank-one nilpotent, its fundamental matrix is I+t*J, and every period monodromy eigenvalue is one but nonsemisimple. The exact nearby family (r*cos(phi+(C-A)*epsilon*t/A), r*sin(phi+(C-A)*epsilon*t/A),epsilon) solves Euler's equations. With r=Omega and arbitrarily small positive epsilon it reaches squared distance 2*Omega^2+epsilon^2 from the fixed member, so that member is not Lyapunov stable. By contrast, squared Euclidean distance to the entire circle is (r-Omega)^2+epsilon^2 and is constant, so E_Omega is stable as a set in this declared state space. Separately, for an ordinary axisymmetric density with radial second moment R2 and axial moment Z, I_zz-I_xx=-(3/2)*(I_STF)_zz exactly. This ordinary inertia identity does not identify a field theory's collective rotational metric. The theorem establishes no orientation-space stability, forced or dissipative rotor, Skyrme action or inertia, rotating field solution, full-field stability, selected Omega, physical state, fission, gravity, radiation, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-FLO-001. Assumptions: The state is exactly the body angular-velocity vector of a torque-free rigid Euler top with Euclidean distance; attitude variables and other state spaces are outside the claim., A, C, and Omega are exact and positive with C>A; the prolate, spherical, forced, and dissipative cases require separate classification., Stability of the equilibrium set means Lyapunov set stability in the declared body-angular-velocity space and does not imply stability of any fixed member., R2 and Z are ordinary density second moments in the normalized STF convention; their inertia is not assumed equal to a collective field kinetic metric., No accepted claim identifies this abstract rotor with TX1's conditional rational-map moment or with a full physical Skyrmion.. Comparators: TX4's displayed axisymmetric rotor at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; P183 retains its equations and invariants but refutes its fixed-equilibrium stability reading with an exact nonlinear trajectory.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.135.0` with provenance `campaigns/P183-tx4-floquet-stability-audit/adjudication.yaml`.

- `campaigns/P183-tx4-floquet-stability-audit/verify.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/independent_rotating_stability_review.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/C-ROT-001-claim-review.md`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/source_adjudication.md`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0011/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0017/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/input-provenance.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/dependency-audit.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/primary-provenance.yaml`
- `src/substrate_framework/rotating_stability.py`
- `tests/test_rotating_stability.py`
- `formal/SubstrateFramework/Ingested/Phase40TX_RotatingTorus.lean`
