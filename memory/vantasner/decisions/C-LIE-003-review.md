---
description: Accepted review of exact standard SU3 symmetric tensor claim C-LIE-003
author: vantasner-review
created: '2026-08-10T17:05:00Z'
updated: '2026-08-10T17:05:00Z'
tags: [substrate-framework, claim-review, C-LIE-003, su3-symmetric-tensor]
category: decisions
confidence: established
status: archived
---
# C-LIE-003 Claim Review

## Claim Under Review

C-LIE-003 fixes the symmetric trace tensor of the accepted standard fundamental
SU3 convention. It states full permutation symmetry, exact anticommutator
reconstruction, vanishing on the standard generators zero through two, and a
nonzero witness outside that embedded SU2 restriction. It claims only exact
representation algebra.

## Sourced Inputs

The review read v0.123.0, C-LIE-001, the frozen and source-aware P160 proposal,
the hash-pinned QCD1 source and dossier, canonical implementation, primary and
independent verifiers, mutations, impact report, and consumer graph. QCD1's
loop, action, physical color, and dimensional statements are excluded.

## Independence

The canonical route derives the tensor from the accepted generator API. The
independent route reconstructs all eight Gell-Mann matrices locally, computes
both f and d without importing the new API, tests all 512 symmetry entries and
all 64 anticommutators, and checks the embedded restriction and an outside
witness.

## Verification Status

Exact evaluated SymPy matrices and scalars support symbolic verification. The
primary oracle passes 38 checks and the independent route passes 27; every
anticommutator residual is zero rather than an unevaluated symbolic object.
The 71 focused and adjacent tests include exact standard components, index
domain controls, and downstream SU3/WZW consumers.

## Sensitivity and Counterexamples

Deleting the identity term breaks the anticommutator reconstruction. Scaling
all generators by two changes d cubically. The fresh Pauli-half comparison has
no symmetric rank-three tensor, while d_118 is nonzero in the full SU3 basis.
This supports the scoped embedded-restriction statement without claiming a
unique group characterization.

## Framework Compatibility

The claim is a native additive extension of C-LIE-001. It reuses the same
generator ordering, trace, and normalization and adds no coupling, field,
dimension, or physical sector. The shared index validator admits exact Python
and SymPy integers and rejects booleans, floats, symbols, and invalid ranges.

## Dependency and Consumer Replay

C-LIE-001 is the sole direct dependency. GitNexus gives the new evidence API
LOW risk and no external graph caller. The unchanged generator root has a
fourteen-symbol WZW and invariant reach; P024 and P028 pass 27 and 23 checks,
and the focused adjacent tests pass. The 17-node source graph replays 170
predicates without promoting pending consumers.

## Competing Candidate Audit

Candidates were frozen before QCD1 body inspection. Accepted composition could
not supply d, while an SU3-specific loop wrapper would duplicate rather than
explain the algebra. Exact matrix reconstruction selects the symmetric-tensor
candidate by dependency closure and representation fit, not comparator values.

## Four-Axis Decision

The four status axes support additive promotion.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive exact standard-representation theorem

## Promotion Transaction

Promotion adds the pure SU3 APIs and tests, C-LIE-003, the P160 immutable
campaign, release v0.124.0, qualified QCD1 disposition, generated records, and
accepted memory. C-LIE-001 is unchanged and remains the convention root.

## Continuation if Not Accepted

Nonacceptance would retain P160's algebra as proposal evidence and require a
fresh exact basis derivation. No loop or physical interpretation could repair
a failed matrix identity.

## Done Gate

Acceptance requires registry, release, source disposition, generated state,
memory, downstream consumers, and an empty debt ledger to agree. It does not
promote QCD1's gauge-sector headline.

## Cross-References

See P160, QCD1, C-LIE-001, `su3.py`, `test_su3.py`, and P160's exact,
independent, source-graph, provenance, and impact evidence.
