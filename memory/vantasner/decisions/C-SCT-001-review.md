---
description: Independent review of exact passive half-line scattering claim C-SCT-001
author: vantasner-review
created: '2026-08-10T02:48:00Z'
updated: '2026-08-10T02:48:00Z'
tags: [substrate-framework, claim-review, boundary-scattering, passivity]
category: decisions
confidence: established
status: archived
---
# Review of C-SCT-001

## Claim Under Review

C-SCT-001 states the exact passive harmonic scattering ledger for a massless
scalar on the right half-line. It fixes wave directions, boundary sign,
amplitude, power, energy rate, reciprocal-impedance degeneracy, and the ceiling
on an optionally declared reference-channel contrast.

## Sourced Inputs

The review reads v0.115.0, frozen P150 and revision 0001, hash-pinned W5, its
dossier and imported piston equations, attempts 0001 through 0008, accepted
boundary, scalar-stress, representation, kinematic, and branching ceilings,
the new exact module, focused tests, primary and independent verifiers, and the
thirteen-node graph. Source physical labels and pending W7, M1, and M2 authority
remain outside the claim delta.

## Independence and Verification

The canonical route returns an exact immutable ledger. The independent route
imports none of it: it differentiates the two harmonics directly, solves the
boundary residual, integrates the canonical energy sign, and derives rational
reciprocity and contrast identities. The maximum verdict is
symbolic_verified.

Primary, independent, focused, and graph routes pass 32, 17, 15, and 46 checks.
The graph pins thirteen nodes, 154 source predicates, and fourteen assertions.
Mutations reverse wave roles, boundary sign, reference normalization, and
storage closure. The preserved failed attempts establish that each single sign
or role reversal inverts the amplitude ratio and that W5's double mistake
cancels only in the displayed algebra.

## Framework Compatibility and Consumers

The claim is a compatible exact extension depending only on C-BRN-001 for its
optional contrast. It changes no accepted scalar normalization, boundary API,
current, state, or interaction. Its API is pure, exact-input, additive, and has
no quadrature or NumPy compatibility shape. GitNexus reports LOW risk, zero
indexed upstream callers, zero affected modules, and no affected flow. Pending
W7 and YM1 gain no physical authority from W5.

## Competing Candidate and Four-Axis Decision

Literal reproduction alone is rejected as headline support. Correct passive
scattering is the smallest novel theorem; C-BRN-001 prevents duplication,
direct action elimination rejects the local piston claim, reciprocity limits
identifiability, and countermodels delimit parity and weak readings. No source
value selected the candidate.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive exact scattering theorem depending on C-BRN-001

## Promotion and Continuation

Promotion adds the exact module and tests, package exports, C-SCT-001, release
v0.116.0, generated records, and qualified W5 disposition. A physical chiral
asymmetry or weak interaction remains open only to a future proposal supplying
states, parity action, current, coupling, complete boundary dynamics, detector
map, and event data.

## Done Gate and Cross-References

Exact derivation, passivity, limits, reciprocal degeneracy, mutations,
independent proof, implementation, compatibility, nonduplication, dependency
and consumer closure, W5 qualification, release, and generated state close
with an empty ledger. See P150, W5, C-BRN-001, C-BND-001, C-SG-012,
`boundary_scattering.py`, its tests, and all P150 audits.
