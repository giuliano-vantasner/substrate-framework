---
description: Accepted framework claim C-GSK-002
author: framework-registry
created: '2026-08-06T11:41:41Z'
updated: '2026-08-06T11:41:41Z'
tags:
- substrate-framework
- accepted-claim
- C-GSK-002
category: claims
confidence: established
status: active
---
# C-GSK-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GSK-001 with independently supplied (c6,c0)=(1/2,1/4) and angular inputs (B,I)=(1,1), (2,pi+8/3), and (4,20.6496264884189), adaptive double-precision collocation with regular-origin and massive-tail Robin data finds one monotone stationary branch for each input on [10^-4,20]. With solver tolerance 10^-6, 401 initial points, eight coefficient-continuation steps, at most 200000 adaptive nodes, and 8001 independent output quadrature points, the dimensionless energy coefficients E/(12*pi^2*B) are respectively 1.4326169552, 2.7988849886, and 5.1973886988, and 3*pi^2*(2*b_2-b_4)=11.85481448. The maximum reported collocation RMS residual is below 1.1e-6, the maximum endpoint residual below 2e-11, and the maximum relative Derrick residual below 2e-6. Individual coefficients and the signed difference stabilize as the outer radius changes from 14 to 20 to 26; the B=2 residual decreases from about 1.99e-6 to 4.94e-7 as tolerance tightens from 2e-6 to 5e-7; and the B=4 coefficient changes by less than 3e-11 as the inner cutoff changes through 2e-4, 1e-4, and 5e-5. An independent vacuum-complement DOP853 shooting route with Simpson quadrature at outer radius 14 agrees within 3e-7 per coefficient and 1e-5 in the signed difference. Replacing I by B^2 or setting c6=0 moves the signed difference to about 8.12019 or 8.85035 respectively. This is resolution-bounded evidence for the declared truncated-domain stationary branches only; it proves no half-line existence, uniqueness, global or local minimality, full three-dimensional solution, physical coefficient, baryon, nucleus, binding prediction, observation, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GSK-001, C-RMAP-001, C-RMAP-002. Assumptions: The three degree and angular-integral pairs and the two dimensionless coefficients are supplied benchmark inputs, not derived physical parameters., Evidence uses IEEE binary64 arithmetic and the displayed finite domains, endpoint laws, continuation, tolerances, grids, residual norms, and quadrature rules., The reported branch is identified numerically by monotonicity, continuation, refinement, and independent-method agreement; no theorem excludes another branch., Energy coefficients use the exact C-GSK-001 density and normalization E/(12*pi^2*B); the signed difference is not a variational bound or a physical binding energy., The independent method's agreement is limited to the like-for-like outer-radius-14 problem.. Comparators: MK5's source value uses rejected physical inputs, biased angular quadrature, finite Dirichlet walls, and weaker refinement, so it is not this claim, A vacuum-complement shooting representation repairs the preserved degree-four direct-field loss of origin signal without relaxing the oracle, I=B squared and c6=0 mutations materially change the signed difference and defeat a copied-value check.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.157.0` with provenance `campaigns/P218-mk5-generalized-skyrme-solve-audit/adjudication.yaml`.

- `campaigns/P218-mk5-generalized-skyrme-solve-audit/verify.py`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/independent_generalized_skyrme_review.py`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/C-GSK-002-claim-review.md`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/source_adjudication.md`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/candidate-claim.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/primary-numerical-evidence.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/dependency-audit.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/primary-provenance.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/independent-provenance.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/evidence/compatibility-audit.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/reviews/impact_analysis.md`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/attempts/0004/result.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/attempts/0005/result.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/attempts/0006/result.yaml`
- `campaigns/P218-mk5-generalized-skyrme-solve-audit/attempts/0007/result.yaml`
- `src/substrate_framework/generalized_skyrme_radial.py`
- `tests/test_generalized_skyrme_radial.py`
