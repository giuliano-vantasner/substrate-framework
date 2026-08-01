---
description: Audit EL6's measured-mass confrontation for genuine predictive closure
author: vantasner
created: '2026-08-01T14:42:30Z'
updated: '2026-08-01T14:42:30Z'
tags:
- substrate-framework
- campaign-proposal
- confrontation-closure
- migration-EL6
category: proposals
confidence: exploratory
status: archived
---
# P023 Confrontation Closure Audit

## Question and Positive Deliverable
P023 must determine whether EL6 produces a comparator-independent prediction or
only solves the accepted coordinate map for an unassigned input. The positive
deliverable is an exact, premise-tagged confrontation object that reports the
remaining required scale or prefactor and cannot label a comparator-derived
input as a prediction.

## Base Release and Provenance
The accepted base is `v0.20.0` at commit `f71606c`. Direct authority is
`C-DIM-003`, `C-RGE-001`, `C-DIM-005`, and `C-LIN-001`. The hash-pinned candidate
is EL6 at
`merged-framework/bridges/phase-46/bridge_EL6_confrontation_and_ledger.py`,
SHA-256 `f6ea408d674d2fcc88a9bb0d6564b56b21dfde124161f3786724dd1179259f5e`.
Its AS, B, MR, QCD, and S5 references remain noncanonical unless separately
accepted. Memory supplies only migration history.

## Invariants, Conventions, and Allowed Imports
All scale and coordinate quantities are positive. `C-DIM-005` retains `q`,
`b0`, and `beta^2`; `C-DIM-003` retains the basis length. A measured mass may be
used only after the symbolic prediction and free-input inventory freeze. Solving
an equation for `a`, `q`, or another premise using that measurement is a required
input, calibration, or confrontation result—not an independent prediction.

## Candidate Preregistration
The candidates are frozen before the EL6 body and numerical comparison are read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote a distinct exact inverse confrontation map for the required length or prefactor | C-DIM-005 premises plus a declared target mass | `q`, `b0`, `beta^2`, target | Compatible only if the inverse adds reusable semantics beyond C-DIM-003 | Compose forward/inverse maps and mutate every free input |
| B | Classify EL6 as duplicate or qualifying evidence for C-DIM-003/C-DIM-005 | Accepted coordinate maps | Existing free inputs | Preferred if every confrontation formula is an algebraic inverse already accepted | Normalize all source formulas to accepted APIs |
| C | Accept an electron-mass prediction | Treat source `a`, `q`, beta data, and particle map as independently fixed | Hidden or comparator-derived inputs | Conflicts with accepted ceilings | Construct two admissible input sets or solve a free input from the comparator |

## Selection Criteria and Blinding
Selection is ordered by dependency closure, comparator independence, retained
free information, exact inverse composition, dimensional consistency, and
distinct consumer value. Numerical closeness cannot select a candidate. The
measured electron mass and any reported mismatch factor remain blinded until
the symbolic map, input tags, and selection verdict freeze.

## Proposed Claim Delta
Provisional `C-DIM-006` would state a distinct inverse confrontation relation
only if EL6 adds semantics beyond `m=N_m*S/(c0*a)` and
`N_m=q*exp(-8*pi^2/(b0*beta^2))`. Otherwise no claim is proposed and EL6's
exact content maps to the existing claims with a terminal mixed disposition.

## Implementation and Oracle Plan
SymPy exact substitution will compose the accepted coordinate formulas, solve
for each free input, and verify forward/inverse identities. Mutations vary the
length, prefactor, beta coefficient, and coupling. An independent route will
normalize dimensions before substitution. Comparator use is audited after the
symbolic selection gate; numerical arithmetic is regression evidence only.

## Attempts and Continuation
Attempt `0001` will reproduce EL6 and inventory every declared, derived, spent,
and measured quantity. If the inverse is duplicate, Candidate B closes the unit
without adding an API. If the source uses the comparator to assign a premise,
that route is preserved as confrontation evidence and its prediction reading is
rejected.

## Debt Ledger
The campaign tracks comparator and closure debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The absolute length may remain unassigned | Expose it or show accepted independent closure | discharged |
| The mass-energy prefactor may remain free | Retain it in every formula | discharged |
| The comparator may be used to solve an input | Tag inverse solutions as calibration/confrontation | discharged |
| Repeated accepted formulas may be promoted again | Prove distinct consumer value or classify duplicate evidence | discharged |

## Review and Promotion Plan
Review will independently reconstruct the input ledger and exact inverse map.
Any new claim requires an importable API and tests; a duplicate/qualified result
requires durable source evidence, terminal EL6 disposition, synchronized queue
and parent effort, and targeted workflow validation without manufacturing a
release.

## Results and Promotion
EL6 reproduces all eight source checks. Twelve exact and five independent checks
show that the derived-side expression is `C-DIM-005` with a renamed prefactor,
and both required-input inverses depend on the target comparator. Proposed
`C-DIM-006` is rejected as duplicate. EL6 is qualified without a release change;
its numerical confrontation is preserved as noncanonical evidence.

## Done Gate
P023 is complete. The confrontation and provenance ledger are exact, comparator
calibration is exposed, EL6 is terminally qualified, and campaign debt is empty.
