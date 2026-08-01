---
description: Independent review of C-TOP-001
author: vantasner-review
created: '2026-08-01T14:03:06Z'
updated: '2026-08-01T14:03:06Z'
tags:
- substrate-framework
- claim-review
- topology-labels
category: decisions
confidence: working
status: archived
---
# Review of C-TOP-001

## Claim Under Review
For integer additive winding, `p(w)=(-1)^w` is a homomorphism from `Z` to
`{+1,-1}`. Odd winding has label `-1`, even winding has `+1`, and adding any
even winding preserves the label while adding odd winding flips it. The claim
does not identify the label with fermionic exchange statistics, spin, baryon
number, electric charge, or a physical composite.

## Sourced Inputs
The review read `v0.16.0`, P019 and attempt `0001`, the topology-label APIs and
tests, both exact routes, hash-pinned EL2, its source adjudication, and the U1
claim ceilings. No pending Lean theorem, composite, Standard Model table, or
numeric Q-ball result is an input.

## Independence
The main verifier uses the proposed sign-character API and an algebraic residue
case split. The independent route explicitly maps integers to `Z/2Z` and then
maps the two residues to signs without importing the API.

## Verification Status
The residue proof, integer grids, and independent quotient construction earn
`symbolic_verified`. This status applies to the label algebra only and gives no
verification to a physical statistics representation.

## Sensitivity and Counterexamples
Nonintegers are rejected. Even dressing preserves the label over exact and
finite-grid tests; odd dressing flips it. Countermodels attach distinct
statistics, baryon, and charge assignments to the same odd label, proving the
physical mappings are absent.

## Framework Compatibility
The claim is a native pure-label root with no dependency on the conditional U1
sector. Its terminology and API docstring explicitly prevent EL2's
spin-statistics overreach.

## Dependency and Consumer Replay
The claim has no accepted dependencies. Consumers are the topology-label module
and tests, P019's verifier, EL2's disposition, and later governed topology work.
Thirteen focused topology/U1 tests pass.

## Competing Candidate Audit
The proposal registered exact label promotion, adjudication without an API, and
physical composite promotion. Reusable even/odd dressing operations select the
label API. Independent-label countermodels and the negative Derrick curvature
reject the physical composite route without comparator input.

## Four-Axis Decision

The exact sign character supports acceptance with a strict physical ceiling.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive pure topology-label root

## Promotion Transaction
Promotion adds topology-label APIs/tests, `C-TOP-001`, frozen P019 evidence,
`v0.17.0`, qualified EL2 disposition, and regenerated canonical records.

## Continuation if Not Accepted
A failed homomorphism would reject the label candidate. A pending
spin-statistics theorem could not repair the exact group law and would require
its own governed proposal.

## Done Gate
The positive label algebra, independent quotient proof, mutations, countermodels,
consumer replay, and source qualification are complete with no claim debt.

## Cross-References
See P019, EL2, `C-U1-001`, the topology-label module/tests, and the parent
migration effort.
