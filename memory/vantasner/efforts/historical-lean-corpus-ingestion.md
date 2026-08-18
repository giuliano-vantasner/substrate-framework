---
description: Ingest the historical Lean corpus from /home/dan/substrate into the framework as provenance-governed formal artifacts
author: prime-agent
created: '2026-08-18T19:05:00+02:00'
updated: '2026-08-18T19:05:00+02:00'
tags:
- substrate-framework
- effort
- lean
- ingestion
category: efforts
confidence: established
status: active
---

## Goal and Success Contract

Execute the ingestion workstream of issue #92 — the historical external Lean
incorporation that issue #90 deferred — as part of #92's SINGLE merge unit
(one PR, no phase split, no stopping point after ingestion). Survey every Lean
file under `/home/dan/substrate`, land the corpus in the repository library
with recorded provenance (`scripts/check_lean.sh` gate, per-file provenance
manifest, axiom audits), adapting files as needed with every adaptation
auditable; where sources needed zero statement/proof changes, record that
stronger guarantee.

Success for this workstream: the corpus builds as part of the repository
library, the gate passes, every file's provenance and every recorded
adaptation is machine-checked. The workstream is NOT itself a done point: the
same PR must also census every ingested theorem against the accepted registry
(corroboration evidence, new standalone exact facts, synthesized higher
theorems, or recorded dispositions) and promote the real claims through the
theorem and synthesis workflows with individual review, registry entry, and
release pinning before it is ready for review. #92 closes only at that merge.

## Survey (all 170 .lean files in /home/dan/substrate @ 6d1f4e0)

The survey walked every Lean file in the historical workspace and assigned
each family a disposition, deduplicating byte-identical copies (14
dynamics_lean files and 3 formalization files are identical to their bridges
counterparts) and excluding superseded attempt candidates and audit-time
snapshot tooling.

| Family | Files | Disposition |
| --- | --- | --- |
| `merged-framework/bridges/phase-*/lean` | 38 | INGESTED (unified-framework phase oracle contributions) |
| `sg-breather-ionization/dynamics_lean` | 30 | 14 byte-identical to bridges copies (deduplicated); 16 INGESTED |
| `sg-breather-ionization/formalization` | 8 | 3 identical to bridges copies; 5 INGESTED (core library incl. the Charge re-export shim) |
| `federico_comparsi/.../ComparsiVirial.lean` | 1 | INGESTED (exact virial certificates) |
| `sg-breather-ionization/attempts/*/candidate.lean` | 41 | EXCLUDED: superseded historical attempts, not canonical |
| `sg-breather-ionization/audits/*/print_axioms.lean` | ~36 | EXCLUDED: audit-time snapshot tooling, superseded by the repo Audit.lean |

Ingested total: 60 files, 467 theorems. Every ingested file imports only
Mathlib or other ingested modules.

## Recorded Adaptations (all mechanical, all machine-checked)

1. **Namespace wraps (29 files)**: files that historically declared root-level
   names were checked standalone; inside one library, 10 root names would
   collide (e.g. `gravitonPolarizations` in Phase5Gravity and Phase12GW,
   `odV2`/`fab`/`isOverdetermined` in Phase21AS and Phase22AS). Each is wrapped
   in `namespace <File> / end <File>`; imports and opens keep cross-file
   references resolving (`Charge`→`Formalization`, `ActionQuantum`→`Energy`,
   `DetectorGeometry`→`ProductionAmplitude`).
2. **Comment rewording (9 files)**: prose such as "no `sorry`" would trip the
   gate's escape scan; reworded to "no proof escape" without touching any
   statement. Exact originals recoverable from the recorded source sha256.
3. **Import-path rewrites (3 files)**: `formalization.*` / `dynamics_lean.*`
   imports rewritten to `SubstrateFramework.Ingested.*`.

`tests/test_lean_ingestion.py::test_statements_and_proofs_are_unchanged`
proves token-for-token that after removing exactly those surfaces, every
ingested file equals its source: no statement or proof body changed.

## Evidence

- Gate: `scripts/check_lean.sh` PASS (escape scan; 8,089-job `lake build`;
  axiom audit).
- Axiom footprints of all 59 audited main theorems: 12 axiom-free, 5
  `[propext]`, 1 `[propext, Quot.sound]`, 42 `[propext, Classical.choice,
  Quot.sound]` — every footprint a subset of Mathlib's standard axioms; no
  project axioms, no escapes.
- Consistency tests: 12 passed (manifest/schema/umbrella/audit/collisions/
  digests/verbatim/unchanged-statements).
- Toolchain match: source project pinned the identical `leanprover/lean4:
  v4.28.0` and mathlib rev `8f9d9cff6bd7`.

## Debt Ledger

One deliberate debt remains open by design, recorded in the table below.

| Debt | Introduced by | Why it is real | Discharge artifact | Status |
| --- | --- | --- | --- | --- |
| Ingested theorems are not yet framework claims | The ingestion workstream | Promotion requires individual review with dependency closure through the theorem/synthesis workflows | Discharged by P232-P235 on this branch: census of all 60 files, 46 lean evidence attachments to 43 accepted claims, 12 promotions (10 fixed-theorem, 2 synthesized) into v0.163.0, remaining theorems with recorded dispositions | Discharged |

## Done Gate

Discharged: the census and promotion transactions landed on the same branch
(campaigns P232-P235, release v0.163.0) with every claim-bearing theorem
promoted or carrying a recorded, reviewed disposition; the formal surface is
unchanged from the gate commit and the full validation suite runs once at the
merge boundary. See memory/vantasner/efforts/issue-92-claim-promotion.md.
