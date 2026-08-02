---
description: Independent review of C-CHR-001 cyclic and binary sign-character classification
author: vantasner-review
created: '2026-08-03T01:50:00Z'
updated: '2026-08-03T01:50:00Z'
tags:
- substrate-framework
- claim-review
- sign-characters
category: decisions
confidence: established
status: archived
---
# C-CHR-001 Claim Review

## Claim Under Review

C-CHR-001 classifies every homomorphism from a finite cyclic group or positive-
rank binary product group to the multiplicative signs. It states exact
generator images, kernels, quotient order, faithfulness, character counts, and
the distinction between equal point values and function identity. It derives no
OM1 source-domain, representation, operator, topology, statistics, or physical
mechanism.

## Sourced Inputs

The review reads release `v0.59.0`, C-TOP-001 and its P019 quotient evidence,
the frozen P066 domain/equality contract, hash-pinned OM1, attempts 0001 and
0002, source audit and adjudication, primary provenance, canonical module and
tests, both exact verifier routes, and the impact boundary. Pending B1, G2,
NA1, T1Z2, and W7 supply no premise.

## Independence

The independent review imports no topological-label API. It enumerates every
function C_n->{+1,-1} through n=8 and retains only full Cayley-table
homomorphisms. It separately enumerates all functions from C2^r through rank
three, derives the exact character counts, reconstructs kernels, and compares
full truth tables. This route finds the omitted C4 sign character without using
the promoted generator formula.

## Verification Status

The maximum verdict is `symbolic_verified`. Canonical results use exact finite
integers and sign values, while the independent oracle exhausts finite function
spaces. No numerical approximation, quadrature, tolerance, empirical value, or
source-sector interpretation enters the result.

## Sensitivity and Counterexamples

Odd orders admit only the trivial generator image. Every even order admits
`1->-1`; C4 has truth table `(1,-1,1,-1)`, kernel `{0,2}`, and passes OM1's
single/double values while remaining nonfaithful. C6 and C8 behave analogously.
Only C2's nontrivial map has trivial kernel. In C2 squared, selectors `(1,0)`
and `(0,1)` both evaluate to `-1` at `(1,1)` but differ at `(1,0)` and have
different kernels. Full-truth-table mutations reject the false identity.

## Framework Compatibility

The claim is a native extension of C-TOP-001. It preserves the existing integer
parity API and makes the quotient/faithfulness ceiling explicit. A common sign
codomain is not a common domain; pullback language is valid only after each
quotient map is supplied. No accepted claim identifies OM1's copied holonomy,
Wilson, Berry, parity, Skyrmion, or exchange constructions.

## Dependency and Consumer Replay

The sole accepted dependency is C-TOP-001. Consumers are the additive
topological-label API, focused tests, P066 exact verifiers, governance,
generated docs and memory, OM1's disposition, and future finite-character
audits. Post-change graph detection reports LOW risk and no affected execution
process. The full promotion workflow passes all 514 repository tests, and
existing topological-label signatures are unchanged.

## Competing Candidate Audit

Candidates B and C are selected because they exhaust the relevant character
spaces and expose the missing kernel and independent-factor cases. Candidate A
is rejected because scalar set equality cannot prove cross-domain object
identity. Candidate E maps OM1.1 to existing C-TOP-001 evidence. Candidate D is
retained only as a conditional ceiling because OM1 supplies no accepted
quotient maps. The printed minus signs did not select the theorem.

## Four-Axis Decision

The independent evidence supports a new exact conditional theorem.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: exact extension depending on C-TOP-001

## Promotion Transaction

Promotion adds C-CHR-001 to release `v0.60.0`, qualifies OM1, and synchronizes
implementation, tests, registry, release, queue, docs, and memory. Both exact
routes, staged graph detection, one full workflow gate, and diff checks must
pass before commit.

## Continuation if Not Accepted

This clause is inactive after the promotion gate. A future cross-sector
identity claim must supply accepted typed domains, quotient maps, generator and
orientation conventions, representation intertwiners or operator equality,
and a separately governed physical interpretation.

## Done Gate

The claim-level debt is empty only after canonical synchronization and the
promotion replay. The parent corpus migration remains active while later queue
units are pending.

## Cross-References

See P066, OM1, C-TOP-001, `topological_labels.py`,
`test_topological_labels.py`, release `v0.60.0`, and the parent migration
effort.
