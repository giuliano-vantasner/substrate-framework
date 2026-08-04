---
description: Accepted framework claim C-KRN-002
author: framework-registry
created: '2026-08-09T06:00:00Z'
updated: '2026-08-09T06:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-KRN-002
category: claims
confidence: established
status: active
---
# C-KRN-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let C-KRN-001 fix the inverse-angular Fourier convention and its subcritical Riesz kernel. Supply a positive real analytic dimension parameter d, positive radii r and r0, and a real nonzero inverse-kernel coefficient A. Put s=d/2-epsilon with epsilon>0, subtract the subcritical kernel's value at r0, and only then take epsilon to zero from above. The exact critical limit is Gcrit(r;r0)=2*log(r0/r)/[A*4^(d/2)*pi^(d/2)*Gamma(d/2)]. The unsubtracted kernel diverges through Gamma(epsilon); changing r0 changes Gcrit only by a radius-independent constant; and dGcrit/dr=-2/[A*4^(d/2)*pi^(d/2)*Gamma(d/2)*r]. At d=2 this becomes log(r0/r)/(2*pi*A), with the same unit radial-flux normalization as C-MAX-001's source-normalized logarithmic branch. C-MAX-001's ordinary d=1 full-line linear branch is a separately prescribed distributional inverse and is outside the subcritical Riesz integral. Separately, for the C-KRN-001 subcritical domain 0<s<d/2, if real source Q and probe q are supplied and the dictionary phi=Q*G, U=q*phi, F_r=-dU/dr is declared, then the radial-force power is 2s-d-1. Inverse-square behavior therefore selects the family d=2s+1, not d or s separately; the valid noninteger pair (s,d)=(9/10,14/5) is one exact counterexample to endpoint uniqueness. A real d in these gamma functions is an analytic continuation parameter, not by itself an integer Euclidean space, metric-measure space, Hausdorff or spectral dimension, Dirichlet form, diffusion, fractal medium, or physical dimension. The theorem imports d, s, A, Fourier convention, source, probe, reference, and force dictionary. It derives no endpoint selection, dimensional lift, gauge action, charged ontology, observed force, geometry, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-KRN-001, C-MAX-001. Assumptions: The inverse-angular Fourier convention, subcritical normalization, positive r and d, nonzero A, and one-sided approach s=d/2-epsilon are supplied; the critical theorem is a reference-subtracted limit rather than the divergent unsubtracted kernel., The positive reference radius fixes an additive constant only. Other boundary or quotient prescriptions define separately governed inverses., The subcritical force theorem additionally supplies 0<s<d/2, source Q, probe q, phi=Q*G, U=q*phi, and F_r=-dU/dr. Without that dictionary a Green-kernel derivative is not a physical force., Inverse-square behavior constrains one combination of d and s. Selecting d=3 requires s=1 independently, and selecting s=1 requires d=3 independently; neither follows from the exponent alone., The ordinary d=1 and critical d=2 branches require the separately stated distributional or reference prescriptions and cannot be obtained by silently evaluating the subcritical integral outside its domain., Analytic continuation in d supplies no metric, measure, topology, diffusion, Dirichlet form, Hausdorff dimension, spectral dimension, walk dimension, or physical medium., No accepted claim identifies these parameters or source/probe strengths with a substrate excitation, electric charge, gauge sector, observed force, or dimensional lift.. Comparators: EM7 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its declared-symbol identities subcritical Riesz formula and Coulomb endpoint survive, while its single-regime d1/d2/d3 reading, critical Boolean, supercritical FFT residual, fractal geometry, endpoint selection, dimensional lift, gauge-sector, physical-force, and substrate conclusions are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.104.0` with provenance `campaigns/P136-em7-fractional-force-audit/adjudication.yaml`.

- `campaigns/P136-em7-fractional-force-audit/verify.py`
- `campaigns/P136-em7-fractional-force-audit/reviews/independent_critical_riesz_review.py`
- `campaigns/P136-em7-fractional-force-audit/reviews/replay_source_graph.py`
- `campaigns/P136-em7-fractional-force-audit/attempts/0002/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/attempts/0004/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/attempts/0005/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/attempts/0006/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/attempts/0007/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/attempts/0008/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/attempts/0009/result.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/source-reproduction.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/source-audit.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/check-adjudication.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/input-provenance.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/dependency-audit.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/consumer-audit.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/candidate-comparison.yaml`
- `campaigns/P136-em7-fractional-force-audit/evidence/primary-provenance.yaml`
- `campaigns/P136-em7-fractional-force-audit/reviews/source_adjudication.md`
- `campaigns/P136-em7-fractional-force-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-KRN-002-review.md`
- `memory/vantasner/decisions/EM7-qualified-review.md`
- `src/substrate_framework/momentum_kernels.py`
- `tests/test_momentum_kernels.py`
