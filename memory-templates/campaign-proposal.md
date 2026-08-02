# Campaign Proposal Template

Instantiate before a campaign computes or inspects comparator values. Store the prose contract in memory and create a matching `proposals/<id>/proposal.yaml` manifest.

Begin every section with a plain-prose sentence. Inline code, a table, or a
list does not satisfy the memory index's first-content disclosure contract.

```md
---
description: <positive campaign objective>
author: <agent-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- campaign-proposal
category: proposals
confidence: exploratory
status: active
---

## Question and Positive Deliverable
State the exact question and object to derive. A no-go, failed concept, residual, or honest account of an obstruction does not complete this campaign.

## Base Release and Provenance
Record the accepted release and commit. Resolve inventory paths against the pinned source root, record both locations, and verify the source checkout commit and file hash before execution; a queue path need not be relative to the framework working directory. List source claims and modules actually read. For predecessor work, name each hash-pinned `migration/source-claims.yaml` unit and its current disposition; its bridge is the candidate unit while linked dossiers, formalizations, and legacy rungs are evidence rather than extra claims. Newer directories and working-tree prose are not authority.

## Invariants, Conventions, and Allowed Imports
Freeze what the campaign must preserve and every input it may use. Anything added later becomes explicit debt and requires proposal revision.

## Candidate Preregistration
Register at least two plausible concepts unless uniqueness is proved. Do not retrofit the framework after selecting one.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A |  |  |  |  |  |
| B |  |  |  |  |  |

## Selection Criteria and Blinding
Order the structural selection criteria and state the comparator-blinding point. Numerical agreement is evaluated only after structural selection freezes.

## Proposed Claim Delta
List claims proposed or challenged, their dependencies, evidence plan, and consumers. Do not use `supersedes` before acceptance.

## Implementation and Oracle Plan
Name importable APIs, claim-appropriate exact/numeric/formal oracles, mutations, counterexamples, refinements, independent routes, and global replay commands. Campaign verifiers run directly with `PYTHONPATH=src`; import reusable package APIs rather than repository scripts, which remain CLI adapters. Pin the campaign's own source, claim, and release evidence, but never make future valid work fail by asserting unrelated queue units stay pending or mutable `current` remains the historical release; replay old campaigns through durable snapshots or their canonical modules/tests. State why SymPy, Lean, or a particular SciPy method fits each obligation. Do not plan a numerical rerun as independent evidence when an exact result already fixes its right-hand side or output; classify it as regression coverage and prefer exact sensitivity or Taylor separation for tractable counterexamples. Structural oracles must evaluate the claimed object rather than a literal boolean, stand-in constant, copied period, or unrelated bounded sample. For differential forms, predeclare the full graded Leibniz/cyclic expansion and keep nonvanishing, closedness, global non-exactness, period normalization, filling dependence, and gauge descent as separate gates. For genuinely unresolved ODE/BVP/PDE or quadrature work, specify precision, equations, domain, initial/boundary data, discretization, mesh/time/sample refinement, tolerances, error norm, invariants or controlled dissipation, solver-status gate, and method cross-check. For FFT differentiation or spectral line claims, freeze the active frequencies and window, require commensurability or measured endpoint closure, distinguish an identity on one FFT coefficient from independent evidence, and predeclare the claimed line's minimum norm or power fraction. Express near-zero and agreement thresholds in a declared dimensional or scale-relative error model, and keep exact analytic nulls separate from numerical roundoff regressions.

## Attempts and Continuation
Append failed routes with diagnoses and next candidates. An ill-fitting concept is rejected or reformulated; unrelated earlier work is not rewritten to save it.

## Debt Ledger
Describe what this campaign's ledger tracks, then list new assumptions,
imports, parameters, residuals, convention conflicts, and broken consumers.
The campaign remains active until the ledger is empty.

## Review and Promotion Plan
Name claim-level reviewers, acceptance gates, package extraction, release update, generated documentation, and accepted-memory synchronization. State the resulting source-unit disposition; a partial migration must preserve its exact remaining subclaims. Terminal `qualified`, `refuted`, `duplicate_evidence`, and `out_of_scope` decisions must name their disposition-specific reason and durable evidence paths; use `qualified` for mixed units that also map accepted claims.

## Done Gate
The campaign closes only on the complete positive success contract in `AGENTS.md`. If any gate fails, state the next attempt and continue.
```

Matching manifest:

```yaml
id: P000
base_release: <release-id>
source_baseline: <repository and immutable commit or release>
question: <exact question>
invariants:
  - <accepted invariant>
allowed_imports:
  - <claim id or external source>
candidates:
  - id: A
    description: <candidate concept>
  - id: B
    description: <candidate concept>
uniqueness_evidence: null
selection_criteria:
  - framework invariant compatibility
  - assumption and parameter economy
  - correct limits and cross-sector composition
claims_proposed:
  - <claim id>
comparators_blinded_until: <artifact or gate>
status: draft
```
