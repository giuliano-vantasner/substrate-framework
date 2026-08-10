---
description: Add a clear agent onboarding and independently reviewable pull-request workflow
author: codex
created: '2026-08-10T06:37:00Z'
updated: '2026-08-10T06:45:50Z'
tags:
- substrate-framework
- effort
- agent-collaboration
category: efforts
confidence: established
status: archived
---

## Goal and Success Contract
This effort delivers a concise start-here guide for contributing agents, a discoverable README entry point, and a pull-request template and review process that use repository memory, GitNexus, and the repository-scoped skills. It is complete when a fresh agent can establish authority and task ownership, avoid overlapping work, choose the right durable contract and skill, perform graph-aware implementation and review, distinguish artifact merge from claim promotion and goal completion, and reproduce the required validation without weakening `AGENTS.md`.

## Accepted Baseline
The process work starts from accepted release `v0.159.0` and framework commit `a562568`. `governance/releases/current.yaml`, `governance/claims.yaml`, `AGENTS.md`, `README.md`, the memory templates, both repository-scoped skills, current GitHub issue and PR examples, and the GitNexus context at the same commit were inspected. No accepted scientific claim or canonical source module is changed by this effort.

## Constraints and Invariants
The root `AGENTS.md` remains the normative scientific contract, chronology remains non-authoritative, generated documentation remains generated, and a merge remains distinct from scientific acceptance. The write boundary is onboarding and collaboration documentation, a GitHub pull-request template, README and contract cross-links, and this effort record. Existing user changes and contributor branches must not be rewritten, and GitHub visibility or branch-protection settings are not changed without separate authorization.

## Decomposition
Work proceeds through a minimal operational layer over the existing scientific contract.

1. [x] Inspect repository authority, status, history, memory, skills, GitNexus, and current GitHub collaboration examples.
2. [x] Compare extending the long root contract, adding a conventional human-only guide, and adding a dedicated agent start-here guide.
3. [x] Add the start-here workflow and collision-avoidance rules.
4. [x] Add the PR author and independent-review contract.
5. [x] Link the guide from the README and root agent contract.
6. [x] Validate links, memory, repository state, and the final diff.

## Candidate Selection
The selected route is a short `AGENTS_START_HERE.md` operational index backed by the existing normative `AGENTS.md`, plus a `.github/pull_request_template.md`. Expanding the already long root contract would obscure the first actions new contributors need, while a generic `CONTRIBUTING.md` would not reliably reach agent runtimes or encode the repository-specific memory, graph, skill, and scientific-review boundaries.

## Attempts
Attempts are append-only and preserve process findings that affect the chosen collaboration design.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Public repository inspection | Browser open of the supplied GitHub URL plus `gh repo view` | access boundary identified | The repository is currently private, so public fetch returns not found while authenticated CLI access succeeds | Add repository rules locally; leave visibility changes to a separately authorized operation |
| 0002 | GitNexus workflow inspection | Repository context, concept query, validator context, and `node .gitnexus/run.cjs status` | usable with documented limitation | The index is current but this documentation-heavy repository has no inferred execution processes | Require queries and symbol impact where applicable and an honest documentation-only result when no symbols map |
| 0003 | Recent merged-PR authority audit | PRs #4, #5, #7, #8, #11, and #14 plus merge diffs | workflow distinction confirmed and onboarding tightened | Five scientific harvests added public functions and result types while all six left claims and releases unchanged; package export is therefore not an authority signal | Require an authority-status and owning-issue inventory for every new public API |
| 0004 | Final archived-record validation | `memory validate --base "$PWD" "$PWD/memory/vantasner/efforts/agent-collaboration-onboarding.md"` | failed after all substantive gates | The Results section began with an inline filename instead of a plain-prose disclosure sentence | Rewrite only the opening sentence and rerun record-sensitive validation |

## Validation
Validation checked onboarding accuracy and the repository's existing workflow gates. Explicit path checks resolved the guide, PR template, README, memory templates, both repository skills, and bundled-memory source link. Repository validation reports 202 registered and accepted claims with no proposal or migration-queue change. The targeted memory invocation passes this record's frontmatter, category, confidence, status, and section-disclosure checks.

GitNexus was current at `a562568`; final change detection classified the tracked documentation surface as low risk with zero affected consumers or execution processes. The new untracked guide, PR template, and memory record were checked directly because Git diff based graph detection cannot inventory untracked documentation.

The single full `scripts/validate.sh` boundary passed all governance, generated-state, memory, skill, compilation, import, and 2,002 pytest checks in 204.30 seconds. The separately invoked `git diff --check` passed.

## Debt Ledger
The process debt ledger is empty. The repository's current private visibility and unavailable private-repository rulesets on the present GitHub plan are external access settings, not hidden debt in this documentation change.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
The new agent start-here guide gives fresh agents one read order and operational path through issue coordination, branch ownership, memory recall and contract selection, repository skill loading, GitNexus discovery and impact analysis, implementation boundaries, validation, independent review, and post-merge issue handoff. The guide keeps artifact merge, claim promotion, and goal completion independent.

`.github/pull_request_template.md` turns that workflow into author and reviewer fields, including unit-level dispositions, exact verification evidence, GitNexus impact, debt versus campaign frontier, and the terminal three-decision review. The audit of PRs #4, #5, #7, #8, #11, and #14 prompted an explicit public-interface authority inventory: new APIs must be mapped to accepted claims, conditional unpromoted infrastructure, or non-scientific utility, so package export cannot be mistaken for accepted framework truth.

README and root-contract links make the operational guide discoverable without demoting `AGENTS.md`. No accepted claim, release, generated document, campaign, migration disposition, or importable physics implementation changed.

## Canonicalization
This is a process-only effort. It changes no claim registry entry, release manifest, campaign, generated documentation, accepted-claim memory, or importable physics API.

## Done Gate
The effort is complete because the guide, template, cross-links, public-interface authority rule, targeted checks, GitNexus diff audit, full repository workflow, and separate whitespace gate pass with no process debt.

## Cross-References
The normative contract is `AGENTS.md`; reusable task state comes from `memory-templates/`; native workflows live under `.agents/skills/`; the requested public collaboration surface begins in `README.md` and `.github/pull_request_template.md`.
