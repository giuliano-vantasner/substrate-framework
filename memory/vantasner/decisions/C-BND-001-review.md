---
description: Independent review of scalar boundary parity claim C-BND-001
author: vantasner-review
created: '2026-08-09T20:35:00Z'
updated: '2026-08-09T20:35:00Z'
tags: [substrate-framework, claim-review, boundary, parity]
category: decisions
confidence: established
status: archived
---
# Review of C-BND-001

## Claim Under Review

C-BND-001 states the exact parity and underdetermination theorem for the affine
scalar boundary residual `R=a*u+beta*v-J`. Scalar fixed-coordinate parity maps
`beta` to `-beta`; a fixed residual is invariant for arbitrary traces iff
`beta=0`; the residual splits into even `a*u-J` and odd `beta*v` parts. A
simultaneous right-to-left half-line parity map preserves the outward-normal
coefficient. One residual leaves a one-parameter trace family and supplies no
sign correlation or topological transfer without extra dynamics and vacuum
data.

## Sourced Inputs

The review reads v0.112.0, frozen P146 and revision 0001, hash-pinned W1 and its
dossier, attempts 0001 through 0005, the canonical boundary and sine-Gordon
modules, focused tests, primary and independent verifiers, and the eleven-node
source graph. C-SG-001, C-SG-011, and C-SG-013 supply only their accepted
equation, characteristic, parity, correlation, and charge-transfer ceilings.
W1's numeric witnesses, charge map, fermion map, chiral labels, and weak-sector
interpretation remain outside the claim delta.

## Independence

The canonical route uses the new boundary ledgers. The independent review
imports none of those APIs. It represents the affine residual as a row acting
on augmented trace space, derives parity projectors by matrix algebra, solves
the invariance and pure-odd conditions, reconstructs the right-to-left normal
map, computes row nullity and a general solution family, and gives a fresh
periodic counterexample separating sign correlation from field change.

## Verification Status

The maximum verdict is symbolic_verified. The primary route passes 39 checks,
the independent route passes 23, and 21 focused package tests pass. The graph
route passes 45 checks over eleven nodes, 129 source predicates, and ten source
assertions. All promoted obligations use exact SymPy expressions and declared
exact inputs. W1's alias-only NumPy replay is source evidence only and supplies
no accepted threshold or witness value.

## Sensitivity and Counterexamples

Removing the spatial-trace sign from parity breaks coefficient reflection.
Changing the trace-family sign leaves residual `2*a*u`. Giving the scalar
source intrinsic odd parity changes the pullback by `2*J`, demonstrating why
source transformation is a load-bearing assumption. Keeping the wrong
left-domain orientation changes the normal residual by `2*beta*v`. A periodic
trace has nonzero aligned sign correlation and zero field change. W1's
epsilon-plus chiral witness leaves residual `J`, while its temporal-only vector
law permits every coordinate trace rather than forcing zero.

## Framework Compatibility

The claim is a compatible exact extension of C-SG-013 through C-SG-011 and
C-SG-001. It preserves the normalized sine-Gordon field convention and the
existing distinction between correlation and topological transfer. It adds no
boundary action, field evolution, charge selection, chiral matter, fermionic
state, gauge law, or weak interaction. The new exact-input APIs are pure and
additive. GitNexus reports LOW risk and no affected execution process.

## Dependency and Consumer Replay

The accepted closure is C-BND-001 to C-SG-013 to C-SG-011 to C-SG-001. W1's
source dependencies NC1 and NC4 grant no rejected authority. The frozen graph
covers W1, both dependencies, and nine reverse consumers. Accepted NC1, NC2,
and NC3 remain independently closed. Pending W2, W3, W5, W7, M1, and WM7 gain
no authority from W1's rejected readings. Immutable W1, NC4, and W3 retain
their exact alias-only legacy integration shapes; mutable P146 and canonical
code contain no legacy integration access.

## Competing Candidate Audit

Literal reproduction alone is rejected as headline support. The exact
fixed-coordinate pullback, outward-normal domain map, and symmetry classifier
were registered before implementation and jointly selected as the smallest
positive theorem. The missing boundary action blocks a dynamical expansion,
while source-data countermodels and governance closure delimit consumers. No
source witness or comparator selected the concept.

## Four-Axis Decision

The exact boundary parity theorem earns acceptance while W1's physical parity,
charge, chiral, fermionic, and weak-sector narrative is qualified.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive exact boundary theorem depending on C-SG-013

## Promotion Transaction

Promotion adds three boundary ledger dataclasses and APIs, package exports,
focused tests, C-BND-001, release v0.113.0, generated claim and release records,
and a qualified W1 disposition. The queue is regenerated from
`migration/dispositions.yaml`; generated docs and accepted memory are rendered
from canonical inputs. Primary, independent, graph, focused, governance, and
one integrated repository gate must all pass.

## Continuation if Not Accepted

This clause is inactive for C-BND-001. It remains active for W1's rejected
physical objective: a future proposal must supply a boundary action or declared
dynamical law, evolved solutions, vacuum-endpoint charge data, independently
derived charge and fermion maps, and a weak-sector embedding without importing
the desired labels as premises.

## Done Gate

Exact parity pullback, fixed-theory criterion, even/odd projectors, oriented
normal map, trace family, mutations, counterexamples, independent derivation,
implementation, dependency and consumer closure, compatibility,
nonduplication, source qualification, release, and generated-state
synchronization close with an empty campaign ledger.

## Cross-References

See P146, W1, C-SG-001, C-SG-011, C-SG-013,
boundary_correlations.py, test_boundary_correlations.py, the source,
predicate, dependency, consumer, and nonduplication audits, impact analysis,
independent derivation, and frozen source graph.
