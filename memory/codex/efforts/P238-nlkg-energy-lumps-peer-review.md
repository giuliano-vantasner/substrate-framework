---
description: Claim-by-claim peer review and machine validation of the 2+1D NLKG energy-lumps effective-metric paper
author: codex
created: '2026-08-19T20:08:36+00:00'
updated: '2026-08-19T20:45:30+00:00'
tags:
- substrate-framework
- research-arc
- nlkg
- effective-metric
- peer-review
category: efforts
confidence: exploratory
status: active
---

## Positive Objective and Success
This effort performs a full peer review of
`2026-08-19_NLKG_2plus1D_energy_lumps_effective_metric_v0.1.pdf`. It will
extract every substantive mathematical, numerical, and physical claim; create
one canonical GitHub issue per unique claim; apply the strongest practical
SymPy, Lean, or SciPy oracle claim by claim; and submit a pull request containing
the review, executable evidence, unique claim artifacts, and all in-boundary
debt repairs. Success requires traceable source locations, explicit assumptions,
independent reproduction rather than output matching, claim-level dispositions,
an empty in-boundary debt ledger, impact-bounded replay, and a final summary on
canonical issue #108.

## Authority and Prior Work
The accepted baseline is release `v0.163.0` on exact worktree base
`f00d11b0fca02fd5ac27c80b0d00d8b7f5de8853`. The current release manifest and
`governance/claims.yaml` are authority; the paper and its issue are source
objects under audit. Repository memory searches for `NLKG effective metric
energy lumps peer review` found effective-metric precedents, especially
`C-GOR-001`, but no prior record for this paper. GitNexus then located the
effective-metric, einbein, and NLKG/oscillon implementation surfaces before the
source was adjudicated. Exact registry inspection found that P238-S09 duplicates
`C-WLN-001` through `C-WLN-003`; `C-GOR-001` and `C-PDE-001` define important
interpretive ceilings rather than dependencies.

- Accepted release: `v0.163.0`
- Accepted claims reused: C-WLN-001 through C-WLN-003 as nonpromotion comparators
- Source modules read: `gordon_metric.py`, `substrate_metric.py`, `pseudo_riemannian.py`, `relativistic_particle.py`; P044/P227 evidence and tests
- Memory searches: `paper peer review claim extraction validation`; `NLKG effective metric energy lumps peer review`
- Campaign evidence: P237 workflow shape and P229 paper-audit proposal shape only
- Genuine unresolved objective: none inside the frozen review boundary; PR publication and landing remain operational next steps

## Definitions and Invariants
Before the PDF body is opened, the review freezes the distinction between exact
identity, derived conditional result, numerical observation, fitted comparison,
and physical interpretation. Every claim must carry its source page and equation
or figure, variables, domain, units, signature, coordinate dimension,
normalization, initial or boundary conditions, regularity assumptions, and
known limits. For numerical work, precision, discretization, domain truncation,
stability condition, tolerances, refinement ladder, and error norm will be
frozen before published comparison values influence adjudication.

## Permitted Imports and Assumptions
Permitted tools are the repository environment, SymPy for exact symbolic
obligations, SciPy and repository numerical helpers for genuinely numerical
obligations, and Lean installed through the repository setup for suitable finite
theorems. Accepted claims and modules may be used only after exact dependency
and convention checks. The issue-108 PDF is evidence, not authority. No
unstated physical closure, effective-medium interpretation, numerical boundary
condition, observed value, or fitted parameter may enter as a hidden premise.

## Candidate Set
The fixed peer-review objective uses complementary independent routes because
the title signals exact, numerical, and interpretive layers that require
different falsifiers.

| Candidate | Construction | New objects/parameters | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A | Symbolic-first clean-room derivation and limit audit | Only variables and assumptions declared by each extracted claim | Actions, field equations, tensors, conservation laws, effective metrics, exact limits | Sign, dimension, derivative, symmetry, domain, or mutation failure | complete: 26/26 predicates |
| B | Independent SciPy reproduction with refinement and alternate or soluble cross-check | Declared mesh, domain, tolerances, initial/boundary data, and error metric | Directional gaps, inverse residuals, exterior domains, roots, and Kerr coefficient differences | Method disagreement or threshold failure | complete: 12/12 probes |
| C | Lean formalization of tractable exact propositions | Explicit types, hypotheses, definitions, and imported lemmas | Finite exact identities and rational counterexamples | False theorem or missing hypothesis | complete: 10/10 theorems |

## Selection Criteria and Comparator Gate
Selection is ordered by exact claim-oracle fit, dependency closure, invariant
compatibility, dimensions/signs/symmetries/limits, mutation sensitivity,
numerical convergence and independent cross-check, nonduplication, maintenance
cost, and only then agreement with published values. The PDF body and comparator
values remain unopened until the proposal and this contract validate. After
source extraction, each claim's statement, assumptions, oracle, and threshold
will be frozen before a published number or plot is used for comparison.

