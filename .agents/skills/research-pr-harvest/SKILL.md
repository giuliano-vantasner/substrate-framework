---
name: research-pr-harvest
description: Autonomously process goal-directed research or campaign pull requests, preserve the strongest correct reusable progress even when the headline objective is incomplete, and leave a compact handoff on the linked goal issue. Use whenever the user supplies a PR URL or number, asks what to merge from a scientific PR, needs merge eligibility separated from claim promotion and goal completion, wants useful code or proofs salvaged without recursive re-review, or is handing off a long campaign whose later work is diminishing.
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

In this repository, treat the user's act of supplying a PR URL or number to an agent that did not open, commit to, or materially implement that PR as standing authorization to complete the normal PR lifecycle without further operator prompts: review and comment, edit PR metadata, request changes, create a focused harvest branch or follow-up PR, merge when eligible, close only after the terminal-close test below, and update the linked issue. Use a distinct merger by default. The user or repository owner may explicitly direct an authoring agent to self-merge a named PR; record that operational override without presenting it as independent scientific review. Do not force-push a contributor's branch, delete unrelated branches, broaden the issue objective, or promote unsupported claims. If an external permission or branch rule blocks an action, preserve the exact next action and report the actual blocker.

## Slice the PR into harvest atoms

Do not adjudicate a large PR as one indivisible story, but do not atomize it into
every file, theorem entrypoint, evidence row, or prose sentence either. Identify
only independently mergeable units or materially different risk boundaries,
such as:

- a pure utility or compatibility repair;
- an exact identity or narrowly scoped theorem;
- a reusable solver, transformation, source construction, or verifier;
- a conditional model component with explicit inputs;
- a speculative composition that depends on the headline hypothesis;
- campaign narration, memory, attempts, and generated output.

For each unit, state its local positive claim, dependencies, evidence, affected
consumers, and whether it still works if the PR's favored headline mechanism is
removed. Group closely related entrypoints under one proposition.

## Apply the three-question merge gate

Freeze this gate to the PR diff and the units the PR actually proposes to
merge. Use one substantive pass and one correction check. Do not recursively
audit neighboring accepted claims, historical artifacts, count labels, or
workflow rules. A finding blocks only if it falsifies a selected unit, exposes
an absent/circular load-bearing step, removes a proposition used from its
declared dependency closure, or breaks a consumer in the recorded impact
boundary. Record everything else once as follow-up.

Merge a unit only when all three answers are yes:

1. Is it correct under its stated inputs and conventions?
2. Is it materially novel or reusable enough to avoid future reinvention?
3. Is it locally complete, proportionately validated, compatible with the repository, and free of unresolved defects inside its own scope?

Do not require the unit to complete the parent campaign. Do require it to stand without borrowed conclusions, hidden parameters, convention conflicts, or tests that merely repeat copied formulas. A narrower evidence attachment may merge as a corroborating subclaim, regression, applicability result, or provenance record; it need not be discarded merely because it does not prove the parent claim.

Classify every unit as one of:

- **merge unchanged** — independent, clean, and already well scoped;
- **correct then merge** — valuable core exists and needs the minimum decoupling, naming, quantifier, hypothesis, evidence-role, or convention repair;
- **leave in PR history** — speculative capstone, duplicated machinery, unsupported interpretation, failed route, or maintenance cost with no durable reusable unit.

`Correct then merge` is an active lifecycle state, not a polite rejection. Name
the exact minimum repair and one landing check. Keep the source PR open in
`request changes`, `active refactor`, or
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
- Record the authoring or implementing agent and intended merger. Use a distinct
  merger unless the user or repository owner explicitly authorizes self-merge;
  that exception never supplies missing scientific review.
- Keep the goal issue open when the campaign remains incomplete.
- Remove campaign memory, attempt directories, debt ledgers, stale generated output, and proof-shaped narrative unless one is itself the reviewed durable artifact.
- Preserve a failed route in main only when it yields a reusable theorem, counterexample, oracle, fixture, or compatibility repair. Merge that object, not its diary.
- Do not make generated or canonical records claim more than the harvested unit establishes.
- Preserve the strongest useful positive statement. Fix an overbroad quantifier,
  add an honest hypothesis, split an interpretive layer, or relabel evidence
  before deleting a result. “Not proved by this artifact” is not “refuted.”

