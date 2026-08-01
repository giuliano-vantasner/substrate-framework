---
description: Independent review of C-SG-006
author: vantasner-review
created: '2026-08-01T12:37:56Z'
updated: '2026-08-01T12:37:56Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- secant-scale
category: decisions
confidence: working
status: archived
---
# Review of C-SG-006

## Claim Under Review
For `0<omega<1`, define the secant action scale `H=E/omega`. Then
`H=16*sqrt(1-omega^2)/omega` is positive and strictly decreasing from positive
infinity to zero. The ratio `Pi=J/H=omega*acos(omega)/sqrt(1-omega^2)` is
strictly increasing from zero to one, so `0<J<H`. Moreover `dE/dH=omega^3`,
whereas the canonical action satisfies `dE/dJ=omega`; hence `H` is not the
canonical action away from the harmonic endpoint.

## Sourced Inputs
The review read `v0.10.0`, `C-SG-002/003`, P011 attempts `0001`–`0003`, the
sine-Gordon API/tests, HE4, and its source adjudication. No HE1/HE2 conclusion,
Planck interpretation, or literature spectrum is imported.

## Independence
The main route composes accepted frequency formulas through the new APIs. The
review instead sets `theta=acos(omega)`, so `E=16*sin(theta)`, `J=16*theta`,
`H=16*tan(theta)`, and `Pi=theta*cot(theta)`. It does not import the proposed
secant APIs.

## Verification Status
Exact calculus establishes all formulas, derivatives, endpoint limits, and
global monotonicity. The positive derivative numerator is certified by its
exact derivative and endpoint. The claim earns `symbolic_verified`.

## Sensitivity and Counterexamples
Changing the energy coefficient, frequency divisor power, or action coefficient
breaks the coupled scale/ratio predicate. The exact identity
`dE/dH=omega^3` rejects the action-variable interpretation everywhere inside
the open interval because `omega^3-omega=-omega*(1-omega^2)<0`.

## Framework Compatibility
The claim is a native consequence of `C-SG-002/003`, adds no parameter, and
uses precise secant semantics. The endpoint agreement with `J` is a limit, not
an equality on the family and not a universal constant.

## Dependency and Consumer Replay
Dependencies are `C-SG-002/003`. Direct consumers are the sine-Gordon module,
exports/tests, HE4's disposition, and future HE1/HE2 audits. Existing energy,
action, and gradient consumers remain unchanged.

## Competing Candidate Audit
Direct accepted-formula composition, repeated field integration, and
literature-led selection were preregistered. Dependency closure selects the
first. The second duplicates accepted action evidence; the third is comparator-
led and unnecessary. External values were quarantined until after selection.

## Four-Axis Decision

The exact native consequence supports acceptance.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive consequence of C-SG-002/003

## Promotion Transaction
Promotion adds secant-scale APIs/tests and `C-SG-006`, freezes P011, creates
`v0.11.0`, qualifies HE4 with durable source evidence, and regenerates canonical
records.

## Continuation if Not Accepted
A global-inequality failure returns to the angle-coordinate proof. Literature
agreement cannot repair a failed classical identity.

## Done Gate
The positive classification, independent angle route, mutations, endpoint
ceiling, and consumers are complete with no claim debt.

## Cross-References
See `C-SG-002`, `C-SG-003`, P011, HE4, the sine-Gordon module/tests, and the
parent migration effort.
