---
description: Accepted framework claim C-KIN-001
author: framework-registry
created: '2026-08-10T01:55:00Z'
updated: '2026-08-10T01:55:00Z'
tags:
- substrate-framework
- accepted-claim
- C-KIN-001
category: claims
confidence: established
status: active
---
# C-KIN-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let m1 and m2 be exact positive masses and theta an exact real rapidity. In 1+1 signature (+,-), take the center-of-mass threshold four-vector P=(m1+m2,0) and one observed on-shell vector p1=(m1*cosh(theta),m1*sinh(theta)). The residual p2=P-p1 closes total four-momentum exactly and has mass-shell defect p2^2-m2^2=2*m1*(m1+m2)*(1-cosh(theta)), which is nonpositive and vanishes if and only if theta=0. At that equality point p1=(m1,0) and p2=(m2,0), so both particles are at rest. Thus a nonzero two-particle recoil requires total energy above threshold; otherwise the residual cannot be a second free particle of mass m2 and requires a separately modeled channel such as boundary storage, work, or radiation. This exact kinematic theorem derives no scattering outcome, state production, detector response, charge selection, current, neutrino, weak interaction, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Inputs are exact; floating values are outside the exact API., Both masses are explicitly positive and rapidity is explicitly real., Components use ordering energy then momentum and signature (+,-)., The total is separately declared to be the center-of-mass threshold vector (m1+m2,0), and the observed particle is on shell with mass m1., The equality conclusion uses cosh(theta)>=1 for real theta with equality only at theta=0., Above-threshold energy, boundary work or storage, radiation, state identity, detector acceptance, charge, and interaction data are not inferred.. Comparators: W4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all eight predicates without a NumPy compatibility event, while its moving hidden free kink, threshold recoil, neutrino analogy, charge-conditioned invisibility, physical V-A current, weak interaction, detector, and substrate readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.115.0` with provenance `campaigns/P149-w4-missing-energy-audit/adjudication.yaml`.

- `campaigns/P149-w4-missing-energy-audit/verify.py`
- `campaigns/P149-w4-missing-energy-audit/reviews/independent_threshold_review.py`
- `campaigns/P149-w4-missing-energy-audit/reviews/replay_source_graph.py`
- `campaigns/P149-w4-missing-energy-audit/attempts/0008/result.yaml`
- `campaigns/P149-w4-missing-energy-audit/attempts/0009/result.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/source-reproduction.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/source-audit.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/check-adjudication.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/input-provenance.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/dependency-audit.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/consumer-audit.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/candidate-comparison.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/primary-provenance.yaml`
- `campaigns/P149-w4-missing-energy-audit/evidence/literature-audit.yaml`
- `campaigns/P149-w4-missing-energy-audit/reviews/source_adjudication.md`
- `campaigns/P149-w4-missing-energy-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-KIN-001-review.md`
- `memory/vantasner/decisions/W4-qualified-review.md`
- `src/substrate_framework/relativistic_thresholds.py`
- `tests/test_relativistic_thresholds.py`
