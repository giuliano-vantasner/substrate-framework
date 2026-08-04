---
description: Independent review of SU2 carrier-factor claim C-REP-002
author: vantasner-review
created: '2026-08-09T22:50:00Z'
updated: '2026-08-09T22:50:00Z'
tags: [substrate-framework, claim-review, representation, su2]
category: decisions
confidence: established
status: archived
---
# Review of C-REP-002

## Claim Under Review

C-REP-002 states the exact separation theorem for a standard irreducible SU2
carrier and an independent Hermitian-projector factor. Tensor-factor left and
right generators are Hermitian and close, a declared factor exchange gives
vector-even and axial-odd combinations, the fundamental commutant is scalar,
and a common Abelian charge has unit doublet separation. It explicitly supplies
no physical state, chirality, gauge, interaction, or weak-sector identity.

## Sourced Inputs

The review reads v0.113.0, frozen P147 and revision 0001, hash-pinned W2 and its
dossier, imported Lean and solution artifacts, attempts 0001 through 0006,
accepted spin, sine-Gordon, boundary, and representation modules, focused tests,
the primary and independent verifiers, and the 24-node source graph. C-SPN-002
supplies only the accepted normalized abstract SU2 representation. All W2
labels, event values, physical names, same-carrier semantics, and desired guard
verdicts remain outside the claim delta.

## Independence

The canonical route uses the new ledger APIs. The independent review imports
none of them. It builds fresh Pauli-half matrices, solves the full intertwiner
system, constructs block tensor actions directly, checks adjoints and cyclic
commutators, solves the common-charge equations, and exercises independent
generator, projector, exchange, and label mutations.

## Verification Status

The maximum verdict is symbolic_verified. The primary route passes 49 checks,
the independent route passes 25, and fourteen focused package tests pass. The
graph route passes 83 checks over 24 pinned units, 234 source predicates, and
26 assertions. Every promoted obligation uses exact SymPy expressions and
declared exact inputs; no numerical closeness or source witness enters it.

## Sensitivity and Counterexamples

Doubling one generator breaks the fixed normalization and commutator. A
non-idempotent projector is rejected. Moving a rank-one projector onto the
isospin carrier produces two non-Hermitian matrices and three failed
commutators. An identity parity map cannot exchange complementary projectors.
Changing the lower label destroys the fixed unit gap. The plus-minus-one W2
pair is an exact counterexample to compatibility with one common scalar
Abelian shift.

## Framework Compatibility

The claim is an additive exact extension depending only on C-SPN-002. It
preserves that claim's standard carrier and normalization and adds no physical
state or dynamics. The package APIs are pure, exact-input, and additive.
GitNexus reports LOW risk and no affected execution process; its inability to
map untracked new definitions is covered by direct exports, tests, verifiers,
and the integrated gate.

## Dependency and Consumer Replay

The accepted closure is C-REP-002 to C-SPN-002. W2's thirteen source
dependencies include six pending nodes and seven dependency-consumer cycles;
none supplies accepted authority to the theorem. The frozen graph covers
seventeen reverse consumers. Qualified neighboring units retain independent
claims, duplicate WM2 gains no authority, and pending consumers may import only
the exact theorem rather than W2's rejected state, charge, chirality, or gauge
readings.

## Competing Candidate Audit

Literal reproduction alone is source evidence. Existing C-SPN-002 prevents
duplicate promotion of the Pauli algebra. The preregistered full-commutant and
independent-factor candidates jointly provide the smallest natural exact
extension; the missing-dynamics candidate establishes the explicit ceiling,
and governance closure delimits consumers. No source output selected them.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive exact representation theorem depending on C-SPN-002

## Promotion Transaction

Promotion adds four ledger dataclasses and APIs, package exports, focused tests,
C-REP-002, release v0.114.0, generated claim and release records, and a
qualified W2 disposition. The queue, generated docs, and accepted memory are
rendered from canonical inputs. Primary, independent, graph, focused,
governance, and one integrated repository gate must all pass.

## Continuation if Not Accepted

This clause is inactive for the exact theorem. It remains active for W2's
physical objective: a future proposal must construct provenance-bearing matter
states on independent Lorentz and internal carriers, a common charge action, a
connection and covariant derivative, an action and current, anomaly and parity
analysis, boundary evolution, and independently derived observables.

## Done Gate

Carrier normalization, full commutant, tensor-factor closure, parity exchange,
charge spectrum, wrong-carrier counterexamples, mutations, independent
derivation, implementation, source adjudication, graph closure, release, and
generated-state synchronization close with an empty campaign ledger.

## Cross-References

See P147, W2, C-SPN-002, C-REP-001, C-SG-011, C-BND-001,
su2_doublets.py, test_su2_doublets.py, source and predicate audits, dependency
and consumer audits, impact analysis, independent derivation, and frozen graph.
