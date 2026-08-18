---
description: Promote the derived usable total gravitational coupling claims C-IGR-004 and C-GRV-002
author: vantasner-review
created: '2026-08-18T15:48:27+00:00'
updated: '2026-08-18T15:48:27+00:00'
tags:
- substrate-framework
- effort
- induced-gravity
- P231
category: efforts
confidence: working
status: active
---

## Goal and Success Contract
This effort promotes two claims from P231: C-IGR-004 (the derived usable total gravitational coupling composition and its exact substrate-internal scheme selection) and C-GRV-002 (the exact necessary-and-sufficient total-sign map, the declared-premise baseline provenance, and the reciprocal total Newton constant). It is complete only when both exact statements enter the accepted registry, are pinned in release v0.162.0, individually reviewed, dependency-closed against accepted claims, materialized in importable code with tests, replayed against consumers, synchronized in generated docs and accepted memory, and validated once at the final boundary with an empty debt ledger. Merge authority stays with the distinct reviewer; pre-merge this contract sends status only, never a delivery claim.

## Accepted Baseline
The work starts from release v0.161.0 at branch base commit 7dfe89b. Accepted inputs read directly: C-GRV-001 (v0.68.0) for the additive baseline ledger and C-IGR-001..003 (v0.161.0) for the exact sharp/smooth/power-subtracted constant-mass coefficient families. The landed conditional modules `scalar_induced_newton` and `covariant_sine_gordon_action` are implementation reuse only, not authority.

## Constraints and Invariants
The two claims are conditional compositions of accepted families; no fitted constant, no borrowed Einstein-Hilbert coefficient, no observed-G or Planck comparator enters selection, formulas, tolerances, or tests. The usable scheme set and its finite parts are outputs of the exact legs L1/L2/L3, not choices. The additive baseline B stays a declared premise. The `tau^-1` higher-curvature and nonlocal sectors stay in the control ledger with a predeclared domain, never folded into the coupling. Write surfaces: `campaigns/P231-total-coupling-rung/`, `governance/claims.yaml`, `governance/releases/`, `memory/vantasner/decisions/`, and generated `docs/generated/`, `memory/framework/` via scripts only.

## Decomposition
Work proceeds through these dependency-ordered steps.

1. [x] Recall and source verification (accepted claims, campaign artifacts, verifiers reproduced).
2. [x] Independent governance rederivation of each load-bearing step (fresh SymPy + mpmath, no module import).
3. [x] Move proposal to the immutable campaign log; write adjudication and per-claim reviews.
4. [x] Registry entries + release v0.162.0 + current.yaml (current-set closed).
5. [x] Accepted-memory review files + generated docs and memory synchronization.
6. [ ] Full validation at the final boundary; finalize the promotion-gate attempt record; hand off for independent review and merge.

## Attempts
Attempts 0001-0004 (in the campaign log) delivered and audited the derived object across three self-adversarial repair rounds (F1-F10, A1-A4). Attempt 0005 is this promotion-gate record: the reviewed registry-materialization event, not a new scientific route.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0005 | Promotion transaction | campaigns/P231-.../attempts/0005/manifest.yaml; scripts/validate.sh --full | pending final boundary | registry/release/docs/memory materialization | none; hand off to independent reviewer |

## Validation
Validation covers the two claim statements, verifier sensitivity, dependency closure, consumer replay, and generated state, not merely a check count.

- Targeted scientific command: `PYTHONPATH=src .venv/bin/python campaigns/P231-total-coupling-rung/verify.py` (expect ALL 32 CHECKS PASS) and `.../reviews/independent_total_coupling_review.py` (expect ALL 20 CHECKS PASS).
- Mutation/counterexample: covered by the primary verifier's mutation legs (prefactor, conformal weight, Bessel order, E1 branch, reference member) and the excluded-scheme rejection.
- Dependency replay: accepted P230 and C-GRV-001 consumer suites are additive-only and replay green.
- Targeted tests: `pytest tests/test_total_gravitational_coupling.py` (41).
- Impact analysis and scope rationale: claim promotion + release governance semantics => full validation required.
- `scripts/validate.sh --full` once at the unchanged boundary.
- `git diff --check` run separately from commit.

## Debt Ledger
No debt is carried. The dependency, consumer, and nonduplication audits close with empty debt.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results
The registry gained C-IGR-004 and C-GRV-002; release v0.162.0 pins the closed current set (212 accepted); the campaign log, per-claim reviews, accepted-memory reviews, generated docs, and framework memory are synchronized. Final-boundary validation results are recorded in the attempt-0005 manifest and the campaign adjudication integrated gate.

## Canonicalization
Registry: `governance/claims.yaml` adds C-IGR-004, C-GRV-002. Release: `governance/releases/v0.162.0.yaml` + `current.yaml`. Immutable campaign: `campaigns/P231-total-coupling-rung/` with `adjudication.yaml`. Extracted API: `src/substrate_framework/total_gravitational_coupling.py` with `tests/test_total_gravitational_coupling.py`. Generated: `docs/generated/claim-index.md`, `memory/framework/claims/{C-IGR-004,C-GRV-002}.md`, `memory/framework/releases/v0.162.0.md`. No proposal prose was merged into canonical memory.

## Done Gate
The ten AGENTS.md success conditions are checked at the final boundary; merge remains with the distinct reviewer, so this contract stays active until the independent reviewer reproduces the evidence and merges.

## Cross-References
Link the P231 proposal and campaign record, C-IGR-004, C-GRV-002, C-GRV-001, C-IGR-001..003, `total_gravitational_coupling.py`, `tests/test_total_gravitational_coupling.py`, release v0.162.0, issue #88, and PR #89.
