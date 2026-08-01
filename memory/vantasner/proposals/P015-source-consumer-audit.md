---
description: Build a reproducible source-consumer audit and adjudicate HE5 as migration evidence
author: vantasner
created: '2026-08-01T13:14:45Z'
updated: '2026-08-01T13:24:25Z'
tags:
- substrate-framework
- campaign-proposal
- source-audit
- migration-HE5
category: proposals
confidence: exploratory
status: archived
---
# P015 Source Consumer Audit

## Question and Positive Deliverable
P015 must deliver a deterministic reusable audit that identifies which files in
a hash-pinned source tree contain declared token families. The audit must record
scope, exclusions, relative paths, and content hashes, then use that evidence to
adjudicate HE5. A token occurrence is lexical evidence only; it cannot become a
scientific dependency or accepted physics claim by being counted.

## Base Release and Provenance
The accepted base is `v0.14.0` at commit `4724876`. The candidate source unit is
HE5 at `merged-framework/bridges/phase-45/bridge_HE5_consumer_dependency_parse.py`,
SHA-256 `70a8402413e3bdde15a9d9b93fb4fc282f277b28a5943da9fad4a8cc6c561b81`.
The pinned read-only source root is the isolated `substrate@6d1f4e0` snapshot.
The memory search produced no project-local HE5 record; unrelated global-memory
hits are not imported.

## Invariants, Conventions, and Allowed Imports
The scan is UTF-8 text over an explicit include glob. Exclusions are relative
path prefixes or exact paths, never implicit current-directory behavior. Every
matched file is content-hashed. Literal and regex token groups are declared in
the audit invocation. `migration/source-claims.yaml` remains the canonical
candidate-unit inventory; the audit is evidence about consumers, not authority
over scientific claims. No accepted scientific claim changes in P015.

## Candidate Preregistration
The alternatives are frozen before reading HE5's implementation details.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Generic deterministic audit plus evidence-only disposition | Pinned readable tree | include, exclusions, token groups | Reusable and authority-safe | Reproduce matches and reject scope/content mutations |
| B | Accepted scientific claim from token counts | Lexical occurrence treated as semantic import | HE5's token list | Violates authority and claim meaning | Same token in comments or quotations gives false dependency |
| C | Manual copied list | Human transcription | none | Non-reproducible and stale-prone | Source or exclusion mutation is undetected |

## Selection Criteria and Blinding
The frozen order is reproducibility, explicit lexical scope, hash provenance,
semantic humility, mutation sensitivity, and reuse. Candidate A is selected
structurally. B confuses source metadata with physics; C lacks a verifier. There
is no empirical comparator.

## Proposed Claim Delta
No scientific claim is proposed. The positive delta is a reusable source-audit
API and executable evidence report. HE5 will receive a terminal disposition
with a disposition-specific reason and durable paths.

## Implementation and Oracle Plan
A pure source-audit module will accept an explicit root, include glob, excluded
paths, and named regex patterns, and return sorted records with SHA-256 hashes
and matched groups. Unit tests will cover sorting, exclusions, overlapping token
groups, comments as lexical matches, invalid roots, and content mutations. The
campaign verifier will reproduce HE5's declared scan at the pinned tree, compare
the source's asserted path sets rather than only its terminal tally, and mutate
tokens, exclusions, and file content. No numerical or scientific oracle is
appropriate.

## Attempts and Continuation
Attempt `0001` implements Candidate A after the full HE5 source is audited. If
HE5's scan depends on current-directory or broad substring accidents, the
framework audit will preserve that discrepancy and use its own explicit scope.

## Debt Ledger
The campaign starts with three explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| HE5 may conflate lexical occurrence with dependency | Source adjudication labels every result as lexical evidence | discharged |
| The source scan may hide exclusions or path assumptions | Canonical API records root, glob, exclusions, and hashes | discharged |
| A static list can become stale | Executable verifier and mutation tests reproduce the pinned result | discharged |

## Review and Promotion Plan
Review will audit HE5's implementation and every asserted consumer set against
the independent canonical scan. The campaign will freeze its evidence, update
HE5's terminal migration disposition, regenerate the inventory, and validate
the governance boundary. Because no accepted scientific claim changes, P015
does not create a release solely for source metadata.

## Results and Promotion
Attempt `0001` preserved a direct-execution import-boundary failure; attempt
`0002` preserved an unreachable mutation-predicate return introduced during its
repair. Attempt `0003` passes 20 deterministic checks, including full source-
tree and matched-file hashes, positive controls, content mutation, and token and
exclusion mutations. An independent direct-pathlib traversal passes six checks,
and five package tests cover reusable behavior. HE5 is terminally out of
scientific-claim scope and retained as exact lexical migration evidence; the
accepted release remains `v0.14.0`.

## Done Gate
P015 is complete. The positive audit object exists, its scope and hashes are
durable, HE5 is terminally adjudicated without semantic overreach, mutations
demonstrate sensitivity, affected consumers agree, and the campaign debt is
empty.
