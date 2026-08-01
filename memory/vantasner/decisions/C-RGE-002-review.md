---
description: Independent review of C-RGE-002
author: vantasner-review
created: '2026-08-01T15:07:43Z'
updated: '2026-08-01T15:07:43Z'
tags:
- substrate-framework
- claim-review
- conditional-one-loop-coefficient
category: decisions
confidence: working
status: archived
---
# Review of C-RGE-002

## Claim Under Review
Conditional on `C-LIE-001`, nonnegative integer `n_f`, and declared one-loop
weights `11/3` for the gauge-plus-ghost term and `4/3` for Dirac fundamentals,
the coefficient is `b0=11-(2/3)n_f`. It is positive for integer `n_f<=16`,
negative from 17 onward, and gives `b0=7` at declared `n_f=6`. Combined with
`C-RGE-001`, positive cases have decreasing one-loop ultraviolet running.

## Sourced Inputs
The review read `v0.20.0`, `C-RGE-001`, proposed `C-LIE-001`, P024, both exact
derivations, package APIs/tests, hash-pinned QCD3, and its source adjudication.
The loop weights are explicit premises, not outputs of the matrix computation.

## Independence
The main route calls a helper whose loop weights remain arguments and mutates
each group factor and weight. The independent route substitutes exact invariant
values outside the helper and recomputes the integer threshold; it also changes
the matter weight to demonstrate threshold sensitivity.

## Verification Status
Exact substitution, solving, sign checks, derivative, and limit support
`symbolic_verified`. QCD3's NumPy sweep is correctly downgraded to regression
because exact `C-RGE-001` calculus already fixes the behavior.

## Sensitivity and Counterexamples
Mutating `C_A`, `T_F`, `11/3`, or `4/3` changes the coefficient and fails the
baseline. Changing the matter weight moves the critical flavor count. Deleting
the gauge term leaves `-(2/3)n_f`, negative for positive declared flavor count.

## Framework Compatibility
The claim is a compatible conditional extension of `C-RGE-001`. It closes an
exact SU(3) specialization while explicitly retaining the perturbative formula,
field representation, flavor content, and one-loop regime as premises. It
asserts no substrate/QCD identity, unique group selection, or confinement.

## Dependency and Consumer Replay
Direct dependencies are `C-LIE-001` and `C-RGE-001`. Consumers are the
weight-explicit coefficient API/test, P024, QCD3's disposition, and pending CF4,
AS1, EL, and QCD audits. Nineteen focused tests pass and no debt remains.

## Competing Candidate Audit
Combined conditional promotion was selected over Lie-only promotion because the
weight-explicit helper adds a distinct safe consumer. Physical closure was
rejected because YM1/EM5 and substrate field content remain unaccepted.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: conditional composition of C-LIE-001 and C-RGE-001

## Promotion Transaction
Promotion adds the conditional coefficient API/test, individual registry entry,
P024 evidence, qualified QCD3 disposition, release manifest, and generated
records. Imported weights remain visible in API and claim assumptions.

## Continuation if Not Accepted
A weight-sensitivity or threshold failure would reject the specialization. A
physical beta-function derivation would require a separate loop campaign.

## Done Gate
The exact conditional coefficient, independent threshold, mutations, limits,
consumers, source qualification, and debt closure are complete.

## Cross-References
See `C-LIE-001`, `C-RGE-001`, P024, QCD3, SU(3)/renormalization APIs, and the
parent migration effort.
