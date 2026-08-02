---
description: Accepted framework claim C-PRB-001
author: framework-registry
created: '2026-08-03T17:00:00Z'
updated: '2026-08-03T17:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-PRB-001
category: claims
confidence: established
status: active
---
# C-PRB-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a separately supplied real initial frequency x in [0,1] and real dimensionless selection ratio S, define the continuous exponential fixation family by U(x,0)=x and, for S nonzero, U(x,S)=(1-exp(-S*x))/(1-exp(-S)). The value at zero is the unique continuous extension. For every real S, U(0,S)=0, U(1,S)=1, and U lies in [0,1]; for nonzero S its x derivative is S*exp(-S*x)/(1-exp(-S))>0, and U(x,S)+U(1-x,-S)=1. Conditional on the separately declared backward equation U_xx+S*U_x=0 with absorbing boundary values zero and one, this is its unique solution: for S nonzero the two-constant boundary matrix has determinant exp(-S)-1, while S=0 gives the unique linear solution U=x. For 0<x<1, U is strictly increasing in S because its S derivative is a positive factor times the strict-convexity gap (1-x)+x*exp(S)-exp(S*x)>0; its limits as S tends to negative and positive infinity are zero and one. Thus every supplied target in (0,1) has a unique implicit S preimage, which is inverse inference rather than a prediction. The neutral expansion is U=x+S*x*(1-x)/2+S^2*x*(1-x)*(1-2*x)/12 -S^3*x^2*(1-x)^2/24+O(S^4). Separately, for positive intensities I1,I2, total N=I1+I2 and x=I1/N, the raw contrast is I1-I2=N*(2*x-1). A declared S=kappa*(I1-I2) scales by lambda^2 under a common amplitude rescaling when kappa is held fixed, but kappa->kappa/lambda^2 preserves S, and unit-normalizing the intensities preserves S with kappa_unit=kappa*N. Hence raw-amplitude scale sensitivity requires a separately established physical normalization and coefficient convention. These exact facts establish no Wright-Fisher or Moran microscopic process, quantum state or Born postulate, measurement or actualization rule, empirical deviation, observable amplitude norm, parameter value, medium action quantum, cutoff, dimensional instability, or substrate granularity.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The initial frequency is a real member of the closed unit interval and S is a separately supplied real dimensionless coordinate; the nonzero formula is never evaluated at its removable singularity., The BVP, absorbing boundary data, and coefficient convention inside S are declared premises; the exact solution does not derive a stochastic generator or microscopic process., Strict selection monotonicity and target-preimage uniqueness use the open frequency domain 0<x<1 and strict convexity of the real exponential., The two intensities and common amplitude-rescaling factor are positive; kappa and whether it transforms or remains fixed belong to a separately declared normalization convention., Calling raw intensity, kappa, or S observable requires a physical state and measurement map absent from this claim., No AS8 factor identification, numerical example, quantum label, AS7 granularity, or pending S3 mechanism enters the theorem.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.72.0` with provenance `campaigns/P079-as8-superborn-fixation-audit/adjudication.yaml`.

- `campaigns/P079-as8-superborn-fixation-audit/verify.py`
- `campaigns/P079-as8-superborn-fixation-audit/attempts/0001/result.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/attempts/0002/result.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/attempts/0003/result.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/attempts/0004/result.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/reviews/independent_fixation_review.py`
- `campaigns/P079-as8-superborn-fixation-audit/evidence/source-reproduction.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/evidence/source-audit.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/evidence/candidate-comparison.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/evidence/primary-provenance.yaml`
- `campaigns/P079-as8-superborn-fixation-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-PRB-001-review.md`
- `tests/test_fixation_probability.py`