## Claim Delta
Eighteen source units were frozen as P238-S01 through P238-S18 and mapped to
GitHub issues #127 through #144. Five bounded statements pass, four require
qualification, and nine fail. No accepted-registry delta is proposed: exact
einbein content is duplicate and the other survivors remain conditional
proposal evidence.

| Claim id | Exact statement | Dependencies | Relationship | Oracle | Consumers |
| --- | --- | --- | --- | --- | --- |
| P238-S01–S18 | Exact statements in `evidence/claim-inventory.yaml` | Source digest plus per-unit dependency closure | 5 pass, 4 qualified, 9 fail; no registry promotion | SymPy, SciPy, Lean, literature and dependency audit | issue #108 and claim issues #127–#144 |

## Frozen Review Transaction
The transaction contains the issue-108 PDF at its recorded digest, P238 proposal
and effort records, the complete claim inventory, one issue per unique claim,
claim-appropriate executable evidence, peer-review prose, necessary clean
package APIs, focused tests, claim-review records for any proposed registry
entry, debt repairs introduced or exposed inside this scope, and the final PR.
Accepted releases and unrelated campaigns remain unchanged unless a separate
claim review earns promotion. The base is
`f00d11b0fca02fd5ac27c80b0d00d8b7f5de8853`; the final head/tree and validation
receipt are frozen immediately before commit and PR publication.

## Claim Ladder
The dependency ladder begins with source fidelity and definitions, proceeds
through exact derivations, then numerical evidence, and reaches physical
interpretation only after its bridges survive.

| Step | Claim | Oracle | Sensitivity/counterexample | Prerequisites | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Complete unique claim inventory with exact source anchors | PDF extraction plus manual source audit | omitted/duplicated claim and source-anchor check | validated proposal and source digest | complete: 18 units |
| 2 | Definitions, conventions, and exact mathematical claims | SymPy or Lean as claim-appropriate | sign, factor, domain, assumption, and limit mutations | step 1 | complete |
| 3 | Numerical profiles and observables | SciPy exact-limit and domain probes | tolerance, domain, matrix and root checks | steps 1-2 | complete |
| 4 | Effective-metric and physical interpretations | dependency graph plus exact/numeric bridge audit | counterexamples with the same local mathematics but absent bridge | steps 1-3 | complete |

## Importable Implementation
No package API or accepted claim is warranted by this source audit. The
importable deliverable is instead the portable, standalone companion corpus:
`sympy_checks.py`, `scipy_checks.py`, `P238PaperChecks.lean`, pinned Python
requirements, Lean toolchain/lake files, and a README. `verify.py` composes the
oracles with exact inventory, issue, terminal-disposition, count, and zero-debt
checks without treating counterexample success as paper-claim acceptance.

## Harvest Checkpoints
The canonical goal is GitHub issue #108. All scientific obligations are now
terminal and the PR may use `Fixes #108` plus `Closes #127` through `#144` once
the final validation receipt passes.

- Canonical goal issue: https://github.com/vantasnerdan/substrate-framework/issues/108
- PR issue reference: `Advances #108` while review is active
- Source PR lifecycle: PR #145 open at validated head; required-review branch gate remains
- Refactor owner/handoff, live PR, and landing test: codex; no package refactor required; PR is mergeable with no reported CI checks
- Terminal-close evidence: 18 resolved dispositions, zero open debt, final validation receipt pending
- Final issue handoff: required after all claim dispositions and PR results

| Unit | Local claim | Independent of headline? | Evidence | Commit/PR | Disposition |
| --- | --- | --- | --- | --- | --- |
| Source and claim inventory | Every substantive unique statement has a source anchor | yes | source provenance and 18-unit inventory | PR #145 | complete |
| Exact/numerical/formal corpus | Independent predicates cover all machine-checkable load-bearing statements | yes | 26 SymPy, 12 SciPy, 10 Lean | PR #145 | complete |
| Peer-review disposition | Every issue has one terminal finding and correction | yes | claim results and peer review | PR #145 | complete |

## Attempts
The append-only ledger records the complete sequence from source acquisition
through terminal adjudication without rewriting the early gate states.

| Attempt | Candidate/method | Artifact | Verdict | Diagnosed layer | Next materially different route |
| --- | --- | --- | --- | --- | --- |
| 0001 | Trusted email `faaaaabi` source acquisition | agent-mail body/structure query | request received but no attachment or paper link existed | operational source provenance | request source and establish canonical issue |
| 0002 | Canonical issue inspection | GitHub issue #108 | authoritative PDF attachment located; body remains unopened | source gate ready | validate P238 manifest and contract, hash source, then extract claims |
| 0003 | Source extraction and claim freeze | source provenance plus claim inventory | 17 pages and 18 unique units frozen with issues #127–#144 | source/claim boundary | assign claim-specific oracles |
| 0004 | Symbolic, numerical, and formal reconstruction | portable companion corpus | 26/26 SymPy, 12/12 SciPy, 10/10 Lean predicates pass | adjudication complete | audit literature and dependencies |
| 0005 | Primary-source and framework-fit audit | literature audit, claim results, peer review | 5 pass, 4 qualified, 9 fail; no accepted claim delta | terminal review | final repository gate and PR |

