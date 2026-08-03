---
description: Repair legacy NumPy trapezoidal calls without misclassifying compatibility aborts as scientific campaign failures
author: vantasner
created: '2026-08-03T12:24:00Z'
updated: '2026-08-03T12:45:00Z'
tags:
- substrate-framework
- effort
- workflow-compatibility
category: efforts
confidence: established
status: archived
---

## Goal and Success Contract
This effort makes the active DBD consumers execute on the pinned current NumPy API and makes compatibility repair precede scientific adjudication. It is complete only when the clean mutable scripts use `np.trapezoid`, their affected consumers replay, the root contract, physics skill, and applicable task templates encode the same distinction, validation is sensitive to the edited paths, and no debt remains.

## Accepted Baseline
The framework starts from release v0.85.0 at commit `b34721e`; the external source checkout remains based on `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. P100 attempt 0008 preserves the earlier native DBD abort, while the two targeted external files are clean relative to that source commit and unrelated source-repository changes are excluded.

## Constraints and Invariants
The edit surface is `AGENTS.md`, `.agents/skills/physics-erdos-loop/SKILL.md`, the applicable files under `memory-templates/`, this effort record, and the clean external files `engineering/dbd/{pipeline.py,l1_plasma.py}`, `engineering/seeding_kernel.py`, and `engineering/nucleation_efficiency_model.py`. Historical adjudicated campaigns, generated documents, hash-pinned bridge sources, unrelated dirty source files, equations, grids, tolerances, and scientific predicates remain unchanged.

## Decomposition
Work proceeds through a compatibility-first path and does not consume a scientific candidate attempt for a missing library alias.

1. [x] Verify the active boundary, external file cleanliness, and applicable contracts.
2. [x] Compare direct repair, mass historical rewrite, and runtime-only shimming.
3. [x] Replace the active legacy calls with `np.trapezoid`.
4. [x] Consolidate compatibility-before-adjudication in the root contract, skill, and task templates.
5. [x] Replay direct and downstream DBD consumers and inspect graph-visible changes.
6. [x] Validate workflow assets and record the terminal result.

## Candidate Selection
The selected route is a direct mechanical repair of the clean active DBD and shared-consumer scripts plus consolidated workflow guidance. A mass rewrite is rejected because it would alter hash-pinned historical evidence and unrelated dirty work; a runtime-only shim is rejected because it leaves the known mutable defect in place.

## Attempts
Attempts are append-only and distinguish environment compatibility from scientific failure.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Pre-change source replay inherited from P100 | `campaigns/P100-bd2-thermal-rate-audit/attempts/0008/result.yaml` | compatibility abort | Current NumPy has `np.trapezoid` but no legacy `np.trapz` attribute | Repair the three clean active calls, then rerun the unchanged consumers |
| 0002 | Direct active-script replay after the first repair | `/home/dan/substrate-framework/.venv/bin/python engineering/dbd/{l1_plasma.py,pipeline.py,scaling_law.py,verify.py}` | three pass; L1 compatibility abort | L1 reaches clean shared `engineering/seeding_kernel.py:seeded_population`, whose remaining legacy alias aborts before later checks | Impact-audit and repair the shared mutable call, then rerun L1 and its affected consumers |
| 0003 | Shared-kernel downstream replay | framework interpreter on the graph-identified consumers | eight scientific consumers pass; optional plotting consumer aborts at import | `nucleation_efficiency_model.py` documents plotting as optional but imports Matplotlib unconditionally, while the current-NumPy framework venv does not install it | Move the optional import into its guarded plotting block, then rerun the consumer |
| 0004 | First targeted skill validation | `.venv/bin/python .agents/skills/physics-erdos-loop/scripts/validate_skill.py` | usage exit 1 | The validator requires the skill-directory positional argument | Rerun with `.agents/skills/physics-erdos-loop` and retain the first invocation as command-usage evidence |
| 0005 | First terminal-record patch | `apply_patch` on this effort | context verification failure | The patch omitted the still-open workflow-ambiguity row from its expected debt-table context | Re-read the file and apply a context-complete terminal update |

## Validation
Validation targets the repaired runtime paths and consolidated instructions, not the already-passed P100 scientific claim.

- Direct DBD scripts: run `engineering/dbd/l1_plasma.py` and `engineering/dbd/pipeline.py` with the framework interpreter.
- Downstream consumers: rerun `engineering/dbd/scaling_law.py` and the DBD verifier named by graph impact.
- Graph audit: use GitNexus impact before editing and `detect_changes` after editing.
- Workflow assets: run the physics-skill validator and memory validation for this effort.
- Repository boundary: run targeted repository validation and `git diff --check`; run the full suite once because validation logic and project-wide workflow instructions change.

## Debt Ledger
The ledger is empty: active aliases, the shared-kernel alias, the optional plotting import, provenance, and workflow consistency are discharged by the edits and replay below.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
The compatibility-only repair changes nine legacy calls to `np.trapezoid` across `engineering/dbd/pipeline.py`, `engineering/dbd/l1_plasma.py`, and `engineering/seeding_kernel.py`; `engineering/nucleation_efficiency_model.py` now imports its documented optional plotting dependency only inside the existing guarded plot block. The current-NumPy framework interpreter passes the seeding kernel's 14 checks, L1's 20, pipeline's 16, scaling law's 16, master DBD verifier's 49, uncertainty's 15, optimizer's 27, and CM5's 18; the optional nucleation consumer exits zero and passes its self-checks. GitNexus classifies every pre-edit impact and the final combined diff as LOW risk with no affected execution process.

The workflow repair is consolidated in `AGENTS.md`, the physics skill, and four applicable task templates. The corrected skill validator passes, targeted repository validation reports 115 accepted claims and 120 pending units, both repositories pass `git diff --check`, and the one integrated workflow gate passes all 914 tests with all 427 memory files and the skill valid.

## Canonicalization
This process-only effort changes no accepted claim, release, generated documentation, or migration disposition. Framework workflow assets are committed in the framework repository. The four external script edits remain an explicit compatibility overlay on clean target files so the source checkout stays at pinned baseline `6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; historical source hashes and native-error records are unchanged.

## Done Gate
The effort is complete because the mutable consumers use the current API, the repaired scientific routes pass, compatibility provenance is separated from scientific verdicts, workflow assets agree, validation is sensitive, and the debt ledger is empty.

## Cross-References
The prior failure evidence is `campaigns/P100-bd2-thermal-rate-audit/attempts/0008/result.yaml`; the parent migration state is `memory/vantasner/efforts/framework-migration.md`.
