---
description: Accepted framework claim C-BPS-001
author: framework-registry
created: '2026-08-07T18:00:00Z'
updated: '2026-08-07T18:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BPS-001
category: claims
confidence: established
status: active
---
# C-BPS-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let X be a closed connected oriented three-manifold with volume form dvol, and let the target be the oriented unit round S^3 with volume form Omega normalized by integral_{S^3} Omega=2*pi^2. For a sufficiently regular map U:X->S^3 of nonzero signed degree B, define the normalized pullback density by U*Omega/(2*pi^2)=B0*dvol. Let lambda and mu be positive, let V:S^3->[0,infinity) have integrable square root, and set W=(1/(2*pi^2))*integral_{S^3} sqrt(V)*Omega. Then the declared energy E[U]=integral_X[(lambda*pi^2*B0)^2+mu^2*V(U)]dvol has the exact decomposition E=integral_X(lambda*pi^2*B0-sign(B)*mu*sqrt(V(U)))^2*dvol +2*lambda*mu*pi^2*abs(B)*W and therefore obeys E>=2*lambda*mu*pi^2*abs(B)*W. Equality holds if and only if the displayed square vanishes almost everywhere. This theorem does not establish that an equality configuration exists in any degree sector, select a potential or coupling, identify degree with a physical baryon or nucleus, or derive a mass, reaction, binding, or yield.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: X and S^3 satisfy the stated compactness orientation and regularity hypotheses, and U is regular enough for the standard degree and pullback integration theorem and for every displayed integral., B0 is the normalized density whose spatial integral is the signed integer degree; using the unnormalized target pullback changes the formula by 2*pi^2., V is nonnegative and dimensionless, sqrt(V) is target-integrable, and the two spatial energy terms are integrable., Lambda and mu are positive and use the convention with sextic density lambda^2*pi^4*B0^2. In the convention lambda_A^2*B0^2, lambda_A=pi^2*lambda and the bound coefficient is 2*lambda_A*mu*W., If physical coordinates have length dimension, B0 has L^-3, lambda has E^(1/2)*L^(3/2), mu has E^(1/2)*L^(-3/2), and lambda*mu has energy dimension., The theorem imports the standard oriented degree identity integral_X B0*f(U)dvol=B*(1/(2*pi^2))*integral_{S^3} f*Omega. It does not prove existence or attainment of the equality equation.. Comparators: E4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its formula was exposed before P107, while both orientations, normalization, independent AM-GM route, counterexamples, and convention mutations were frozen before execution.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.91.0` with provenance `campaigns/P107-e4-bps-zero-binding-audit/adjudication.yaml`.

- `campaigns/P107-e4-bps-zero-binding-audit/verify.py`
- `campaigns/P107-e4-bps-zero-binding-audit/reviews/independent_bps_review.py`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0001/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0002/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0004/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/attempts/0005/result.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/source-reproduction.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/source-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/check-adjudication.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/dependency-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/consumer-audit.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/candidate-comparison.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/evidence/primary-provenance.yaml`
- `campaigns/P107-e4-bps-zero-binding-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-BPS-001-review.md`
- `tests/test_bps_energy.py`
