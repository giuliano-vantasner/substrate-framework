---
description: Require a pre-existing canonical issue for every pull request and prohibit agent self-merge
author: codex
created: '2026-08-10T09:16:31Z'
updated: '2026-08-10T09:27:24Z'
tags:
- substrate-framework
- effort
- agent-collaboration
- pull-request-policy
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort makes two collaboration gates universal: every pull request links one canonical issue created before PR submission, and no agent may merge a PR that it authored or materially implemented. It is complete when the normative root contract, operational start guide, PR template, and agent issue intake surface agree; reviewers can reject a PR missing either gate; issue #23 records the work; and all process validation passes without changing scientific authority.

## Accepted Baseline
The process change starts from accepted release `v0.159.0` and framework merge commit `5dc6d4d`. The current release, claim registry, root contract, start-here guide, PR template, recent collaboration effort, git history, open work, and canonical issue #23 were inspected. No accepted scientific claim or importable physics API is in scope.

## Constraints and Invariants
Issue #23 existed before the corrective branch and future PR. Agents may create their own canonical issue, but documentation, tooling, compatibility, harvest, and scientific PRs receive no exception. The author boundary includes an agent that wrote commits or materially implemented the PR; that agent may not perform the merge. A distinct reviewing agent or repository owner must decide and execute the merge. Existing claim-governance, harvest, validation, generated-state, and contributor-branch protections remain unchanged.

## Decomposition
Work proceeds through one process-only policy transaction.

1. [x] Verify current rules, authority, history, and memory.
2. [x] Create canonical issue #23 before the corrective PR.
3. [x] Make issue-first and non-self-merge rules normative in `AGENTS.md`.
4. [x] Align the start guide, PR template, harvest skill, continuation template, and agent issue intake form.
5. [x] Run GitNexus, link, schema, memory, generated-state, and repository validation.
6. [x] Open PR #24 linked to #23 and hand merge authority to a distinct reviewer or owner.

## Candidate Selection
The selected route combines explicit normative text, operational instructions, required PR fields, and a structured agent-task issue form. Editing only the start guide would leave the root contract ambiguous; editing only the PR template would be advisory without defining authorship and merge separation; a remote ruleset alone would not teach agents how to create and hand off compliant work.

## Attempts
Attempts are append-only and record any policy or validation defect before correction.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Audit merged collaboration rules | `rg` across `AGENTS.md`, `AGENTS_START_HERE.md`, and the PR template | policy gap confirmed | The guide exempted small docs/tooling PRs and prohibited self-merge only by default for scientific work | Replace both with universal rules and align intake/review fields |
| 0002 | First harvest-skill validation | Physics skill validator applied to `.agents/skills/research-pr-harvest` | invalid validator selection | The physics validator requires physics-only `references/governance.md` and is not a generic skill checker | Load `$skill-creator` and use its `quick_validate.py` |
| 0003 | First generic quick-validator invocation | Execute `quick_validate.py` directly | environment permission failure | The installed script lacks its executable permission bit | Run the unchanged validator through the repository Python interpreter |

## Validation
The issue form passed targeted YAML and required-field validation. The edited harvest skill passed the skill-creator `quick_validate.py` check after attempts 0002 and 0003 identified the correct validator and invocation. The effort memory passed an absolute-path repository-local `memory validate`; `scripts/validate_repository.py` passed with 202 accepted claims and no active proposals; GitNexus classified the documentation/process change as low impact with no affected consumers or processes; and direct path and policy-consistency checks passed. The one full `scripts/validate.sh` boundary completed with `2002 passed` and `ALL REPOSITORY WORKFLOW CHECKS PASS`. A separate `git diff --check` invocation passed afterward. PR #24 references the pre-existing issue #23, identifies Codex (`/root`) as its author and implementer, and leaves merge authority to a distinct reviewing agent or repository owner.

## Debt Ledger
The ledger tracks only defects introduced inside this policy transaction.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| Root and operational policies still contain exceptions | Baseline collaboration guide | Agents can submit issue-less docs PRs and self-merge non-scientific work | Contract and guide edits | resolved |
| Intake surfaces do not enforce the required declarations | Baseline templates | Authors and reviewers are not prompted for issue chronology or merger independence | PR template and agent issue form | resolved |

## Results
The validated branch makes issue-first PRs and independent merging universal across documentation, tooling, compatibility, harvest, and scientific work. `AGENTS.md` defines the normative gates; `AGENTS_START_HERE.md` supplies the operational sequence; the PR template records issue chronology, author identity, and the distinct merger; the structured agent-task issue form captures the required objective and handoff before PR submission; and the harvest skill and continuation template preserve the same separation. No terminal result is claimed until an independently reviewed PR lands.

## Canonicalization
This is a process-only effort. It changes no claim registry entry, release manifest, campaign, migration disposition, generated accepted documentation, accepted-claim memory, or physics implementation.

## Done Gate
The effort remains active until the universal rules and intake surfaces agree, the validation boundary passes, the PR links #23, and a distinct reviewer or owner performs the merge.

## Cross-References
Canonical work item: https://github.com/vantasnerdan/substrate-framework/issues/23. Independent-merge handoff: https://github.com/vantasnerdan/substrate-framework/pull/24. Predecessor process record: `memory/vantasner/efforts/agent-collaboration-onboarding.md`.
