---
name: research-pr-harvest
description: Autonomously process goal-directed research or campaign pull requests, harvest correct, novel, reusable progress even when the headline objective is incomplete, and leave a structured handoff on the linked goal issue. Use whenever the user supplies a PR URL or number, asks what to merge from a scientific PR, needs merge eligibility separated from claim promotion and goal completion, wants strong milestone code or proofs salvaged, needs merged/refactor/history dispositions recorded with rationale, or is handing off a long campaign whose later work is diminishing.
---

# Research PR Harvest

Review for durable value, not only for headline victory. Keep three decisions independent:

1. **Artifact merge:** is a locally complete unit worth owning?
2. **Claim promotion:** has a scientific statement earned accepted authority?
3. **Goal completion:** has the whole campaign objective been achieved?

A PR may merge useful progress while its claims remain proposed and its goal issue remains open. A merge establishes provenance and availability, not scientific truth.

## Establish the boundary

Read the PR, linked goal, base release, accepted claim boundary, diff, tests, and review discussion. For physics work, also load `physics-erdos-loop`; for code impact, use the available PR-review or dependency-graph workflow.

Identify one canonical goal issue and confirm that it existed before the PR was submitted, including before a draft PR. The PR must mention that issue explicitly: use `Advances #N` while the goal remains incomplete and reserve `Fixes #N` for full completion. If the source PR has no pre-existing issue, do not merge it. Create the canonical issue, preserve the source PR as provenance, and place any selected units in a new compliant harvest PR opened after the issue.

In this repository, treat the user's act of supplying a PR URL or number to an agent that did not open, commit to, or materially implement that PR as standing authorization to complete the normal PR lifecycle without further operator prompts: review and comment, edit PR metadata, request changes, create a focused harvest branch or follow-up PR, merge when eligible, close only after the terminal-close test below, and update the linked issue. An agent must not merge any PR it opened, committed to, or materially implemented. If the reviewing agent performs substantive repairs or creates a follow-up harvest PR, a distinct agent or repository owner must execute that merge. Leave a validated handoff when no distinct merger is available. Do not force-push a contributor's branch, delete unrelated branches, broaden the issue objective, or promote unsupported claims. If an external permission or branch rule blocks an action, preserve the exact next action and report the actual blocker.

## Slice the PR into harvest atoms

Do not adjudicate a large PR as one indivisible story. Partition it by dependency into the smallest coherent units, such as:

- a pure utility or compatibility repair;
- an exact identity or narrowly scoped theorem;
- a reusable solver, transformation, source construction, or verifier;
- a conditional model component with explicit inputs;
- a speculative composition that depends on the headline hypothesis;
- campaign narration, memory, attempts, and generated output.

For each unit, state its local claim, inputs, outputs, dependencies, tests, consumers, and whether it still works if the PR's favored headline mechanism is removed.

## Apply the three-question merge gate

Merge a unit only when all three answers are yes:

1. Is it correct under its stated inputs and conventions?
2. Is it materially novel or reusable enough to avoid future reinvention?
3. Is it locally complete, proportionately validated, compatible with the repository, and free of unresolved defects inside its own scope?

Do not require the unit to complete the parent campaign. Do require it to stand without borrowed conclusions, hidden parameters, convention conflicts, or tests that merely repeat copied formulas.

Classify every unit as one of:

- **merge unchanged** — independent, clean, and already well scoped;
- **refactor then merge** — valuable core exists but must be decoupled, renamed, narrowed, or convention-corrected;
- **leave in PR history** — speculative capstone, duplicated machinery, unsupported interpretation, failed route, or maintenance cost with no durable reusable unit.

`Refactor then merge` is an active lifecycle state, not a polite rejection. Name
the repair owner or handoff, live source or harvest PR, exact change, and landing
test. Keep the source PR open in `request changes`, `active refactor`, or
`active harvest` state until that unit lands or becomes terminal.

Close an unmerged PR only when every reusable atom has landed elsewhere, every
remaining atom has unit-level evidence that it is incorrect, non-novel, or
unmaintainable, the author or owner explicitly withdraws it, or a superseding
landed implementation makes it redundant. Missing accepted dependency closure,
a conflict with current canon, lack of a distinct merger, or a pending finite
repair does not pass this terminal-close test.

## Build a harvest merge

