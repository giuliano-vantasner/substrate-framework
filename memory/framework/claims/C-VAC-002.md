---
description: Accepted framework claim C-VAC-002
author: framework-registry
created: '2026-08-11T11:56:00Z'
updated: '2026-08-11T11:56:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VAC-002
category: claims
confidence: established
status: active
---
# C-VAC-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GAU-001's connection convention and C-DIM-009's mass- dimension and normalization bookkeeping, independently declare one free complex charged-Dirac field, its fermionic determinant at one loop, the tensor convention Pi_mn=(q^2*g_mn-q_m*q_n)*Pi2(q^2), and a common shift- invariant gauge-preserving regulator. For exact invertible free propagator matrices A=S(p) and B=S(p+q), a spectator vertex G, and the inverse-propagator identity qslash=B^-1-A^-1, exact trace cyclicity gives Tr(qslash*B*G*A)=Tr(G*A)-Tr(G*B); the regulated momentum translation then derives the integrated Ward contraction rather than imposing a transverse ansatz. For exact positive spacelike Q=-q^2, nonnegative mass square M2, positive charge magnitude e with [e^2]=4-d, positive integration dimension d away from unevaluated Gamma poles, and a separately declared positive-integer spinor trace n_gamma, define Delta=M2+x*(1-x)*Q. The exact source-convention form factor is Pi2(-Q)=-2*n_gamma*e^2*Gamma(2-d/2)/(4*pi)^(d/2) times the integral from zero to one of x*(1-x)*Delta^(d/2-2) dx. Pi2 is dimensionless, while the mixed-projector coefficient q^2*Pi2=-Q*Pi2 has mass dimension two. No analytic n_gamma(d) is asserted. The endpoint d=2, n_gamma=2, M2=0 at Q>0 gives Pi2(-Q)=-e^2/(pi*Q) and q^2*Pi2=e^2/pi for one Dirac fermion; it is not the massless complex-scalar limit of C-VAC-001. Separately, hold n_gamma=4, set d=4-2*epsilon, and multiply the master by mu2^epsilon. At zero momentum the bare form factor is -e^2*Gamma(epsilon)*(4*pi*mu2/M2)^epsilon/(12*pi^2), with Laurent residue -e^2/(12*pi^2). Adding the displayed MS-bar pole counterterm and an arbitrary finite local constant c_fin gives Pi2_MSbar(0)=e^2*log(M2/mu2)/(12*pi^2)+c_fin; its log(M2) and log(m) slopes are e^2/(12*pi^2) and e^2/(6*pi^2), while the scale slopes have the opposite signs. For real timelike w=q^2/M2 with 0<=w<4, the finite subtraction is e^2/(2*pi^2) times the integral from zero to one of x*(1-x)*log(1-w*x*(1-x)) dx. Its series begins -e^2/(2*pi^2)*(w/30+w^2/280+w^3/1890), with convergence radius and first branch point four; above threshold requires a separately typed -i0 boundary value. A generator convention change T->c*T, g->g/c preserves only g^2*tr(T*T), not the trace alone. These exact conditional identities derive no physical charged excitation, bare or total Maxwell coefficient, finite matching condition, selected coupling, physical representation or gauge group, preferred dimension, on-shell polarization count, dimensional lift, observation, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GAU-001, C-DIM-009. Assumptions: The free complex charged-Dirac field, fermionic determinant sign, loop order, mass, charge, vertex, tensor sign, quadratic-action convention, and regulator are declared rather than derived from accepted substrate matter., The regulator preserves the common loop-momentum translation used by the Ward difference, or any restoring counterterm is separately governed. A transverse tensor ansatz alone does not satisfy this premise., The physical-dimension family uses [e^2]=4-d and an independently declared integer spinor trace. Dimensional continuation near four holds n_gamma=4 and supplies mu2^epsilon; 2^floor(d/2) is not analytically continued., Q is strictly positive in the spacelike projector representation. The D2 massless endpoint is fermionic and is not an evaluation of an undefined zero-momentum projector or the scalar limit of C-VAC-001., The D4 bare pole is regulator data. MS-bar specifies the displayed pole subtraction but does not fix c_fin, a bare kinetic term, field normalization, matching condition, or total coupling., The real timelike subtraction is restricted to 0<=q^2/M2<4. At and above pair threshold, an explicit complex boundary-value convention and branch analysis are required., Generator and coupling conventions must transform together. No representation, group, matter multiplicity, or coupling value is selected by the invariant weight., No accepted claim identifies this conditional Dirac field, e, M2, mu2, or c_fin with physical matter, observations, a preferred dimension, or a substrate realization.. Comparators: GK3D1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its exact conditional master endpoints and series route survive, while its imposed Ward check, floor-based analytic trace, regulator-free wording, scalar continuity, total-normalization, physical-polarization, group, dimensional-lift, and substrate readings are corrected qualified or rejected, C-VAC-001 remains the distinct massive complex-scalar Euclidean D2 bubble-plus-seagull theorem with a divergent fixed-Q massless limit, Laporta and Jentschura, Phys. Rev. D 109, 096020 (2024), arXiv:2403.07127v2, independently corroborate the dimensional regulator, threshold, zero-momentum subtraction, and opposite-tensor-convention low-momentum coefficient.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.137.0` with provenance `campaigns/P185-gk3d1-general-vacuum-polarization-audit/adjudication.yaml`.

- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/verify.py`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/reviews/independent_dirac_polarization_review.py`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/reviews/replay_source_graph.py`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/reviews/C-VAC-002-claim-review.md`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/reviews/source_adjudication.md`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/attempts/0004/result.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/attempts/0005/result.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/attempts/0006/result.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/evidence/formula-freeze.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/evidence/literature-audit.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/evidence/input-provenance.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/evidence/dependency-audit.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/evidence/consumer-audit.yaml`
- `campaigns/P185-gk3d1-general-vacuum-polarization-audit/evidence/primary-provenance.yaml`
- `src/substrate_framework/dirac_vacuum_polarization.py`
- `tests/test_dirac_vacuum_polarization.py`