## Update the goal issue

After the final merge boundary is known, update the goal issue—not only the PR—with a jump-start record for the next agent. Link the reviewed PR and landed commit or follow-up PR. List every disposition, using `None` when a category is empty:

```md
## Harvest handoff from PR #<number>

### Landed
- <unit/path>: <positive local claim>. Evidence: <one receipt>.

### Correct next
- <unit>: <minimum repair and one landing check>, or `None`.

### History only
- <unit>: <specific terminal reason>, or `None`.

### Frontier
- Claims promoted: <none or ids>; goal: <open or complete>.
- Strongest result retained: <statement>.
- One next decisive action: <command, derivation, or experiment>.
- Reconsider a blocker if: <specific counterevidence>, or `not applicable`.
```

Keep this handoff short and unit-level. Link exact files, evidence, and commits so
the next agent can resume without reconstructing the PR. Add lifecycle or
terminal-close details only when they are actually in dispute. When authorized
to mutate GitHub, post the record; otherwise return it ready to post.

## State the closure contract without prescribing the solution

State the one decisive remaining gap before the goal can close, independently
of the reviewed route. Classify it as `verification`,
`implementation/representation`, or `scientific construction`, then name one
sufficient next move. Do not inventory every imaginable missing proof or make a
favored architecture mandatory.

Say what the artifact positively establishes before saying what it does not.
Distinguish an identity from a derivation, kinematics from dynamics, and an
applicability test from exact proof. Treat the review conclusion as rebuttable:
for a blocker, name the specific evidence that would change it. A conflict with
accepted canon blocks promotion, not a truthful conditional artifact; route an
independently surviving conflict through `challenges` without expanding the PR
review into a foundational campaign.

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

Run targeted tests and claim-appropriate oracles for each harvested unit, impact analysis for changed public symbols, affected consumers, and one repository validation at the final unchanged merge boundary. An additive public export may use scoped validation when impact is bounded, no existing contract changes, consumers are known, and targeted API coverage passes. Reserve full validation for promotion or release, shared numerics or verification machinery, claim/release governance semantics, changed existing public contracts with consumers, dependency or cross-cutting convention changes, multi-sector changes, or uncertain impact. The submitting agent uses `scripts/validate_changed.py` locally for this conservative decision and uses fixed checks only when no pytest scope is affected; the review agent checks the recorded decision against the diff and impact boundary without requiring a duplicate GitHub Actions replay. Run the periodic full backstop locally when scheduled or explicitly requested. Do not rerun unrelated full validation for each discarded campaign artifact or again after merge.

Process prose, memory templates, reviewer records, and evidence-count corrections
receive only their affected structural checks and `git diff --check`; they do
not stale or trigger scientific validation.

Do not add meta-tests for the review, reviewer, tally, or validation ledger.
After a repair, rerun only the stale check. If the user directs merge without
further validation, preserve the existing evidence and blocker record, stop
expanding the review, and proceed as far as repository protection permits.

## Report the disposition

Use this compact structure:

```md
## Harvest review

### Merge unchanged
- <unit>: <local claim and evidence>

### Correct then merge
- <unit>: <strong positive core, minimum repair, and one landing check>

### Leave in PR history
- <unit>: <why it should not enter main>

### Authority and goal state
- Claims promoted: <none or ids>
- Goal issue: <number/link and open or complete>
- Issue predates PR: <yes/no and timestamp evidence>
- Authoring or implementing agent: <identity>
- Merger: <distinct identity, or explicit owner-authorized self-merge>
- Issue handoff: <posted link or ready-to-post pending>
- PR lifecycle: <request changes, active refactor, active harvest, merged, or terminal closed>
- Terminal-close evidence: <not applicable, or qualifying reason plus landed replacement links>
- Campaign frontier: <next decisive question>
```

Lead with what remains useful and the concrete files or symbols to keep. Avoid
a large scorecard: the frozen boundary and three-question gate are the policy.
