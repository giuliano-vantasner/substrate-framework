---
description: Accepted framework claim C-PDE-013
author: framework-registry
created: '2026-08-11T07:12:00Z'
updated: '2026-08-11T07:12:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PDE-013
category: claims
confidence: established
status: active
---
# C-PDE-013

## Statement
The accepted statement is reproduced exactly from the claim registry.

On the exact C-STG-002 reduced model, declare central amplitude A=3, dimensionless coupling alpha=0.03, IEEE float64, origin cutoff epsilon=0.001, finite wall R=40, and frequency constrained to 0<Omega<1. Use the C-STG-002 second-order scalar and lapse and cubic mass origin series, the finite-wall approximate evanescent Robin condition a_x(R)+[k_R+1/R]*a(R)=0 with k_R^2=[1-Omega^2/f(R)]/f(R)>0, and the exterior Schwarzschild gauge match Phi(R)=log(f(R))/2. SciPy adaptive collocation with 400 initial points, tolerance 1e-10, and at most 100000 nodes converges to Omega=0.890839827775792, m(R)=0.290960714264522, and extrapolated central Phi_0=-0.182426921486489. It uses 3408 adaptive nodes, has maximum collocation RMS residual 9.99802e-11, zero boundary residual at reported precision, maximum off-grid relative first-order ODE residual 7.01282e-11, and minimum full-domain f=0.879013430362296. Axis-isolated initial-mesh 200/400/800, tolerance 1e-6/1e-8/1e-10, origin-cutoff 0.002/0.001/0.0005, and wall 30/40/60 studies all pass the frozen solver, residual, evanescent-tail, and horizon gates. Across each axis against its finest or largest reference, the maximum normalized state, frequency, and outer-mass differences are respectively 1.8344020768e-8, 3.1371716336e-10, and 4.7119512736e-9, below the frozen 2e-6, 2e-7, and 2e-7 gates. An independently written DOP853 plus two-variable root-shooting method with wall continuation gives Omega=0.890839827776100, m(R)=0.290960714264587, Phi_0=-0.182426921486121, and minimum f=0.879018721894243. Zero-coupling, wrong-central-amplitude, and wrong-J_1-sign mutations fail their preregistered gates. This is numeric evidence for one declared finite-wall solution of the phase-averaged reduced BVP. The amplitude and alpha are free branch coordinates, the wall is not spatial infinity, and the result establishes no uniqueness, exact half-line state, pointwise time-dependent Einstein-scalar solution, full oscillaton, nonminimal Horndeski theory, physical scale, observation, material gravity, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-STG-002, C-PDE-012. Assumptions: Every exact equation, scale, domain, and phase-averaging ceiling is inherited from C-STG-002; finite-wall and forced-endpoint semantics inherit C-PDE-012., The central amplitude, dimensionless coupling, origin cutoff, finite wall, Robin approximation, lapse gauge, precision, initial mesh, tolerance, maximum nodes, and frequency parameterization are declared numerical-model data., Solver completion is accepted only with finite output, positive full-domain f, positive evanescent tail rate, retained collocation and off-grid residuals, boundary residuals, every declared axis refinement, independent shooting, and load-bearing mutations., Off-grid residuals compare an independent cubic-spline derivative with the first-order ODE and normalize by one plus the pointwise maximum RHS magnitude; state comparisons normalize each component by one plus its reference maximum., The outer Robin condition is an asymptotic finite-radius approximation. Wall stability supports the reduced core but does not prove exact half-line localization or suppress C-STG-002's discarded time harmonics., Alpha and A are free dimensionless branch coordinates; no accepted evidence selects physical kappa, F, mu, total mass, or a material or observational interpretation.. Comparators: SC2's amplitude-three alpha=0.03 branch at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64, inspected before corrected threshold selection and used only as a post-freeze reproduction comparator, C-PDE-006's flat amplitude-2.5 multiharmonic finite-box family, which differs in amplitude, harmonic content, gravity, and outer-channel data and does not select this branch.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.131.0` with provenance `campaigns/P179-sc2-static-einstein-scalar-audit/adjudication.yaml`.

- `campaigns/P179-sc2-static-einstein-scalar-audit/verify.py`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/independent_einstein_scalar_review.py`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/replay_source_graph.py`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/C-PDE-013-claim-review.md`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/source_adjudication.md`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0005/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0006/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0007/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0008/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/attempts/0010/result.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/numeric-thresholds.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/numerical-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/input-provenance.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/dependency-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/consumer-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/candidate-comparison.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/accepted-evidence-reuse.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/compatibility-audit.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/evidence/primary-provenance.yaml`
- `campaigns/P179-sc2-static-einstein-scalar-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-PDE-013-review.md`
- `memory/vantasner/decisions/SC2-qualified-review.md`
- `src/substrate_framework/spherical_einstein_scalar_bvp.py`
- `tests/test_spherical_einstein_scalar_bvp.py`
