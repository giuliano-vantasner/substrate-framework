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
This effort delivers <exact positive result>. It is complete only when the object exists, accepted dependencies close, framework fit is established, the strongest practical verifier and sensitivity audit pass, downstream consumers replay, implementation is importable, canonical records agree, and the debt ledger is empty. A failed attempt, no-go, residual, bound, or obstruction is not completion. Delivery to the requester happens only after the PRs are reviewed and merged; pre-merge, send status updates only, never a delivery claim.

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
Attempts are append-only and individually reproducible. A failed row must name the diagnosed mechanism and next materially different attempt. A missing legacy library alias is environment compatibility, not a failed scientific candidate: detect direct, imported, and dynamic `np.trapz` access, including eagerly evaluated nested `getattr` defaults; repair mutable code to `np.trapezoid` or a safe two-step fallback, or record an alias-only replay for immutable source, before adjudicating the unchanged route.

When drift or fragmented campaign context may explain the failure, the next
attempt also names the nearest accepted analogue, the source-verified
construction that can transfer, and the mismatch that prevents literal reuse.
Do not use memory prose or a generic external method as substitute authority.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 |  |  |  |  |  |

## Validation
Validation covers the actual objective, verifier sensitivity, limits, conventions, dependencies, consumers, and generated state—not merely an exit code or check count. No freestyle writing: every claim in any produced document is backed by a machine check (SymPy, Lean, SciPy, or numerical) or by an explicit citation, and check/test names map to the document's equation or claim numbers so text-to-proof agreement is auditable.

- Targeted scientific command and claim-appropriate oracle (SymPy, Lean, SciPy, or simulation), with process status zero, terminal tally, lexical check-call sites, runtime check executions, and assertion nodes recorded as distinct inventories rather than forced-equal counts:
- Mutation/counterexample command, including shared-variable elimination for any allegedly independent downstream check and explicit field/measure/coefficient maps for cross-sector matches:
- Numerical solver-status, refinement, conservation/stability, and independent-route command (when applicable):
- Dependency replay, after AST preflight for direct/imported/dynamic legacy trapezoid access and repair of mutable consumers to `np.trapezoid` or a safe two-step fallback, or an alias-only replay for immutable source:
- Targeted tests during implementation:
- `scripts/validate.sh` (includes the full pytest suite; run once at the unchanged promotion boundary):
- `git diff --check` (run separately from commit so a later command cannot mask failure):

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
