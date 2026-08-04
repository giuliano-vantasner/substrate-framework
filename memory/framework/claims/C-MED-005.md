---
description: Accepted framework claim C-MED-005
author: framework-registry
created: '2026-08-09T19:15:00Z'
updated: '2026-08-09T19:15:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MED-005
category: claims
confidence: established
status: active
---
# C-MED-005

## Statement
The accepted statement is reproduced exactly from the claim registry.

In SI base-dimension order (M,L,T,I), permittivity epsilon has (-1,-3,4,2), inverse permeability mu_inverse has (-1,-1,2,2), mechanical mass density rho has (1,-3,0,0), and stiffness or energy density K has (1,-1,-2,0). Conditional on exact positive quantities and separately declared multiplicative conversions rho=a*epsilon and K=b*mu_inverse, both a and b require dimension (2,0,-4,-2), and c_m^2=K/rho=(b/a)*mu_inverse/epsilon. Hence c_m^2 equals the electromagnetic wave-speed square mu_inverse/epsilon exactly iff a=b. Their common value remains a free calibration: common rescaling changes rho, K, and energy while leaving speed fixed. For separately declared exact dimensionless real strain xi, u=K*xi^2/2 and u/c_m^2=a*epsilon*xi^2/2. Thus bare SI epsilon/2 is not a mass density and bare mu_inverse/2 is not an energy density. This exact conditional constitutive theorem derives no material, calibration, field or strain state, gravity coupling, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-MED-001. Assumptions: Inputs are exact; floating values are outside the exact API., SI base-dimension rows use the declared M L T I order and SI unit definitions., Epsilon, mu_inverse, a, and b are positive; a and b are supplied conversion factors rather than inferred values., Xi is exact, real, and dimensionless, and the quadratic strain energy is a separately declared mechanical model., Electromagnetic and mechanical speeds agree exactly only iff a=b; their common positive scale remains free., No physical material, field state, gravitational coupling, observation, or substrate realization is supplied.. Comparators: G5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all fifteen predicates without a NumPy compatibility event, while its bare density and energy relabeling, three-prediction count, symbolic-membership linkage, free-kappa gravity, material, observation, and substrate readings are corrected qualified or rejected, The 2026 BIPM SI Brochure and 2022 CODATA values delimit current SI definitions and source rounding only; no measured value enters the exact theorem or selects it.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.112.0` with provenance `campaigns/P145-g5-medium-density-audit/adjudication.yaml`.

- `campaigns/P145-g5-medium-density-audit/verify.py`
- `campaigns/P145-g5-medium-density-audit/reviews/independent_medium_conversion_review.py`
- `campaigns/P145-g5-medium-density-audit/reviews/replay_source_graph.py`
- `campaigns/P145-g5-medium-density-audit/attempts/0003/result.yaml`
- `campaigns/P145-g5-medium-density-audit/attempts/0004/result.yaml`
- `campaigns/P145-g5-medium-density-audit/attempts/0005/result.yaml`
- `campaigns/P145-g5-medium-density-audit/attempts/0006/result.yaml`
- `campaigns/P145-g5-medium-density-audit/attempts/0007/result.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/source-reproduction.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/source-audit.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/check-adjudication.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/input-provenance.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/dependency-audit.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/consumer-audit.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/candidate-comparison.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/primary-provenance.yaml`
- `campaigns/P145-g5-medium-density-audit/evidence/literature-audit.yaml`
- `campaigns/P145-g5-medium-density-audit/reviews/source_adjudication.md`
- `campaigns/P145-g5-medium-density-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-MED-005-review.md`
- `memory/vantasner/decisions/G5-qualified-review.md`
- `src/substrate_framework/constitutive.py`
- `tests/test_constitutive.py`
