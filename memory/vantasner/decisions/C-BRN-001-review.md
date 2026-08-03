---
description: Independent review of C-BRN-001 exact two-channel allocation theorem
author: vantasner-review
created: '2026-08-08T11:30:00Z'
updated: '2026-08-08T11:30:00Z'
tags:
- substrate-framework
- claim-review
- branching-fraction
- rate-ceiling
category: decisions
confidence: established
status: archived
---
# C-BRN-001 Review

## Claim Under Review

C-BRN-001 states the exact normalized allocation of two nonnegative
common-dimension inputs with positive total, including endpoints, odds,
derivatives, limits, common-scale invariance, a weighted positive-integer
specialization, a relative-odds corollary, unequal-gate sensitivity,
identifiability, and the ceiling between declared rate dimensions and physical
channels.

## Sourced Inputs

The review reads v0.97.0, C-CMP-001, C-SPN-002, P110's qualified PN2 result,
the frozen P122 contract, all attempts, the canonical branching module and
tests, both verifiers, and every P122 audit. GB1 is pinned at SHA-256
`ace0515d7ea362ef45a55db22308aecffdad9a003d03f2b1209c0a11874b489b`.

Every one of GB1's eighteen runtime predicates is reviewed individually. The
exact fraction algebra survives with stronger domains. The physical channel,
weight, dependency, common-factor, and barrier-free readings do not.

## Independence

The independent route imports none of `branching.py`. It parameterizes two
shares by a positive total and a simplex coordinate, reconstructs the
rate-ratio form, differentiates and takes limits afresh, derives the weighted
specialization and odds ratio, and builds unequal-gate, dimension, zero-
interaction, arbitrary-target, unused-symbol, and missing-physical-input
countermodels.

The primary implementation history preserves a rejected patch anchor, two
focused-test representation errors, and an initially ineffective dimension
mutation. Two prefreeze workflow mistakes and one graph-lock overlap are also
recorded. None changes the theorem, domains, or physical ceiling.

## Verification Status

The verdict is symbolic verified. Forty-two primary and twenty-six independent
checks establish the exact normalization, endpoints, excluded double zero,
odds, derivatives, limits, scale laws, specialization, enhancement,
dimensions, source predicate limitations, and mutations. Fifteen focused tests
exercise the exact public API and guards.

GB1 itself passes eighteen checks. Its rho check substitutes the desired ratio
into itself, its dimension checks encode declared premises, and its symbol and
square-root checks are finite syntax. No numeric tolerance, sampled integral,
or compatibility alias carries the accepted claim.

## Sensitivity and Counterexamples

The API accepts either zero endpoint and rejects both zero, negative inputs,
floating inputs, zero weights, noninteger populations, zero odds denominators,
and zero baseline weights. Common scaling cancels while relative scaling does
not. A dimensionful weight breaks the common-rate typing.

Unequal channel gates leave an exact residual proportional to their
difference. A zero interaction removes both physical rates, and every interior
fraction is fitted by a free positive baseline ratio. Benign square roots cause
scanner collisions; non-square-root barriers, opaque imports, aliases,
constants, and weight semantics evade it.

## Framework Compatibility

The claim is a compatible extension with no accepted dependencies. It begins
from two declared common-dimension inputs and normalizes them exactly. It does
not import C-CMP-001's loss composition, C-SPN-002's ladder, or PN2's
arithmetic. Those sources are reviewed only to block GB1's unsupported rate
premises.

The weighted specialization requires positive rate baselines, a positive
dimensionless weight, and a positive integer population. A physical branching
fraction additionally requires accepted states, exhaustive channels,
interactions, final-state measures, kinetics, normalizations, and parameter
provenance.

## Dependency and Consumer Replay

GB4, GB6, WN2, and WN5 are direct candidate consumers; ten WN and MD scripts
are transitive descendants. They replay 576 checks from pinned hashes. WN2,
WN3, and WN4 participate in a pending cycle, and all descendants remain
noncanonical. The campaign debt ledger is empty.

## Competing Candidate Audit

Literal reproduction, the general allocation, weighted specialization,
relative odds, countermodels, accepted-dependency audit, finite syntax audit,
and no-new-claim alternative were frozen before source execution. The general
theorem wins on exact domain closure, parameter economy, direct GB4 reuse, and
clear physical boundaries. Source wording and green output select nothing.

## Four-Axis Decision

The claim receives separate accepted axes after claim-level review.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: no challenge or supersession

## Promotion Transaction

Promotion adds `src/substrate_framework/branching.py` and fifteen tests,
exports its four public APIs, archives P122, adds C-BRN-001 to the registry and
v0.98.0 manifest, qualifies GB1, regenerates the source queue, renders
canonical docs and memory, and validates every affected path.

One integrated repository gate must pass after assembly. The final attempt is
created in progress before that gate and finalized only after clean exit; only
record-sensitive checks follow.

## Continuation if Not Accepted

If the promotion gate fails, P122 remains active and the affected verifier,
consumer, API, registry, release, generated artifact, or evidence layer is
repaired without weakening the denominator domain or importing the rejected
physical interpretation.

## Done Gate

C-BRN-001 is accepted only with its importable exact APIs, independent
derivation, sensitive domains and mutations, complete predicate and consumer
audit, synchronized governance state, and empty debt ledger.

## Cross-References

See P110, P111, P116, P122, PN2, PN3, CM2, GB1, GB4, C-CMP-001, C-SPN-002,
C-BRN-001, v0.97.0, and the framework-migration effort.
