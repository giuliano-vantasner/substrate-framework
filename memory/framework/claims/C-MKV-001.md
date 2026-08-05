---
description: Accepted framework claim C-MKV-001
author: framework-registry
created: '2026-08-05T19:00:00Z'
updated: '2026-08-05T19:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-MKV-001
category: claims
confidence: established
status: active
---
# C-MKV-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let N_t be a separately declared continuous-time Markov chain on the nonnegative integers, let S>0 be a dimensionless stationary mean, and let r>0 have inverse-time units. For birth rates lambda_n=r*S and death rates mu_n=r*n, with mu_0=0, the exact generator is Lf(n)=r*S*(f(n+1)-f(n))+r*n*(f(n-1)-f(n)). The normalized factorial-one mass pi_n=exp(-S)*S^n/n! from C-CMB-003 is reversible because pi_n*lambda_n=pi_(n+1)*mu_(n+1). The identity-function local drift is r*(S-n). For a separately declared initial law with finite mean m0, the mean is S+(m0-S)*exp(-r*t). If the initial probability generating function is G0, then G(z,t)=G0(1+(z-1)*exp(-r*t))*exp(S*(z-1)*(1-exp(-r*t))). For deterministic initial state n0, the transition law is the independent sum of Binomial(n0,exp(-r*t)) and Poisson(S*(1-exp(-r*t))). The stationary mass alone does not select this generator: detailed balance fixes only lambda_n/mu_(n+1)=S/(n+1), and the distinct positive rates lambda_n=r*S/(n+1), mu_n=r for n>=1 with mu_0=0 share the same stationary mass while having different holding rates, drift, and transients. A positive local drift does not imply monotone sample paths because death jumps remain possible at every positive state. The state space, generator, initial law, S, and r are independent model declarations. Neither a static factorial-one mass nor a coherent-state number measurement, continuum mode count, vacuum variance, or accepted medium supplies them. No material state preparation, granularity map, participation law, physical growth, open or rescued channel, transition matrix element, branching fraction, isotope effect, reaction, rate, or substrate realization follows.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-CMB-003. Assumptions: The state space is exactly the nonnegative integers and the boundary death rate mu_0 is zero., S is a separately supplied exact positive dimensionless number and r is a separately supplied exact positive inverse-time rate., The initial law is separately declared and normalized. The mean formula requires a finite initial mean and the PGF formula requires a valid initial probability generating function., The immigration-death rates define a continuous-time Markov chain independently of C-CMB-003. Agreement of its stationary mass with C-CMB-003 does not reverse that dependency., Detailed balance determines adjacent rate ratios only. A stationary mass does not determine holding rates rate scale transients generator or sample paths., Local conditional drift and ensemble-mean relaxation do not imply monotone sample paths or a physical material growth process., C-OSC-001 and C-VOP-001 provide mathematical state and one-time measurement context only and are not dependencies of the time-process theorem., No accepted claim maps S or r to MD4's beta beta_a ell over a PN2 band or a material event observable.. Comparators: MD4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its 34-check result was exposed before P199 froze process candidates criteria mutations and ceilings, C-CMB-003 supplies the normalized static factorial-one mass adjacent ratio modes moments and tails but no time process, A pure-birth process from zero has a transient Poisson law with mean r*t but no finite stationary restoring target, The alternative reversible rates r*S/(n+1) and r share the same stationary mass while differing from immigration-death dynamics.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.148.0` with provenance `campaigns/P199-md4-growth-threshold-audit/adjudication.yaml`.

- `campaigns/P199-md4-growth-threshold-audit/verify.py`
- `campaigns/P199-md4-growth-threshold-audit/reviews/independent_birth_death_review.py`
- `campaigns/P199-md4-growth-threshold-audit/reviews/replay_source_graph.py`
- `campaigns/P199-md4-growth-threshold-audit/reviews/C-MKV-001-claim-review.md`
- `campaigns/P199-md4-growth-threshold-audit/reviews/MD4-disposition-review.md`
- `campaigns/P199-md4-growth-threshold-audit/reviews/source_adjudication.md`
- `campaigns/P199-md4-growth-threshold-audit/reviews/impact_analysis.md`
- `campaigns/P199-md4-growth-threshold-audit/attempts/0003/result.yaml`
- `campaigns/P199-md4-growth-threshold-audit/attempts/0004/result.yaml`
- `campaigns/P199-md4-growth-threshold-audit/attempts/0005/result.yaml`
- `campaigns/P199-md4-growth-threshold-audit/attempts/0006/result.yaml`
- `campaigns/P199-md4-growth-threshold-audit/attempts/0007/result.yaml`
- `campaigns/P199-md4-growth-threshold-audit/attempts/0008/result.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/formula-freeze.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/input-provenance.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/dependency-audit.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/consumer-audit.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/candidate-comparison.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/implementation-audit.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/gitnexus-impact.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/primary-provenance.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/independent-provenance.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/source-reproduction.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/consumer-reproduction.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/compatibility-audit.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/source-audit.yaml`
- `campaigns/P199-md4-growth-threshold-audit/evidence/check-adjudication.yaml`
- `memory/vantasner/decisions/C-MKV-001-review.md`
- `memory/vantasner/decisions/MD4-qualified-review.md`
- `src/substrate_framework/birth_death.py`
- `tests/test_birth_death.py`
