# Agent Contributors: Start Here

This is the operational entry point for agents that propose, implement, review,
or harvest work in Substrate Framework. Read the root [`AGENTS.md`](AGENTS.md)
in full before changing the repository. That file is the normative scientific
and governance contract; this guide tells collaborators how to apply it without
duplicating work or confusing a merged artifact with accepted science.

## 1. Establish authority and scope

Use this read order at the start of a task:

1. `AGENTS.md` and any more-local agent instructions.
2. `governance/releases/current.yaml` and `governance/claims.yaml`.
3. The canonical source modules, immutable campaigns, proposal, issue, and PR
   relevant to the requested scope.
4. Repository-local memory, verified back against those sources.
5. Exploratory artifacts and external comparators.

A pinned accepted release and accepted claim registry outrank a newer commit,
confident prose, a passing script, or an attractive numerical match. Never edit
`docs/generated/` or `migration/source-claims.yaml` by hand. This authority
controls release and promotion decisions; canon remains scientifically
challengeable, and a truthful conditional artifact may merge without claim
promotion while a challenge is reviewed.

## 2. Coordinate before editing

Begin from a clean understanding of the shared repository. With the GitHub CLI
available, use:

```bash
git status --short --branch
git log -5 --oneline --decorate
gh issue list --state open --limit 30
gh pr list --state open --limit 30
```

Otherwise inspect the repository's Issues and Pull requests pages before
claiming work, and record any access limitation in the handoff.

Every intended pull request must have exactly one canonical issue before even a
draft PR is submitted. A contributing agent may create the issue itself. This
requirement applies without exception to documentation, tooling, compatibility,
harvest, and scientific work. Do not open a standalone PR.

The issue must state the positive objective, scope, success gate, dependencies,
and coordination boundary. Before substantive work, comment there with:

- the exact slice you are taking and the positive deliverable;
- your branch name and intended write surfaces;
- claim identifiers, proposal identifiers, and dependencies in play;
- anything another contributor should avoid editing concurrently.

Issue comments coordinate ownership; they do not grant scientific authority.

Use focused branch names such as `research/<proposal>-<topic>`,
`harvest/<issue-or-pr>-<topic>`, `fix/<topic>`, or `docs/<topic>`. One agent owns
the contributor branch unless collaboration is explicitly agreed. Reviewers do
not force-push or silently rewrite that branch; they request changes or create a
focused follow-up or harvest branch.

Treat a merged topic branch as disposable transport, not durable memory. The
repository automatically deletes same-repository pull-request head branches
after merge; the merge commit, PR, issue handoff, and landed `main` history are
the durable discovery paths. If automatic cleanup does not occur, the merger
deletes that exact merged head after verifying the PR state and target. Preserve
open heads and closed-unmerged or failed heads by default so unresolved work is
not erased; retire those only through an explicit owner decision after the
terminal-close reason and any landed replacement are recorded. Never delete
`main`, a protected branch, another open contributor branch, or an unverified
head merely because it appears old.

Before allocating a claim ID, search the registry, campaigns, proposals, and
memory. Rejected and provisional IDs remain reserved. Refresh the issue, PR,
Git status, and shared canonical files before editing them; never overwrite a
dirty worktree or another agent's uncommitted changes.

## 3. Bootstrap the local tools

From the repository root:

```bash
scripts/bootstrap.sh
memory --version
```

If the clone already has the project-local GitNexus runner, check the index:

```bash
node .gitnexus/run.cjs status
```

On a fresh clone where `.gitnexus/run.cjs` does not exist, initialize the local
index with `npx gitnexus analyze`, then inspect `git status` and do not keep any
generated change to tracked repository instructions. If the index is stale,
run `node .gitnexus/run.cjs analyze`. The index is navigation evidence, not an
authority source.

## 4. Use memory as working state

Search before creating a new route:

```bash
memory search --base "$PWD/memory" "<issue, claim, symbol, or mechanism>"
memory grep --base "$PWD/memory" -F "<exact claim ID or symbol>"
```

Verify every useful hit at its cited source. Then instantiate the appropriate
file from [`memory-templates/`](memory-templates/) before substantive work:

| Work | Contract |
| --- | --- |
| Durable multi-step task | `effort-contract.md` |
| New scientific campaign | `campaign-proposal.md` plus `proposals/<id>/proposal.yaml` |
| Long research program | `research-arc.md` |
| Independent claim review | `claim-review.md` |
| Bounded continuation or harvest PR | `delegated-continuation-pr-template.md` |
| Explicitly authorized subagent slice | `subagent-task.md` |

