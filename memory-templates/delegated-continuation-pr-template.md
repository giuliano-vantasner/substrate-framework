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
- Distinct intended merger: <identity or handoff pending>
- Source PR lifecycle: <request changes, active refactor, active harvest, merged, or terminal closed>
- Refactor owner/handoff and live PR: <identity and link, or not applicable>
- Terminal-close evidence: <not applicable, or qualifying rationale and landed replacement>
- Final issue handoff: <posted comment link or ready-to-post pending>

| Unit | Local claim | Headline-independent? | Evidence | Merge disposition |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

After the merge boundary is known, update the canonical issue with three unit-level lists: merged and rationale, requires refactor and rationale plus exact required change, owner, live PR, and landing test, and left in PR history and rationale. Link landed paths/commits, the reviewed PR, and the next decisive action. Keep the source PR open while a finite refactor or harvest is live. Close unmerged only after the terminal-close test in `AGENTS.md`, and record the qualifying reason. If GitHub mutation is not authorized, preserve the exact ready-to-post comment and mark the handoff pending.

## Decomposition and Ownership
List dependency-ordered local work and one child contract per authorized worker. Give workers disjoint write surfaces and raw sourced inputs. The agent that opens, commits to, or materially implements the PR may not merge it; reserve merge authority for the named distinct reviewer or repository owner.

## Finding Intake
Every finding becomes a repair, candidate rejection, new candidate, targeted foundation proposal, or promotion action.

| Finding | Source | Meaning | Next materially different action | Owner |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Continuation Cycles
After every result, failed test, review, or apparent success, rerun this cycle.

### Cycle <n>
Record the result, whether it advances the positive success contract, the failed/remaining gate, diagnosed layer, next candidate or repair, changed artifact, retest, sensitivity audit, dependency replay, and canonical-state check. The decision is `continue` until every success gate passes.

## Framework-Fit and Foundation Gate
Record why the selected concept fits naturally. If it does not, determine whether the mismatch is a candidate defect or independent evidence against canon. Reject a defective candidate and try another; route independent canonical inconsistency through a separate `challenges` or foundational-revision proposal with alternate repairs, minimum-change rationale, migration map, and global replay. A conflict blocks promotion, not a correct conditional artifact.

## Validation Ledger
Every failed row creates the next task.

| Gate | Command/evidence | Result | Next task if not passed |
| --- | --- | --- | --- |
| Positive claim |  |  |  |
| Claim-appropriate symbolic/formal/numerical oracle |  |  |  |
| Verifier mutations/counterexamples |  |  |  |
| Solver status, refinement, conservation/stability, and independent route where numerical |  |  |  |
| Global dependency replay |  |  |  |
| Importable API tests |  |  |  |
| Impact analysis and scoped/full validation rationale |  |  |  |
| Registry/release validation |  |  |  |
| Generated docs and memory agree |  |  |  |
| Debt ledger empty |  |  |  |

## Debt Ledger
Track every introduced assumption, import, parameter, residual, convention conflict, broken consumer, and narrative mismatch inside a unit proposed for merge or promotion until discharged. The uncompleted remainder of the parent goal is campaign frontier, not debt.

## Promotion Record
List individually accepted claims, source API/tests, immutable campaign record, release id, generated outputs, memory synchronization, commit, PR, and review evidence.

## Results and Next Action
Record the verified positive result and every harvested unit. If the parent objective is incomplete, use `Advances #N`, preserve the exact next decisive action, and leave the goal active. A clean harvest handoff may end this PR or agent run without pretending the campaign is complete.

## Done Gate
For full campaign completion, check all success conditions from `AGENTS.md`, targeted checks, downstream replay, generated-state consistency, one `scripts/validate.sh --full` run at the unchanged promotion boundary, and empty debt. For a progress merge, require that the canonical issue predates the PR, a distinct merger is identified, and each harvested unit passes its local claim, dependency, convention, consumer, impact, and proportionate scoped/full validation gates; keep the campaign and any live source-refactor PR open and do not promote unsupported headline claims.

## Cross-References
Link parent/child contracts, proposal, claims, campaigns, source, tests, release, generated docs, and PR.
```
