---
description: Accepted framework claim C-COH-002
author: framework-registry
created: '2026-08-04T12:30:00Z'
updated: '2026-08-04T12:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-COH-002
category: claims
confidence: established
status: active
---
# C-COH-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

For the declared Brownian phase process delta_t=sqrt(2*D)*W_t with D>=0, t>=0, delta_0=0, and a standard real Wiener process, the exact integer-harmonic characteristic is E[exp(i*n*delta_t)]=exp(-n^2*D*t), and Var(delta_t)=2*D*t. Hence the one-ensemble mean phasor is exp(-D*t), while the iid same-time pair coherence is its square exp(-2*D*t); neither is a survival probability. For a positive uniform observation window T, their temporal averages are respectively (1-exp(-D*T))/(D*T) and (1-exp(-2*D*T))/(2*D*T), with continuous value one at D=0, and they are not their endpoint values. Separately, if an independent deterministic coordinate-amplitude envelope exp(-Gamma*t/2) with Gamma>=0 is declared, its product with the Brownian mean phasor is the coherent mean-field factor exp(-(Gamma/2+D)*t), whose quadratic factor is exp(-(Gamma+2*D)*t). These formulas derive no physical diffusion coefficient, fluctuation-dissipation normalization, effective temperature, oscillator or breather phase projection, total energy, lifetime, survival fraction, population, event rate, or material or discharge map.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-COH-001, C-DYN-001. Assumptions: The phase process is declared exactly as delta_t=sqrt(2*D)*W_t with constant exact D>=0, standard real Wiener normalization Var(W_t)=t, delta_0=0, and t>=0., Characteristic harmonics are integers. The pair formula additionally assumes two iid phase samples at the same elapsed time., Uniform-window averages use normalized Lebesgue time averaging over [0,T] with T>0 and the continuous D=0 extension., The damped composition assumes an independent deterministic coordinate-amplitude envelope exp(-Gamma*t/2); its quadratic factor is the square of that coherent mean factor, not pointwise mechanical energy., D and Gamma are supplied nonnegative inverse-time quantities in one convention. No stochastic field equation, bath spectrum, quantum model, temperature, energy, action, physical unit, or phase-coordinate map is imported., Mean phasor, iid pair coherence, endpoint value, temporal average, coordinate amplitude, quadratic factor, energy, survival probability, population, and rate retain distinct meanings.. Comparators: LB4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; main formulas and the 0.125 target were previously exposed, while P094 froze candidates and structural criteria before source execution, remaining-body inspection, output, or additional consumer output.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.80.0` with provenance `campaigns/P094-lb4-thermal-decoherence-window/adjudication.yaml`.

- `campaigns/P094-lb4-thermal-decoherence-window/verify.py`
- `campaigns/P094-lb4-thermal-decoherence-window/reviews/independent_stochastic_review.py`
- `campaigns/P094-lb4-thermal-decoherence-window/evidence/source-reproduction.yaml`
- `campaigns/P094-lb4-thermal-decoherence-window/evidence/source-audit.yaml`
- `campaigns/P094-lb4-thermal-decoherence-window/evidence/check-adjudication.yaml`
- `campaigns/P094-lb4-thermal-decoherence-window/evidence/consumer-audit.yaml`
- `campaigns/P094-lb4-thermal-decoherence-window/evidence/candidate-comparison.yaml`
- `campaigns/P094-lb4-thermal-decoherence-window/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-COH-002-review.md`
- `tests/test_coherence_gates.py`
