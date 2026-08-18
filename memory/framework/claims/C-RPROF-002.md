---
description: Accepted framework claim C-RPROF-002
author: framework-registry
created: '2026-08-07T15:30:00Z'
updated: '2026-08-07T15:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RPROF-002
category: claims
confidence: established
status: active
---
# C-RPROF-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RPROF-001 and on accepted angular inputs (B,I)=(1,1),(2,pi+8/3),(4,20.6496264884189), two independent float64 routes give resolution-bounded evidence for one monotone stationary branch at each input. Vacuum-complement DOP853 amplitude shooting on [10^-4,24] with regular-origin and massless-tail Robin data, rtol=3e-10, atol=3e-12, maximum step 0.05, 2401 samples, shared trapezoidal integration, and explicit leading endpoint-energy estimates gives conventional conditional coefficients E/(12*pi^2) of 1.2314456867, 2.4162704269, and 4.5460579996, hence per-degree values 1.2314456867, 1.2081352135, and 1.1365144999. The relative E2/E4 imbalances are 4.98e-9, 1.50e-11, and 3.42e-13. Independent solve_bvp collocation from a fresh two-power initial construction on the same cutoffs, tolerance 3e-7, adaptive residual below 3e-7, and Simpson integration gives 1.2314503696, 2.4162703856, and 4.5460579996. Isolated sampled-quadrature, origin-cutoff, outer-domain, IVP-tolerance, and maximum-step refinements preserve the values and ordering. Accepted, source-biased, I=B, and I=B^2 angular inputs give materially distinct energies; both simple mutations still preserve the selected ordering, so comparator rejection is not its oracle. This is numeric evidence for three declared stationary branches and their conditional selected ordering only. It proves no half-line existence or uniqueness theorem, local or global minimum, rational-map angular minimum, variational upper bound, full three-dimensional solution, physical baryon, deuteron, alpha particle or nucleus, fission threshold, binding hierarchy, reaction, yield, quantum state, mass scale, material, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RPROF-001, C-RMAP-001, C-RMAP-002. Assumptions: All C-RPROF-001 premises and interpretation ceilings hold. C-RMAP-001 supplies I(1) and I(2), while C-RMAP-002 supplies only resolution-bounded I(4) for its declared map and no angular or radial minimization theorem., Every reported decimal is resolution-bounded IEEE-754 binary64 evidence at the displayed equations, cutoffs, boundary data, solver settings, sampling, integration, and leading endpoint-estimate conventions., The canonical route evolves g=pi-f because the B>1 origin perturbation is smaller than ordinary relative error on f near pi; attempts 0002 and 0003 preserve the failed direct-f representation and root-tightening oracle., Leading origin and tail energy estimates are asymptotic truncation estimates, not exact omitted integrals. Independent collocation uses the same leading convention only for like-for-like comparison., Monotonic profiles, small residuals, virial balance, method agreement, refinements, and angular-input mutations validate the stationary-branch claim but do not establish existence, uniqueness, or minimization outside the tested numerical surface., C-MOD-002 is a compatibility comparator at B=1 and is not a derivation input. No literature energy decimal, physical state name, mass, binding, reaction, or yield enters branch selection or pass thresholds.. Comparators: E2's hash-pinned biased-angular hard-wall results and cited literature neighborhoods; P105 claims no comparator blinding and rejects decimal closeness as a concept-selection oracle.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.89.0` with provenance `campaigns/P105-e2-rational-map-radial-profiles/adjudication.yaml`.

- `campaigns/P105-e2-rational-map-radial-profiles/verify.py`
- `campaigns/P105-e2-rational-map-radial-profiles/reviews/independent_radial_review.py`
- `campaigns/P105-e2-rational-map-radial-profiles/attempts/0002/result.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/attempts/0003/result.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/attempts/0004/result.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/attempts/0005/result.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/attempts/0006/result.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/source-reproduction.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/source-audit.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/check-adjudication.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/dependency-audit.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/consumer-audit.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/candidate-comparison.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/primary-provenance.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RPROF-002-review.md`
- `tests/test_rational_map_radial.py`
- `formal/SubstrateFramework/Ingested/Phase29YieldKernel.lean`
- `formal/SubstrateFramework/Ingested/Phase40TX_RotatingTorus.lean`
