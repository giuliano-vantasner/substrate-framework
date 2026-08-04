---
description: Repair legacy NumPy trapezoidal calls without misclassifying compatibility aborts as scientific campaign failures
author: vantasner
created: '2026-08-03T12:24:00Z'
updated: '2026-08-09T02:10:00Z'
tags:
- substrate-framework
- effort
- workflow-compatibility
category: efforts
confidence: established
status: archived
---

## Goal and Success Contract
This effort makes active consumers execute on the pinned current NumPy API and makes compatibility repair precede scientific adjudication. It is complete only when clean mutable scripts use `np.trapezoid`, executable preflight detects direct, imported, and dynamic legacy access, their affected consumers replay, the root contract, physics skill, and applicable task templates encode the same distinction, validation is sensitive to the edited paths, and no debt remains.

## Accepted Baseline
The framework starts from release v0.85.0 at commit `b34721e`; the external source checkout remains based on `substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`. P100 attempt 0008 preserves the earlier native DBD abort, while the two targeted external files are clean relative to that source commit and unrelated source-repository changes are excluded.

## Constraints and Invariants
The workflow edit surface is `AGENTS.md`, `.agents/skills/physics-erdos-loop/SKILL.md`, the applicable files under `memory-templates/`, and this effort record. The compatibility overlay covers mutable current-environment files under `engineering/`: the original DBD, shared seeding, and optional plotting consumers plus the remaining spark-discharge, ideal-coherence, spark-geometry, and screening integration call sites found during P119. Historical adjudicated campaigns, `runs/` attempt artifacts, hash-pinned bridge sources, unrelated dirty source files, equations, grids, tolerances, and scientific predicates remain unchanged.

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
| 0006 | P119 all-engineering compatibility sweep | `rg -n 'np\.trapz' engineering --glob '*.py'` plus targeted module replays | compatibility completion; one aggregate replay blocked | Nine legacy references remained in eight mutable engineering scripts; the ideal-coherence aggregate imports absent Matplotlib before either changed module | Replace every mutable engineering reference with `np.trapezoid`, then directly run the edited ideal-coherence modules instead of installing an unrelated plotting dependency |
| 0007 | P134 immutable source-graph replay | `campaigns/P134-em3-maxwell-coulomb-audit/reviews/replay_source_graph.py` | compatibility abort, not scientific failure | YM2 uses `getattr(np, "trapezoid", getattr(np, "trapz"))`; Python eagerly evaluates the missing legacy default even though the current attribute exists, and the first AST preflight detected only direct attributes | Add a reusable AST audit for direct, imported, and dynamic names plus eager defaults; update the shared workflow surfaces and rerun the unchanged source graph with alias-only compatibility |

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
The compatibility-only repair now changes eighteen legacy integration references across eleven numerical scripts: the original nine direct calls in `engineering/dbd/pipeline.py`, `engineering/dbd/l1_plasma.py`, and `engineering/seeding_kernel.py`, followed by seven fallback assignments in the spark-discharge, ideal-coherence, and spark-geometry phase-matching/FEM/coherence modules and two direct calls in `engineering/screening/dynamic_fluctuations.py`. `engineering/nucleation_efficiency_model.py` separately imports its documented optional plotting dependency only inside the existing guarded plot block. A repository-wide search of mutable `engineering/**/*.py` now finds no `np.trapz` token; immutable bridge and run evidence remains untouched.

The current-NumPy framework interpreter passes the seeding kernel's 14 checks, L1's 20, pipeline's 16, scaling law's 16, master DBD verifier's 49, uncertainty's 15, optimizer's 27, spark-discharge's 61, spark-geometry's 55, the screening self-report, CM5's 18, and direct ideal-coherence phase-matching and FEM executions plus an exact import identity check. The ideal-coherence aggregate verifier remains blocked before the edited modules by its unrelated unconditional Matplotlib import; this is recorded rather than hidden or repaired by installing a plotting stack. GitNexus classifies the canonical reuse as LOW risk with no affected execution process.

The workflow repair is consolidated in `AGENTS.md`, the physics skill, and four applicable task templates. The corrected skill validator passes, targeted repository validation reports 115 accepted claims and 120 pending units, both repositories pass `git diff --check`, and the one integrated workflow gate passes all 914 tests with all 427 memory files and the skill valid.

P134 exposes and closes a subtler compatibility form in immutable YM2 and
QCD2: nested `getattr` defaults are evaluated eagerly.
`source_audit.audit_numpy_trapezoid_compatibility` now
detects direct attributes, `from numpy import trapz`, dynamic literal
`getattr`, and the eager current-name/legacy-default pattern while ignoring
comments and docstrings. The root contract, physics skill, and the same four
task templates now require that AST preflight and a safe two-step mutable
fallback. Immutable sources still receive only an explicit runtime alias, so
their hashes and scientific predicates remain untouched.

## Canonicalization
This process-only effort changes no accepted claim, release, or generated accepted-claim documentation. Framework workflow assets are committed in the framework repository. The twelve external mutable-script edits remain an explicit compatibility overlay so the source checkout stays at pinned baseline `6d1f4e02f87a0bd1dc326cb68af01872d1e88c64`; historical bridge hashes, run artifacts, and native-error records are unchanged. P119 records the later overlay hashes separately from the baseline blobs.

## Done Gate
The effort is complete because mutable consumers use the current API, direct and dynamic legacy access is detected before adjudication, repaired scientific routes pass, compatibility provenance is separated from scientific verdicts, workflow assets agree, validation is sensitive, and the debt ledger is empty.

## Cross-References
The prior failure evidence is `campaigns/P100-bd2-thermal-rate-audit/attempts/0008/result.yaml`; the parent migration state is `memory/vantasner/efforts/framework-migration.md`.
