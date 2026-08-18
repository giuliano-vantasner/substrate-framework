# Physics Research Arc Template

Use with `$physics-erdos-loop`. The contract is the live plan, append-only research history, continuation state, and promotion record for one positive physics objective.

```md
---
description: <exact physics object, mechanism, or derivation sought>
author: <agent-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- research-arc
- <topic>
category: efforts
confidence: exploratory
status: active
---

## Positive Objective and Success
State the requested result precisely. Completion requires the result itself, accepted dependency closure, natural framework fit, a sensitive verifier, candidate comparison, global replay, importable implementation, accepted claim promotion, synchronized generated records, and an empty debt ledger. Honest failure and honest no-go reports are attempt evidence, never the deliverable.

## Authority and Prior Work
Record the accepted release, source commit, claim ids, importable modules, campaigns, memory searches, and graph/source queries actually checked. Distinguish accepted state, proposal state, and attempt state. Accepted canon controls release and promotion; it remains falsifiable, so record credible independent challenges rather than treating conflict as automatic rejection.

- Accepted release:
- Accepted claims reused:
- Source modules read:
- Memory searches:
- Campaign evidence:
- Genuine unresolved objective:

## Definitions and Invariants
Freeze variables, domains, units, normalizations, symmetries, topology, initial/boundary conditions, regularity assumptions, known limits, and cross-sector invariants before candidate selection. For numerical work also freeze the precision, discretization family, domain truncation, stability condition, and error norm before inspecting results.

## Permitted Imports and Assumptions
List every permitted external or framework input with provenance. Any new item enters the debt ledger until independently accepted or eliminated.

## Candidate Set
Register plausible concepts before opening empirical comparators. Include at least two unless uniqueness is proved.

| Candidate | Construction | New objects/parameters | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A |  |  |  |  | untested |
| B |  |  |  |  | untested |

## Selection Criteria and Comparator Gate
Freeze the ordered structural criteria before seeing comparison values: invariant compatibility, explanatory reach, assumption cost, parameter economy, symmetry/topology, dimensions, limits, cross-sector composition, robustness, then empirical prediction. State when comparator values may be opened and any justified exception.

## Claim Delta
List each claim proposed, challenged, qualified, or potentially superseded. A proposal uses `challenges`; only accepted replacements use `supersedes`.

| Claim id | Exact statement | Dependencies | Relationship | Oracle | Consumers |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Claim Ladder
Build the smallest dependency-first ladder. Each row names the strongest practical oracle and sensitivity test. Use SymPy for exact algebraic obligations, Lean for an auditable formal theorem, and SciPy for root/spectrum/integral/optimization/ODE/BVP/PDE evidence when no tractable closed form exists; do not force every obligation into the same tool.

| Step | Claim | Oracle | Sensitivity/counterexample | Prerequisites | Status |
| --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  | pending |

## Importable Implementation
Name canonical package APIs to add or reuse. Campaign scripts must call these APIs and must not duplicate constants, solvers, profiles, convention conversions, or check helpers. For numerical work, state whether `substrate_framework.numerics` applies and identify the claim-owned equation, operator, initial/boundary data, mesh, tolerances, and error metric. Route canonical sampled trapezoidal integration through its compatibility helper; mutable standalone scripts for the current environment use `np.trapezoid`, never removed `np.trapz`, and tractable exact integrals stay symbolic. Preflight direct attributes, imported names, and dynamic `getattr` access; nested fallback defaults are eager, so use a two-step `None` fallback.

## Harvest Checkpoints
Record each locally complete unit as soon as it becomes independently correct and reusable. Use `$research-pr-harvest` to decide whether to merge it unchanged, refactor it into a clean unit, or leave it in PR history. A harvested unit does not complete the parent objective or promote its headline claim. Missing campaign links belong in the active frontier, not the debt ledger.

- Canonical goal issue: <number/link>
- PR issue reference: <`Advances #N` or `Fixes #N`>
- Source PR lifecycle: <request changes, active refactor, active harvest, merged, or terminal closed>
- Refactor owner/handoff, live PR, and landing test: <details or not applicable>
- Terminal-close evidence: <not applicable, or qualifying reason plus landed links>
- Final issue handoff: <posted comment link or ready-to-post pending>

