---
description: Audit MR2 pi-squared BPS normalization correction
author: vantasner
created: '2026-08-06T12:15:20Z'
updated: '2026-08-06T12:15:20Z'
tags:
- substrate-framework
- campaign-proposal
- migration-MR2
- convention-audit
- nonduplication
category: proposals
confidence: exploratory
status: active
---
# P220 MR2 BPS Normalization Audit

## Question and Positive Deliverable

P220 must reproduce MR2's correction through independent normalization routes,
decide whether it adds anything beyond accepted claims, and give MR2 a terminal
disposition. The positive object is an exact convention and dependency ledger;
a correct source criticism is not by itself a new framework claim.

## Base Release and Provenance

The base is v0.158.0 at clean framework commit `7c98ec7`, with 201 accepted
claims and five pending units. MR2 is pinned at substrate commit `6d1f4e0`,
SHA-256 `2e62ce...8e990`, and 20,989 bytes; its file is clean while unrelated
source changes are excluded. The queue exposes eight checks, one assertion,
both sextic conventions, the pi-squared map, the MK6 correction, and the MK5
reduced-coefficient cross-check.

## Invariants, Conventions, and Allowed Imports

C-BPS-001 already fixes the normalized current, BPS lambda convention, bound,
and equivalent lambda-A form. C-VEC-002 already proves
`lambda_A=pi^2*lambda_BPS` for the same current. C-GSK-001 already gives the
reduced c6 formula in both coordinates, and P219 already corrects MK6. Only
these exact ceilings and direct symbolic algebra are permitted; no physical
vector, pion, baryon, mass, coefficient, or state map is imported.

## Candidate Preregistration

The candidates compare density, reduced-coefficient, and bound routes, a
current-normalization mutation, a physical firewall, a no-new-claim outcome,
and terminal consumer governance.

| Candidate | Description | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- |
| A | Equate same-current sextic densities | Should reproduce C-VEC-002 | Exact positive-root elimination |
| B | Eliminate through reduced c6 | Should reproduce C-GSK-001 | Independent coefficient cancellation |
| C | Transform the BPS bound | Should reproduce P219 | Exact bound equality and corrected substitution |
| D | Rescale the current | Must change the coupling coordinate | Normalization mutation |
| E | Remove physical imports | Leaves only conditional algebra | Free-symbol and dependency audit |
| F | Add no claim or API | Expected if all exact content duplicates | Repository-wide nonduplication |
| G | Close MR2 and replay consumers | No backward authority | Pinned graph audit |

## Selection Criteria and Blinding

Same-current typing, exact independent elimination, accepted closure,
parameter economy, rescaling sensitivity, novelty, and physical firewall rank
before numeric comparison. Queue-exposed facts cannot be blinded; remaining
source values, predicates, output, and consumer details remain unopened through
the validated committed freeze.

## Proposed Claim Delta

P220 proposes no identifier. C-VEC-002 already owns the lambda map, C-BPS-001
owns both bound coordinates, C-GSK-001 owns both reduced coefficients, and P219
owns the corrected MK6 consequence. A new claim is allowed only if the source
contains a distinct exact object with different premises or reach.

## Implementation and Oracle Plan

SymPy and direct algebra are the strongest oracles. Primary checks will
eliminate both positive lambda coordinates, rederive c6 and the bound, mutate
current normalization, and audit source predicates. The independent route will
not import the source or campaign verifier. Existing package APIs are reused;
no wrapper is added for duplicate algebra. Compatibility preflight covers
direct, imported, dynamic, and eager legacy access before one native run, or
reuses a hash-identical root execution if its exact output is already durable.

## Attempts and Continuation

Attempt 0001 freezes seven candidates, no provisional claim, three exact
normalization routes, mutations, provenance, compatibility handling, and
nonduplication criteria before the source body opens.

Attempt 0002 reuses P215's hash-identical clean MR2 execution: eight runtime
checks, one assertion, exit zero, and 1.076 seconds. MR2 imports neither NumPy
nor SciPy and has no legacy trapezoidal integration surface. Claim-by-claim
inspection finds that MR2.1 through MR2.5 duplicate accepted normalization,
convention, coefficient, bound, and P219 correction content. MR2.6 reuses those
same coefficients and is a dependent algebraic regression, MR2.7 is a supplied
`N_c=3`, `m_pi=138.03 MeV` substitution rather than a physical prediction, and
MR2.8 is only a selected-token AST guard. No provisional claim or API survives.

## Debt Ledger

The ledger tracks source predicates, current normalization, lambda coordinate,
positive-root branch, reduced coefficient, bound, supplied physical inputs,
novelty, compatibility, consumers, and terminal records.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| MR2 body and predicates remain unopened | Reproduce after committed freeze | discharged: P215 hash-identical execution reused and body audited |
| Routes may share a copied intermediate | Eliminate independently to the same coefficient surface | diagnosed: MR2.6 is dependent; fresh verifier remains open |
| Current rescaling may be hidden | Explicit wrong-normalization mutation | source lacks it; fresh verifier remains open |
| Correct source result may be promoted twice | Registry campaign module and memory nonduplication audit | source-level duplication established; independent gate remains open |
| Physical inputs may leak through corrected numerics | Free-symbol and accepted-dependency audit | discharged: N_c, m_pi, and B remain supplied |
| Later MR units may grant backward authority | Pinned graph replay | open |
| Governed records remain unresolved | Source disposition and canonical synchronization | open |

## Review and Promotion Plan

Every MR2 predicate receives individual review. If no distinct claim survives,
the terminal duplicate-evidence or qualified disposition must still name exact
owners and preserve corrected and rejected surfaces. Package and release state
remain unchanged in that case, so the latest full boundary may be reused after
targeted and record-sensitive validation.

## Done Gate

P220 closes only with independent convention routes, normalization mutations,
source and consumer adjudication, a supported nonduplication decision,
synchronized records, and an empty campaign debt ledger.

## Cross-References

See v0.158.0, C-BPS-001, C-VEC-002, C-GSK-001, C-VAR-002, P107, P215,
P218, P219, MK2, MK5, MK6, MR2-MR6, and the framework migration effort.
