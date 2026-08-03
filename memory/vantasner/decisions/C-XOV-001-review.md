---
description: Independent review of C-XOV-001 exact monotone level-crossing theorem
author: vantasner-review
created: '2026-08-08T06:00:00Z'
updated: '2026-08-08T06:00:00Z'
tags:
- substrate-framework
- claim-review
- monotone-crossover
- screened-factor
category: decisions
confidence: established
status: archived
---
# C-XOV-001 Review

## Claim Under Review

C-XOV-001 states the exact level classification for a continuous strictly
increasing response on the nonnegative half-line with an attained lower value
and finite unattained upper limit. It specializes the theorem to the
exponential saturation and C-SCR-001 shifted inverse-square-root factor,
including endpoints, exact inverses, sensitivities, scale covariance,
counterexamples, identifiability, and a physical-semantic ceiling.

## Sourced Inputs

The review reads v0.96.0, C-SCR-001, C-CMP-001, the frozen P117 contract, all
ten attempts, the canonical crossover module and tests, both verifiers, and
every P117 audit. CM3 is pinned at SHA-256
`d62d8deadbba30c4d240ed57c204149ffe0d6b2ec49ed0e200206a4b4a8eccdb`.

Each of CM3's ten predicates is reviewed individually. Its exact structural
and exponential results survive at their mathematical ceiling. Its flat CM2
rate, physical channel ordering, predicted energy, tunnelling sufficiency,
material, rate, yield, heat, and observation readings remain outside the claim
delta.

## Independence

The independent route imports none of `crossovers.py`. It defines the
exponential and shifted factors afresh, derives their inverses by separate
positive-odds and logarithmic-coordinate parameterizations, differentiates
them independently, reconstructs the C-CMP nonflat counterexample, and builds
plateau, discontinuous, nonmonotone, zero-prefactor, and arbitrary-target
countermodels.

Two independent-route defects are preserved before repair: an opaque SymPy
sign inference for `1-exp(-q)` and a parameterization mix-up after separating
the exponential odds variable from the shifted logarithmic coordinate. The
repairs change the oracle representation and bookkeeping, not the theorem.

## Verification Status

The maximum verdict is symbolic verified. Forty-five primary checks and
thirty-five independent checks establish the exact classifications, formulas,
derivatives, limits, scale laws, countermodels, and rejected mutations.
Fifteen focused package tests exercise the reusable exact-domain APIs and
guards. No unevaluated integral, derivative, root object, or numerical
tolerance carries the claim.

CM3 itself passes all ten checks, but its solve equivalence is sampled at four
points, global signs are reduced to one or two points, and its 200-step
bisection and 200001-point sweep repeat an exact result. Those computations are
regression evidence only.

## Sensitivity and Counterexamples

Mutations of the exponential complement, sign, scale, shifted-factor sign, and
logarithmic power all fail the relevant defining equation. A plateau has more
than one crossing at the same level, a discontinuity skips an interior level,
and a nonmonotone square has two exact roots. Out-of-range levels have no finite
crossing.

C-SCR-001's positive shift is load bearing: it changes the zero-input value
from zero to a positive floor and restricts the admissible level interval. A
zero physical normalization gives no channel, while a free positive
normalization or free exponential scale fits any selected target. No sampled
integration occurs and no NumPy compatibility event exists.

## Framework Compatibility

The claim is a compatible extension with dependency C-SCR-001 only. It
preserves the common energy dimension and the distinction between a
dimensionless conditional factor and a physical observable. C-CMP-001 is
reviewed to reject CM3's flat-rate premise but is not imported into the new
mathematical derivation.

For the exponential response, E and E0 share one energy unit while c is
dimensionless. For the shifted factor, E, U, and G share one energy unit.
Common positive rescaling multiplies either inverse energy by the same factor.
No states, interactions, kinetic normalization, common observable, material
map, or uncertainty model is added.

## Dependency and Consumer Replay

CM1 is admitted only through C-SCR-001, and CM2 only through the already
accepted C-CMP-001 ceiling used in source adjudication. Pending CM7 supplies no
premise and the CM1/CM3 and CM3/CM7 source cycles create no authority.

Two direct source consumers replay forty checks and three indirect consumers
replay one hundred eight, for 148 clean checks. CM1 is a cycle return and every
other descendant remains pending. The debt ledger is empty.

## Competing Candidate Audit

Six candidates were frozen before renewed CM3 execution and whole-body review.
Literal reproduction is retained only as source evidence. The general range
theorem, exponential specialization, actual shifted-factor specialization,
countermodels, and independent governance closure are selected by exact
domains, accepted dependency fit, sensitivity, dimensional typing,
identifiability, and semantic honesty. Neither log(2) nor a comparator curve
selected the theorem.

## Four-Axis Decision

The claim receives separate accepted axes after claim-level review.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: no challenge or supersession

## Promotion Transaction

Promotion adds `src/substrate_framework/crossovers.py` and fifteen tests,
archives P117 under campaigns, adds C-XOV-001 to the registry and v0.97.0
manifest, qualifies CM3 in the editable disposition map, regenerates the
source queue, renders canonical docs and memory, and validates the claim,
release closure, proposal lifecycle, hashes, and all affected paths.

One integrated repository gate must pass after assembly. The final attempt is
created in progress before that gate and finalized only after clean exit; only
record-sensitive checks follow.

## Continuation if Not Accepted

If the promotion gate fails, P117 remains active and the failing verifier,
consumer, registry, release, or evidence layer is repaired without weakening
the claim or importing the rejected physical interpretation.

## Done Gate

The claim is accepted only with its importable exact APIs, independent
derivation, mutation sensitivity, complete predicate and consumer audit,
synchronized governance state, and empty debt ledger. P117's scientific ledger
is empty before the integrated promotion gate.

## Cross-References

See P117, CM3, C-SCR-001, C-CMP-001, C-XOV-001, v0.96.0, the P117
audits and verifiers, and the framework-migration effort.
