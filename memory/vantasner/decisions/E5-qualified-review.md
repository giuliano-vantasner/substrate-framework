---
description: Independent review of E5's selected reaction ratios, scale inference, and alpha-state interpretation
author: vantasner-review
created: '2026-08-07T18:40:00Z'
updated: '2026-08-07T18:40:00Z'
tags:
- substrate-framework
- source-review
- qualified
- migration-E5
category: decisions
confidence: working
status: archived
---
# Review of E5 Qualified Fuel-Scale Evidence

## Claim Under Review

The review asks whether E5's four supplied reaction releases independently
select the conditional 25.686 MeV coordinate as a physical per-event scale and
whether alpha products are accepted degree-four rational-map states. The
proposed source disposition is `qualified`; no new claim or release is
proposed.

## Sourced Inputs

The review reads v0.91.0, the complete accepted registry, C-DIM-002/003,
C-SK-001, C-RPROF-001/002, C-RDIFF-001, P084, P085, P105, P108's frozen
contract and attempt history, the hash-pinned E5 and O1 queue records, the
primary AME2020 methodology record, the DOE D-T channel description, and every
P108 source, dependency, consumer, candidate, and provenance artifact. Later
dirty source work and the current-NumPy overlay are not scientific authority.

## Independence

The primary route audits E5's source AST, reconstructs its exact rational data
flow, derives scale transformations, and reads accepted dependency ceilings.
The independent route imports none of the primary ledger's expressions; it
rebuilds the four differences from fresh rational values and separately
derives the ratio, bracket, spread, arbitrary-target, sample, and label
countermodels.

## Verification Status

Thirty-four primary and nineteen independent exact checks pass. The source's
five checks reproduce, but they validate a selected table and its literal
predicates. There is no numerical solver, sampled quadrature, fitted model, or
simulation claim. Exact new work contains no NumPy integration alias, and E5
needs no compatibility replay.

## Sensitivity and Counterexamples

Denominators 10 and 100 MeV defeat the 0.3-to-1 bracket on opposite sides.
Setting the denominator equal to each release makes that reaction exactly one
and closest, so the closest-reaction predicate cannot select its own scale.
Zero, negative, and distant positive sample additions defeat positivity,
bracketing, or factor-three claims. A positive non-alpha entry defeats the
universal product inference. Pairwise Q ratios and the finite multiplicative
spread remain scale free, but neither derives a physical denominator.

## Framework Compatibility

Exact Q arithmetic is compatible as conditional data bookkeeping, and the
ratio algebra is already bounded by accepted dimensional-coordinate claims.
C-SK-001 supplies no numerical physical prediction. C-RPROF-002 explicitly
excludes alpha particles, nuclei, reactions, and yields. O1 remains pending and
unrelated. E5 therefore cannot close either the physical scale or state map.

## Dependency and Consumer Replay

NY1 and NY2 are duplicate evidence for C-SK-001; E2 is qualified through
C-RPROF-001/002; O1 remains pending. No bridge directly imports E5 or its path.
Several units independently reuse an F_pi/e literal, but none receives
authority from E5. The transaction changes the generated queue only and has no
accepted code or release consumer.

## Competing Candidate Audit

Candidate B supplies the conditional reaction ledger, Candidate C the exact
scale orbit, Candidate D the finite-sample ceiling, Candidate E the decisive
denominator and sample countermodels, Candidate F the reaction-channel audit,
Candidate G the state-map rejection, and Candidate H the nonduplication result.
Candidate A fails dependency closure. No numerical closeness selects a
candidate or scale.

## Four-Axis Decision

No new claim receives four-axis promotion. The surviving table arithmetic has
exact verification and audited review, is compatible as conditional external
data bookkeeping, and remains epistemically qualified. Existing accepted
claims remain active and unchanged, with no challenge or supersession
relationship.

## Promotion Transaction

There is no registry, package, test, release, or external-source promotion.
The transaction archives P108, records E5's qualified disposition, regenerates
the queue and documentation, synchronizes durable review and parent-effort
memory, and replays the unchanged v0.91.0 boundary once.

## Continuation if Not Accepted

The positive P108 result is the complete reaction-data, ratio, scale,
finite-sample, sensitivity, channel, state-map, dependency, and consumer
ledger. Rejection of the scale and identity overreach does not end the corpus
migration; it proceeds to the next pending source unit.

## Done Gate

The decision closes only after both exact routes, mutations, all five source
predicates, generated queue, memory validation, integrated workflow, and diff
check pass with empty P108 debt.

## Cross-References

This review cross-references P084, P085, P105, P108, E2, E5, NY1, NY2, O1,
C-DIM-002, C-DIM-003, C-SK-001, C-RDIFF-001, C-RPROF-001, and C-RPROF-002.
