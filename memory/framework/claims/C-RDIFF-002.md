---
description: Accepted framework claim C-RDIFF-002
author: framework-registry
created: '2026-08-07T17:00:00Z'
updated: '2026-08-07T17:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RDIFF-002
category: claims
confidence: established
status: active
---
# C-RDIFF-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RDIFF-001, C-RPROF-002's resolution-bounded total stationary-branch energy coefficients b(2)=2.4162704269425106 and b(4)=4.54605799958882, multiplicity n=2, and the separately declared normalization alpha=3*pi^2, the normalized signed difference is 2*b(2)-b(4)=0.2864828542962012 and the coefficient is kappa=8.482417318795285 in IEEE-754 binary64 evaluation. Applying the same transformation to P105's independent collocation values gives 8.482414868843847. Treating the componentwise extrema of those two methods as a rectangular sensitivity input gives [8.482414867768218,8.482417319870914], whose positive lower endpoint preserves the conditional sign. This envelope is method-spread sensitivity evidence, not a confidence interval or rigorous discretization enclosure. The result is a conditional reduced-model coordinate only: it is not a variational bound, physical mass, binding energy, baryon or nucleus map, deuteron or helium state, reaction, empirical comparison, quantum correction, BPS limit, or yield.

## Status Axes
The four governance axes remain independent.

Verification is `numeric_evidence`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `qualified`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RDIFF-001, C-RPROF-002. Assumptions: All C-RDIFF-001 premises and ceilings hold, and C-RPROF-002 supplies only resolution-bounded stationary-branch coefficients rather than physical masses or proven minima., The factor 3*pi^2, multiplicity two, and assignment of the B=2 and B=4 coefficients to the initial and final slots are separately declared inputs., The canonical and independent values retain their P105 solvers, cutoffs, boundary data, tolerances, quadrature, and endpoint-correction provenance; P106 performs no new profile solve., Componentwise extrema across two methods define a transparent rectangular sensitivity envelope but do not prove independent error bounds or account for shared systematic error., The positive conditional difference does not establish exothermic physical binding because no accepted action normalization, state map, correction ledger, or reaction convention is imported., C-SK-001 is compatibility context only and does not extend its declared B=1 premise to a multi-degree physical mass map.. Comparators: E3's biased-input 8.457 value and empirical 23.86 MeV comparison; neither selects the corrected coefficient, normalization, claim, or interpretation.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.90.0` with provenance `campaigns/P106-e3-conditional-energy-difference-audit/adjudication.yaml`.

- `campaigns/P106-e3-conditional-energy-difference-audit/verify.py`
- `campaigns/P106-e3-conditional-energy-difference-audit/reviews/independent_difference_review.py`
- `campaigns/P106-e3-conditional-energy-difference-audit/attempts/0001/result.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/attempts/0003/result.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/attempts/0004/result.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/source-reproduction.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/source-audit.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/check-adjudication.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/dependency-audit.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/consumer-audit.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/candidate-comparison.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/evidence/primary-provenance.yaml`
- `campaigns/P106-e3-conditional-energy-difference-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RDIFF-002-review.md`
- `tests/test_energy_differences.py`
