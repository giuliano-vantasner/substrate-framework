---
description: Independent review of C-VIR-001
author: vantasner-review
created: '2026-08-01T11:55:53Z'
updated: '2026-08-01T11:55:53Z'
tags:
- substrate-framework
- claim-review
- virial-scaling
category: decisions
confidence: working
status: archived
---
# Review of C-VIR-001

## Claim Under Review
Conditional on `w=(a-b)/2` and `e=-(a+b)/2` for real `a,b`, the simultaneous target `w=e=-1/2` holds if and only if `(a,b)=(0,1)`. The named alternatives `(1,0)` and `(1,1)` fail the width and energy targets respectively.

## Sourced Inputs
The review read P007, attempt `0001`, the conditional scaling API/tests, and the virial sections of T1D/T2B. The slope formulas are assumptions. Predecessor fitted slopes, their Skyrme interpretation, and Option-C physical realizability are outside this claim.

## Independence
The main route solves the two simultaneous equations. The review algebraically inverts the map for arbitrary target slopes, obtaining `a=w-e` and `b=-(w+e)`, before substituting the half-slope target.

## Verification Status
The bidirectional exact linear map and wrong-option probes earn `symbolic_verified` for the conditional statement. They do not verify the imported virial model itself.

## Sensitivity and Counterexamples
Changing either target slope changes the recovered pair and fails the Option-C predicate. Options A and B produce `(1/2,-1/2)` and `(0,-1)`, so they fail distinct load-bearing conditions.

## Framework Compatibility
This is a compatible conditional classification with no fitted parameter. Its assumptions prevent a small algebraic result from being inflated into a physical Skyrmion or BEC claim.

## Dependency and Consumer Replay
The claim has no accepted-claim dependencies because its two formulas are declared assumptions. Direct consumers are the conditional API/test and future virial proposals. It supplies the exact classification subclaim needed by T1D/T2B.

## Competing Candidate Audit
Direct simultaneous solution and independent inversion were registered before execution. Numerical closeness of predecessor slope fits was not inspected or used for selection.

## Four-Axis Decision

The conditional linear theorem supports a compatible accepted status.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive conditional theorem

## Promotion Transaction
Promotion records `C-VIR-001`, freezes P007, includes it in `v0.7.0`, updates source dispositions, and regenerates canonical records.

## Continuation if Not Accepted
A failed inversion would reject the conditional selection and leave the physical candidates unselected; numerical fit could not substitute for the exact criterion.

## Done Gate
The exact iff statement, assumptions, inverse derivation, and wrong-target probes are complete with no claim debt.

## Cross-References
See `campaigns/P007-variational-scale`, T1D/T2B in the migration queue, and the parent effort.
