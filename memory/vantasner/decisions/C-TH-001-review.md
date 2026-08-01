---
description: Independent review of C-TH-001
author: vantasner-review
created: '2026-08-01T11:35:04Z'
updated: '2026-08-01T11:35:04Z'
tags:
- substrate-framework
- claim-review
- thermal-gate
- partition-function
category: decisions
confidence: working
status: archived
---
# Review of C-TH-001

## Claim Under Review
For every real dimensionless splitting `x`, the normalized upper-state occupation of `Z=1+exp(-x)` is `P=exp(-x)/Z=1/(1+exp(x))`. Its Bernoulli variance is `P(1-P)=sech^2(x/2)/4`, and the conditional symmetric gate `W=2P(1-P)=sech^2(x/2)/2`. `W` is even, has unique global maximum `1/2` at zero, decreases strictly with absolute splitting, and tends to zero at both infinities. A conditional macroscopic shape `A sech^2(x/2)` equals `2A W` but the identity does not determine `A`.

## Sourced Inputs
The review read release `v0.4.0`, P005's frozen candidates and criteria, both attempt records, canonical thermal APIs/tests, and hash-pinned source unit T1G. The two-level partition function, single-event gate definition, and optional macroscopic shape are explicit conditional inputs; no source program's causal mechanism is inherited.

## Independence
The proposal route rewrites the canonical logistic formulas and audits exact calculus. The review does not import the thermal module: it computes state probabilities, first and second occupation moments, variance, and susceptibility directly from `Z`, then converts the independently obtained variance to the hyperbolic form.

## Verification Status
Exact SymPy algebra proves the occupation, variance, susceptibility, and sech identities. Exact derivative, nonnegative-square, and limit identities establish global behavior rather than a sampled sign. The claim earns `symbolic_verified` under its explicitly named conditional definitions.

## Sensitivity and Counterexamples
The defining predicate rejects an unnormalized raw Boltzmann factor, gate multiplier 1, missing half-angle, and wrong shape factor. The independent route separately rejects the raw factor and half-angle at an exact point. Attempt `0001` preserved a normal-form simplification failure; attempt `0002` rewrote both equivalent sides to exponentials without changing any scientific predicate and passed.

## Framework Compatibility
The claim is a compatible extension providing a reusable exact thermal utility. The domain and dimensionless variable are explicit. It introduces no fitted coefficient, amplitude, device rate, or coupling, and it leaves existing accepted sectors unchanged.

## Dependency and Consumer Replay
Direct consumers are `src/substrate_framework/thermal.py`, package exports, and `tests/test_thermal.py`. Future thermal or ionization campaigns may import the functions but must separately establish their own physical identification and amplitude. Every T1G result and guard is represented by C-TH-001 or its assumptions, so the source unit can be marked migrated.

## Competing Candidate Audit
Candidates A, B, and C were registered before implementation. A was selected for parameter-free exact closure; B independently fixes the variance meaning; C supplies global behavior. There is no empirical comparator.

## Four-Axis Decision
The exact normalized construction supports a conditional compatible extension without importing a device mechanism.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive, with no challenge or supersession

## Promotion Transaction
Promotion freezes P005, adds the thermal APIs/tests and C-TH-001, creates release `v0.5.0`, regenerates docs/memory, marks T1G migrated, regenerates the migration queue, and replays affected consumers.

## Continuation if Not Accepted
Any replay failure withdraws acceptance and activates Candidate B as the primary route. A raw Boltzmann factor or altered half-angle cannot be accepted by weakening the identity.

## Done Gate
The claim gate is satisfied subject to promotion replay: the positive normalized gate exists, global properties and factors are independently established, physical interpretations remain conditional, and no P005 debt remains.

## Cross-References
See `campaigns/P005-two-level-gate`, source unit T1G in `migration/source-claims.yaml`, `governance/claims.yaml`, and the parent migration effort.
