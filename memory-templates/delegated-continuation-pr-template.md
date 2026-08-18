# Delegated Continuation PR Template

This template separates a bounded PR or agent run from the long-lived positive framework objective. Partial progress does not complete the goal, but independently correct, novel, reusable work may be harvested and merged without carrying failed-attempt or debt-ledger bloat into main.

```md
---
description: <positive PR objective>
author: <agent-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- continuation-pr
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
State the user objective and all applicable success gates from `AGENTS.md`. Failure, no-go, residual, split, or partial progress cannot be checked as complete.

## Accepted Frontier
Record the pinned release, accepted claim boundary, live PR lifecycle (`request changes`, `active refactor`, `active harvest`, or ready for review), working-tree provenance, and exact unresolved positive objective. Treat canon as release authority that may be challenged, not as an automatic terminal verdict. Correct stale status before selecting work.

## Proposal and Candidate Set
Link the proposal manifest, invariants, allowed imports, at least two candidates, frozen selection criteria, and comparator-blinding gate.

## Significant Advance
Describe the importable object, claim, or dependency closure this PR must add. Documentation-only reinterpretation and naive bolt-ons are insufficient.

## Harvest Checkpoints
Use `$research-pr-harvest` whenever a local unit becomes complete. Keep utilities, verified local results, and speculative composition in separable commits so later context fade cannot erase earlier value.

- Canonical goal issue: <number/link>
- Issue created before PR: <yes and timestamp/link evidence>
- PR issue reference: <`Advances #N` or `Fixes #N`>
- Authoring or implementing agent: <identity>
- Intended merger: <distinct identity, explicit owner-authorized self-merge, or handoff pending>
- Source PR lifecycle: <request changes, active refactor, active harvest, merged, or terminal closed>
- Refactor owner/handoff and live PR: <identity and link, or not applicable>
- Terminal-close evidence: <not applicable, or qualifying rationale and landed replacement>
- Final issue handoff: <posted comment link or ready-to-post pending>

| Unit | Local claim | Headline-independent? | Evidence | Merge disposition |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

After the merge boundary is known, update the canonical issue compactly: what
landed and its positive local claim, the minimum correction still active, what
is terminally history-only, and one next decisive action. Link the landed
paths/commit and reviewed PR. Add ownership or lifecycle fields only when work
is actually handed off or closure is disputed.

## Decomposition and Ownership
List dependency-ordered local work and one child contract per authorized worker.
Give workers disjoint write surfaces and raw sourced inputs. Use a distinct
merger by default; when the user or repository owner explicitly authorizes
self-merge, record the override without treating it as independent scientific
review.

## Finding Intake
Classify findings against the frozen transaction. Only a direct falsifier,
absent/circular load-bearing step, broken declared dependency, or affected
consumer failure becomes a current repair. Record adjacent observations once as
follow-up; do not assign workers or open a new campaign during this review.

| Finding | Source | Meaning | Next materially different action | Owner |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Continuation Cycles
Open a new cycle only after a materially different scientific attempt or a
correction that changes the claim boundary. Review prose, counts, handoff edits,
and repeated checks do not create cycles.

### Cycle <n>
Record the positive result, one remaining decisive gate, changed artifact, and
the one stale check. The campaign remains active until success, but a bounded
agent run may land a strong milestone and hand off without repeating the cycle.

## Framework-Fit and Foundation Gate
Record why the selected concept fits naturally. If it does not, determine whether the mismatch is a candidate defect or independent evidence against canon. Reject a defective candidate and try another; route independent canonical inconsistency through a separate `challenges` or foundational-revision proposal with alternate repairs, minimum-change rationale, migration map, and global replay. A conflict blocks promotion, not a correct conditional artifact.

## Validation Ledger
Keep one content-addressed receipt for the frozen boundary. Include only
applicable rows; a failed in-boundary row creates one repair, while an unrelated
observation becomes follow-up.

| Gate | Command/evidence | Result | Next task if not passed |
| --- | --- | --- | --- |
| Positive claim |  |  |  |
| Claim-appropriate symbolic/formal/numerical oracle |  |  |  |
| Verifier mutations/counterexamples |  |  |  |
| Solver status, refinement, conservation/stability, and independent route where numerical |  |  |  |
| Impact-bounded dependency replay |  |  |  |
| Importable API tests |  |  |  |
| Impact analysis and scoped/full validation rationale |  |  |  |
| Registry/release validation |  |  |  |
| Generated docs and memory agree |  |  |  |
| Debt ledger empty |  |  |  |

## Debt Ledger
Track hidden premises, unsupported promises, and broken affected consumers
inside a unit proposed for merge or promotion. Declared hypotheses, honest
exclusions, adjacent observations, and the uncompleted parent goal are not debt.

## Promotion Record
List individually accepted claims, source API/tests, immutable campaign record, release id, generated outputs, memory synchronization, commit, PR, and review evidence.

## Results and Next Action
Record the verified positive result and every harvested unit. If the parent objective is incomplete, use `Advances #N`, preserve the exact next decisive action, and leave the goal active. A clean harvest handoff may end this PR or agent run without pretending the campaign is complete.

## Done Gate
For campaign completion, check applicable success conditions from `AGENTS.md`
and run the impact-selected fixed/scoped/full workflow once at the unchanged
promotion boundary. Full validation is not automatic. For a progress merge,
require local correctness, a proportional receipt, and either a distinct merger
or explicit owner self-merge direction; leave unsupported headline claims
unpromoted and the campaign open.

## Cross-References
Link parent/child contracts, proposal, claims, campaigns, source, tests, release, generated docs, and PR.
```