Keep attempts append-only. Memory records active plans, decisions, and reusable
failure mechanisms; it does not replace claims, releases, campaign evidence, or
source code. Validate one explicit target at a time:

```bash
memory validate --base "$PWD" "$PWD/memory/<agent>/<category>/<entry>.md"
```

## 5. Load the repository skills

Agents with native skill discovery should invoke the named skill. Other agents
must read the corresponding `SKILL.md` in full and follow the same workflow.

- Use [`physics-erdos-loop`](.agents/skills/physics-erdos-loop/SKILL.md) for
  derivations, simulations, formalization, campaigns, claim changes, migration,
  canonical physics APIs, and framework reconciliation.
- Use [`research-pr-harvest`](.agents/skills/research-pr-harvest/SKILL.md) when a
  scientific PR URL or number is supplied, when deciding what is mergeable, or
  when harvesting durable units from an incomplete campaign. Also load
  `physics-erdos-loop` when the PR contains physics claims.

Skills specialize the root contract; they do not relax it. Read any reference
files the selected skill routes to before taking the corresponding action.

## 6. Use GitNexus as a second structural view

Use both source search and the graph. A normal MCP-capable workflow is:

1. Read `gitnexus://repos` and
   `gitnexus://repo/substrate-framework/context`; refresh a stale index.
2. Query the task concept to find related symbols and processes.
3. Inspect context for load-bearing symbols.
4. Run upstream impact analysis before changing a canonical API or symbol.
5. Run change detection on the final diff before requesting review.

When MCP tools are unavailable, use `rg` for source discovery and the local
GitNexus CLI for index status. Record the direct and indirect consumers you
actually inspected. A documentation-only diff may map to no symbols or process;
report that limitation honestly instead of inventing an impact result.

Re-index after a substantial committed code change so the next collaborator
does not inherit a stale graph.

## 7. Build a reviewable change

Keep one coherent merge boundary per PR. Put reusable definitions and solvers
under `src/substrate_framework/` with tests; keep exploration in proposals and
campaigns. Do not duplicate canonical helpers in campaign code, edit immutable
campaign history, commit host-specific artifacts, or mix unrelated cleanup into
the branch.

Package visibility is not scientific authority. A harvest PR may add a useful
public API while promoting no claim. Every new or materially changed public
symbol must be inventoried in the PR as one of:

- backed by exact accepted claim IDs;
- conditional, unpromoted infrastructure linked to an open goal;
- non-scientific utility or workflow code.

An unpromoted scientific API needs explicit inputs, assumptions, and exclusions
in its module/API documentation. It may be reused only with that conditional
status declared; its presence in `src/` or the package `__all__` cannot be cited
as accepted framework truth.

For scientific work, freeze candidates and structural selection criteria before
opening comparator values. Use the strongest practical oracle, demonstrate
verifier sensitivity, record assumptions and imports, and replay affected
consumers. A failed route is attempt evidence and triggers the next materially
different attempt; it is not the requested positive result.

Before requesting review:

1. Bring the effort or proposal memory up to date, including remaining frontier
   and debt inside the proposed merge unit.
2. Run targeted tests, scientific verifiers, mutations, and affected consumers.
3. Inspect the diff and GitNexus change impact.
4. Run the fixed repository checks and the pytest scope justified by the diff
   and impact analysis once at the final unchanged PR boundary:

   ```bash
   scripts/validate.sh --pytest-scope tests/test_affected_module.py [more selectors ...]
   ```

   An additive public export may remain scoped when impact analysis shows a
   bounded sector, no changed existing contract, known consumers, and targeted
   API coverage. Use `scripts/validate.sh --full` instead when the change
   reaches shared numerics, verification machinery, claim or release governance
   semantics, changes an existing public contract with consumers, changes
   dependencies or cross-cutting conventions, spans multiple framework
   sectors, or has an uncertain dependency boundary. Claim promotions and
   releases always require `--full`.
5. In a separate invocation, run:

   ```bash
   git diff --check
   ```

Record the exact pytest selectors, commands, status codes, and meaningful
verdicts in the PR; a scoped pass is not a repository-wide pass. A bounded PR
can remain scoped through merge when its impact boundary is still valid against
the current base. Do not repeat an equivalent validation at the same unchanged
boundary. Pull-request CI uses `scripts/validate_changed.py` to reproduce a
conservative changed-file decision, including `--fixed-only` when no pytest
scope is affected and `--full` for cross-cutting or uncertain changes. Scheduled
or manual CI runs the periodic integrated-main full backstop rather than
duplicating it on every merge push; a pass count alone is not a review.

