---
description: Accepted framework claim C-EFT-001
author: framework-registry
created: '2026-08-02T18:00:00Z'
updated: '2026-08-02T18:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-EFT-001
category: claims
confidence: established
status: active
---
# C-EFT-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let V, J_even, and J_odd be real n-entry columns and let K be a nonempty real symmetric invertible n-by-n kernel. In the declared plus-source convention L(V)=V^T*K*V/2+V^T*J with J=J_even+J_odd, component stationarity gives V_star=-K^-1*J, the exact residual K*V_star+J=0, and the reduced term L_eff=-J^T*K^-1*J/2. Its source decomposition consists of the two even squares -J_even^T*K^-1*J_even/2 and -J_odd^T*K^-1*J_odd/2 plus the cross term -(J_even^T*K^-1*J_odd+J_odd^T*K^-1*J_even)/2. Under the declared bookkeeping K and J_even are parity even and J_odd is parity odd, so only the cross term changes sign; it vanishes when either source is absent. For K=M+D with symmetric invertible M and symmetric D, define A=M^-1*D and R_N=sum_(n=0)^N((-A)^n*M^-1). Exact multiplication gives R_N*(M+D)-I=(-1)^N*A^(N+1) and (M+D)*R_N-I=(-1)^N*M*A^(N+1)*M^-1. Thus a finite low-momentum inverse expansion is only a formal truncation under separately supplied power counting and convergence premises; its returned nonzero residual cannot be identified with an exact inverse. Finally, for a field-dependent stationary substitution, the chain rule gives delta Gamma_eff=(delta Gamma)_V+(partial Gamma/partial V)_star*delta V_star, so the induced-field term vanishes on the actual stationary equation while the supplied explicit variation remains. Consequently, if a starting functional is an inhomogeneous term plus invariant local terms with free coefficients, stationary elimination neither selects those coefficients nor creates a missing inhomogeneous anomaly variation. This is a conditional finite-dimensional action theorem. It fixes no field content, source, kernel, mass, coupling, boundary term, operator basis, or coefficient and supplies no HLS field content, no physical vector meson, no WZW functional, no anomaly coefficient, no vector dominance or KSRF relation, no baryon interpretation, no N_c, no absolute scale, and no substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: All matrices and columns are finite-dimensional over the reals; K is nonempty, symmetric, and invertible, and every displayed product has compatible dimensions., The action uses exactly the displayed plus-source and one-half conventions; changing either changes the stationary solution or reduced sign., The parity statement is bookkeeping under separately declared transformations K maps to K, J_even maps to J_even, and J_odd maps to minus J_odd; it does not classify a physical field without its intrinsic parity and spacetime transformation., The inverse series requires symmetric invertible M and symmetric D; treating it as a convergent inverse additionally requires M+D to be invertible and a suitable analytic convergence condition, while derivative power counting alone licenses only the displayed finite formal expansion., The variation statement assumes a differentiable functional, a true stationary solution for every eliminated component, and boundary conditions or integrations by parts that make the displayed variational equation valid., The anomaly consequence is conditional on a separately supplied split into an inhomogeneous variation and exactly invariant local terms; the theorem derives neither split nor any physical anomaly data.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.53.0` with provenance `campaigns/P059-wz4-hls-vector-elimination/adjudication.yaml`.

- `campaigns/P059-wz4-hls-vector-elimination/verify.py`
- `campaigns/P059-wz4-hls-vector-elimination/attempts/0002/result.yaml`
- `campaigns/P059-wz4-hls-vector-elimination/attempts/0003/result.yaml`
- `campaigns/P059-wz4-hls-vector-elimination/reviews/independent_elimination_review.py`
- `campaigns/P059-wz4-hls-vector-elimination/reviews/source_adjudication.md`
- `campaigns/P059-wz4-hls-vector-elimination/evidence/hls-anomaly-provenance.yaml`
- `memory/vantasner/decisions/C-EFT-001-review.md`
- `tests/test_effective_actions.py`
