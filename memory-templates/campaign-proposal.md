# Campaign Proposal Template

Instantiate before a campaign computes or inspects comparator values. Use `theorem-synthesis.md` instead when the target is a fixed higher theorem composed from accepted claims. Store the prose contract in memory and create a matching `proposals/<id>/proposal.yaml` manifest. Run `PYTHONPATH=src .venv/bin/python scripts/validate_repository.py`, validate repository-local memory with `memory validate --base "$PWD" "$PWD/memory"`, and preserve any schema or memory failure before opening the source body or comparator values; a prose contract alone is not the freeze gate. The memory path is a required positional target; `--base` alone does not select it.

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

## Source Inventory and Access Gate
For campaigns whose objective is external literature (a paper, a theory, a dataset): enumerate every load-bearing external source with verified access status BEFORE preregistration — in hand (local path), open (URL), paywalled, or missing — and the exact claims and page/equation numbers extracted from each. An inaccessible primary source blocks the campaign objective as written: escalate to the requester with options (supply the document, restate the objective against the accessible corpus, substitute) before any computation. Auditing secondary literature about an unchecked primary is a defect (skill `quantitative-verification`, AP-14), not a partial result.

| Source | Access status | Extracted claims (with page/eq) |
| --- | --- | --- |

## Invariants, Conventions, and Allowed Imports
Freeze what the campaign must preserve and every input it may use. Accepted canon governs the base release but remains challengeable. Record evidence that would distinguish a candidate defect from an independent canonical inconsistency; anything added later becomes explicit debt and requires proposal revision.

## Candidate Preregistration
Register at least two plausible concepts when selecting among scientific mechanisms unless uniqueness is proved. If the statement is a fixed theorem, declare that target kind and use one complete proof route rather than inventing a competitor. Do not retrofit the framework after selecting a mechanism.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A |  |  |  |  |  |
| B |  |  |  |  |  |

## Selection Criteria and Blinding
Order the structural selection criteria and state the comparator-blinding point. Numerical agreement is evaluated only after structural selection freezes.

## Proposed Claim Delta
List claims proposed or challenged, their dependencies, evidence plan, and consumers. Before assigning a claim identifier, search the registry, campaigns, and durable memory; rejected or provisional identifiers remain reserved even when absent from the accepted registry. Do not use `supersedes` before acceptance.

## Implementation and Oracle Plan
Name importable APIs, claim-appropriate exact/numeric/formal oracles, applicable mutations and counterexamples, refinements, independent routes, and impact-bounded replay commands. A kernel-checked Lean proof calls for statement, import, proof-escape, axiom-footprint, and physical-encoding audits rather than a ceremonial mutation of the kernel. Campaign verifiers run directly with `PYTHONPATH=src`; import reusable package APIs rather than repository scripts, which remain CLI adapters. Pin the campaign's own source, claim, and release evidence, but never make future valid work fail by asserting unrelated queue units stay pending or mutable `current` remains the historical release; replay old campaigns through durable snapshots or their canonical modules/tests. For each replay inventory, record lexical check-call sites, runtime check executions, and assertion nodes separately; loops and dynamic dispatch can make the runtime tally differ legitimately, so equality is not an oracle. Predeclare a compatibility preflight: canonical integration uses `trapezoid_integral`, mutable current-environment scripts use `np.trapezoid`, and executable syntax is checked for direct, imported, and dynamic legacy access. An eager fallback such as `getattr(np, "trapezoid", getattr(np, "trapz"))` is legacy access because the default is evaluated first. Repair mutable code to the current name or a safe two-step fallback; give immutable source an alias-only recorded replay before scientific adjudication. Do not count that native compatibility abort as candidate rejection. State why SymPy, Lean, or a particular SciPy method fits each obligation. Do not plan a numerical rerun as independent evidence when an exact result already fixes its right-hand side or output; classify it as regression coverage and prefer exact sensitivity or Taylor separation for tractable counterexamples. Before labeling a downstream tail, dispersion, normalization, or consistency route independent, eliminate shared intermediate variables and compare the resulting equations or positive solution sets. For cross-sector matches, freeze distinct field types, kinetic metrics, action measures, and coefficient conversions; equal symbols, shapes, or dimensions are not maps. Structural oracles must evaluate the claimed object rather than a literal boolean, stand-in constant, copied period, or unrelated bounded sample. For differential forms, predeclare the full graded Leibniz/cyclic expansion and keep nonvanishing, closedness, global non-exactness, period normalization, filling dependence, and gauge descent as separate gates. For genuinely unresolved ODE/BVP/PDE or quadrature work, specify precision, equations, domain, initial/boundary data, discretization, mesh/time/sample refinement, tolerances, error norm, invariants or controlled dissipation, solver-status gate, and method cross-check. For FFT differentiation or spectral line claims, freeze the active frequencies and window, require commensurability or measured endpoint closure, distinguish an identity on one FFT coefficient from independent evidence, and predeclare the claimed line's minimum norm or power fraction. Express near-zero and agreement thresholds in a declared dimensional or scale-relative error model, and keep exact analytic nulls separate from numerical roundoff regressions.

## Attempts and Continuation
Append failed routes with diagnoses and next candidates. An ill-fitting concept is rejected or reformulated; unrelated earlier work is not rewritten to save it. If a conflict survives independently of the candidate, open a separate `challenges` or foundational-revision proposal rather than treating canon as irrevisable or silently changing it. Execution runs in declared waves whose inputs are explicit; research/grounding is wave 0 and a dependent wave (implementation, verification, report) opens only after every input its wave declares has settled — a research subagent's output is a hard prerequisite, never a race (AP-15).

## Debt Ledger
Track hidden assumptions, unexplained fitted parameters, unsupported promises,
convention conflicts, and broken affected consumers inside the proposed claim.
Declared hypotheses, honest exclusions, open candidate routes, and adjacent
repository observations are frontier rather than debt.

## Review and Promotion Plan
Name one claim-level review per proposed or changed claim, the frozen transaction,
package extraction, release update, generated documentation, and accepted-memory
synchronization. Classify changed attachments by evidence role; do not turn them
into additional claim reviews. Preserve the strongest meaningful positive
statement and use the minimum correction before rejecting it. Reserve
`refuted` for a contradiction or counterexample. For predecessor migration,
edit `migration/dispositions.yaml` and regenerate `migration/source-claims.yaml`;
never hand-edit the queue. Record one impact-selected validation receipt and
reuse it. After corrections, check only changed statements and affected edges.

## Done Gate
The campaign closes only on the complete positive success contract in `AGENTS.md`. If
a gate fails, state the next attempt and continue. Each next step is stated as its
positive contribution to resolution: name the object it constructs, the question it
closes, or the distinction it establishes, phrased as what becomes true in the record
when it succeeds. A refutation counts when stated through its mechanism — the test
distinguishes X from Y by observable O. Prohibitions and avoided failure modes do not
describe a step; if the statement reads entirely as avoidance or risk reduction, the
plan is not ready — find the move whose success advances the objective and state that.
```

Matching manifest:

```yaml
id: P000
base_release: <release-id>
source_baseline: <repository and immutable commit or release>
question: <exact question>
source_inventory:
  - source: <paper/dataset, author title year>
    access: <in-hand path | open URL | paywalled | missing>
    extracted: <claims/pages actually read, or escalation note>
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
