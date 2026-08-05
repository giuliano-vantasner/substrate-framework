---
description: Accepted framework claim C-RMOM-002
author: framework-registry
created: '2026-08-11T07:43:00Z'
updated: '2026-08-11T07:43:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RMOM-002
category: claims
confidence: established
status: active
---
# C-RMOM-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RMOM-001 and the corrected C-RPROF-002 degree-two stationary branch with (B,I)=(2,pi+8/3), IEEE-754 binary64 DOP853 vacuum-complement amplitude shooting on [10^-4,24], 2401 samples, rtol=3e-10, atol=3e-12, maximum step 0.05, canonical trapezoidal integration, and explicit leading origin and massless-tail estimates gives monopole M=286.171598879686 and normalized tensor I_STF=diag(48.4848609876855,48.4848609876855,-96.969721975371). Therefore I_STF_zz/M=-0.338851662271835 in declared dimensionless radial-coordinate-squared units, while the C-MOM-001 triple convention gives Q_zz/M=-1.016554986815505. Independent solve_bvp collocation from a two-power initial profile with tolerance 3e-7, boundary tolerance 3e-8, at most 50000 nodes, and Simpson integration gives M=286.171593977632 and I_STF_zz/M=-0.338851565198, a relative method difference 2.865e-7. Isolated outer-radius 16/24/32/48, origin-cutoff 2e-4/1e-4/5e-5, sample-count 1201/2401/4801, IVP-rtol 1e-8/3e-10/1e-11, and maximum-step 0.1/0.05/0.025 studies pass solver, endpoint, finite-data, monotonicity, trace, convention, and frozen convergence gates. Independent tensor Gauss-Legendre cubature at 24x48 through 96x192 converges to C-RMOM-001's exact B2 angular tensors. This is resolution-bounded evidence for one conditional stationary reduced-ansatz branch. It proves no half-line existence, uniqueness, local or global minimum, full three-dimensional field solution, local conserved stress, physical state or mass, absolute length, rotation, stability, gravitational coupling, waveform, radiation, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RMOM-001, C-RPROF-002. Assumptions: Every exact density, sphere, moment, convention, and interpretation ceiling is inherited from C-RMOM-001, while the radial equation and accepted branch inputs inherit C-RPROF-002., Every decimal is resolution-bounded binary64 evidence at the displayed solver, domain, cutoff, samples, tolerances, step, quadrature, and leading endpoint-estimate conventions., Solver outputs are consumed only after finite-data, endpoint-residual, monotonicity, trace, tensor-convention, energy-closure, refinement, independent-method, and mutation gates pass., Origin and tail additions use leading endpoint powers and are estimates rather than exact omitted nonlinear integrals; isolated cutoff and wall studies bound their practical effect on the stated ratio., The ratio has units of the declared dimensionless radial coordinate squared. A physical value requires an accepted length-scale and state map, neither of which is supplied., The source literal is a post-freeze comparator and does not set a method, parameter, or tolerance. No full-field solution, physical state name, gravitational normalization, rotation frequency, or observation enters the calculation.. Comparators: TX1's exposed I_STF_zz/M literal -0.33885166 and its coupled wall/mesh study; P180 uses it only after exact factorization and independent numeric thresholds were frozen, C-RPROF-002's energy-only branch evidence, which supplies the accepted profile but no intrinsic rank-two moment or physical interpretation.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.132.0` with provenance `campaigns/P180-tx1-intrinsic-quadrupole-audit/adjudication.yaml`.

- `campaigns/P180-tx1-intrinsic-quadrupole-audit/verify.py`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/reviews/independent_moment_review.py`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/reviews/C-RMOM-002-claim-review.md`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/reviews/source_adjudication.md`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/attempts/0006/result.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/numerical-audit.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/input-provenance.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/check-adjudication.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/dependency-audit.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/consumer-audit.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/candidate-comparison.yaml`
- `campaigns/P180-tx1-intrinsic-quadrupole-audit/evidence/primary-provenance.yaml`
- `memory/vantasner/decisions/C-RMOM-002-review.md`
- `memory/vantasner/decisions/TX1-qualified-review.md`
- `src/substrate_framework/rational_map_moments.py`
- `src/substrate_framework/rational_map_radial.py`
- `tests/test_rational_map_moments.py`
- `tests/test_rational_map_radial.py`
