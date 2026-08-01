---
description: Audit CF5's vortex-to-effective-area consistency construction
author: vantasner
created: '2026-08-01T16:08:00Z'
updated: '2026-08-01T16:14:00Z'
tags:
- substrate-framework
- campaign-proposal
- vortex-tension
- effective-area
- migration-CF5
category: proposals
confidence: exploratory
status: archived
---
# P029 CF5 Tension Consistency Audit

## Question and Positive Deliverable

P029 must determine whether CF5 adds independent framework information beyond
composing the accepted conditional vortex tension with the accepted fixed-flux
effective-area inversion. The positive deliverable is a terminal claim-level
decision, reusable code only for genuinely new content, and preserved replay
evidence if the unit is instead duplicate.

## Base Release and Provenance

The accepted base is `v0.25.0` at commit `8e0fbbb`. `C-VTX-001/002` supply the
declared radial model, exact flux and inverse lengths, and bounded numerical
tension. `C-FLX-001` already states that
`A_eff=Phi^2/(2*sigma)` reconstructs a supplied tension and does not predict an
area. The hash-pinned candidate is CF5 at
`merged-framework/bridges/phase-10/bridge_CF5_flux_tube_tension_consistency.py`,
SHA-256 `0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7`.
Memory search found only these accepted boundaries and pending-consumer notes.

## Invariants, Conventions, and Allowed Imports

The campaign may import `C-VTX-001`, `C-VTX-002`, `C-FLX-001`, and exact
dimensionless algebra. The vortex remains an Abelian-Higgs model with smooth
profiles; the ideal tube remains uniform with fixed area. Equality by defining
an area from a supplied tension cannot become an independent model match. No
substrate, dual, chromoelectric, quark, QCD, or confinement identity is allowed.

## Candidate Preregistration

The candidates are frozen from migration metadata before the full CF5 body is
read.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Terminal duplicate evidence for accepted vortex and effective-area claims | C-VTX-001/002 and C-FLX-001 | Existing vortex parameters only | Preferred if all outputs algebraically reconstruct supplied inputs | Symbolic information audit and load-bearing input mutation |
| B | New narrow numerical composition claim for area versus penetration length | Accepted claims plus a predeclared comparison criterion | Existing parameters and ratio | Viable only if the ratio predicts something not already encoded | Independent output/consumer and sensitivity audit |
| C | Physical equivalence and confinement consistency | A cross-model sector and geometry map | Physical flux, area, tension, length | Conflicts absent independently derived map | Smooth-profile versus uniform-area dependency closure |

## Selection Criteria and Blinding

Selection is ordered by independent input-output information, convention and
geometry compatibility, sensitivity of every numerical window, assumption and
parameter economy, and consumer reach. The inventory excerpt already exposed
the approximate ratio `4.69` and the interval `[0.1,100]`; this contamination
is recorded, and neither value may select a candidate. Structural criteria and
mutations are frozen before the full source body is read.

## Proposed Claim Delta

No new claim is preregistered. P029 reviews whether `C-VTX-002` and
`C-FLX-001` already subsume CF5. A new numeric composition claim may be opened
only if Candidate B survives the independent-information and consumer tests;
it cannot be created merely to rename an algebraic transform of accepted data.

## Implementation and Oracle Plan

The exact oracle reconstructs `Phi`, `A_eff`, the energy slope, penetration
length, and their dimensionless ratio from accepted APIs, then substitutes the
area back to test whether the headline equality is an identity. Mutations vary
the supplied tension, flux, energy one-half, and comparison window. Existing
P026 numerical evidence is reused by source and claim identifier; it is not
rerun and renamed independent evidence. An independent route will use symbolic
elimination and dimensional scaling without package bridge helpers.

## Attempts and Continuation

Attempt `0001` preserved CF5's pre-check `np.trapz` failure and passed twenty
exact information checks. Candidate A was selected: no output survives
elimination as independent information, while an independent six-check route
confirms the inverse identity, factor-1000 window, and absent profile geometry.

## Debt Ledger

This ledger tracks information independence, window sensitivity, geometry, and
physical-map debt.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| The effective area may simply invert the supplied tension | Eliminate the area and test whether the slope identity is tautological | discharged |
| The order-one interval may be too broad to discriminate anything | Mutate the ratio and quantify the interval's rejection power | discharged |
| A smooth vortex has no declared uniform cross-sectional boundary | Derive a profile-based map or exclude physical equivalence | discharged |
| Re-solving CF1 may be duplicate numerical evidence | Compare equations, parameters, oracle, and output with C-VTX-002 | discharged |
| Physical confinement terminology may exceed both accepted models | Supply an accepted sector map or explicitly reject the interpretation | discharged |

## Review and Promotion Plan

P029 receives an independent information audit and a full source check-family
adjudication. A duplicate disposition must name the subsuming claims, durable
reproduction and review evidence, and every rejected interpretation. Registry
and release files remain unchanged unless an individually reviewed new claim
survives. The parent queue, generated consumers, tests, and memory are replayed
once at the unchanged terminal boundary.

## Done Gate

P029 closes with every CF5 output classified as accepted replay or
reconstruction, the comparison and geometry audited, terminal duplicate
disposition, replayed consumers, and an empty campaign debt ledger.
