---
description: Claim-by-claim peer review and machine validation of the 2+1D NLKG energy-lumps effective-metric paper
author: codex
created: '2026-08-19T20:08:36+00:00'
updated: '2026-08-19T22:11:31+00:00'
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
The repository workflow baseline is release `v0.163.0` on exact worktree base
`f00d11b0fca02fd5ac27c80b0d00d8b7f5de8853`. The manuscript is the scientific
object under audit, and each frozen statement is judged only against the
manuscript's own definitions, equations, assumptions, and cited dependencies.
Repository memory and GitNexus searches located relevant implementation
surfaces solely to bound PR impact; no Substrate claim, code path, or narrative
is a scientific premise or comparator.

- Accepted release: `v0.163.0`
- Accepted claims reused: none
- Repository modules queried by GitNexus: impact-only; excluded from paper adjudication
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
obligations, SciPy for genuinely numerical obligations, and Lean installed
through the repository setup for suitable finite theorems. Repository claims
and implementations are excluded as scientific premises and comparators. The
issue-108 PDF supplies the statements under test, not proof of them. No
unstated physical closure, effective-medium interpretation, numerical boundary
condition, observed value, or fitted parameter may enter as a hidden premise.

## Candidate Set
The fixed peer-review objective uses complementary independent routes because
the title signals exact, numerical, and interpretive layers that require
different falsifiers.

| Candidate | Construction | New objects/parameters | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A | Symbolic-first clean-room derivation and limit audit | Only variables and assumptions declared by each extracted claim | Actions, field equations, tensors, conservation laws, effective metrics, exact limits | Sign, dimension, derivative, symmetry, domain, or mutation failure | complete: 29/29 predicates |
| B | Independent SciPy reproduction with refinement and alternate or soluble cross-check | Declared mesh, domain, tolerances, initial/boundary data, and error metric | Directional gaps, inverse residuals, exterior domains, roots, and Kerr coefficient differences | Method disagreement or threshold failure | complete: 12/12 probes |
| C | Lean formalization of tractable exact propositions | Explicit types, hypotheses, definitions, and imported lemmas | Finite exact identities and rational counterexamples | False theorem or missing hypothesis | complete: 11/11 theorems |

## Selection Criteria and Comparator Gate
Selection is ordered by exact claim-oracle fit, dependency closure, invariant
compatibility, dimensions/signs/symmetries/limits, mutation sensitivity,
numerical convergence and independent cross-check, claim independence, maintenance
cost, and only then agreement with published values. The PDF body and comparator
values remain unopened until the proposal and this contract validate. After
source extraction, each claim's statement, assumptions, oracle, and threshold
will be frozen before a published number or plot is used for comparison.

## Claim Delta
Eighteen source units were frozen as P238-S01 through P238-S18 and mapped to
canonical GitHub issues #109 through #126. Five bounded statements are
supported as written and thirteen need revision with supplied repair paths.
Issues #127 through #144 were an accidental retry set and are closed as
duplicates rather than treated as additional scientific claims.

| Claim id | Exact statement | Dependencies | Relationship | Oracle | Consumers |
| --- | --- | --- | --- | --- | --- |
| P238-S01–S18 | Exact statements in `evidence/claim-inventory.yaml` | Source digest plus per-unit dependency closure | 5 supported, 13 revision-required, each with a repair | SymPy, SciPy, Lean, literature and dependency audit | issue #108 and canonical claim issues #109–#126 |

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
The importable deliverable is the portable, standalone companion corpus:
audit files `sympy_checks.py`, `scipy_checks.py`, and
`P238PaperChecks.lean`; constructive replacements `sympy_replacements.py`,
`scipy_replacements.py`, and `P238ReplacementProofs.lean`; pinned environments;
an author-ready repair guide; and `evidence/solution-reuse-audit.yaml`, which
records the exact source-to-replacement transformations. All 13 revision findings map to executable
replacement records, including the scoped action, real-lump trajectory,
`O(ell/L)` gradient estimate, conditional worldline observables, exact Kerr
roots, and composed repaired headline. `verify.py` composes the oracles with exact
inventory, canonical-issue, review-completeness, replacement, and zero-debt
checks.

## Harvest Checkpoints
The canonical goal is GitHub issue #108. All peer-review obligations are now
addressed and the PR may use `Fixes #108` plus `Closes #109` through `#126` once
the final validation receipt passes.

- Canonical goal issue: https://github.com/vantasnerdan/substrate-framework/issues/108
- PR issue reference: `Advances #108` while review is active
- Source PR lifecycle: PR #145 open at validated head; required-review branch gate remains
- Refactor owner/handoff, live PR, and landing test: codex; no package refactor required; PR is mergeable with no reported CI checks
- Review-complete evidence: 18 assessments with repair paths, zero open review debt, corrected validation receipt pending
- Final issue handoff: required after all claim dispositions and PR results

| Unit | Local claim | Independent of headline? | Evidence | Commit/PR | Disposition |
| --- | --- | --- | --- | --- | --- |
| Source and claim inventory | Every substantive unique statement has a source anchor | yes | source provenance and 18-unit inventory | PR #145 | complete |
| Exact/numerical/formal corpus | Independent predicates cover all machine-checkable load-bearing statements | yes | 29 SymPy, 12 SciPy, 11 Lean | PR #145 | complete |
| Peer-review disposition | Every issue has one manuscript-internal assessment and repair path | yes | claim results, replacements, and peer review | PR #145 | complete |

## Attempts
The append-only ledger records the complete sequence from source acquisition
through manuscript-internal review and constructive repair without rewriting the early workflow states.

