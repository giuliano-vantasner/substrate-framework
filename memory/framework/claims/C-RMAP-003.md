---
description: Accepted framework claim C-RMAP-003
author: framework-registry
created: '2026-08-11T10:25:00Z'
updated: '2026-08-11T10:25:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RMAP-003
category: claims
confidence: established
status: active
---
# C-RMAP-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

For the oriented-sphere angular functional I[R] and conventions of C-RMAP-001, use the local degree-two chart R=(z^2+a1*z+a0)/(b2*z^2+b1*z+b0) about R=z^2 with real coordinate order (Re(a1),Im(a1),Re(a0),Im(a0),Re(b2),Im(b2),Re(b1),Im(b1), Re(b0-1),Im(b0-1)). Exact differentiation under the full-sphere integral gives I[z^2]=pi+8/3 and zero gradient. The exact real symmetric Hessian has rank five, nullity five, and eigenvalues zero five times, pi once, pi+16/3 twice, and 7*pi+64/3 twice. Its kernel is exactly the span of the five independently derived infinitesimal domain-Mobius, target-Mobius, and phase directions displayed by the canonical API; the displayed complementary five-dimensional quadratic form is positive definite. Hence R=z^2 has an exact positive second variation modulo those symmetry directions inside this coefficient chart. This is a chart-local fixed-degree rational-map angular theorem. It establishes no collective kinetic metric, radial or full-field Hessian, global minimum, full three-dimensional solution, dynamical or Floquet stability, physical Skyrmion, fission barrier, gravity, radiation, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RMAP-001, C-SYM-001. Assumptions: The sphere orientation, stereographic coordinate, conformal Jacobian, normalized average, and angular functional are exactly those of C-RMAP-001., Coefficients are exact local chart coordinates about a denominator with b0=1; singular chart boundaries and degree-changing directions are excluded., The displayed symmetry tangents use the declared domain and target Mobius plus phase actions, and the conclusion concerns the Hessian quotient in this finite chart., Positive second variation does not supply a kinetic metric or dynamical stability, and it does not compare arbitrary full-field perturbations., The TX4 finite-grid eigenvalues are post-freeze comparators only; no displayed decimal selects a formula, eigenvalue, or tolerance.. Comparators: TX4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its one-grid finite-difference positive modes agree within resolution, while P183 independently derives stationarity, every exact Hessian entry, the exact kernel, and mutation-sensitive scope.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.135.0` with provenance `campaigns/P183-tx4-floquet-stability-audit/adjudication.yaml`.

- `campaigns/P183-tx4-floquet-stability-audit/verify.py`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0006/derive_exact_shape_hessian.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/independent_rational_map_hessian_review.py`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/C-RMAP-003-claim-review.md`
- `campaigns/P183-tx4-floquet-stability-audit/reviews/source_adjudication.md`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0006/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0015/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/attempts/0017/result.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/input-provenance.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P183-tx4-floquet-stability-audit/evidence/primary-provenance.yaml`
- `src/substrate_framework/rational_map_stability.py`
- `tests/test_rational_map_stability.py`