## Framework-Fit Audit
Framework fit is complete. C-WLN-001–003 make S09 duplicate; C-GOR-001 supports
only a conditional wave metric and explicitly excludes material gravity; and
C-PDE-001 demonstrates the repository's existing finite-time oscillon evidence
ceiling. No finding contradicts accepted canon and no accepted claim is changed.

## Verifier Audit
The verifier assignment completed as frozen: 26 exact SymPy predicates, 12
independent SciPy matrix/domain/root probes, and 10 Lean theorems cover the
machine-checkable obligations. Literature and dependency conclusions remain
explicit prose audits rather than counterfeit numeric proofs. `verify.py`
requires all 18 issue links, terminal dispositions, exact counts, and an empty
debt ledger in addition to the executable oracles.

## Impact-Bounded Dependency Replay
The initial transaction changes only proposal and effort records, so no physics
consumer is yet affected. GitNexus will index the exact worktree before source
adjudication; after the claim delta and implementation paths are known, it will
name only affected symbols/processes and their scoped replay commands.

| Consumer | Why affected | Command or proof | Result | Repair if needed |
| --- | --- | --- | --- | --- |
| accepted effective-metric code and C-GOR | semantic overlap only; no code change | GitNexus schema/query plus direct registry audit | no affected consumer | none |
| accepted einbein code and C-WLN | S09 duplicates existing exact claims | GitNexus query and accepted-claim replay | no implementation delta | none |
| P044/C-PDE-001 | establishes oscillon evidence ceiling | direct campaign/claim audit | no contradiction or consumer change | none |

## Foundational Revision Gate
No accepted foundational inconsistency has been observed. This gate remains
closed unless independently reproduced evidence from a paper claim contradicts
accepted canon after convention and dependency checks.

## Debt Ledger
All in-boundary debt is discharged. Repository setup installed the pinned Lean
4.28.0/mathlib environment and the repository Python environment; the final
preflight reports seven checks passing and zero warnings. False or unsupported
paper claims have terminal rejected/qualified dispositions and are not hidden
as future review debt.

| Debt | Source | Effect | Discharge | Status |
| --- | --- | --- | --- | --- |
| Lean/Lake unavailable | initial repo preflight | formal oracle route C unavailable | repository setup plus Lean build and clean preflight | discharged |
| Review coverage and issue closure | issue #108 request | partial review would leave hidden debt | 18-unit inventory, terminal results, closing PR references | discharged |

## Independent Claim Review
No accepted statement changes and no registry claim is proposed, so no
`claim-review.md` promotion transaction is required. Every rejected, qualified,
passing-conditional, or duplicate source unit instead has a terminal issue-level
disposition and executable evidence without being misrepresented as promoted.

## Results and Continuation
The strongest result is a complete negative/qualified dependency audit rather
than a promoted headline claim. Exact wave geometry survives in bounded form,
but the real-field existence theorem, square-root collective-coordinate bridge,
covariant inverse, and Kerr reconstruction do not. The reusable outcome is a
portable companion corpus and a correction-complete review. PR #145 is live;
all claim issues carry terminal comments and closing references, canonical
issue #108 has ongoing discussion, and final results were emailed to Dan as
message `fmaaaabl`. The only next action is the repository's normal external
review/landing gate.

## Promotion and Materialization
No promotion has occurred. P238 materializes source provenance, the 18-unit
inventory/results, primary-source audit, full peer review, portable SymPy/SciPy/
Lean sources, a composed verifier, GitNexus impact record, and validation
receipt. Registry and release files remain unchanged by design.

## Done Gate
Done is earned for the requested review-and-PR transaction: every source unit is anchored, independently tested
where machine-checkable, assigned a terminal disposition/correction, and mapped
to a claim issue; all in-boundary debt is discharged; PR #145 publishes the
work with closing references; each claim issue and #108 has discussion; and Dan
received the final email. Merge requires the repository's independent-review
gate and was not part of the requested action.

## Cross-References
Canonical issue: https://github.com/vantasnerdan/substrate-framework/issues/108

Pull request: https://github.com/vantasnerdan/substrate-framework/pull/145

Source attachment: https://github.com/user-attachments/files/31238673/2026-08-19_NLKG_2plus1D_energy_lumps_effective_metric_v0.1.pdf

Proposal: `proposals/P238-nlkg-energy-lumps-peer-review/proposal.yaml`

Exact base: `f00d11b0fca02fd5ac27c80b0d00d8b7f5de8853`
