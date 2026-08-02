---
description: Accepted framework claim C-COH-001
author: framework-registry
created: '2026-08-04T01:55:00Z'
updated: '2026-08-04T01:55:00Z'
tags:
- substrate-framework
- accepted-claim
- C-COH-001
category: claims
confidence: established
status: active
---
# C-COH-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N be a positive integer, I1 a positive exact per-source directional intensity, and z_j independent identically distributed unit complex phasors with common mean mu and pair coherence V=|mu|^2 in [0,1]. Then I1*E[|sum_j z_j|^2]=I1*(N+N*(N-1)*V). The V=0 and V=1 endpoints are N*I1 and N^2*I1, and the expected-to-incoherent ratio is 1+(N-1)*V. For centered iid Gaussian phase noise of variance sigma^2, V=exp(-sigma^2). These are directional ensemble statements at fixed per-source normalization: substituting I1=I_total/N changes the aligned result to N*I_total, and deterministic correlated phases need not obey the iid lower endpoint. Separately, declare the continuous positive-coordinate interpolation Theta(n,V)=theta*n*(1+(n-1)*V) with theta>0, n>0, and V in [0,1]. For a supplied positive barrier E its unique positive continuous crossing is n=E/theta at V=0 and n=(sqrt((1-V)^2+4*V*E/theta)-(1-V))/(2*V) for V>0; the fully aligned endpoint is sqrt(E/theta). Thus alignment lowers the endpoint threshold exactly when E/theta>1, is neutral at one, and reverses below one. Theta is strictly increasing in V for n>1 and independent of V at n=1. The separately conditional activated factor exp(-E/Theta) inherits that monotonicity but is dimensionless and is not a rate without a supplied dimensionful prefactor and kinetic model. These exact results derive no emitter population, phase preparation or dynamics, observable normalization, total or conserved energy, effective temperature, stochastic escape process, material barrier, precursor identity, nuclear interaction, reaction branch, deposition law, event payload, engine replacement, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: N is a positive integer; the phasors are iid, unit magnitude, and share one distribution with V equal to the squared magnitude of its mean phasor., I1 is a fixed positive directional per-source normalization; changing normalization with N changes the scaling, and the theorem is not an integrated-power or energy-conservation statement., The Gaussian specialization assumes centered independent real Gaussian phases with supplied nonnegative variance; it derives no phase-noise dynamics., The continuous population interpolation, positive per-source scale theta, positive barrier E, coherence interval, and threshold convention are separately declared premises; an integer population threshold requires a separately justified ceiling operation., Calling Theta an energy or temperature and calling exp(-E/Theta) an event rate require separate units, state, kinetic, and prefactor premises., No NY3 numerical value, pending BD1/BD3 mechanism, NY1/NY2 payload, spark-discharge channel, or nuclear interpretation enters the theorem.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.75.0` with provenance `campaigns/P086-ny3-coherence-nucleation-audit/adjudication.yaml`.

- `campaigns/P086-ny3-coherence-nucleation-audit/verify.py`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0001/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0002/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0003/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0004/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0005/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0006/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0007/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0008/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0009/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/attempts/0010/result.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/reviews/independent_coherence_review.py`
- `campaigns/P086-ny3-coherence-nucleation-audit/evidence/source-reproduction.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/evidence/source-audit.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/evidence/consumer-audit.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/evidence/candidate-comparison.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/evidence/primary-provenance.yaml`
- `campaigns/P086-ny3-coherence-nucleation-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-COH-001-review.md`
- `tests/test_coherence_gates.py`
