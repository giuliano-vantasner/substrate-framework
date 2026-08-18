---
description: Corrected single-transaction ingestion and promotion of the historical Lean corpus
author: codex
created: '2026-08-18T23:10:00+02:00'
updated: '2026-08-18T23:10:00+02:00'
tags:
- substrate-framework
- research-arc
- lean
- claim-promotion
category: efforts
confidence: exploratory
status: active
---

## Positive Objective and Success
The positive objective is the complete issue #92 merge unit: ingest the 60 claim-bearing Lean files from the surveyed 170-file historical source with exact provenance, classify every ingested theorem, attach only theorem-relevant and independently reviewed Lean evidence to accepted claims, promote every genuine new fixed theorem at its exact encoded scope, record reviewed dispositions for non-claim or circular surfaces, pin the resulting accepted claim set in a release, synchronize generated docs and memory, and merge through a distinct actor. Rollback, ingestion alone, a pass tally, and rejected claim candidates do not complete the issue.

## Authority and Prior Work
The accepted authority is release v0.162.0 at source commit `970633a`; rollback PR #94 restores that exact tree but is awaiting a CODEOWNER approval. PR #93 head `5954c1f` is provenance and proposal input, not accepted authority. The independently reproduced strong atom is its 60-file statement/proof-preserving ingestion at source `/home/dan/substrate@6d1f4e0`. Repository memory searches located the prior issue-92 effort, ingestion survey, P232 evidence transaction, P233 fixed facts, and P234/P235 synthesis proposals; every reused assertion is checked against the source files, registry, PR, or issue.

- Accepted release: v0.162.0 (`970633a`)
- Accepted claims reused: the exact dependency scopes cited by retained evidence records; C-GW-011 only after same-transaction acceptance is a dependency of C-GW-012
- Source modules read: ingested Lean sources, `formal/Audit.lean`, P232-P235 records, registry and release manifests
- Memory searches: historical Lean corpus, issue #92, P232-P235, C-GW-013, C-GW-014
- Campaign evidence: PR #93 and its source commit history, independent post-merge review, rollback PR #94
- Genuine unresolved objective: a corrected, independently reviewed promotion and disposition transaction merged to `main`

## Definitions and Invariants
The Lean files remain provenance-preserving historical artifacts. Formal verification applies only to each exact encoded proposition and its audited axiom footprint. A definition that contains the desired answer, a lookup table, a copied comparator, or a same-file theorem name is not independent verification of a stronger physical claim. Registry statements must include every formal domain hypothesis, distinguish declared physical premises from proved arithmetic, and preserve all exclusions in accepted dependencies. Release closure follows accepted registry membership. The corpus census distinguishes 55 artifact-claim evidence records, their 176 named theorem entrypoints, and the 39 affected claims; none of those count units is interchangeable.

## Permitted Imports and Assumptions
Permitted imports are release v0.162.0 accepted claims, the repository-pinned Lean/mathlib toolchain, the exact historical source at `6d1f4e0`, and physical premises explicitly labeled as declared inputs. No historical module-doc interpretation, hardcoded table, prior self-review, or merge status supplies scientific authority.

## Candidate Set
The fixed-theorem statements have one complete Lean proof route. The open classification concerns the two proposed syntheses and evidence attachments.

| Candidate | Construction | New objects/parameters | Natural-fit case | Expected falsifier | Status |
| --- | --- | --- | --- | --- | --- |
| A | Promote the Phase16QB and Phase14P3D lookup-table conjunctions as core syntheses | Source-class and channel dictionaries | Only if accepted dependencies derive every dictionary entry | Definitions contain triaxial excitation, dipole silence, and channel answers not supplied by dependencies | rejected |
| B | Classify those lookup-table theorems as artifact/supporting dispositions while promoting the genuine fixed facts | None | Exact match to issue #92 classification gate and accepted exclusions | A theorem independent of the lookup definitions that closes the missing source/channel map | selected |
| C | Build new end-to-end TT-source and conserved-multipole glue proofs | New formal source and conservation construction | Potential future synthesis campaign | Failure to derive the maps from accepted primitives without new hidden premises | future route, outside corpus classification transaction |

## Selection Criteria and Comparator Gate
Selection is ordered by exact statement match, dependency closure, absence of imported answers, compatibility with accepted exclusions, parameter economy, and reusable proof content. No empirical comparator enters this fixed-theorem and evidence-scope transaction.

## Claim Delta
The proposed registry additions are C-GW-011, C-GW-012, C-EW-001, C-WK-001, C-CF-001, C-ROT-002, C-GSK-003, C-SG-020, C-SG-022, and C-VIR-002, each narrowed to its exact Lean domain. C-GW-013 and C-GW-014 remain reserved identifiers and receive rejected/disposition records, not registry acceptance. Existing accepted claims receive Lean verification evidence only where the theorem evaluates the actual declared object and the independent reviewer accepts the exact scope.

