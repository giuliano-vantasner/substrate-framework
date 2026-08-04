---
description: Accepted framework claim C-STG-001
author: framework-registry
created: '2026-08-09T16:40:00Z'
updated: '2026-08-09T16:40:00Z'
tags:
- substrate-framework
- accepted-claim
- C-STG-001
category: claims
confidence: established
status: active
---
# C-STG-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let g_ab be an exact four-dimensional Lorentzian metric with mostly-plus signature, let phi be an exact real scalar, let V(phi) be an exact real potential, and let kappa be exact and positive. Declare the action S=integral sqrt(-g)*[R/(2*kappa)-g^ab*partial_a(phi)*partial_b(phi)/2-V(phi)] d^4x, with compact metric variations or the corresponding gravitational boundary term. Its matter stress is T_ab=partial_a(phi)*partial_b(phi)-g_ab*[(partial phi)^2/2+V], its equations are G_ab=kappa*T_ab and box(phi)=V'(phi), and nabla^a T_ab=(box(phi)-V'(phi))*partial_b(phi), so the stress is conserved on shell. For V=0, positive reference time t0 and scale a0, real phi0, branch s in {-1,1}, and domain t>0, the spatially flat FLRW metric ds^2=-dt^2+a(t)^2*(dx^2+dy^2+dz^2), with a(t)=a0*(t/t0)^(1/3) and phi(t)=phi0+s*sqrt(2/(3*kappa))*log(t/t0), is an exact nonvacuum solution. It has H=1/(3*t), rho=p=1/(3*kappa*t^2), Ricci scalar -2/(3*t^2), and Kretschmann scalar 20/(27*t^4). Thus t=0 is a curvature singularity and the solution approaches flatness as t tends to infinity. On noncompact spatial slices its homogeneous positive energy is extensive, not a localized finite-energy source. This theorem does not identify phi with a refractive index or sine-Gordon breather, derive a localized three-dimensional source, select a physical kappa, or supply a material, observational, gravitational-analog, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The metric is exact, four-dimensional, Lorentzian, and mostly plus; kappa is exact and positive, and floating inputs are outside the exact API., The Einstein-Hilbert normalization, canonical healthy scalar kinetic sign, curvature convention, compact-variation or boundary-term premise, and natural units c=hbar=1 are declared action data., In natural units kappa has length squared, phi has inverse-length dimension, t and t0 have length dimension, and the spatial scale factor and a0 use the declared dimensionless-coordinate convention., The explicit solution assumes V=0, spatial flatness, homogeneity, isotropy, t>0, positive a0 and t0, real phi0, and branch exactly plus or minus one., The t=0 boundary is excluded and curvature singular. The solution is homogeneous and has infinite total energy on noncompact R3; compact spatial topology or a finite cell changes global volume but requires separately declared identifications., The action theorem does not determine a potential other than the selected V=0 solution, a scalar-to-index map, a static localized metric, or initial and boundary data for G3's source witness., No accepted claim identifies this scalar with a sine-Gordon breather, Gordon or optical metric, physical gravity, material medium, observation, or substrate field.. Comparators: G3 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all eleven checks without a NumPy compatibility event, while its unused positive kappa, negative one-point fitted ratio, nonzero remaining Einstein and scalar residuals, divergent optical ratio, Delta-vacuum equivalence, breather-source, independent-route, physical-gravity, and substrate readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.110.0` with provenance `campaigns/P143-g3-scalar-tensor-audit/adjudication.yaml`.

- `campaigns/P143-g3-scalar-tensor-audit/verify.py`
- `campaigns/P143-g3-scalar-tensor-audit/reviews/independent_einstein_scalar_review.py`
- `campaigns/P143-g3-scalar-tensor-audit/reviews/replay_source_graph.py`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0002/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0003/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0004/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0005/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0006/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0007/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/attempts/0008/result.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/source-reproduction.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/source-audit.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/check-adjudication.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/input-provenance.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/dependency-audit.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/consumer-audit.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/candidate-comparison.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/primary-provenance.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/evidence/literature-audit.yaml`
- `campaigns/P143-g3-scalar-tensor-audit/reviews/source_adjudication.md`
- `campaigns/P143-g3-scalar-tensor-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-STG-001-review.md`
- `memory/vantasner/decisions/G3-qualified-review.md`
- `src/substrate_framework/einstein_scalar.py`
- `tests/test_einstein_scalar.py`
