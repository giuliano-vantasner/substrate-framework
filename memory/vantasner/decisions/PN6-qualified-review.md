---
description: Terminal review of PN6's exact finite symmetric-pair sum and strictness premises
author: vantasner-review
created: '2026-08-08T01:30:00Z'
updated: '2026-08-08T01:30:00Z'
tags:
- substrate-framework
- claim-review
- paired-resolvent
- finite-sum
category: decisions
confidence: established
status: archived
---
# Review of PN6 Terminal Qualification

## Claim Under Review

PN6 claims an exact E=0 sum over arbitrary finite symmetric detuning pairs,
termwise zero-loss cancellation, and strict nonvanishing under positive common
loss. The review asks for the exact coupling-product and shift premises,
countermodels, limits, stationary scope, size conventions, and whether any
surface is distinct from C-RES-001.

## Sourced Inputs

The review reads v0.94.0, the complete accepted registry, C-RES-001,
C-DYN-001, immutable P112 and P113, P114's frozen contract, and PN6 at SHA-256
`50ebbf97568fef13e69fc926db3e57457aba4685f3140ac8786bed525e71289f`.
It audits all thirty predicates, append-only attempts, exact and independent
verifiers, dependency and literature records, and the empty consumer closure.

## Independence

The primary route uses the canonical C-RES-001 API and a separately assembled
finite block. The independent reviewer imports no paired-resolvent
implementation. It constructs a fresh diagonal inverse and rational pair sum,
then derives cancellation, countermodel, limit, derivative, and normalization
results independently.

## Verification Status

The exact finite-sum surface is `symbolic_verified`, but it earns no new claim.
For equal products within each symmetric pair,
`H=-i*Gamma*sum_j(c_j/(Delta_j^2+Gamma^2/4))`. Direct full-block inversion and
pairwise summation agree exactly. The uniform-ladder digamma base and
recurrence are exact specialization; the source's seven floating block sizes
are regression only.

## Sensitivity and Counterexamples

Resolvent sign, half-width, within-pair product equality, and size
normalization are mutation-sensitive. At zero loss one pair cancels iff its
two products match, while two individually nonzero pairs can cancel across the
full sum. All-zero products refute unrestricted positive-loss strictness.
Signed or complex products can cancel; in particular `g^2` for complex g is
not the Hermitian product `conjugate(g)*g`. Unequal shifts inside one pair
produce a real part and break the common-phase formula.

## Exact Regimes and Size Scope

For real nonnegative products with at least one positive product, real nonzero
detunings, and common positive loss, the sum is strictly negative imaginary.
Pair-specific positive losses preserve this sign when each pair shares one
loss. The small-loss coefficient is `-i*sum_j(c_j/Delta_j^2)` and the
large-loss coefficient is `-4i*sum_j(c_j)`. The stationary equation is the sum
of pair derivatives, and unequal detunings do not inherit a one-pair optimum.
Adding pairs enlarges a finite model; fixed-per-pair and fixed-total products
are different conventions, neither numerical refinement.

## Framework Compatibility

C-RES-001 already owns the exact finite block, pair contribution, cancellation
condition, one-pair regimes, size-normalization distinction, and physical
ceiling. PN6 is their direct finite block-diagonal corollary. C-DYN-001 does not
turn an imaginary shift into a derived bath, decoherence, or physical loss.
No accepted source dependency supplies states, a channel, probability, rate,
nuclear or phonon mechanism, material realization, magnitude, or observation.

## Dependency and Consumer Replay

LB2 and S1 through S5 remain pending candidate provenance. PN1 contributes
only C-SG-019's classical coefficient ceiling, PN4 only C-RES-001, and PN5 no
new premise. The generated queue has no direct PN6 consumer, so its transitive
source closure is empty. Canonical paired-resolvent tests and P112 remain
unchanged and the fourteen focused tests pass.

## Competing Candidate Audit

Literal reproduction, exact summation, independent full-block inversion,
general countermodels, asymptotic and size analysis, and governance
nonduplication were frozen before source execution. Structural completeness
selects mapping to C-RES-001; source tally or example agreement does not select
a concept.

## Four-Axis Decision

The review accepts no new claim and terminally qualifies PN6.

- Verification: surviving exact surface is `symbolic_verified`
- Review: PN6 terminal disposition `qualified`
- Compatibility: native corollary of existing governance
- Epistemic: no new claim; source evidence qualified
- Relationship: challenges and supersedes none

## Promotion Transaction

The transaction moves P114 into immutable campaigns, records PN6 as qualified
through C-RES-001, regenerates the source queue, archives proposal memory, and
checkpoints the parent effort. Registry, v0.94.0, accepted documentation, and
generated accepted memory remain unchanged because no claim is promoted.

## Continuation if Not Accepted

If any exact route, countermodel, predicate, dependency, literature,
nonduplication, or consumer check fails, PN6 returns to P114 for append-only
repair and remains pending. Rejecting an overbroad strictness or physical
narrative does not remove the obligation to preserve its exact finite sum.

## Done Gate

Terminal qualification requires both exact routes, all thirty predicate
verdicts, cancellation and strictness premises, countermodels, limits,
stationary and size ledgers, complete governance records, one integrated
workflow pass, and an empty campaign debt ledger.

## Cross-References

See P112, P113, P114, PN4, PN5, PN6, C-RES-001, C-DYN-001, v0.94.0, and the
framework-migration effort.
