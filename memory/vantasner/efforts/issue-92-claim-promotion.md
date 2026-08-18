---
description: Corrected review and promotion transaction for the ingested historical Lean corpus under issue #92
author: prime-agent
created: '2026-08-18T21:00:00+02:00'
updated: '2026-08-18T23:40:00+02:00'
tags:
- substrate-framework
- effort
- lean
- claim-promotion
category: efforts
confidence: working
status: active
---

## Goal and Success Contract

Issue #92 requires one reviewed disposition for every theorem in the 60-file
historical Lean ingestion, promotion only for claims whose exact statements and
dependency closure are supported, synchronized registry/release/docs/memory,
and one proportionate final-boundary gate. PR #93 did not meet that contract:
it self-reviewed the transaction, attached several answer-table artifacts as
claim evidence, and promoted two circular syntheses. PR #94 restores the
v0.162.0 tree; this corrected transaction is based on that rollback.

Success remains pending until the corrected evidence scopes and ten fixed
theorems receive independent claim-level review, a distinct actor merges the
result, and issue #92 records the rejected C-GW-013/C-GW-014 routes alongside
the landed work. Merge activity alone is not success.

## Accepted Baseline

Release v0.162.0, commit `970633a`, with 212 accepted claims. The ingested Lean
source is `/home/dan/substrate@6d1f4e0`; the repository copy is checked for
token-preserved statements and proofs after the documented namespace, comment,
and import-path normalizations. Its prior gate recorded 8,089 Lean jobs and no
proof escapes. The corrected boundary replays the Lean gate because
`formal/Audit.lean` now audits the load-bearing positive-basin theorem.

## Constraints and Invariants

The corrected transaction preserves these boundaries.

- Historical ingested source statements and proofs remain unchanged.
- An answer encoded directly in a Lean definition is artifact provenance, not
  independent corroboration or synthesized glue.
- C-GW-011 is physically scoped to D >= 3; its D=2 evaluation is an arithmetic
  out-of-regime guard.
- C-GW-012 declares its same-release dependency on C-GW-011.
- C-EW-001, C-ROT-002, C-SG-020, C-SG-022, and C-VIR-002 state only what their
  formal artifacts and declared hypotheses support.
- Reviews from PR #93 are not independent evidence and are replaced, not
  inherited.

## Decomposition

1. [x] Classify all 60 files and every declared theorem/lemma.
2. [x] Correct P232 to 55 artifact-claim evidence records spanning 176 named
   theorem entrypoints and attached to 39 accepted claims; classify the Phase13,
   Phase14, and Phase16 answer tables as artifact-only.
3. [x] Correct P233 to ten fixed-theorem promotions: C-GW-011, C-GW-012,
   C-EW-001, C-WK-001, C-CF-001, C-ROT-002, C-GSK-003, C-SG-020, C-SG-022,
   and C-VIR-002.
4. [x] Reject C-GW-013 and C-GW-014 in P234/P235 because their missing physical
   maps are definition inputs, not consequences of the accepted dependencies.
5. [x] Pin v0.163.0 to the ten supported additions (222 claims total) and
   regenerate accepted docs/memory.
6. [ ] Obtain fresh individual reviews for the 39 evidence attachments, ten
   promotions, and two rejected syntheses.
7. [ ] Run the selected final-boundary validation once, obtain distinct merge,
   update issue #92, and verify merged-branch cleanup.

## Attempts

The failed merged route and its bounded correction are recorded separately.

| Attempt | Candidate or repair | Artifact | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | PR #93 census and promotions | merged commit `c864f33` | rejected and reverted | self-review, overbroad evidence scopes, circular C-GW-013/C-GW-014 glue | exact theorem/scope audit |
| 0002 | Corrected census and bounded promotion | P232-P235 attempt 0002 records | in progress | ten supported promotions; two synthesis routes rejected | independent claim/evidence review |

## Validation

The evidence gates are staged to avoid duplicating an unchanged full run.

- Targeted census/ingestion tests: 17 passed after the scope correction.
- Required before review: repository validator, generated-state checks, memory
  validation, Lean gate, changed-scope selection, and `git diff --check`.
- Required once at the final unchanged boundary: the validator-selected scoped
  or full workflow. The governance and release changes currently imply full.

## Debt Ledger

Two transaction-level obligations remain open.

| Debt | Introduced by | Discharge artifact | Status |
| --- | --- | --- | --- |
| Fresh individual review is absent | rejection of PR #93 self-review | new campaign review records by an independent agent | open |
| Corrected transaction is not on `main` | rollback/codeowner and merge sequencing | merged rollback plus corrected PR by distinct actors | open |

## Canonicalization

Accepted authority remains v0.162.0 until the corrected v0.163.0 transaction
lands. C-GW-013 and C-GW-014 retain durable identifiers only in rejected
proposal/attempt history and do not enter `governance/claims.yaml`.

## Cross-References

Issue #92; PR #93; rollback PR #94; campaigns P232-P235;
`memory/codex/efforts/issue-92-corrected-lean-promotion.md`;
`memory/vantasner/efforts/historical-lean-corpus-ingestion.md`.
