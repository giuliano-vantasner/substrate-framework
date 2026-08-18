---
description: Accepted framework claim C-CHI-001
author: framework-registry
created: '2026-08-02T19:00:00Z'
updated: '2026-08-02T19:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CHI-001
category: claims
confidence: established
status: active
---
# C-CHI-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the declared four-real-coordinate model phi=(sigma,pi1,pi2,pi3), use all six standard independent antisymmetric so(4) generators and V=lambda*(phi^T*phi-v^2)^2 with lambda>0 and v>0. At the declared vacuum phi_0=(v,0,0,0), all six infinitesimal invariance residuals and the gradient vanish, the generator-tangent matrix has rank three, its coefficient kernel has dimension three, and the exact Hessian is diag(8*lambda*v^2,0,0,0). Thus this declared classical model has one radial curvature and three independent zero generalized quadratic-mass directions when supplied a positive kinetic metric. At the symmetric stationary point phi=0 the tangent rank is zero. For the explicitly tilted potential V-c*sigma, a positive shifted stationary branch s0 obeys c=4*lambda*s0*(s0^2-v^2) and has transverse curvature c/s0; an anisotropic quadratic term likewise breaks the relevant invariance and lifts its tangent. Separately, for the declared coordinate model U=exp(i*tau_a*pi_a/F) with Pauli matrices and L=A*Tr(partial U*partial U^dagger), the exact leading trace is 2*sum_a(partial pi_a)^2/F^2 and the scalar kinetic metric is (4*A/F^2)*I. Consequently A=F^2/4 gives metric I and quadratic coefficient one half, while A=F^2/16 gives metric I/4 and coefficient one eighth in the same coordinates. A zero potential has zero Hessian; adding m^2*sum_a(pi_a^2)/2 gives Hessian m^2*I. These are conditional O(4) and SU(2) coordinate-model identities depending on C-SYM-001. They establish no chiral symmetry action or its physical breaking, no quantum Goldstone-particle theorem, no physical pion identification, no sigma or nucleon particle, no GMOR relation, no Skyrmion connection, no value of F_pi or a condensate, no absolute mass scale, and no substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SYM-001. Assumptions: The O(4) coordinates, Euclidean inner product, six generator matrices, radial-quartic normalization, positive lambda and v, vacuum branch, and any kinetic metric are declared model data rather than derived physical fields., The nonzero-vacuum count uses the actual rank of all six generator tangents. The coefficient-kernel dimension is the stabilizer dimension because those six matrices are independently verified as a basis., The linear-tilt formula concerns a positive shifted stationary branch satisfying the displayed relation; it is a sigma-model curvature identity and not a QCD or GMOR derivation., The SU(2) expansion uses Hermitian Pauli generators with Tr(tau_a*tau_b)=2*delta_ab, the displayed exponential coordinate, and one fixed coordinate scale F. A field rescaling changes the coordinate convention and cannot make both action prefactors canonical simultaneously., Absence of a potential is a declared action premise. A zero classical Hessian plus a positive kinetic metric is not by itself a quantum particle or physical pion theorem.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.54.0` with provenance `campaigns/P060-pg1-goldstone-hessian/adjudication.yaml`.

- `campaigns/P060-pg1-goldstone-hessian/verify.py`
- `campaigns/P060-pg1-goldstone-hessian/attempts/0002/result.yaml`
- `campaigns/P060-pg1-goldstone-hessian/attempts/0003/result.yaml`
- `campaigns/P060-pg1-goldstone-hessian/attempts/0004/result.yaml`
- `campaigns/P060-pg1-goldstone-hessian/reviews/independent_symmetry_review.py`
- `campaigns/P060-pg1-goldstone-hessian/reviews/source_adjudication.md`
- `campaigns/P060-pg1-goldstone-hessian/evidence/goldstone-provenance.yaml`
- `memory/vantasner/decisions/C-CHI-001-review.md`
- `tests/test_symmetry_breaking.py`
