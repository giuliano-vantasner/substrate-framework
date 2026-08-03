---
description: Accepted framework claim C-COL-001
author: framework-registry
created: '2026-08-05T12:00:00Z'
updated: '2026-08-05T12:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-COL-001
category: claims
confidence: established
status: active
---
# C-COL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Under C-MED-003, let a dimensionless real field be restricted on a fixed spatial domain D to a declared sufficiently differentiable one-parameter profile family u(x,t)=phi(x,q(t)). If partial_q phi is square-integrable and nonzero and lambda>0, exact substitution into the kinetic density gives the positive finite collective metric M(q)=lambda*integral_D((partial_q phi)^2 dx) and kinetic term M(q)*qdot^2/2. For a separately declared twice-differentiable reduced potential U(q), L_red=M(q)*qdot^2/2-U(q) has exact equation M*qddot+(partial_q M)*qdot^2/2+partial_q U=0. At a rest stationary point q0 with U'(q0)=0 and M(q0)>0, the linearization is M(q0)*delta_qddot+U''(q0)*delta_q=0: positive curvature gives a stable angular frequency sqrt(U''/M), zero curvature is linearly neutral, and negative curvature gives real exponential roots with rate sqrt(-U''/M). Under a smooth locally invertible reparameterization q=g(Q), the metric becomes M_Q=M(g(Q))*g'(Q)^2 and the potential Hessian is U_QQ=U_qq*g'^2+U_q*g''; hence at a stationary point U_QQ/M_Q is coordinate invariant while curvature and inertia separately are not. If q is a length coordinate, x is a length coordinate, and lambda has C-MED-003 dimension (E,L,T)=(1,-1,2), then M has (1,-2,2), U'' has (1,-2,0), and their ratio has (0,0,-2). Conditional on an independently established profile/action identification q=R and C-RG-001's capillary potential, R*=T/P has U''=-2*pi*P, so sqrt(2*pi*P/M(R*)) is an unstable exponential rate, not a stable oscillation frequency. These results do not supply the profile, prove its physical realization, couple the continuum and capillary coefficients, select their normalization or a material, identify a quantum or thermal onset, derive stochastic escape, or establish an ignition or observed event.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MED-003, C-RG-001. Assumptions: All C-MED-003 field, coordinate, coefficient, density, positivity, and boundary assumptions hold. The spatial domain is fixed with respect to q, and phi is regular enough for the displayed chain rule, integral, differentiation, and reduced variation., The profile family and coordinate q are declared model data. Positive finite inertia additionally requires a nonzero square-integrable profile derivative; dimensions alone do not establish existence, convergence, normalization, or a material realization., The reduced potential U is real and twice differentiable near the stationary point. The linearization is about q=q0 at rest, and stability terminology refers only to the displayed conservative one-coordinate linear equation., Coordinate covariance assumes a smooth local inverse with nonzero Jacobian. Away from stationarity the gradient-proportional Hessian term must be retained., The capillary specialization separately assumes that the same reduced action uses q=R, C-RG-001's potential, and a positive finite M(R*). C-MED-003 and C-RG-001 do not themselves derive that cross-sector identification., A local unstable exponent is distinct from a Kramers rate, attempt frequency, stable field-mode frequency, hbar energy, thermal crossover, ignition threshold, and measured event.. Comparators: BD4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its body, main formulas, and tally were already exposed, while P102 froze profile, sign, covariance, normalization, and interpretation alternatives before renewed inspection and execution, Phase28BarrierKernel.lean at the same pinned source revision; it compiles but proves only weaker dimension and separate algebraic encodings.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.86.0` with provenance `campaigns/P102-bd4-collective-inertia-audit/adjudication.yaml`.

- `campaigns/P102-bd4-collective-inertia-audit/verify.py`
- `campaigns/P102-bd4-collective-inertia-audit/reviews/independent_collective_review.py`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/source-reproduction.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/source-audit.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/check-adjudication.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/dependency-audit.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/formal-audit.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/consumer-audit.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/evidence/candidate-comparison.yaml`
- `campaigns/P102-bd4-collective-inertia-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-COL-001-review.md`
- `tests/test_collective_coordinates.py`