Prefer a focused harvest commit or follow-up PR over merging an inseparable campaign dump. Include only the selected implementation, tests, and minimal API documentation.

- Keep accepted-claim authority in the registry; do not promote a headline because related code merges. Treat accepted canon as release authority, not an irrevisable premise: a correct conditional API may merge with explicit assumptions while contrary evidence proceeds through `challenges` or a separately governed foundational revision.
- Create or confirm the canonical goal issue before opening the focused PR. Name it using `Advances #N` for partial progress and use `Fixes #N` only after the full goal passes its completion gate.
- Record the authoring or implementing agent and a distinct intended merger. The authoring agent may prepare, validate, and hand off the PR but may not merge it.
- Keep the goal issue open when the campaign remains incomplete.
- Remove campaign memory, attempt directories, debt ledgers, stale generated output, and proof-shaped narrative unless one is itself the reviewed durable artifact.
- Preserve a failed route in main only when it yields a reusable theorem, counterexample, oracle, fixture, or compatibility repair. Merge that object, not its diary.
- Do not make generated or canonical records claim more than the harvested unit establishes.

## Update the goal issue

After the final merge boundary is known, update the goal issue—not only the PR—with a jump-start record for the next agent. Link the reviewed PR and landed commit or follow-up PR. List every disposition, using `None` when a category is empty:

```md
## Harvest handoff from PR #<number>

### Merged
- <unit and landed location> — Rationale: <why it is correct, reusable, and independent enough to own>. Evidence: <tests/oracle>.

### Requires refactor
- <unit> — Rationale: <valuable core>. Required change: <specific decoupling, correction, or narrowing>. Owner/handoff: <identity>. Live PR: <source or harvest PR>. Landing test: <exact evidence>. Source: <PR path/commit>.

### Left in PR history
- <unit> — Rationale: <why it should not enter main>. Source: <PR path/commit>.

### Continuation
- Claims promoted: <none or ids>
- Goal state: <open or complete>
- PR lifecycle: <request changes, active refactor, active harvest, merged, or terminal closed>
- Landed interfaces: <paths/symbols>
- Next decisive action: <one executable step or test>
- Terminal-close evidence: <not applicable, or qualifying reason plus landed replacement links>

### What closes the goal
- Objective-level closure: <the positive scientific result and governance gates, independent of the reviewed route>
- Current-route gap: <verification-only, implementation/representation, or scientific construction; explain why>
- Necessary obligations: <route-neutral mathematical and physical conditions that remain unsatisfied>
- One sufficient next move, not an exclusive prescription: <an experiment, derivation, or implementation that would decisively advance one obligation>
- Grounds for reconsideration: <evidence or argument that would overturn the blocking review conclusion>
- Reviewer-role boundary: <what was harvested or repaired, and what requires a distinct submitter effort>
```

Write rationales at unit level; do not use one blanket explanation for a category. Point to exact files, symbols, evidence, and commits so the next agent can resume without reconstructing the PR. When authorized to mutate GitHub, post this record after the merge or harvest split. Otherwise, return the exact ready-to-post issue comment and state clearly that the issue update remains pending; never imply it was posted.

## State the closure contract without prescribing the solution

The issue handoff must say exactly what remains before the goal may close while preserving legitimate exploration space. State the objective-level obligations independently of the reviewed proposal. A favored lattice, continuum, formal, analytic, or numerical realization is not an issue requirement unless the issue or accepted framework makes it invariant.

Classify each blocking gap explicitly:

- **verification-only** — the claimed object and derivation exist, but a named transformation, limiting case, sensitivity test, error bound, or consumer replay is missing. Identify the exact relation and explain why that finite addition would suffice;
- **implementation/representation** — the mathematics exists, but the canonical API, convention conversion, integration, or reusable implementation is incomplete;
- **scientific construction** — a load-bearing map, action, dynamics, mechanism, theorem, approximation regime, or degree-of-freedom argument does not yet exist. Say plainly that adding assertions around declared values cannot supply the missing object.

Do not summarize every scientific shortcoming as “more tests needed.” Explain what each script actually establishes as a mathematical proposition and what physical interpretation it does not establish. In particular, distinguish identities from derivations, kinematics from dynamics, a declared parameter count from a constraint analysis, and a closed-form point-source expression from a controlled approximation. Name the falsifier, independent derivation, convergence study, or error estimate that would make the stronger interpretation reviewable.

