---
description: Promote the ingested historical Lean corpus claims for issue #92 - census, corroboration evidence, fixed-theorem and synthesis promotions in the single merge unit
author: prime-agent
created: '2026-08-18T21:00:00+02:00'
updated: '2026-08-18T23:10:00+02:00'
tags:
- substrate-framework
- effort
- lean
- claim-promotion
category: efforts
confidence: established
status: archived
---

## Goal and Success Contract

This effort delivers work items 2-4 of issue #92 on the single merge unit branch
`process/historical-lean-ingestion` (PR #93): the theorem-by-theorem census of
all 60 ingested Lean files against the accepted registry at release v0.161.0,
the reviewed Lean evidence transaction attaching corroborations as
`verification_evidence`, the promotion of the new standalone exact facts
through a fixed-theorem campaign, the promotion of the two composed capstones
through synthesis campaigns, the registry/release/doc/memory
synchronization, and the final-boundary validation. It is complete only when
every claim-bearing theorem is promoted through the workflow or carries a
recorded, reviewed disposition, the debt ledger holds no "ingested theorems
are not claims" residue, and the full validation suite passes at the merge
commit.

## Accepted Baseline

Release v0.161.0 (210 accepted claims), branch head db082ec carrying the
ingested corpus (60 files, 467 theorems, provenance manifest, gate PASS:
escape scan, 8,089-job lake build, axiom audit, 12/12 consistency tests).
Read directly: `governance/claims.yaml` (all 210 statements),
`formal/SubstrateFramework/Ingested/*.lean` (module docs and theorem
statements), `formal/SubstrateFramework/Ingested/provenance.yaml`, campaign
adjudications for every corroborated claim family, and the migration
source-unit queue for family dispositions.

## Constraints and Invariants

The binding constraints for this effort are the following.

- The Lean surface is frozen: no `formal/` edits, no Lean rebuild - the gate
  passed at the ingestion commit and promotion is governance-only. Per owner
  direction, no validation ceremony: the corpus is not rechecked; the full
  suite runs once at the final boundary.
- Accepted atoms are not re-reviewed; each attachment/promotion is reviewed
  individually against what the Lean theorem actually proves, including its
  asserted physics premises encoded as declared inputs.
- Interpretive conditionals name their hypothesis and stay out of the core
  dependency layer; class-4 dispositions name why each theorem is not a claim.
- Claim statements are exact: scope limited to the machine-checked content
  with the declared encoding named; every promotion carries exclusions.

## Decomposition

1. [x] Census: classify all 60 files / 467 manifest theorems / 506 parsed
   theorem-lemma names (46 corroboration attachments on 43 accepted claims,
   10 fixed-theorem promotions, 2 synthesized capstones, class-4 dispositions
   for the remainder; C-SG-021 was reclassified class 4 during review).
2. [x] Instantiate contracts: this effort memory plus P232-P235 proposal
   manifests, validated before registry edits.
3. [x] P232 evidence transaction: 46 lean verification_evidence records on 43
   accepted claims, 43 individual scope reviews, adjudication, census.yaml.
4. [x] P233 fixed-theorem promotions: C-GW-011, C-GW-012, C-EW-001, C-WK-001,
   C-CF-001, C-ROT-002, C-GSK-003, C-SG-020, C-SG-022, C-VIR-002 (C-SG-021
   reclassified class 4 during review: hardcoded branch snapshots, not the
   digamma object - recorded in the adjudication as a preliminary-scan
   correction).
5. [x] P234/P235 synthesis promotions: C-GW-013, C-GW-014.
6. [x] Release v0.163.0 (224 accepted claims: the branch's 222 after merging
   main's PR #89, which added C-IGR-004 and C-GRV-002), regenerated docs and
   accepted memory, 13 decision memories, 2 synthesis contract memories,
   tests/test_lean_claim_census.py (4 checks).
7. [x] Final-boundary validation once (scripts/validate.sh --full, 2,336
   tests green, git diff --check clean), commit, PR #93 updated and merged to
   main as c864f33 (owner-authorized; issue #92 closed by the merge).

## Attempts

Attempts are append-only and reproducible; this table records the single census-and-promotion route with its per-step verdicts.

| Attempt | Candidate or repair | Artifact and command | Verdict | Mechanism | Next attempt |
| --- | --- | --- | --- | --- | --- |
| 0001 | Census + promotions as designed above | campaigns/P232..P235 | in progress | - | - |

## Validation

Validation obligations and their commands are the following.

- Lean gate: unchanged from ingestion commit (check_lean.sh PASS recorded in
  PR #93); promotion edits no formal/ file - verified by diff scope.
- Census machine check: tests/test_lean_claim_census.py (census <-> registry
  <-> artifacts <-> theorem coverage).
- Registry/release/memory/docs: scripts/validate_repository.py,
  scripts/render_docs.py --check, scripts/render_memory.py --check,
  memory validate.
- Final boundary: scripts/validate.sh --full once; git diff --check
  separately.

## Debt Ledger

The single inherited debt from the ingestion workstream is discharged by this effort; no new debt is introduced.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| Ingested theorems are not yet framework claims | ingestion workstream | Promotion requires the census + transactions | This effort: P232-P235 on the same branch | Discharged by this effort |

## Results

Complete. Merged to main as c864f33 (PR #93, owner-authorized issue-scoped
self-merge; issue #92 closed). Census machine-checked (test_lean_claim_census.py:
60 files, all 506 parsed theorem/lemma names classified); registry 224 claims
valid at v0.163.0 with 46 lean evidence attachments on 43 accepted claims and
12 new claims (10 fixed-theorem, 2 synthesized); docs, accepted memory, and
campaign records P232-P235 immutable on main; scripts/validate.sh --full green
(2,336 tests) and git diff --check clean at the merge boundary; the formal
Lean surface is byte-identical to the gate commit 63fa769 (no rebuild).

## Canonicalization

Registry: verification_evidence attachments + 13 new claims; release
v0.163.0; campaigns P232-P235 immutable; docs regenerated; accepted claim
memory synchronized; decision memories per promoted claim.

## Done Gate

Checked at merge: all four #92 work items in one PR, gate green at the merge
commit (formal surface unchanged), full suite green, debt ledger empty.

## Cross-References

Issue #92; PR #93; campaigns/P232-lean-corpus-census,
P233-lean-discrete-facts, P234-lean-polarization-split,
P235-lean-radiating-channel; memory/vantasner/efforts/
historical-lean-corpus-ingestion.md; governance/releases/v0.163.0.yaml.