## 8. Open the pull request

Use [the repository PR template](.github/pull_request_template.md). Record the
pre-existing canonical issue, authoring agent, and intended independent merger.
Link the issue with `Advances #N` while any part of the positive objective
remains and reserve `Fixes #N` for complete success. A draft PR is appropriate
while the merge boundary or evidence is still changing, but the issue must exist
before that draft is opened.

The author must state separately:

1. whether the artifact is locally complete and mergeable;
2. whether any scientific claim is proposed for promotion;
3. whether the canonical goal is actually complete.

An agent may not merge a PR that it opened, authored a commit for, or materially
implemented. This applies to every PR type. A distinct reviewing agent or
repository owner decides the disposition and performs the merge. If the
authoring agent makes substantive review repairs, another actor still must
merge. When no distinct merger is available, leave the validated PR ready for
handoff. Explicit PR-lifecycle authorization never overrides this separation.

## 9. Review the pull request

Review the actual head commit and reproduce load-bearing evidence. Do not review
only the PR narrative or treat all files as one indivisible story.

1. Establish the base release, linked goal, diff, accepted boundary, proposal,
   memory, checks, and review discussion.
2. Confirm the canonical issue predates the PR and identify the authoring agent
   and a distinct merger. Do not review an issue-less PR toward merge.
3. Split the PR into the smallest coherent units. For each, name its local
   claim, dependencies, outputs, tests, consumers, and whether it survives if
   the headline hypothesis is removed.
4. Audit correctness and scope. Independently rederive or reimplement the
   load-bearing step; inspect mutations, counterexamples, limits, numerical
   refinement, and wrong-convention probes as applicable.
5. Audit framework fit and architecture. Check declared imports, units,
   conventions, dependency closure, duplication, GitNexus impact, generated
   consumers, the authority status of every public symbol, and debt created
   inside each unit.
6. Make three independent decisions:

   - **Artifact merge:** is a correct, novel, reusable unit worth maintaining?
   - **Claim promotion:** has a specific statement passed claim-level governance?
   - **Goal completion:** have all success gates for the canonical issue passed?

Classify findings as blocking, required refactor, or follow-up. Correctness
defects, hidden premises, unsupported claim language, insensitive verification,
broken consumers, and unresolved debt within the proposed unit are blocking.
Incomplete future work is campaign frontier and may remain open when a smaller
unit is independently useful.

Treat `request changes`, `active refactor`, and `active harvest` as live review
states. A required-refactor finding must name an owner or handoff, a live source
or harvest PR, the exact repair, and the landing test. Keep the source PR open
while that finite path is active. Close unmerged only when all reusable atoms
land elsewhere, all remaining atoms have unit-level evidence of being
incorrect, non-novel, or unmaintainable, the owner explicitly withdraws the
work, or a landed replacement makes it redundant. A canon conflict, incomplete
dependency closure, or unavailable distinct merger is not by itself terminal.

End the review with an explicit disposition:

```text
Artifact merge: yes/no, with unit-level rationale
Claim promotion: none or exact claim IDs and review evidence
Goal completion: yes/no, with the still-open gate
Merge as written: yes/no
Refactor or harvest: exact units and required changes
Leave in PR history: exact units and rationale
Next decisive action: one concrete step
```

## 10. Merge and hand off

The distinct reviewer or repository owner—not the authoring or implementing
agent—merges only the accepted unit boundary. A merge creates provenance and
reusable code; it does not automatically promote a claim or close the parent
issue.

After the final disposition:

- update the canonical issue with unit-level lists for merged, requires
  refactor, and history-only work, including landed links and rationales;
- after a successful merge, confirm the exact same-repository PR head was
  automatically deleted and delete it explicitly if the repository setting did
  not do so; retain closed-unmerged or failed heads unless their owner explicitly
  retires them after recording the terminal-close rationale;
- keep a source PR open while a promised refactor or harvest is live; close it
  as superseded only after the reusable unit lands, or close it unmerged only
  after the terminal-close test in the review section passes;
- leave the issue open with the next decisive action when the PR only advances
  it;
- synchronize durable effort or decision memory with the landed commit and
  actual scientific status;
- promote claims only through individual review, registry and release updates,
  generated documentation, accepted-memory synchronization, and full closure;
- refresh GitNexus after substantial merged code changes.

If permissions or branch rules block the lifecycle, preserve the exact
ready-to-post review or issue handoff and report the external blocker. Do not
rewrite the objective into a smaller success.
