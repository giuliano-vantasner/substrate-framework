---
description: Migrate the committed Substrate corpus into a self-consistent accepted framework release
author: vantasner
created: '2026-08-01T10:31:34Z'
updated: '2026-08-01T11:15:03Z'
tags:
- substrate-framework
- effort
- corpus-migration
category: efforts
confidence: working
status: active
---
# Substrate Corpus Migration

## Goal and Success Contract
This effort delivers a reproducible accepted release whose individually reviewed claims reconstruct the scientifically supportable content of the predecessor Substrate corpus as importable, tested framework APIs.

Completion requires the positive framework object itself: every in-scope source claim is inventoried and adjudicated; every accepted claim has closed dependencies, declared imports, natural framework fit, a claim-appropriate sensitive verifier, downstream replay, importable implementation, synchronized registry/release/docs/memory, and no unresolved debt. Failed or rejected source claims remain attempt or campaign evidence and do not count as completion.

## Accepted Baseline
The effort began from the null release at framework commit `6220237`: at that commit `governance/releases/current.yaml` had `release: null`, and `governance/claims.yaml` contained no claims.

The predecessor evidence baseline is `/home/dan/substrate` commit `6d1f4e0`, which is also its recorded `origin/main` at effort start. The predecessor worktree is dirty with later Phase 47/48 and memory artifacts; those uncommitted files are excluded from the source baseline unless admitted later through a separately recorded source-baseline revision. A source commit supplies provenance and candidate evidence, never authority.

The current accepted frontier is `v0.3.0`, containing dependency-root claims `C-SG-001/002`, exact action claim `C-SG-003`, and exact averaged squared-gradient claim `C-SG-004`. The null release remains the recorded start state, not the current authority.

## Constraints and Invariants
The migration preserves chronology as provenance only, immutable adjudicated campaigns, claim-level rather than campaign-level acceptance, four independent status axes, generated canonical documentation, append-only failed attempts, and exact separation of derivation inputs from empirical comparators.

No legacy declaration, pass tally, Lean theorem, fitted number, or late synthesis sentence is accepted without auditing its exact statement, assumptions, physical interpretation, and dependency closure. No existing framework invariant may be revised to rescue a candidate. Only the user may reduce the corpus objective.

The write boundary is `/home/dan/substrate-framework`; the predecessor repository is read-only evidence. Delegation is not authorized for this effort.

## Candidate Migration Strategies
The strategy choice is frozen before inspecting empirical comparator values.

| Candidate | Construction | Assumption cost | Expected advantage | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A | Reconstruct a dependency DAG from minimal mathematical and physical roots, then promote claims in topological order | Requires explicit source inventory and new canonical APIs | Maximizes dependency honesty and exposes hidden imports early | No stable root set or dependency order can be recovered from source artifacts | preregistered |
| B | Migrate the predecessor's late `merged-framework` sector summaries as bounded claim batches, then audit and backfill their cited dependencies | Treats late synthesis organization as a navigation aid | Preserves existing sector grouping and may accelerate consumer discovery | A batch relies on undeclared, cyclic, contradicted, or non-importable prerequisites | preregistered |
| C | Start from independently reproducible verifier artifacts, promote the narrow predicates they actually establish, then connect them into a claim graph | Risks privileging easy-to-test claims over explanatory roots | Quickly separates executable evidence from narrative overclaim | Verifiers are tautological, insensitive, or lack interpretable physical claims | preregistered |

## Selection Criteria and Comparator Gate
Candidate strategies are ranked by accepted-dependency closure, assumption and parameter economy, preservation of conventions and invariants, ability to expose contradictions, reusable API fit, downstream reach, and verifier sensitivity. Empirical agreement is excluded from strategy and concept selection. Comparator values may be inspected only inside a claim proposal after its equations, conventions, structural criteria, and pass thresholds are frozen.

## Decomposition
Work proceeds dependency-first and continues after failed source claims.

1. [x] Establish framework authority, predecessor commit boundary, git state, tool availability, and memory state.
2. [ ] Complete the source claim and dependency inventory from commit `6d1f4e0`; the hash-locked role/bridge inventory is generated, while exact claim decomposition remains active.
3. [x] Freeze and adjudicate the first claim ladder and matching P001 campaign proposal.
4. [x] Implement the first selected construction through importable APIs.
5. [x] Audit the first exact claims and their mutation sensitivity.
6. [x] Independently review, replay, and promote the first dependency-root release.
7. [ ] Repeat until every in-scope source claim is accepted, qualified, superseded, or refuted with the positive framework objective still satisfied and the debt ledger empty.

