# Effort Contract Template

Use for durable multi-step framework work. Instantiate it as a memory entry before substantial execution. Honesty about failure is required, but failure is not an accepted outcome: preserve failed attempts and continue toward the positive objective.

```md
---
description: <positive object or improvement this effort must deliver>
author: <agent-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- effort
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort delivers <exact positive result>. It is complete only when the object exists, accepted dependencies close, framework fit is established, the strongest practical verifier and sensitivity audit pass, downstream consumers replay, implementation is importable, canonical records agree, and the debt ledger is empty. A failed attempt, no-go, residual, bound, or obstruction is not completion.

## Accepted Baseline
The work starts from release <id and commit>. Record accepted claims and source artifacts actually read; chronology and memory prose are not authority.

## Constraints and Invariants
State the user constraints, accepted invariants, conventions, units, permitted imports, and write boundaries. A new concept may not silently redefine them.

## Decomposition
Work proceeds through these dependency-ordered steps and continues after failed attempts.

1. [ ] Recall and source verification.
2. [ ] Candidate and selection-criteria preregistration.
3. [ ] Importable implementation.
4. [ ] Verifier and sensitivity audit.
5. [ ] Framework-fit and downstream replay.
6. [ ] Claim review, promotion, generation, and memory synchronization.

## Attempts
Attempts are append-only and individually reproducible. A failed row must name the diagnosed mechanism and next materially different attempt.

When drift or fragmented campaign context may explain the failure, the next
attempt also names the nearest accepted analogue, the source-verified
construction that can transfer, and the mismatch that prevents literal reuse.
Do not use memory prose or a generic external method as substitute authority.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 |  |  |  |  |  |

## Validation
Validation covers the actual objective, verifier sensitivity, limits, conventions, dependencies, consumers, and generated state—not merely an exit code or check count.

- Targeted scientific command and claim-appropriate oracle (SymPy, Lean, SciPy, or simulation), with both terminal tally and process status zero recorded:
- Mutation/counterexample command:
- Numerical solver-status, refinement, conservation/stability, and independent-route command (when applicable):
- Dependency replay:
- Targeted tests during implementation:
- `scripts/validate.sh` (includes the full pytest suite; run once at the unchanged promotion boundary):
- `git diff --check`:

## Debt Ledger
Every new assumption, import, parameter, residual, broken consumer, or narrative inconsistency is recorded and discharged. This table must be empty at close.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
Record positive verified outcomes and exact reproduction commands. Failures belong in Attempts and keep this contract active.

## Canonicalization
List claim-registry changes, release manifest, extracted APIs, immutable campaign record, generated docs, and accepted-memory synchronization. Confirm no proposal prose was merged into canonical memory.

## Done Gate
All ten success conditions in `AGENTS.md` are checked individually. If any is false, record the next action and leave status active.

## Cross-References
Link the proposal, claims, source modules, tests, campaign record, release, generated docs, and related memory entries.
```
