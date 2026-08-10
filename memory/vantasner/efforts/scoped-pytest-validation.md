---
description: Keep fixed repository validation mandatory while scoping pytest to affected PR tests
author: codex
created: '2026-08-10T19:39:35Z'
updated: '2026-08-10T19:42:49Z'
tags:
- substrate-framework
- effort
- validation
- pytest
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort removes full-suite pytest from every bounded pull-request boundary
without weakening the inexpensive repository gates. It is complete when
`scripts/validate.sh` has explicit scoped and full modes, scoped verdicts cannot
be confused with repository-wide evidence, contributor instructions and the PR
template agree, regression tests exercise the interface, issue #30 owns the
change, and a distinct reviewer or repository owner decides the PR.

## Accepted Baseline
The tooling-only change starts from `origin/main` commit `65e4a7c` and accepted
release `v0.159.0`. The validation script, root contract, contributor guide, PR
template, README, git history, current issues and PRs, and related durable memory
were inspected. No accepted claim or scientific source module is changed.

## Constraints and Invariants
Every validation mode retains the repository, generated-state, memory, skill,
dependency-import, and compile gates. No arguments remain a backward-compatible
full-suite invocation. Scoped mode accepts only repository test selectors and
must reject empty scopes, source paths, and pytest options that could replace
test execution with collection or help output. Impact analysis, direct tests,
named verifiers, and consumer replay determine the scope; filename coincidence
does not. Full pytest remains the gate for promotions, releases, cross-cutting
or uncertain changes, and periodic integrated-main replay.

## Decomposition
1. [x] Profile the existing workflow and identify pytest as more than 94 percent of runtime.
2. [x] Inspect validation history, callers, policy surfaces, and GitNexus impact.
3. [x] Add `--pytest-scope` and explicit `--full` behavior with honest verdicts.
4. [x] Add interface regression tests and align contributor documentation.
5. [x] Exercise the real scoped workflow and run the diff audit.
6. [x] Submit the issue-linked PR for independent review and merge disposition.

## Attempts
Rejected designs remain recorded so later workflow work does not reintroduce
the original bottleneck or a weak scoped oracle.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Keep scoped author validation but require full pytest for every merge candidate | First policy draft | rejected | This retained the six-minute per-PR bottleneck at merge and did not satisfy the requested bounded-PR workflow | Permit a bounded scope through merge when its impact basis remains valid; retain explicit full triggers and periodic integrated replay |
| 0002 | Pass arbitrary pytest selection options through scoped mode | First script draft and test | rejected | Options such as `--collect-only` can exit successfully without executing tests and create a false passing verdict | Restrict the interface to repository test files, directories, and node IDs and insert `--` before selectors |

## Validation
Validation exercises the command interface, the real fixed-gate path, and the
limited scope claimed by this tooling-only change.

- `bash -n scripts/validate.sh`: passed.
- `.venv/bin/python -m pytest -q tests/test_validate_script.py`: 6 passed.
- `.venv/bin/python -m pytest -q -- tests/test_validate_script.py tests/test_repository_validation.py`: 11 passed.
- `/usr/bin/time -f 'elapsed=%e seconds' scripts/validate.sh --pytest-scope tests/test_validate_script.py tests/test_repository_validation.py`: every fixed gate passed, 11 scoped tests passed, elapsed 14.71 seconds.
- GitNexus change detection reported no affected execution process; its index does not map the shell script or new untracked test, so source inspection and direct regression tests remain the load-bearing impact evidence.
- `git diff --check`: passed before this record was added and must be rerun at the final boundary.

## Debt Ledger
No unresolved defect, unsupported promise, or broken consumer remains inside
the proposed merge unit.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
The implementation preserves every inexpensive validation stage and reduces the
measured bounded workflow from minutes to 14.71 seconds for this change. Full
pytest remains available through `--full` and the backward-compatible
no-argument invocation. Scoped mode names its limited verdict and rejects
arguments that could masquerade as executed tests.

## Canonicalization
This effort changes workflow tooling and contributor instructions only. It does
not alter the claim registry, release manifest, migration dispositions,
campaigns, generated accepted documentation, or scientific APIs.

## Done Gate
The implementation and local validation are complete. The effort remains active
until an issue-linked PR is independently reviewed and receives a merge
disposition from an actor who did not author or materially implement it.

## Cross-References
Canonical issue: https://github.com/vantasnerdan/substrate-framework/issues/30.
Implementation branch: `tooling/scoped-pytest-validation`.
Independent-review handoff: https://github.com/vantasnerdan/substrate-framework/pull/31.
