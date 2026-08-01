---
description: Independent review of C-LIE-001
author: vantasner-review
created: '2026-08-01T15:07:43Z'
updated: '2026-08-01T15:07:43Z'
tags:
- substrate-framework
- claim-review
- su3-invariants
category: decisions
confidence: working
status: archived
---
# Review of C-LIE-001

## Claim Under Review
For the eight explicit standard fundamental SU(3) generators
`T_a=lambda_a/2`, the claim fixes trace normalization, commutator convention,
structure constants, and the exact invariants `T_F=1/2`, `C_F=4/3`, and
`C_A=3`, including both adjoint-Casimir constructions.

## Sourced Inputs
The review read `v0.20.0`, P024, attempt `0001`, package APIs/tests, both exact
derivations, hash-pinned QCD3, and its source adjudication. No loop weight,
physical flavor count, YM1, or EM5 statement enters this claim.

## Independence
The main route constructs commutators, structure constants, and adjoint
matrices. The independent route redefines the matrices locally and verifies the
fundamental completeness relation component by component, then derives the
fundamental Casimir and total trace without importing the package.

## Verification Status
Exact matrix equality supports `symbolic_verified`. Twenty-seven joint main
checks and five independent checks cover the composite campaign; the Lie claim
is exercised by every generator pair, all component completeness identities,
two adjoint-Casimir routes, and representation consistency.

## Sensitivity and Counterexamples
Doubling generator normalization breaks the trace and structure-constant
values. Reversing all generators preserves quadratic traces but flips the
declared `f_123=1` orientation, so the joint convention check fails. Index
domain guards and exact known components prevent a weak aggregate-only oracle.

## Framework Compatibility
The claim is a native exact mathematical root. Its convention is encoded once
in the package and introduces no physical parameter or unaccepted field-theory
premise.

## Dependency and Consumer Replay
There are no accepted scientific dependencies. Direct consumers are the SU(3)
APIs/tests, P024, `C-RGE-002`, QCD3's disposition, and future QCD-sector audits.
Nineteen focused SU(3)/renormalization tests pass with no debt.

## Competing Candidate Audit
The proposal separated combined conditional promotion, Lie-only promotion, and
physical substrate closure before reading QCD3. Exact matrices select the Lie
claim independently of the conditional coefficient decision.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: new exact standard-representation root

## Promotion Transaction
Promotion adds pure SU(3) APIs/tests, P024 evidence, `C-LIE-001`, qualified QCD3
disposition, a pinned release, and regenerated canonical records.

## Continuation if Not Accepted
A convention or completeness failure would reject the representation claim and
require a new explicit basis; loop physics could not repair it.

## Done Gate
The exact representation, independent completeness route, mutations, consumers,
source qualification, and debt closure are complete.

## Cross-References
See P024, QCD3, `C-RGE-002`, SU(3) APIs/tests, and the parent migration effort.
