---
description: Accepted framework claim C-RGE-006
author: framework-registry
created: '2026-08-08T22:00:00Z'
updated: '2026-08-08T22:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RGE-006
category: claims
confidence: established
status: active
---
# C-RGE-006

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let C-RGE-005 supply an exact three-factor gauge-only coefficient ledger (b,B), and let inverse couplings a_i=4*pi/g_i^2 remain positive. In the downward coordinate u=log(Lambda/mu), its declared beta convention gives da_i/du=b_i/(2*pi)+sum_j B_ij/(8*pi^2*a_j). Supply a positive reference scale mu0, positive high-boundary ratios S, a real rank-two 2-by-3 constraint matrix C with nonzero target vector d, a nonzero real readout vector w, and a positive readout normalization N. The conditional inverse problem is a(0)=A*S with unknown A>0 and T=log(Lambda/mu0)>0, subject to C*a(T)=d; its remaining declared coordinate is w dot a(T)/N. When B=0, q=T/(2*pi) and a(T)=A*S+q*b. If the exact design matrix with columns C*S and C*b is nonsingular and its solution (A,q) and resulting trajectory are positive, (A,q)=design^(-1)*d is the unique exact solution. For the separately supplied specialization b=(41/10,-19/6,-7), B=((199/50,27/10,44/5),(9/10,35/6,12),(11/10,9/2,-26)), mu0=227969/2500 in the supplied scale unit, S=(1,1,1), C rows (0,0,1) and (5/3,1,0), d=(500/59,1279/10), w=(0,1,0), and N=1279/10, the zero-matrix solution is exactly A=1639681/39530, q=186383/39530, and readout=6296809/30335322. The nonzero-matrix status-gated numerical solution is A=41.3445253, T=29.1415861, Lambda=4.13015e14 in the supplied scale unit, and readout=0.210641136; DOP853 tolerance refinement, Radau, and an independent direct-gauge- coupling formulation agree beyond the reported digits, close the two constraints below 6e-14, and remain positive. Rescaling mu0 by a common positive factor rescales Lambda by that factor and leaves A, T, the low inverse couplings, and readout unchanged. This is a conditional inverse solution on supplied coordinates, not an ab-initio prediction. It excludes physical input provenance and uncertainty, a preferred equal boundary, Yukawa terms, multiple-Abelian kinetic mixing, thresholds, matching, scheme conversion, global perturbative validity, observed running, unification, unknown higher-order tensors, an all-orders no-go, and substrate realization. A comparator-fitted replacement B->k*B is a target-dependent one-parameter inverse family and grants none of those excluded conclusions.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RGE-004, C-RGE-005. Assumptions: The factor order, exact gauge-only coefficient ledger, inverse-coupling convention, positive reference scale, positive boundary ratios, rank-two low constraints, nonzero targets and readout, and positive normalization are supplied rather than selected by the solver., The exact zero-matrix formula requires a nonsingular two-column design, positive solved amplitude and log span, and a positive affine trajectory. Other ranks, signs, domains, or constraint counts require separate branches., The nonzero-matrix result is double-precision numerical evidence for the displayed specialization. Solver success, root residual, trajectory positivity, tolerances, integration method, shooting coordinates, and sample policy remain part of its evidence., The supplied low coordinates and scale label are not accepted observations or derived physical inputs. The measured weak coordinate is excluded from construction and appears only as a post-solve comparator or explicit inverse-target probe., C-RGE-005's same-order Yukawa and multiple-Abelian omissions remain in force. Thresholds, matching, scheme conversion, higher-loop tensors, boundary provenance, and uncertainty data would define a different problem., The reference-scale covariance changes only the common dimensionful scale while holding every dimensionless coefficient, boundary ratio, constraint coordinate, and normalization fixed., A physical unification or prediction interpretation requires separately accepted field content, perturbative regime, thresholds, matching, boundary dynamics, input provenance, measurement map, and uncertainty propagation.. Comparators: WM6 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its conditional gauge-only solve survives, while its rounded exactness, hard-coded regression, pending-SM4 scale window, comparator-use prose, local coefficient forecast, fitted uniform-matrix all-orders reading, effect-attribution list, physical prediction, unification, and substrate conclusions are qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.100.0` with provenance `campaigns/P130-wm6-two-loop-running-audit/adjudication.yaml`.

- `campaigns/P130-wm6-two-loop-running-audit/verify.py`
- `campaigns/P130-wm6-two-loop-running-audit/reviews/independent_direct_coupling_review.py`
- `campaigns/P130-wm6-two-loop-running-audit/attempts/0001/result.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/attempts/0002/result.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/attempts/0003/result.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/source-reproduction.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/source-audit.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/check-adjudication.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/input-provenance.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/dependency-audit.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/consumer-audit.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/candidate-comparison.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/evidence/primary-provenance.yaml`
- `campaigns/P130-wm6-two-loop-running-audit/reviews/source_adjudication.md`
- `campaigns/P130-wm6-two-loop-running-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-RGE-006-review.md`
- `src/substrate_framework/gauge_running.py`
- `tests/test_gauge_running.py`
