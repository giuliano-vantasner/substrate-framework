---
description: Independent review of C-SG-008
author: vantasner-review
created: '2026-08-01T12:46:13Z'
updated: '2026-08-01T12:46:13Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- lorentz-kinematics
category: decisions
confidence: working
status: archived
---
# Review of C-SG-008

## Claim Under Review
For an accepted breather with `0<omega<1` and a real boost `|v|<1`, let
`gamma=(1-v^2)^-1/2`. The boosted phase components are
`(Omega,k)=(gamma*omega,gamma*omega*v)` and energy-momentum is
`(E,P)=(gamma*E0,gamma*E0*v)`. They obey
`(E,P)=H(omega)*(Omega,k)`, where `H=E0/omega`, and invariant norms
`Omega^2-k^2=omega^2` and `E^2-P^2=E0^2`. Ratio formulas are corollaries only
when their denominators are nonzero.

## Sourced Inputs
The review read `v0.11.0`, `C-SG-001/002/006`, P012 and attempt `0001`, the
sine-Gordon API/tests, HE1, and its source adjudication. No quantum or universal-
constant premise is imported.

## Independence
The main route uses the proposed velocity APIs. The review instead parameterizes
the boost by rapidity and reconstructs both vectors with `cosh` and `sinh`; it
does not import the proposed boost APIs.

## Verification Status
Exact Lorentz algebra establishes both components, invariant norms,
proportionality, phase/group-velocity corollaries, and the regular rest limit.
The claim earns `symbolic_verified`.

## Sensitivity and Counterexamples
Wrong phase frequency, phase spatial sign, energy coefficient, or momentum
boost factor breaks the coupled vector-and-norm predicate. Replacing the boosted
frequency by a time-dilated value or dropping gamma from momentum also fails.

## Framework Compatibility
The claim is a native kinematic consequence of `C-SG-001/002/006`, adds only a
boost coordinate, and preserves normalized signs. It explicitly inherits the
family dependence of `H`; no Planck or quantum interpretation is introduced.

## Dependency and Consumer Replay
Dependencies are `C-SG-001/002/006`. Direct consumers are boost APIs/tests,
HE1's disposition, and future HE3 audits. Existing rest-frame formulas remain
unchanged.

## Competing Candidate Audit
Full vector proportionality, ratio-only algebra, and a universal-constant
reading were preregistered. Covariance and the regular rest limit select the
first. The second is weaker; the third contradicts `C-SG-006`.

## Four-Axis Decision

The exact native consequence supports acceptance.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive consequence of C-SG-001/002/006

## Promotion Transaction
Promotion adds boost APIs/tests and `C-SG-008`, freezes P012, creates `v0.12.0`,
qualifies HE1 with durable evidence, and regenerates canonical records.

## Continuation if Not Accepted
A sign failure returns to explicit covector/vector convention separation. Ratio
identities cannot repair a failed invariant norm.

## Done Gate
The positive vector relation, independent rapidity route, mutations, rest guard,
semantic ceiling, and consumers are complete with no claim debt.

## Cross-References
See `C-SG-001`, `C-SG-002`, `C-SG-006`, P012, HE1, the sine-Gordon module/tests,
and the parent migration effort.
