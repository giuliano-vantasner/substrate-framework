---
description: Independent duplicate review of NY2's one-unit nuclear-yield and engine claim
author: vantasner-review
created: '2026-08-04T00:55:00Z'
updated: '2026-08-04T00:55:00Z'
tags:
- substrate-framework
- source-review
- duplicate-evidence
- migration-NY2
category: decisions
confidence: working
status: archived
---
# Review of NY2 Duplicate Evidence

## Claims Under Review

The review asks whether NY2 changes C-SK-001, instantiates a dimensionally
fixed nuclear yield, derives a D+D reaction payload, or supplies an engine
replacement. The proposed source disposition is `duplicate_evidence`.

## Sourced Inputs

The review reads v0.74.0, C-SK-001, C-DIM-002, C-DIM-003, their canonical
sources, P084, HE4's terminal adjudication, P085's frozen contract, hash-pinned
NY2 body and reproduction, source and consumer audits, candidate comparison,
literature provenance, and impact map. External masses and reaction papers are
comparator/channel evidence only.

## Independence

The primary route composes the accepted conditional Skyrme helper and audits
the registry and consumers. The independent route imports no Skyrme API or
P085 expression: it derives the energy-coordinate inverse, multi-soliton sign
family, arbitrary exothermic factors, and radiative two-body kinematics from
fresh symbols.

## Existing-Claim Decisions

C-SK-001 is unchanged because NY2 only repeats its conditional scale before
adding an unsupported event label. C-DIM-002 is unchanged because it already
states that dimensions do not select dimensionless coefficients. C-DIM-003 is
unchanged and supplies only the imported-coordinate ceiling.

## Verification Status

Thirty-four primary and eleven independent exact checks support the terminal
classification. They add no verification status to existing claims. NY2's ten
source checks reproduce but test only scale evaluation, rounded comparator
arithmetic, broad bands, residuals, and deterministic recomputation.

## Sensitivity and Counterexamples

Changing coefficient one to 0.9, 1.1, or 0.93 changes the yield while all are
dimensionless and the first two remain inside the declared band. Generic
`2*a_2-a_4` spans positive, zero, and negative binding and every positive
target. The empirical and old-engine values infer distinct nonunit
coefficients. A one-body final state fails positive-release CM conservation,
while a radiative state partitions energy between photon and recoil.

## Framework Compatibility

The duplicate conditional scale is compatible. No multi-Skyrmion functional,
solution, state identity, reaction branch, cross section, deposition map,
common H2/D2 payload, or engine value is promoted. Primary literature is used
to classify the external radiative channel, never to fill those gaps.

## Dependency and Consumer Replay

NY1 is duplicate evidence and HE4 supplies unrelated sine-Gordon action
claims. The C035 engine and passing parity oracle retain 24 MeV, while separate
engineering code embeds 25.686 MeV. Their disagreement proves the replacement
is incomplete; neither consumer is accepted scientific authority.

## Competing Candidate Audit

Candidate B supplies the nonpromoted coefficient ledger; Candidates C--G
supply missing-object, reaction, consumer, arbitrary-target, and oracle audits;
Candidate H finds no distinct claim. Candidate A fails dependency closure.
Comparator proximity and source tally selected no candidate.

## Four-Axis Decision

No new claim receives four-axis promotion. Existing claims remain unchanged,
and NY2 is noncanonical duplicate evidence for C-SK-001 with its physical
interpretations rejected.

## Promotion Transaction

There is no registry, package, external-consumer, or release promotion. The
transaction freezes P085, records NY2's duplicate disposition and evidence,
regenerates the source queue, archives proposal memory, synchronizes the parent
effort, and replays the unchanged v0.74.0 boundary once.

## Continuation if Not Accepted

The positive P085 result is the complete coefficient, multi-soliton, reaction,
consumer, and duplication ledger. The migration continues to the next pending
unit instead of treating absent nuclear dynamics as completion.

## Done Gate

The decision closes after exact primary and independent routes, every source
predicate, coefficient mutations, consumer replay, literature provenance,
focused consumers, generated queue, memory validation, integrated workflow,
and diff check pass with empty campaign debt.

## Cross-References

See P085, NY2, P084, NY1, HE4, C-SK-001, C-DIM-002, and C-DIM-003.
