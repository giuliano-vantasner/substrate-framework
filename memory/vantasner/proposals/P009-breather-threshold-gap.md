---
description: Derive the exact sine-Gordon breather threshold deficit and qualify T1E
author: vantasner
created: '2026-08-01T12:12:08Z'
updated: '2026-08-01T12:14:50Z'
tags:
- substrate-framework
- campaign-proposal
- sine-gordon
- migration-T1E
category: proposals
confidence: exploratory
status: archived
---
# P009 Breather Threshold Deficit

## Question and Positive Deliverable
P009 derives the positive threshold-deficit function `Delta(omega)=16-E(omega)` from accepted `C-SG-002`. The proposed `C-SG-005` will give its closed form, strict monotonicity, convexity, endpoint limits, bounds, and exact partition `E+Delta=16`.

The name “threshold deficit” is intentional. T1E calls the complement a binding gap, but its Lean theorem defines that complement and proves a ring identity; it does not independently derive a two-body binding interaction. The accepted claim will not overstate the semantics.

## Base Release and Provenance
The accepted base is `v0.8.0` at framework commit `d35f3ee`. `C-SG-002` supplies `E=16*sqrt(1-omega^2)` and identifies 16 as the two-kink threshold. `C-SG-004` supplies the distinct gradient functional that T1E uses as an object guard.

The hash-pinned source unit is T1E at `merged-framework/bridges/phase-1/bridge_T1E_E0_triple_oracle.py`, SHA-256 `bdd57d929b7bed2436ad5803f0a614d4887a35a7eab5ecd78b23041888e48a97`. It is partially migrated through `C-SG-002`; its remaining scope names the binding-gap encoding and cross-program lift.

## Invariants, Conventions, and Allowed Imports
The domain is real `0<omega<1`. The normalized threshold is exactly 16. `Delta` is an energy difference in the same normalized units as `E`. Its positivity follows from the open-domain energy range; its endpoint values are limits, not attained values.

The T1E lift `E_shadow=E_adim*N^-1/2` and `E_vantasner=E0/sqrt(N)` assumes `E_adim=E0` and writes both sides in the same form. P009 may record this as definitional consistency evidence but cannot promote a physical cross-program identity.

## Candidate Preregistration
Three exact routes are registered with no empirical comparator.

| Candidate | Description | Assumptions | Parameters | Framework-fit prediction | Decisive test |
| --- | --- | --- | --- | --- | --- |
| A | Direct accepted-threshold complement | C-SG-002 | none | Minimal dependency and clean API | Exact formula, derivatives, bounds, limits |
| B | Integrate `-dE/domega` from the threshold endpoint | Differentiability and accepted endpoint | none | Independent construction of the same complement | Integral equals Candidate A without inserting it |
| C | Use the action representation | C-SG-003 in addition | action `J` | Useful consumer identity but unnecessary dependency | Substitution gives `16*(1-sin(J/16))` |

## Selection Criteria and Blinding
The frozen order is accepted dependency closure, exact global behavior, parameter economy, independent construction, then API reach. Candidate A is primary. Candidate B is the independent route. Candidate C is a valid downstream representation but is not load-bearing and will not expand the dependency set. No comparator exists.

## Proposed Claim Delta
P009 proposes one native sine-Gordon consequence.

| Claim | Exact statement | Dependencies | Oracle | Consumers |
| --- | --- | --- | --- | --- |
| C-SG-005 | `Delta=16-E=16*(1-sqrt(1-omega^2))` lies in `(0,16)`, increases strictly and convexly, tends to 0 and 16 at the domain endpoints, and partitions the threshold exactly | C-SG-002 | exact SymPy algebra/calculus and independent marginal-loss integral | future binding, threshold, and stability campaigns |

## Implementation and Oracle Plan
The canonical sine-Gordon module will add `breather_threshold_deficit`. Tests will cover an exact frequency, partition identity, and existing frequency-domain guards.

The main verifier will derive the complement through the API, prove first and second derivative formulas, endpoint limits, and exact partition, and reject threshold, coefficient, and power mutations. The independent review will integrate the accepted marginal energy loss from zero to `omega` without importing the new API. The source-adjudication review will classify T1E's Hamiltonian integral as duplicate evidence for `C-SG-002`, its single-point numeric evaluation as regression coverage, its distinct-object guard as consistent with `C-SG-004`, and its lift as definitional conditional algebra.

## Attempts and Continuation
Attempt `0001` implements Candidate A with Candidate B review. If the marginal integral disagrees, audit endpoint conventions and signs before acceptance. Cross-program identity cannot be used to repair the threshold calculation.

## Debt Ledger
P009 begins with three debts.

| Debt | Discharge condition | Status |
| --- | --- | --- |
| T1E's “binding gap” could imply unproved interaction physics | Registry and API use threshold-deficit semantics | discharged |
| The triple-oracle headline could be mistaken for three derivations | Source review distinguishes derivation, definition, and regression evidence | discharged |
| The cross-program lift is definitional after shared premises | T1E receives an evidence-backed qualification rather than physical promotion | discharged |

## Review and Promotion Plan
One claim review and one source adjudication will audit the exact function and every T1E check family. Promotion will freeze P009, add the API/test and `C-SG-005`, create a pinned release, change T1E from partial to evidence-backed qualified, regenerate canonical records and the queue, replay sine-Gordon consumers, and run full validation once.

## Results and Promotion
Attempt `0001` passed 13 exact checks. Independent integration of the marginal energy loss passed four checks and recovered the same global function. `C-SG-005` was accepted as a native symbolically verified consequence in `v0.9.0`.

The T1E source audit maps its exact content to `C-SG-002`, `C-SG-004`, and `C-SG-005`. T1E is terminally qualified: the Hamiltonian calculation duplicates accepted evidence, the single-point evaluation is regression coverage, and the cross-program lift is equality after both sides are declared to share the same expression.

## Done Gate
P009 is complete. The positive deficit has exact global verification, the independent integral agrees, T1E's duplicate and definitional evidence is honestly classified, all affected consumers replay, and campaign debt is empty.