## Claim Ladder
The ingestion/provenance manifest is checked first, then census completeness and structural classification, then fixed-theorem statement/axiom/domain audits, evidence relevance, dependency closure, independent claim review, release materialization, and full downstream replay. Kernel proof audits inspect exact statements, imports, escapes, axioms, and physical encodings; translation/census tests receive wrong-entrypoint and artifact-scope mutations.

## Importable Implementation
The reusable implementation is the imported Lean library under `formal/SubstrateFramework/Ingested/`, its aggregate import, provenance manifest, and exact census tests. No simulation or numerical API is introduced. Campaign and governance records refer to those modules rather than copying their statements into executable stand-ins.

## Harvest Checkpoints
The canonical goal is issue #92. PR #93 is the reviewed source, PR #94 is the active exact rollback, and the corrected branch is `correct/92-lean-corpus-promotion`. The final PR uses `Fixes #92` only if the complete ingestion, disposition, promotion, review, release, and validation gates pass. The implementing agent cannot review or merge its own transaction.

## Attempts
Attempt 0001 is PR #93: ingestion passed, but self-review, circular syntheses, missing formal hypotheses/dependencies, wrong census entrypoints, and artifact-as-verification attachments invalidated promotion. Attempt 0002 is the present corrected classification route: retain the exact ingestion, narrow fixed statements, reject lookup syntheses, strengthen census sensitivity, and obtain independent theorem/attachment reviews before promotion.

## Framework-Fit Audit
The corrected route changes no accepted v0.162.0 statement. New fixed claims are conditional finite theorems with their physical premise boundary explicit. C-GW-012 records C-GW-011 as a same-release dependency. Literal source and radiation dictionaries are not promoted as core claims because they conflict with accepted exclusions that deny the missing dynamics and source maps.

## Verifier Audit
The historical ingestion already reproduced exact source digests, normalized statement/proof equality, 16 targeted tests, and an 8,089-job Lean build with no proof escapes and only standard Mathlib axioms. The corrected boundary must additionally prove census entrypoint membership, exact census/adjudication/registry evidence mapping, explicit attachment/theorem counts, load-bearing theorem audit coverage, formal-domain equality, and independent reviewer provenance. Full validation is run once at the final release-changing boundary.

## Global Dependency Replay
Affected surfaces are the formal aggregate import, census tests, accepted registry, release manifest, generated claim index, claim/release memory, and campaign consumers. GitNexus is useful for Python/test callers but its low execution-flow risk does not assess Lean or governance semantics. The final replay includes the Lean gate, changed-test selector, full repository validation, registry/rendering consistency, memory validation, direct imports, and `git diff --check`.

## Foundational Revision Gate
No accepted foundation inconsistency is asserted. The rejected P234/P235 routes fail because the candidates import missing answers; they do not challenge accepted claims.

## Debt Ledger
The live transaction debt is: independent review files must be supplied by an actor distinct from the implementer; every retained evidence attachment must pass theorem-level relevance; all ten registry statements must match formal domains; C-GW-013/C-GW-014 dispositions must be durable; and the final release consumers must agree. Each item must be discharged before merge.

## Independent Claim Review
One fresh review is required for each proposed fixed claim, plus theorem-level review of every retained evidence attachment and explicit rejection reviews for C-GW-013/C-GW-014. A reviewer who authors substantive review records cannot merge the PR; a third actor performs merge adjudication.

## Results and Continuation
No corrected claim is accepted yet. The verified ingestion and the independent rejection mechanisms from PR #93 are the current strong milestone. Work continues through corrected classification, review, promotion, release, and merge.

## Promotion and Materialization
Successful claims enter `governance/claims.yaml`, a corrected v0.163.0 release, generated docs, accepted claim memory, and immutable P232/P233 campaign records. Rejected P234/P235 candidates remain adjudicated attempt evidence without registry entries. `scripts/render_docs.py` generates documentation.

## Done Gate
Done requires all issue #92 work items in one merged corrected PR, exact source provenance, complete theorem census, individually accepted evidence and fixed claims, reviewed rejected dispositions, closed dependencies, passing Lean and full repository gates at the unchanged final boundary, synchronized release/docs/memory, empty debt, distinct review, and distinct merge.

## Cross-References
Issue #92, PRs #93 and #94, source commit `6d1f4e0`, accepted base `970633a`, campaigns P232-P235, and the independent PR #93 review define the correction boundary.
