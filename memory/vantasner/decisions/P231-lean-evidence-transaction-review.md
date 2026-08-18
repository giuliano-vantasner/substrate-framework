---
description: Independent review of the P231 Lean corroboration evidence transaction
author: vantasner-review
created: '2026-08-18T21:50:00+02:00'
updated: '2026-08-18T21:50:00+02:00'
tags:
- substrate-framework
- claim-review
- lean-evidence
category: decisions
confidence: working
status: archived
---
# Review of the P231 lean verification-evidence transaction

## Claim Under Review
Not a new claim: 43 accepted claims receive Lean `verification_evidence` records
(46 attachments across 41 ingested files) from the historical corpus census. Each
attachment was reviewed individually at `campaigns/P231-lean-corpus-census/reviews/`.

## Sourced Inputs
Every registry statement with its assumptions and exclusions, the ingested Lean sources,
the census, and the original campaign adjudications for scope comparison.

## Independence
Each attachment's scope was audited clause-by-clause against the accepted statement: the
Lean theorem must machine-check content inside the accepted claim (its algebraic core in
the file's declared encoding), every physics premise the file asserts as input must be
recorded in the scope, and content the claim explicitly excludes must not be imported.

## Verification Status
formal corroboration evidence: kernel-checked at the pinned toolchain inside the gate that
passed at the ingestion commit; the formal surface is unchanged by the transaction.

## Sensitivity and Counterexamples
Attachments whose Lean content fell outside the accepted scope were withheld or reclassified
(notably the WZW level-winding identification beyond C-WZW-002's stated scope, kept out; the
hardcoded S-matrix time-delay snapshots, class 4). The preliminary-scan corrections are
recorded in the adjudication.

## Framework Compatibility
Append-only on accepted claims: no statement, dependency, or status axis changes; the
evidence lists gain the ingested artifacts.

## Dependency and Consumer Replay
No consumer changes; generated docs and accepted memory regenerated from registry state.

## Four-Axis Decision
- Verification: unchanged per claim (evidence attachment only)
- Review: accepted (each attachment individually)
- Compatibility: unchanged per claim
- Epistemic: unchanged per claim

The 46 attachments are recorded in `campaigns/P231-lean-corpus-census/adjudication.yaml`.
