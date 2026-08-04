---
description: Independent review of exact two-body threshold claim C-KIN-001
author: vantasner-review
created: '2026-08-10T01:44:00Z'
updated: '2026-08-10T01:55:00Z'
tags: [substrate-framework, claim-review, kinematics, threshold]
category: decisions
confidence: established
status: archived
---
# Review of C-KIN-001

## Claim Under Review

C-KIN-001 states the exact residual mass-shell theorem at center-of-mass
two-body threshold. For positive masses and real observed rapidity, subtracting
one on-shell particle from `(m1+m2,0)` leaves defect
`2*m1*(m1+m2)*(1-cosh(theta))` relative to the second mass. It vanishes only at
zero recoil, where both particles are at rest.

## Sourced Inputs

The review reads v0.114.0, frozen P149 and revision 0001, hash-pinned W4 and its
dossier and imported outcome catalog, attempts 0001 through 0008, accepted
sine-Gordon and boundary ceilings, the new exact module, focused tests, primary
and independent verifiers, and the six-node graph. Source values, charge labels,
detector semantics, W3's rejected physical current, and the neutrino analogy
remain outside the claim delta.

## Independence and Verification

The canonical route returns an exact immutable ledger. The independent route
imports none of it: it uses a Minkowski metric matrix, subtracts components,
and rewrites `cosh(theta)` through the positive coordinate `u=exp(theta)`. The
defect becomes `-m1*(m1+m2)*(u-1)^2/u`, making nonpositivity and the unique
equality point manifest. The maximum verdict is symbolic_verified.

Primary, independent, focused, and graph routes pass 33, 15, 13, and 25 checks.
The graph pins six nodes, 63 source predicates, and six assertions. At W4's
exact `v=3/5` point, mutation and counterexample checks obtain observed `(10,6)`
and residual `(6,-6)`, whose invariant is zero rather than 64. Raising total
energy from 16 to 20 restores two mass-eight shells. Flipping residual momentum
preserves its invariant but breaks vector closure.

## Framework Compatibility and Consumers

The claim is a dependency-free compatible exact extension. It changes no
accepted sine-Gordon normalization, boundary convention, current, state, or
interaction. Its API is pure, exact-input, and additive, with no quadrature or
NumPy integration compatibility shape. GitNexus reports LOW risk, zero indexed
upstream callers, and no affected flow; its untracked-file mapping limitation
is covered by direct tests and oracles. Pending W5 and NA1 gain no authority
from W4's rejected readings.

## Competing Candidate and Four-Axis Decision

Literal reproduction alone is rejected as headline support. The accepted
scalar threshold partition is not duplicated. The two-body kinematic candidate
is the smallest novel positive theorem; absent boundary evolution blocks a
flux claim, and countermodels delimit observability. No numeric comparator
selected it.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: dependency-free additive exact threshold theorem

## Promotion and Continuation

Promotion adds the exact module and tests, package exports, C-KIN-001, release
v0.115.0, generated records, and qualified W4 disposition. W4's rejected
physical objective remains open only to a future proposal that supplies evolved
boundary stress-energy flux, complete reservoirs, on-shell outgoing states,
detector reconstruction, and independently derived currents and interactions.

## Done Gate and Cross-References

Exact derivation, equality condition, zero and above-threshold limits,
mutations, independent proof, implementation, compatibility, nonduplication,
dependency and consumer closure, W4 qualification, release, and generated state
close with an empty ledger. See P149, W4, C-SG-005, C-SG-008, C-SG-012,
C-BND-001, `relativistic_thresholds.py`, its tests, and all P149 audits.
