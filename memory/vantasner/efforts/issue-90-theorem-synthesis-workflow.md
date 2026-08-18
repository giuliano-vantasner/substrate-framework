---
description: Make higher-theorem promotion a proof-first repository workflow with Lean-ready onboarding
author: Codex
created: '2026-08-18T17:19:01+02:00'
updated: '2026-08-18T17:19:01+02:00'
tags:
- substrate-framework
- effort
- theorem-synthesis
category: efforts
confidence: working
status: active
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
- Active P231 work and its uncommitted test edit are outside this worktree.
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
2. [ ] Implement synthesized/interpretive governance and focused tests.
3. [ ] Implement the advisory dependency graph and CLI.
4. [ ] Add the theorem-synthesis skill, memory template, and Lean onboarding.
5. [ ] Consolidate proportional proof-first guidance in the agent contracts.
6. [ ] Validate once at the final boundary, self-review, PR, and merge.

## Attempts

Technical attempts are append-only so onboarding and validation failures remain reproducible.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Backward-compatible optional metadata plus strict rules when `category: synthesized` or `layer: interpretive` is declared | Issue #90 and branch `process/theorem-synthesis-90` | In progress | Avoids bulk rewriting accepted claims while giving new theorems an executable contract | Implement and test the exact schema |
| 0002 | First idempotent Lean onboarding replay | `scripts/setup_lean.sh` | Technical failure: existing toolchain returned status 1 | Elan 4.2.3 treats reinstall of an installed toolchain as an error | Inventory `elan toolchain list` before installation, then rerun setup |
| 0003 | First formal axiom-audit replay | `scripts/check_lean.sh` and `lake env lean Audit.lean` | Technical failure: the library had not produced an olean | The Lake library was declared but not a default build target, so bare `lake build` completed with zero jobs | Mark the library as `@[default_target]`, rebuild, and rerun the audit |

## Validation

Validation is proportional to this cross-cutting workflow change and includes the actual Lean environment.

- Targeted governance/analyzer tests: pending.
- Lean project build and axiom inspection of the infrastructure theorem: pending.
- Skill and memory-template validation: pending.
- Impact analysis: `validate_registry` has two direct and one indirect consumer;
  `validate_proposal` and `render_claim_index` have no indexed upstream callers.
  Overall indexed risk is LOW, with repository scripts and tests still included
  manually because the graph omits some script-level calls.
- Final repository workflow: pending `scripts/validate_changed.py --base 7dfe89b`
  decision and one matching validation run.
- `git diff --check`: pending, separately from commit.

## Debt Ledger

The merge unit currently has no known unresolved debt.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |

## Results

Pending implementation.

## Canonicalization

No accepted claim, campaign, release, or accepted-memory record changes. Generated
claim documentation will be regenerated only if the renderer's backward-compatible
output changes. Workflow guidance, schema support, tooling, setup, and templates
will land together.

## Done Gate

This is a workflow implementation rather than a claim-promotion campaign. It is
done when every scope item in issue #90 exists, targeted negative/positive tests
and the final repository validation pass, Lean builds from the pinned scaffold,
and the PR is merged without modifying accepted scientific state.

## Cross-References

The canonical issue and accepted baseline anchor this effort.

- Canonical issue: https://github.com/vantasnerdan/substrate-framework/issues/90
- Branch: `process/theorem-synthesis-90`
- Base release: `governance/releases/current.yaml`
- Registry: `governance/claims.yaml`
