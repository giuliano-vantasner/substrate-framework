---
description: Make higher-theorem promotion a proof-first repository workflow with Lean-ready onboarding
author: Codex
created: '2026-08-18T17:19:01+02:00'
updated: '2026-08-18T17:43:46+02:00'
tags:
- substrate-framework
- effort
- theorem-synthesis
category: efforts
confidence: established
status: archived
---

## Goal and Success Contract

Issue #90 delivers a backward-compatible synthesized-claim model, an advisory
claim graph, a focused theorem-synthesis skill and memory template, and a pinned
Lean environment installed by agent onboarding. The workflow must make positive
theorem promotion easier without treating accepted atoms as new review targets,
turning measurements into proofs, or adding ceremony unrelated to the theorem.

The implementation PR may merge once its bounded workflow contract is validated;
it does not itself promote a scientific claim. The repository owner explicitly
authorized the author to self-review and self-merge this PR without a distinct
reviewer. That issue-scoped exception does not change the default contract.

## Accepted Baseline

The work starts from release `v0.161.0`, pinned to
`substrate-framework@0beaac3`, on repository base `7dfe89b`. Authority remains
with the accepted entries in `governance/claims.yaml` and the current pinned
release. No accepted statement or release membership changes in this effort.

## Constraints and Invariants

The effort preserves these scientific and coordination boundaries.

- Historical Lean ingestion from `/home/dan/substrate` is a separate workflow.
- Active P232 work and its uncommitted test edit are outside this worktree.
- A synthesized theorem has at least two distinct accepted dependencies, a named
  structural gap, and a repository-local glue proof. There is no arbitrary
  three-claim threshold or positive-statement length cap.
- Lean and SymPy are proof backends. Measurement or simulation tests physical
  applicability and empirical adequacy; it is not the definition of proof.
- Lean can corroborate symbolic work, but is not mandatory for claims whose
  strongest practical oracle is elsewhere.
- Interpretive theorems are explicitly conditional and may not leak into the
  core dependency layer.
- Candidate comparison applies to genuinely competing mechanisms. A fixed
  theorem target need not invent rival scientific concepts merely to proceed.
- The dependency analyzer ranks possibilities; its output never gates promotion.

## Decomposition

1. [x] Verify authority, memory, issue, worktree isolation, and impact boundary.
2. [x] Implement synthesized/interpretive governance and focused tests.
3. [x] Implement the advisory dependency graph and CLI.
4. [x] Add the theorem-synthesis skill, memory template, and Lean onboarding.
5. [x] Consolidate proportional proof-first guidance in the agent contracts.
6. [x] Validate once at the final boundary and open the owner-authorized self-merge PR.

## Attempts

Technical attempts are append-only so onboarding and validation failures remain reproducible.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Backward-compatible optional metadata plus strict rules when `category: synthesized` or `layer: interpretive` is declared | Issue #90 and branch `process/theorem-synthesis-90` | Pass | Existing 210-claim registry validates unchanged; positive and negative synthesis tests pass | Complete |
| 0002 | First idempotent Lean onboarding replay | `scripts/setup_lean.sh` | Repaired and passed | Elan 4.2.3 treats reinstall of an installed toolchain as an error | Installed-toolchain inventory and cache detection make repeat setup idempotent |
| 0003 | First formal axiom-audit replay | `scripts/check_lean.sh` and `lake env lean Audit.lean` | Repaired and passed | The Lake library was declared but not a default build target, so bare `lake build` completed with zero jobs | Default target builds 8,028 jobs; glue theorem has no axioms |
| 0004 | First direct validation-scope selection | `scripts/validate_changed.py --base origin/main --head HEAD --print-only` | Repaired and passed | The documented shebang command lacked an executable file mode | Selector is executable, tested, and chose the correct full boundary for this PR |

## Validation

Validation is proportional to this cross-cutting workflow change and includes the actual Lean environment.

- Targeted governance/analyzer/selector/onboarding/public-surface tests: 50 passed.
- Lean setup and build: pinned Lean/mathlib setup passed; the library build completed 8,028 jobs.
- Formal audit: `SubstrateFramework.compose_implications` depends on no axioms.
- Skill validation: the skill-creator quick validator and repository skill validator passed.
- Impact analysis: `validate_registry` has two direct and one indirect consumer;
  `validate_proposal` and `render_claim_index` have no indexed upstream callers.
  Overall indexed risk is LOW, with repository scripts and tests still included
  manually because the graph omits some script-level calls.
- Final repository workflow: `scripts/validate_changed.py --base origin/main --head HEAD`
  selected full validation because governance semantics changed; 2,279 tests and
  all fixed checks passed in 291.60 seconds, followed by the Lean audit.
- `git diff --check`: passed separately before commit.

## Debt Ledger

The merge unit currently has no known unresolved debt.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results

The workflow now supports synthesized and interpretive claim metadata, fixed
theorem synthesis campaigns, scoped evidence modalities, and exact composition
artifacts without changing accepted claims. The advisory graph surfaces live
cross-sector intersections; the SG/MOM/GW run ranked `C-GW-007`, `C-MOM-002`,
and `C-GW-004` at the frontier. Agent bootstrap installs the pinned Lean 4.28.0
and mathlib v4.28.0 environment, builds the repository library, and exposes an
axiom audit. Pull request #91 contains the complete merge unit.

## Canonicalization

No accepted claim, campaign, release, or accepted-memory record changed, and
generated claim documentation remained current. Workflow guidance, schema
support, tooling, setup, templates, and tests land together in PR #91.

## Done Gate

This workflow implementation has met every in-scope gate: positive and negative
tests pass, the repository and generated state validate, Lean builds with an
empty axiom footprint, the debt ledger is empty, and PR #91 is ready for the
repository-owner-authorized self-merge. It promotes no scientific claim.

## Cross-References

The canonical issue and accepted baseline anchor this effort.

- Canonical issue: https://github.com/vantasnerdan/substrate-framework/issues/90
- Pull request: https://github.com/vantasnerdan/substrate-framework/pull/91
- Branch: `process/theorem-synthesis-90`
- Base release: `governance/releases/current.yaml`
- Registry: `governance/claims.yaml`