## Attempts
Attempts are append-only and individually reproducible.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Phase-0 authority and workflow preflight | `.agents/skills/physics-erdos-loop/scripts/preflight.sh` plus git, registry, memory, and source checks | passed | Established a null accepted boundary and a clean framework tree; detected an uninstantiable memory category contract | Repair memory-category validation, then inventory the pinned source commit |
| 0002 | Candidate A, direct exact sine-Gordon root | `campaigns/P001-sine-gordon-root` and its exact/independent verifiers | accepted in v0.1.0 | Full residual, two energy derivations, mutations, limits, and successor replay passed | Extend the source inventory into the next dependency-ordered claim proposal |
| 0003 | Initial full promotion replay | `scripts/validate.sh` | failed before terminal tally | Generated C-SG-002 review memory began one section with inline code, violating the memory index's plain-prose disclosure contract; suppressed validator output initially hid the diagnosis | Repair the section description and expose memory validation output in the workflow script, then rerun the unchanged full boundary |
| 0004 | Candidate A, exact breather action with Candidate B review | `campaigns/P002-sine-gordon-action` exact and field phase-space verifiers | accepted in v0.2.0 | Endpoint-fixed exact calculus passed 19 checks; the independent phase-space construction passed 19 checks with precision refinement and a normalization mutation | Derive the nearest accepted-root functional consumer without importing its predecessor conclusion |
| 0005 | P003 attempt 0001, implicit inverse-width limits | `campaigns/P003-sine-gordon-gradient/attempts/0001` | failed | SymPy could not infer positivity of `sqrt(1-omega^2)` inside the spatial limit oracle | Preserve the failure and expose the accepted positive inverse width explicitly only for localization checks |
| 0006 | P003 attempt 0002, virial and direct-field routes | `campaigns/P003-sine-gordon-gradient` | accepted in v0.3.0 | Exact virial closure passed 25 checks; an independent field integral passed 16 checks and rejected the half-factor convention | Return to claim inventory and identify the next dependency-closed sector root |

## Validation
Validation targets scientific predicates and dependency closure, with workflow checks used only where they protect a real boundary.

- Targeted scientific command and oracle: recorded per claim proposal.
- Mutation and counterexample command: recorded per claim proposal.
- Numerical refinement and independent route: required only for claims whose oracle is numerical or simulation-based.
- Dependency replay: generated from each claim delta and consumer map.
- Repository validation: run at promotion boundaries and after changes to validation logic, not after every prose update.
- `scripts/validate.sh` includes the full test suite and runs once at an unchanged promotion boundary; `git diff --check` remains separate.

## Debt Ledger
Every row must be discharged before the parent effort can close.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| D1: no predecessor claim registry | Sequential source corpus | Source chronology and synthesis prose do not provide an authoritative dependency graph | Generated, source-cited inventory and reviewed proposal manifests | open |
| D2: no accepted framework roots | Intentional null release | No scientific claim can yet serve as an accepted dependency | `v0.1.0` with C-SG-001 and C-SG-002 | discharged |
| D3: dirty predecessor worktree | Ongoing Phase 47/48 work | Uncommitted artifacts cannot define the reproducible source baseline | Isolated snapshot inventory with tree SHA-256 `fa5366af628363d71bf91f219ac203c8009bca3a80f3de532c022e14e1b7e001` | discharged |
| D4: migration scope inventory incomplete | Corpus size and mixed artifact roles | Completion cannot be measured until claims, attempts, engineering layers, and narrative consumers are classified | Full corpus inventory with explicit in-scope categories and exclusions | open |

## Results
The authority boundary and source commit are fixed. The memory-template category mismatch and relative validation-path hazard were corrected at their shared contract surfaces. P001 produced the exact normalized sine-Gordon breather and energy APIs in `v0.1.0`. P002 added the exact canonical action and energy-action inversion in `v0.2.0`, while explicitly withholding every literature-dependent quantization conclusion. P003 added the exact averaged squared-gradient integral and its virial-Legendre identity in `v0.3.0`, while preserving the full-versus-half factor convention.

## Canonicalization
The registry, `v0.3.0` manifest, current release, generated claim index, and generated framework memory agree on `C-SG-001/002/003/004`. P001 through P003 are frozen under `campaigns/`; proposal, attempt, review-work, and effort memory remain distinct from accepted-state memory.

## Done Gate
The effort remains active. The exact breather mechanics ladder is complete through its averaged gradient functional, but D1 and D4 remain open and the broader predecessor corpus is still a migration backlog. The next executable action is to complete the measurable claim-scope inventory and select the next dependency-closed sector root rather than treating `v0.3.0` as whole-corpus completion.

## Cross-References
The governing sources are `AGENTS.md`, `.agents/skills/physics-erdos-loop/SKILL.md`, `governance/claims.yaml`, `governance/releases/current.yaml`, and the proposal and claim-review contracts under `memory-templates/`.
