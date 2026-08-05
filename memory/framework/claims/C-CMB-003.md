---
description: Accepted framework claim C-CMB-003
author: framework-registry
created: '2026-08-11T19:07:00Z'
updated: '2026-08-11T19:07:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CMB-003
category: claims
confidence: established
status: active
---
# C-CMB-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let S be one exact positive dimensionless real and define the normalized all-nonnegative factorial-one mass p_S(n)=exp(-S)*S^n/n! for every nonnegative integer n. For every n>=1 its interior log-concavity quotient is p_S(n)^2/(p_S(n-1)*p_S(n+1))=(n+1)/n>1. This strict log-concavity retains the exact C-OSC-001 mode set: noninteger S has the unique mode floor(S), while positive integer S has the adjacent tied modes S-1 and S. Its probability-generating function is G_S(t)=exp(S*(t-1)), and every nonnegative integer falling-factorial moment is E[(N)_r]=S^r; in particular its mean and variance are both S. For exact alpha>0 and integer N>=0 satisfying N+1>=S*exp(alpha), one has p_S(N+k)<=p_S(N)*exp(-alpha*k) for every integer k>=0 and sum_{n=N+1}^infinity p_S(n)<=p_S(N)/(exp(alpha)-1). Moreover, for every fixed nonnegative integer r and every exact rational q in (0,1), any integer N>=1 with N+1>=S*2^r/q makes the consecutive ratio of n^r*p_S(n) at most q for all n>=N, hence n^r*p_S(n) tends to zero. These are exact mathematical distribution and tail statements on counting measure. They do not derive a physical Poisson process, occurrence rate, time interval, phase-space law, energy-gap suppression, power-law interpolation, subdivision mechanism, medium mean, material parameter, branching channel, or prediction.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-OSC-001. Assumptions: S is one separately supplied exact positive dimensionless real and the sample space is all nonnegative integers with counting measure; positive-only and positive-odd restrictions are distinct C-OSC-001 families., The log-concavity theorem is interior and does not erase the adjacent positive-integer mode tie. Its exact quotient is (n+1)/n for n>=1., The PGF and falling-factorial moments are mathematical identities of the normalized mass. Interpreting N as occurrences of a physical process requires a process, time or exposure variable, dynamics, and parameter provenance not imported here., The geometric majorant declares alpha, N, and N+1>=S*exp(alpha). Its tail starts at N+1 and is bounded relative to p_S(N); it is not a physical high-energy or phase-space law., The fixed-power certificate declares one fixed nonnegative integer r, one rational contraction q in (0,1), and N>=1 with N+1>=S*2^r/q. The constructive API restricts S and q to exact rationals for decidable thresholds without restricting the symbolic theorem., The exact adjacent step residual is S-(n+1), not S-n. WN4's PN2-band checks do not evaluate the mass and supply no accepted premise., A physical probability, rate, regime crossover, branching channel, medium mean, or material prediction would require accepted interaction, state, spectral, dynamical, unit, and parameter-provenance inputs; none is imported here., WN5 through WN7 and MD1 through MD6 remain separately governed and supply no premise to this claim.. Comparators: WN4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its result was exposed by prior reverse-consumer replay, while P192 froze sample-space, integer-tie, tail-quantifier, physical-typing, mutation, nonduplication, and consumer criteria before renewed execution and implementation, C-OSC-001 supplies the normalized all-nonnegative factorial-one mass, adjacent ratio, and complete mode set but not the distinct log-concavity, generating, moment, or quantified-tail theorem, C-CMB-001 and C-CMB-002 remain distinct inverse-square-factorial and positive-odd Bessel-normalized families.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.143.0` with provenance `campaigns/P192-wn4-derived-weight-crossover-audit/adjudication.yaml`.

- `campaigns/P192-wn4-derived-weight-crossover-audit/verify.py`
- `campaigns/P192-wn4-derived-weight-crossover-audit/reviews/independent_factorial_one_review.py`
- `campaigns/P192-wn4-derived-weight-crossover-audit/reviews/replay_source_graph.py`
- `campaigns/P192-wn4-derived-weight-crossover-audit/reviews/C-CMB-003-claim-review.md`
- `campaigns/P192-wn4-derived-weight-crossover-audit/reviews/source_adjudication.md`
- `campaigns/P192-wn4-derived-weight-crossover-audit/reviews/impact_analysis.md`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0003/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0004/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0005/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0006/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0007/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0008/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0009/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0010/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/attempts/0011/result.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/formula-freeze.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/input-provenance.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/dependency-audit.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/consumer-audit.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/candidate-comparison.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/implementation-audit.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/primary-provenance.yaml`
- `campaigns/P192-wn4-derived-weight-crossover-audit/evidence/independent-provenance.yaml`
- `memory/vantasner/decisions/C-CMB-003-review.md`
- `memory/vantasner/decisions/WN4-qualified-review.md`
- `src/substrate_framework/bosonic_fock.py`
- `tests/test_factorial_one_distribution.py`
