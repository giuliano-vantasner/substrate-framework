---
description: Audit EL3's unit-length product as a conditional mass-coordinate composition
author: vantasner
created: '2026-08-01T14:08:42Z'
updated: '2026-08-01T14:12:01Z'
tags:
- substrate-framework
- campaign-proposal
- conditional-mass-coordinate
- migration-EL3
category: proposals
confidence: exploratory
status: archived
---
# P020 Conditional Mass-Length Coordinate

## Question and Positive Deliverable
P020 must determine exactly what follows when EL3's declared unit and length
relations are composed with the accepted mass-coordinate map. The positive
object is a premise-explicit, importable relation among mass, length, action,
speed, and a dimensionless coupling, with every free input retained. A claim
that the mass import has vanished does not complete the campaign.

## Base Release and Provenance
The accepted base is `v0.17.0` at commit `7f518ab`. Direct authority is
`C-DIM-003`; `C-SK-001` supplies only a conditional mass-formula equality and
P017 classifies MR1 as duplicate evidence for it. No accepted claim derives
MR1's Skyrme length, selects a coupling value, or identifies an electron object.
The hash-pinned candidate is EL3 at
`merged-framework/bridges/phase-46/bridge_EL3_me_is_not_a_dimensionful_primitive.py`,
SHA-256 `ab4549b5c147113beec18c2513a42dfbdd34c25ad21d125dfa6d8e9d9f0de69d`.
Its other listed dependencies remain pending or qualified. Memory search is
historical context only and supplies no premise.

## Invariants, Conventions, and Allowed Imports
All scales and the coupling are positive. `C-DIM-003` remains a lossless
coordinate map. Any Skyrme unit, length, unit identification, restored-units
factor, or coupling value introduced by EL3 is a declared conditional premise
unless independently accepted. A dimensionless formula may relocate an import
but cannot remove a free coupling or establish physical identity.

## Candidate Preregistration
The candidates are frozen before EL3's full body is read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Promote a conditional unit-length composition retaining `e` | Declared EL3 unit, length, and unit-identification equations | Free dimensionless coupling `e` | Exact useful specialization of C-DIM-003 | Substitute stepwise, invert, and mutate every coefficient/power |
| B | Classify EL3 as duplicate evidence for C-DIM-003 | Mass-coordinate map only | Free coordinate | Preferred if EL3's formulas add no distinct reusable conditional relation | Normalize to C-DIM-003 and inspect consumers |
| C | Promote physical closure that the mass carries no independent information | Declared formulas treated as derived physics and `e` treated as fixed | Hidden coupling/object premises | Conflicts with accepted import ceiling | Vary `e` and reconstruct different masses with valid dimensions |

## Selection Criteria and Blinding
Selection is ordered by premise closure, exact unit restoration, retained free
information, dependency economy, reusable consumer reach, and mutation
sensitivity. Candidate A survives only as a conditional theorem with `e`
explicit. Candidate C fails if varying `e` changes the coordinate or if the
source imports any length/unit relation it calls derived. Numerical electron or
coupling values are blinded until equations and tests freeze.

## Proposed Claim Delta
Provisional `C-DIM-004` states that if positive quantities obey the declared
relations `U=S*c0/(2*e^2*L)` and `U=4*pi*m*c0^2`, then
`m=S/(8*pi*e^2*L*c0)`, the `C-DIM-003` coordinate relative to length `L` is
`N_m=1/(8*pi*e^2)`, and `S/(m*c0)=8*pi*e^2*L`. These are equivalent conditional
forms. The coupling and both input equations remain premises; no mass, length,
or particle identity is predicted.

## Implementation and Oracle Plan
The dimensional-analysis module will gain pure conditional conversion helpers
only if the relation survives source audit and has a distinct consumer. SymPy
exact substitution fits the claim. The verifier will derive every form from
the declared equations, check dimensions through `C-DIM-003`, vary `e`, and
reject missing `pi`, factor-two, speed, length, and coupling powers. An
independent route will eliminate `U` directly without importing the helper.
Campaign scripts run with `PYTHONPATH=src`; numerical examples are regression,
not independent evidence for an exact identity.

## Attempts and Continuation
Attempt `0001` will reproduce hash-pinned EL3 and audit the exact composition.
Technical failures will be preserved and repaired without moving coefficients
or ceilings. If the result is only C-DIM-003 in renamed symbols, the claim will
be withdrawn. If exact conditional algebra survives but physical closure fails,
the source will be qualified and the positive conditional object retained.

## Debt Ledger
The campaign starts with four explicit debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| Restored-unit factors may be guessed | Independent dimensional and algebraic reconstruction | discharged |
| The coupling may be hidden as already known | Claim and mutations retain `e` | discharged |
| MR1 length/unit premises may be called accepted | Import inventory labels them conditional | discharged |
| Electron identity may leak from EL2 | Source audit excludes the qualified composite narrative | discharged |

## Review and Promotion Plan
Review will independently eliminate the declared unit, test all equivalent
forms, and audit EL3 check by check against C-DIM-003 and P017. Promotion
requires package APIs/tests, individual claim review, terminal EL3 disposition,
registry/release/generated-record synchronization, targeted replay, and one
full repository gate at the unchanged boundary.

## Results and Promotion
EL3's nine source checks reproduce at the pinned hash. Attempt `0001` passes 16
exact checks, independent unit elimination passes five, and 25 focused tests
pass. `C-DIM-004` is accepted as a conditional composition with `e` and both
coefficients explicit. EL3 is qualified because monomial uniqueness does not
fix a function of `e`, the mass column carries the C-DIM-003 nullspace
coordinate, and its coupling-free route substitutes other free inputs.

## Done Gate
P020 is complete. The positive conditional object exists with exact units, all
free inputs remain explicit, sensitivity and independent checks pass, EL3 is
terminally qualified, consumers agree, and debt is empty.