For the current route, list necessary proof obligations and the evidence that would discharge them, but present any concrete architecture as one sufficient route rather than the unique repair. If the gap plausibly can be finished, say so. During the same adjudication, however, do not rescue a headline claim by choosing its missing mechanism or new assumptions and then acting as its submitter. Narrow correctness repairs and independently complete harvest units remain appropriate; continuing the rejected or incomplete mechanism belongs in a separately identified submitter effort or proposal.

Treat review conclusions as reasoned and rebuttable, not as accepted scientific authority. For every blocking conclusion, state what counterexample, derivation, constraint count, controlled limit, or other evidence would change the assessment. Invite focused disagreement without weakening the completion gate.

When a route conflicts with accepted canon, separate its artifact claim from its
authority claim. A canon conflict blocks promotion and accepted downstream use;
it does not by itself block a correct conditional artifact, erase contrary
evidence, or close the PR. Test whether the mismatch is a candidate defect or a
pre-existing canonical inconsistency. If it survives independently of the
favored route, open a `challenges` or foundational-revision proposal with
competing repairs and keep the scientific frontier active.

## Preserve novelty without creating debt

Missing pieces of the parent goal are the **campaign frontier**, not debt. Debt means an unresolved defect, unsupported promise, broken consumer, or hidden assumption inside the scope being merged or promoted.

When an unmerged speculative mechanism is genuinely worth remembering, preserve one compact frontier summary in the PR or linked issue when authorized:

- the proposed mechanism;
- its explicit hypotheses;
- the strongest verified consequence;
- the decisive unresolved question;
- links to the PR commit and harvested APIs.

Do not generate parallel memory files, multi-attempt archives, or an active debt ledger merely to remember an idea. Git and the PR retain provenance; the compact frontier summary makes it discoverable.

## Protect long campaigns from context fade

Treat the goal as long-lived and each agent run or PR as bounded.

- After the canonical issue exists, open a draft PR early enough to preserve reviewable milestones.
- Keep foundation utilities, verified local results, and speculative composition in separate commits.
- Harvest a unit as soon as it becomes locally complete; do not hold all value hostage to the capstone.
- Maintain a short PR frontier with `landed`, `current hypothesis`, and `next decisive test` rather than expanding narrative state.
- If later work becomes repetitive, weakens claims, substitutes ceremony for new evidence, or only restates earlier results, stop that run at the last strong milestone. Merge the harvest, leave the goal open, and hand the frontier to a fresh agent.
- Keep the source PR open while a declared refactor or harvest remains live; reassess closure only after the unit lands or the terminal-close test passes.

An individual run may end at a clean handoff without lowering or closing the campaign objective.

## Validate proportionately

Run targeted tests and claim-appropriate oracles for each harvested unit, impact analysis for changed public symbols, affected consumers, and one repository validation at the final unchanged merge boundary. An additive public export may use scoped validation when impact is bounded, no existing contract changes, consumers are known, and targeted API coverage passes. Reserve full validation for promotion or release, shared numerics or verification machinery, claim/release governance semantics, changed existing public contracts with consumers, dependency or cross-cutting convention changes, multi-sector changes, or uncertain impact. Pull-request CI uses `scripts/validate_changed.py` for this conservative decision and uses fixed checks only when no pytest scope is affected; scheduled/manual CI supplies the periodic full backstop. Do not rerun unrelated full validation for each discarded campaign artifact or again after merge.

## Report the disposition

Use this compact structure:

```md
## Harvest review

### Merge unchanged
- <unit>: <local claim and evidence>

### Refactor then merge
- <unit>: <valuable core and required decoupling>

### Leave in PR history
- <unit>: <why it should not enter main>

### Authority and goal state
- Claims promoted: <none or ids>
- Goal issue: <number/link and open or complete>
- Issue predates PR: <yes/no and timestamp evidence>
- Authoring or implementing agent: <identity>
- Distinct merger: <identity or handoff pending>
- Issue handoff: <posted link or ready-to-post pending>
- PR lifecycle: <request changes, active refactor, active harvest, merged, or terminal closed>
- Terminal-close evidence: <not applicable, or qualifying reason plus landed replacement links>
- Campaign frontier: <next decisive question>
```

Lead with the concrete files or symbols to keep. Avoid a large scorecard: the dependency slice and three-question gate are the policy.
