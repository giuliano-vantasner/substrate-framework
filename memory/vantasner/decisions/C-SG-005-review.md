---
description: Independent review of C-SG-005
author: vantasner-review
created: '2026-08-01T12:14:50Z'
updated: '2026-08-01T12:14:50Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- threshold-deficit
category: decisions
confidence: working
status: archived
---
# Review of C-SG-005

## Claim Under Review
For `0<omega<1`, the accepted breather's deficit below the normalized two-kink threshold is `Delta=16-E=16*(1-sqrt(1-omega^2))`. It lies strictly between 0 and 16, increases strictly, is strictly convex, tends to 0 as `omega->0+`, tends to 16 as `omega->1-`, and satisfies `E+Delta=16` exactly.

## Sourced Inputs
The review read `v0.8.0`, `C-SG-002`, P009 and attempt `0001`, the sine-Gordon API/tests, T1E, and its source adjudication. Threshold 16 and the energy function are accepted dependencies. No cross-program lift or interaction potential is imported.

## Independence
The main route computes the accepted threshold complement through the package API. The review does not import that API; it integrates the exact positive marginal energy loss `16*u/sqrt(1-u^2)` from the threshold endpoint to `omega` and obtains the same function.

## Verification Status
Exact algebra, derivatives, limits, rationalization, and the independent definite integral establish the full open-domain statement. The claim earns `symbolic_verified`. “Threshold deficit” accurately describes the proven energy difference without asserting a separate dynamical binding mechanism.

## Sensitivity and Counterexamples
Threshold 8, energy coefficient 15, and power one each fail the exact function. The independent integral also rejects the wrong linear-power complement at `omega=3/5`.

## Framework Compatibility
The claim is a native consequence of `C-SG-002`, preserves normalized conventions, adds no parameter, and remains distinct from `C-SG-004`'s averaged gradient integral.

## Dependency and Consumer Replay
The sole dependency is `C-SG-002`. Direct consumers are `sine_gordon.py`, exports/tests, T1E's disposition, and future threshold/stability work. Existing energy, action, and gradient consumers are unchanged.

## Competing Candidate Audit
Direct complement, independent marginal integration, and action representation were preregistered. The first two give closure without adding `C-SG-003`; no comparator influenced selection.

## Four-Axis Decision

The exact native consequence supports acceptance.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive consequence of C-SG-002

## Promotion Transaction
Promotion adds the API/test and `C-SG-005`, freezes P009, creates `v0.9.0`, qualifies T1E with durable evidence, and regenerates canonical records.

## Continuation if Not Accepted
Any integral disagreement returns to endpoint and sign conventions. A declared program lift cannot repair the one-sector energy difference.

## Done Gate
The positive function, global behavior, independent construction, mutations, semantic ceiling, and consumers are complete with no claim debt.

## Cross-References
See `C-SG-002`, `C-SG-004`, `campaigns/P009-breather-threshold-gap`, T1E, and the parent effort.
