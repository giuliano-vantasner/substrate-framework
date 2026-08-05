---
description: Accepted framework claim C-QBL-005
author: framework-registry
created: '2026-08-05T22:38:24Z'
updated: '2026-08-05T22:38:24Z'
tags:
- substrate-framework
- accepted-claim
- C-QBL-005
category: claims
confidence: established
status: active
---
# C-QBL-005

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-QBL-003's declared quartic whole-line energy, write its field potential as V_kappa(f)=kappa^2*f^2/2-f^4/48. For any real field value f, V_kappa''(0)-V_kappa''(f)=f^2/4. If, independently, a nonzero real lambda and local multiplier c=lambda*f are declared, then the exact conditional relation is D=c^2/(4*lambda^2). The multiplier declaration and its normalization do not follow from the potential. On C-QBL-001's profile f0=sqrt(24)*kappa*sech(kappa*(x-x0)), D=6*kappa^2*sech(kappa*(x-x0))^2 and the associated fluctuation potential has one global minimum at x0. For the actual two C-QBL-003 bound-mode shapes and multiplier f0, the C-OVL-001 normalized expectations are 9*pi*sqrt(24)*kappa/32 and 3*pi*sqrt(24)*kappa/16, with fixed ratio 2/3; both tend to zero as kappa tends to zero while the two levels remain below the positive continuum threshold for every kappa>0. Thus the local identity neither states that a nonzero shallow one-dimensional well has no bound state nor makes small absolute overlap and binding contradictory. Independently, C-OVL-002's exact Poschl-Teller ground eigenvalue is negative for every positive well depth. Replacing c by a nonlinear or independent multiplier, rescaling its lambda, or deforming the potential changes the relation. These statements derive no stability, physical condensate or Yukawa interaction, generation, mass hierarchy, mixing, multisoliton solution, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-QBL-003, C-OVL-001, C-OVL-002. Assumptions: The quartic field potential and whole-line scalar Hessian are exactly C-QBL-003's declared dimensionless model; they are not inferred from the exact-sine or radial Q-ball models., The local coupling multiplier c=lambda*f and its real nonzero normalization lambda are separate model declarations. The pointwise c is not the integrated C-OVL-001 expectation y., The one-center statement concerns C-QBL-001's positive translated sech profile and the associated quartic fluctuation potential on the real line. It is not an arbitrary-potential or arbitrary-profile uniqueness theorem., The two C-QBL-003 levels are bound relative to the positive continuum threshold in the declared scalar Hessian. Their negative and zero eigenvalues remain nonparticle nongeneration objects., The overlap formulas use C-OVL-001's normalized whole-line Cartesian measure and the profile amplitude sqrt(24)*kappa. Their absolute small-kappa limit is not a physical mass prediction and their fixed ratio is not a hierarchy., The shallow-well counterexample is C-OVL-002's separately declared whole-line Poschl-Teller Hamiltonian. It disproves a universal no-bound-state inference but does not identify a physical second condensate or multisoliton., Nonlinear or independent multiplier maps and potential deformations define different conditional models; the displayed lock is not invariant under those changes., No accepted claim maps the field multiplier Hessian levels or translated wells to Yukawa interactions physical masses generations mixing Standard-Model matter or substrate objects.. Comparators: GC1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its native nine-check result is retained only after the committed P208 freeze and individual predicate audit, GC1's exact-sine numerical section has curvature deficit (1-cos(f))/2 rather than f^2/4 beyond leading small amplitude, C-OVL-002's positive-depth Poschl-Teller family and the C-QBL-003 small-kappa scale family are exact counterexamples to the claimed light-versus-bound contradiction, Nonlinear and independent multiplier maps plus an epsilon*f^6 potential deformation test the declaration boundary.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.151.0` with provenance `campaigns/P208-gc1-overlap-binding-lock-audit/adjudication.yaml`.

- `campaigns/P208-gc1-overlap-binding-lock-audit/verify.py`
- `campaigns/P208-gc1-overlap-binding-lock-audit/reviews/independent_curvature_review.py`
- `campaigns/P208-gc1-overlap-binding-lock-audit/reviews/replay_source_graph.py`
- `campaigns/P208-gc1-overlap-binding-lock-audit/reviews/C-QBL-005-claim-review.md`
- `campaigns/P208-gc1-overlap-binding-lock-audit/reviews/GC1-disposition-review.md`
- `campaigns/P208-gc1-overlap-binding-lock-audit/reviews/source_adjudication.md`
- `campaigns/P208-gc1-overlap-binding-lock-audit/reviews/impact_analysis.md`
- `campaigns/P208-gc1-overlap-binding-lock-audit/attempts/0001/result.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/attempts/0002/result.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/attempts/0003/result.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/formula-freeze.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/input-provenance.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/dependency-audit.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/consumer-audit.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/candidate-comparison.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/implementation-audit.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/impact-analysis.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/primary-provenance.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/independent-provenance.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/source-reproduction.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/compatibility-audit.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/source-audit.yaml`
- `campaigns/P208-gc1-overlap-binding-lock-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-QBL-005-review.md`
- `memory/vantasner/decisions/GC1-qualified-review.md`
- `src/substrate_framework/qball_fluctuations.py`
- `tests/test_qball_fluctuations.py`
