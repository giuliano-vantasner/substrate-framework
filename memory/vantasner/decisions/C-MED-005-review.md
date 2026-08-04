---
description: Independent review of SI mechanical-conversion claim C-MED-005
author: vantasner-review
created: '2026-08-09T18:55:00Z'
updated: '2026-08-09T18:55:00Z'
tags: [substrate-framework, claim-review, constitutive, SI-units]
category: decisions
confidence: established
status: archived
---
# Review of C-MED-005

## Claim Under Review

C-MED-005 states the exact conditional conversion from SI electromagnetic
response coefficients to mechanical mass density, stiffness, wave speed, and
quadratic strain energy. In SI base order M,L,T,I, both multiplicative
conversion factors require dimension M^2*T^-4*I^-2. The mechanical and
electromagnetic wave speeds agree exactly iff the positive factors agree, while
their common scale remains arbitrary. A dimensionless strain amplitude is
required for energy, and neither a material nor a gravity coupling is derived.

## Sourced Inputs

The review reads v0.111.0, frozen P145 and revision 0001, hash-pinned G5 and its
dossier, attempts 0001 through 0005, the canonical constitutive and gravity-
dimension modules, focused tests, primary and independent verifiers, official
BIPM SI definitions, current NIST CODATA comparator values, and the fourteen-
node graph. C-MED-001 supplies only the accepted conditional wave-response
ratio. C-MED-002, C-DIM-002, C-IDN-001, and C-GRV-001 are neighboring ceilings.
G5's density, energy, prediction-count, gravity, material, and substrate
subclaims remain outside the claim delta.

## Independence

The canonical route uses the new constitutive ledgers. The independent review
imports none of those new APIs. It reconstructs every M,L,T,I column from SI
units, solves both conversion dimensions, eliminates the two-factor speed
ratio, derives the common rescaling orbit and amplitude-aware energy directly,
builds the four-row log design, and restores energy- and mass-source Einstein
coupling dimensions independently.

## Verification Status

The maximum verdict is symbolic_verified. The primary route passes 36 checks,
the independent route passes 20, and 17 focused package tests pass. The graph
route passes 34 checks over fourteen nodes and 145 source predicates. All
promoted obligations use exact SymPy integers, rationals, matrices, and declared
exact inputs. Native G5's loose decimal regressions are source evidence only and
do not enter the accepted theorem, thresholds, or selection.

## Sensitivity and Counterexamples

Changing the electric-current exponent of the conversion breaks both
mechanical unit maps. Taking unequal positive conversion factors changes
mechanical speed by their ratio; setting the stiffness factor to twice the
inertia factor doubles speed squared. Common rescaling changes density,
stiffness, and energy but not speed. Changing strain from one to two multiplies
energy and mass-equivalent density by four while leaving speed fixed. Bare
epsilon/2 and inverse-mu/2 retain electromagnetic rather than mechanical units.
Free kappa realizes any target G/c^2 ratio, and assigning bare G to either an
energy- or mass-density Einstein source fails the source-dimension ledger.

## Framework Compatibility

The claim is a compatible exact extension of C-MED-001. It preserves
C-MED-002's abstract, declared dictionary while forbidding an undeclared
substitution of measured SI epsilon0. It adds no physical material, absolute
scale, field amplitude, gravity coupling, observation, or substrate identity.
The new exact-input APIs are pure and additive. GitNexus reports LOW risk and
no affected execution process.

## Dependency and Consumer Replay

The accepted dependency closure is C-MED-005 to C-MED-001. Four qualified G
source dependencies grant no rejected authority. The frozen graph covers G5,
G1 through G4, and nine reverse consumers, inventories 145 predicates, and
passes 34 checks. W5 remains pending, QCD1 and SM1 are lexical G5 false
positives, four qualified consumers retain independent closure, and two
duplicate consumers remain duplicate. Immutable G1 and G4 retain their
alias-only legacy integration shapes; G5 and every mutable P145 file have no
legacy integration access.

## Competing Candidate Audit

Literal G5 is rejected as headline support because its unit checks omit L2 and
L3 and its linkage guard counts names. The exact SI ledger, dimensioned common-
conversion theorem, source-typed gravity ceiling, rank audit, rescaling
countermodels, and governance route were registered before implementation.
C-MED-005 is selected for dimensional correctness, assumption economy,
sensitivity, exact-input reusability, and distinct consumer value, independent
of numerical agreement.

## Four-Axis Decision

The exact conditional SI conversion theorem earns acceptance while G5's
physical density, energy, prediction, and gravity narrative is qualified.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive exact constitutive theorem depending on C-MED-001

## Promotion Transaction

Promotion adds constitutive dataclasses and APIs, package exports, focused
tests, C-MED-005, release v0.112.0, generated claim and release records, and a
qualified G5 disposition. The queue is regenerated from
migration/dispositions.yaml; generated docs and accepted memory are rendered
from canonical inputs. Primary, independent, graph, focused, governance, and
one integrated repository gate must all pass.

## Continuation if Not Accepted

This clause is inactive for C-MED-005. It remains active for G5's rejected
physical objective: a future proposal must supply a dimensionally valid
calibration from a material action, a field or strain state, independently
measured constraints, and a source-typed gravitational coupling without using
the desired density or Newton value as input.

## Done Gate

Exact unit columns, conversion iff, free-scale orbit, amplitude-aware energy,
mutations, independent derivation, implementation, dependency and consumer
closure, compatibility, nonduplication, source qualification, release, and
generated-state synchronization close with an empty campaign ledger.

## Cross-References

See P145, G5, C-MED-001, C-MED-002, C-IDN-001, C-GRV-001,
constitutive.py, test_constitutive.py, the source and literature audits,
impact analysis, independent derivation, and frozen source graph.