| Attempt | Candidate/method | Artifact | Verdict | Diagnosed layer | Next materially different route |
| --- | --- | --- | --- | --- | --- |
| 0001 | Trusted email `faaaaabi` source acquisition | agent-mail body/structure query | request received but no attachment or paper link existed | operational source provenance | request source and establish canonical issue |
| 0002 | Canonical issue inspection | GitHub issue #108 | authoritative PDF attachment located; body remains unopened | source gate ready | validate P238 manifest and contract, hash source, then extract claims |
| 0003 | Source extraction and claim freeze | source provenance plus claim inventory | 17 pages and 18 unique units frozen; #109–#126 are canonical and retry-created #127–#144 are duplicate workflow debt | source/claim boundary | assign claim-specific oracles and close duplicate set |
| 0004 | Symbolic, numerical, and formal reconstruction | portable companion corpus | 29/29 SymPy, 12/12 SciPy, 11/11 Lean audit predicates pass | adjudication complete | audit literature and dependencies |
| 0005 | Manuscript-internal primary-source audit | literature audit, claim results, peer review | 5 supported and 13 revision-required against the paper's own claims | review complete | construct repairs |
| 0006 | Constructive repair pass | replacement SymPy/SciPy/Lean files and repair guide | 12 SymPy replacement records, two SciPy claim solutions in one refined dual-integrator program, and 9 Lean replacement theorems pass; every revision finding has executable coverage | author-ready correction | update canonical issues and PR |

## Framework-Fit Audit
Framework fit is intentionally not a scientific question in P238. This required
template section records the boundary: Substrate provides the workflow,
execution environment, issue tracking, and PR destination only. All claim
verdicts use the manuscript's own definitions, equations, assumptions, and
cited dependencies. S09 was independently rederived rather than replayed from
a repository claim.

## Verifier Audit
The verifier assignment completed as frozen: 29 exact SymPy predicates, 12
independent SciPy matrix/domain/root probes, and 11 Lean theorems cover the
machine-checkable obligations. Literature and dependency conclusions remain
explicit prose audits rather than counterfeit numeric proofs. Twelve SymPy
replacement records, two SciPy claim solutions, and nine Lean replacement
theorems supply executable coverage for all 13 claims that need revision.
`verify.py`
requires all 18 canonical issue links, complete assessments, exact counts, an
empty debt ledger, and passing constructive replacements in addition to the
audit oracles.

## Impact-Bounded Dependency Replay
The initial transaction changes only proposal and effort records, so no physics
consumer is yet affected. GitNexus will index the exact worktree before source
adjudication; after the claim delta and implementation paths are known, it will
name only affected symbols/processes and their scoped replay commands.

| Consumer | Why affected | Command or proof | Result | Repair if needed |
| --- | --- | --- | --- | --- |
| existing effective-metric code | operational change-impact check only | GitNexus detect-changes | no affected consumer | none |
| existing einbein code | operational change-impact check only; excluded from S09 proof | GitNexus detect-changes | no affected consumer | none |
| existing NLKG/oscillon code | operational change-impact check only; excluded from S06 proof | GitNexus detect-changes | no affected consumer | none |

## Foundational Revision Gate
The foundational-revision gate is not invoked because P238 does not compare the
paper to accepted Substrate canon. Any future import or promotion would require
a separate transaction after this manuscript-internal review.

## Debt Ledger
All in-boundary debt is discharged. Repository setup installed the pinned Lean
4.28.0/mathlib environment and the repository Python environment; the final
preflight reports seven checks passing and zero warnings. False or unsupported
paper claims that need revision have explicit language, algebra, numerical, or
derivational repairs and are not hidden as future review debt.

| Debt | Source | Effect | Discharge | Status |
| --- | --- | --- | --- | --- |
| Lean/Lake unavailable | initial repo preflight | formal oracle route C unavailable | repository setup plus Lean build and clean preflight | discharged |
| Review coverage and issue closure | issue #108 request | partial review would leave hidden debt | 18-unit inventory, complete assessments, replacements, closing PR references | discharged |

## Independent Claim Review
No repository statement changes and no registry claim is proposed, so no
`claim-review.md` promotion transaction is required. That administrative fact
does not enter any scientific verdict; all 18 source units have complete
manuscript-internal assessments, repair language, and executable evidence.

## Results and Continuation
The strongest result is a complete manuscript-internal review plus constructive
repair. Exact wave geometry is supported; scoped numerical real-lump evidence,
an explicit `O(ell/L)` frozen-background estimate, a conditional boosted-family
square-root derivation, corrected clock/ruler/geodesic relations, the corrected
covariant inverse, exact Kerr null roots, and an exact conformal equatorial Kerr
map are supplied as replacement files. The repaired headline is a complete
conditional analogue-kinematics statement, not an unresolved promise. PR #145 is live;
all canonical claim issues carry review comments and closing references, canonical
issue #108 has ongoing discussion, and final results were emailed to Dan as
message `fmaaaabl`. The only next action is the repository's normal external
review/landing gate.

## Promotion and Materialization
No promotion is in scope. P238 materializes source provenance, the 18-unit
inventory/results, primary-source audit, full peer review, portable SymPy/SciPy/
Lean sources, a composed verifier, GitNexus impact record, and validation
receipt. Registry and release files remain unchanged by design.

## Done Gate
Done is earned for the requested review-and-PR transaction: every source unit is anchored, independently tested
where machine-checkable, assigned an assessment and constructive repair, and mapped
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
