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
Record the accepted release, source commit, claim ids, importable modules, campaigns, memory searches, and graph/source queries actually checked. Distinguish accepted state, proposal state, and attempt state.

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

## Attempts
Append one row per scientific attempt. Preserve source, stdout/stderr, elapsed time, and exact command. A native immutable-source abort caused only by missing direct, imported, or dynamic `np.trapz`—including an eagerly evaluated nested fallback—is compatibility provenance: run an alias-only compatibility replay and use that replay for scientific adjudication rather than consuming or rejecting a candidate. Failure of the repaired scientific route triggers the next route; it never closes the arc.

| Attempt | Candidate/method | Artifact | Verdict | Diagnosed layer | Next materially different route |
| --- | --- | --- | --- | --- | --- |
| 0001 |  |  |  |  |  |

## Framework-Fit Audit
Assess each candidate before empirical fit: invariant preservation, imports, free parameters, conventions, known limits, cross-sector consumers, and whether it demands unrelated narrative changes. Reject and replace an ill-fitting candidate before considering foundational revision.

## Verifier Audit
Record clean exit and tally, derivation-vs-literal inspection, mutations, counterexamples, wrong conventions, refinement, conservation/limit tests, independent rederivation, and exact formal theorem/axioms where applicable. For SciPy ODE/BVP/PDE evidence, record routine/algorithm, precision, solver status, domain, mesh, time policy, tolerances, residual/error norm, convergence order, and a soluble limit or independent method.

## Global Dependency Replay
List direct and indirect consumers and every replay command. Preflight direct/imported/dynamic legacy access and eager fallback defaults. Repair mutable code to `np.trapezoid` or a safe two-step fallback—or use an alias-only replay for immutable evidence—before assigning a scientific verdict. Local pass with a scientifically broken repaired consumer is failure.

| Consumer | Why affected | Command or proof | Result | Repair if needed |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Foundational Revision Gate
Leave empty unless independent evidence shows accepted foundations are inconsistent. If opened, link a separate proposal containing the pre-existing inconsistency, two or more repair candidates, minimum-change decision, migration map, independent review, and full replay. Never use this section to rescue a favored concept.

## Debt Ledger
Track every assumption, import, parameter, residual, unresolved convention, broken consumer, or documentation mismatch. Empty it before completion.

| Debt | Source | Effect | Discharge | Status |
| --- | --- | --- | --- | --- |

## Independent Claim Review
Link one `claim-review.md` instance per promoted claim. Record all four status axes and why verifier success establishes the exact headline claim.

## Results and Continuation
Record accepted positive results and reproduction commands. For each failed route, record the next active candidate or repair. If the environment pauses, preserve the exact next executable action and keep status active.

## Promotion and Materialization
Record extracted APIs/tests, accepted registry entries, immutable campaign location, release id, generated docs command, accepted-memory synchronization, and proposal/attempt memory separation.

## Done Gate
Check every success condition from `AGENTS.md`, confirm targeted science checks, downstream replay, `scripts/validate.sh` (including its full test suite) once at the unchanged promotion boundary, and an empty debt ledger. Otherwise continue.

## Cross-References
Link the proposal, source artifacts, claims, reviewers, campaign, release, generated outputs, and related memory entries.
```