| Unit | Local claim | Independent of headline? | Evidence | Commit/PR | Disposition |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

At the final harvest boundary, update the canonical issue with unit-level lists and rationales for what merged, what requires refactor plus its owner, live PR, exact change, and landing test, and what remains only in PR history. Include landed paths/commits and the next decisive action so a fresh agent can resume from the issue alone. Keep a source PR open while finite refactor or harvest work is active; close only after the terminal-close test in `AGENTS.md`.

## Attempts
Append one row per scientific attempt. Preserve source, stdout/stderr, elapsed time, and exact command. A native immutable-source abort caused only by missing direct, imported, or dynamic `np.trapz`—including an eagerly evaluated nested fallback—is compatibility provenance: run an alias-only compatibility replay and use that replay for scientific adjudication rather than consuming or rejecting a candidate. Failure of the repaired scientific route triggers the next route; it never closes the arc.

| Attempt | Candidate/method | Artifact | Verdict | Diagnosed layer | Next materially different route |
| --- | --- | --- | --- | --- | --- |
| 0001 |  |  |  |  |  |

## Framework-Fit Audit
Assess each candidate before empirical fit: invariant preservation, imports, free parameters, conventions, known limits, cross-sector consumers, and whether it demands unrelated narrative changes. Determine whether a mismatch is a candidate defect or independent evidence against canon. Reject and replace a defective candidate; route a surviving canonical inconsistency through the separate revision gate without blocking correct conditional artifacts.

## Verifier Audit
Record clean exit and tally, derivation-vs-literal inspection, mutations, counterexamples, wrong conventions, refinement, conservation/limit tests, independent rederivation, and exact formal theorem/axioms where applicable. For SciPy ODE/BVP/PDE evidence, record routine/algorithm, precision, solver status, domain, mesh, time policy, tolerances, residual/error norm, convergence order, and a soluble limit or independent method.

## Global Dependency Replay
List direct and indirect consumers and every replay command. Preflight direct/imported/dynamic legacy access and eager fallback defaults. Repair mutable code to `np.trapezoid` or a safe two-step fallback—or use an alias-only replay for immutable evidence—before assigning a scientific verdict. Local pass with a scientifically broken repaired consumer is failure.

| Consumer | Why affected | Command or proof | Result | Repair if needed |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Foundational Revision Gate
Leave empty unless independent evidence shows accepted foundations are inconsistent. If opened, link a separate proposal containing the pre-existing inconsistency, two or more repair candidates, minimum-change decision, migration map, independent review, and full replay. This is an active advancement route when the evidence qualifies; never use it merely to rescue a favored concept.

## Debt Ledger
Track every assumption, import, parameter, residual, unresolved convention, broken consumer, or documentation mismatch inside the scope proposed for promotion. Empty it before completion. Do not list the still-open parent objective or an unselected future route as debt.

| Debt | Source | Effect | Discharge | Status |
| --- | --- | --- | --- | --- |

## Independent Claim Review
Link one `claim-review.md` instance per promoted claim. Record all four status axes and why verifier success establishes the exact headline claim.

## Results and Continuation
Record accepted positive results and reproduction commands. Also record harvested progress and the last strong milestone. For each failed route, record the next active candidate or repair. If an agent run reaches diminishing returns, hand off the exact campaign frontier to a fresh run without changing the objective or marking the arc complete.

## Promotion and Materialization
Record extracted APIs/tests, accepted registry entries, immutable campaign location, release id, generated docs command, accepted-memory synchronization, and proposal/attempt memory separation.

## Done Gate
Check every success condition from `AGENTS.md`, confirm targeted science checks, downstream replay, `scripts/validate.sh --full` once at the unchanged promotion boundary, and an empty debt ledger. A progress harvest uses the impact-justified fixed-only/scoped/full workflow and records the agreeing local `scripts/validate_changed.py` decision instead; it leaves the arc active. Otherwise continue.

## Cross-References
Link the proposal, source artifacts, claims, reviewers, campaign, release, generated outputs, and related memory entries.
```
