---
description: Keep viable scientific pull requests active through repair or harvest and scope validation by impact
author: codex
created: '2026-08-18T09:27:59Z'
updated: '2026-08-18T09:35:01Z'
tags:
- substrate-framework
- effort
- pull-request-policy
- research-harvest
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort corrects the PR process exposed by the premature closure of PR #77. It succeeds when viable work with a finite repair or harvest path remains active, terminal closure requires unit-level evidence, canon conflicts can open governed challenges instead of ending inquiry, validation scope follows measured impact, and the root contract, onboarding, PR template, research skills, and task templates agree. Issue #81 is canonical, and a distinct reviewer or repository owner must merge the corrective PR.

## Accepted Baseline
The process change starts from accepted release `v0.160.0` and framework commit `da4d927`. The current release, accepted registry, PR #77 and goal #76, the prior issue-first workflow memory, both repository skills, affected task templates, Git history, and GitHub state were inspected. No accepted scientific claim, release manifest, generated documentation, migration disposition, or physics implementation changes in this effort.

## Constraints and Invariants
Artifact merge, claim promotion, and goal completion remain independent. Accepted canon governs releases and promotion but remains scientifically challengeable. Non-self-merge, issue-first coordination, immutable campaign history, and branch protections remain in force. The correction consolidates existing clauses rather than creating a parallel review system, and it must not turn speculative or defective work into mergeable code.

## Decomposition
The effort follows one bounded process transaction and one separately reviewed scientific harvest.

1. [x] Restore and reopen PR #77 and correct its PR/issue handoff.
2. [x] Extract its independently reusable exact-mass unit into harvest PR #82 while leaving #77 open.
3. [x] Define active-refactor and terminal-close lifecycle rules.
4. [x] Make canon conflicts eligible for a separate challenge without weakening promotion authority.
5. [x] Replace the public-export full-suite trigger with impact-based scoped/full selection.
6. [x] Align AGENTS, onboarding, the PR template, both research skills, and five memory templates.
7. [x] Add a conservative changed-file CI selector, fixed-only mode, and focused regression tests so PRs do not replay the full suite mechanically.
8. [x] Open process PR #83 for issue #81 and hand merge authority to a distinct reviewer or owner.

## Attempts
The attempts preserve the process failures that motivated and tested the repair.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Close PR #77 after identifying unmet promotion dependencies | GitHub close and branch cleanup | rejected process action; reversed | The review conflated claim promotion with artifact merge and treated canonical dependency gaps as terminal | Restore the head, reopen the PR, and create a focused harvest |
| 0002 | Apply the categorical public-export full-suite rule to harvest #82 | `scripts/validate.sh --full` | stopped at the user's scope correction; not counted as validation | The rule ignored low measured impact and repeated integrated coverage | Run the focused API tests and scoped workflow; revise the trigger |
| 0003 | First lifecycle-policy regression assertion | scoped workflow for `tests/test_public_contribution_surfaces.py` | one assertion failed | The test expected `live PR` while the skill deliberately requires the stronger `live source or harvest PR` wording | Correct only the assertion and rerun the failed scoped boundary |
| 0004 | Verify final GitHub execution state | PR #82 check rollup and `.github/workflows/validate.yml` | CI optimization gap found | The workflow still hard-coded `--full` for every PR and would negate the local impact rule | Add `validate_changed.py`, fixed-only support, conservative full triggers, and a scheduled/manual full backstop |

## Validation
Validation is proportionate to this process, selector, and regression-test surface. Both edited skills pass their native validators. GitNexus reports low risk and no affected execution process. The final workflow command is `scripts/validate.sh --pytest-scope tests/test_public_contribution_surfaces.py tests/test_repository_validation.py tests/test_validate_changed.py tests/test_validate_script.py`; its 32 focused tests cover public policy, fixed checks, full/scoped/fixed-only dispatch, conservative source/governance/removal triggers, and workflow wiring. The earlier interrupted full run and failed scoped attempt are not counted. The final effort record passes absolute-path memory and repository-schema validation, and `git diff --check` passes separately.

## Debt Ledger
The process-unit debt ledger is empty; independent merge remains workflow state, not hidden debt.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
PR #77 is open with its restored head, and focused harvest PR #82 advances goal #76 without promoting claims. The corrective policy makes `refactor then merge` active work with an owner, live PR, repair, and landing test; permits unmerged closure only under enumerated terminal conditions; treats accepted canon as authoritative but revisable; and allows bounded additive public APIs to use scoped validation when impact evidence supports it. Pull-request CI now makes that same conservative decision automatically; periodic or manually requested CI retains the integrated full-suite backstop.

## Canonicalization
This is a process-only correction. Durable policy lives in `AGENTS.md`, `AGENTS_START_HERE.md`, the PR template, both research skills, and the aligned memory templates. The regression test prevents those public contribution surfaces from silently returning to the failed behavior.

## Done Gate
The local process unit is complete and validated in PR #83, but this effort remains active until a distinct reviewer or repository owner merges it. PR #77 remains active while harvest #82 is reviewed; neither an unpromoted dependency nor unavailable self-merge authority closes it.

## Cross-References
Canonical process issue: https://github.com/vantasnerdan/substrate-framework/issues/81. Corrective process PR: https://github.com/vantasnerdan/substrate-framework/pull/83. Corrected source campaign: https://github.com/vantasnerdan/substrate-framework/pull/77. Focused scientific harvest: https://github.com/vantasnerdan/substrate-framework/pull/82. Predecessor process record: `memory/vantasner/efforts/issue-first-non-self-merge-policy.md`.
