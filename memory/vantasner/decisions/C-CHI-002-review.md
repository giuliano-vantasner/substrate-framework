---
description: Independent review of C-CHI-002 SU2 trace normalization
author: vantasner-review
created: '2026-08-02T19:45:00Z'
updated: '2026-08-02T19:45:00Z'
tags:
- substrate-framework
- claim-review
- su2-trace-normalization
category: decisions
confidence: established
status: archived
---
# C-CHI-002 Claim Review

## Claim Under Review

C-CHI-002 pairs the kinetic and trace-breaking terms of the declared
one-coordinate SU(2) exponential. It derives the trace, scalar kinetic
coefficient, potential curvature, and coordinate-independent generalized
mass. It specializes the result to the declared Skyrme coefficient pair and
records PG2's exact factor-four mismatch without accepting a physical pion,
GMOR relation, coefficient prediction, or substrate map.

## Sourced Inputs

The review reads C-BRK-001, C-CHI-001, base release `v0.54.0`, the P061
proposal and attempts, the pinned PG2 executable and audit, the primary
Battye-Manton-Sutcliffe-Wood Lagrangian, canonical APIs/tests, independent
Pauli-eigenvalue derivation, impact analysis, and source adjudication. The
cited source's paired `F^2/16` and `m^2*F^2/8` coefficients are treated as a
conditional model convention, not framework authority.

## Independence

The independent route obtains `Tr(U-I)` from the two eigenvalues of `tau3`,
derives the trace Gram without the canonical kinetic helper, differentiates
the potential separately, and only then forms the ratio. It solves for the
trace prefactor required by PG2's advertised potential rather than copying
the claimed factor.

## Verification Status

The maximum verdict is `symbolic_verified`. Both routes derive
`K=4*Z*q^2/F^2`, `H=2*C*q^2/F^2`, and `H/K=C/(2*Z)` exactly. They reproduce
the `q=1` quarter-normalized and `q=2` canonical-coordinate cases and expose
PG2's factor four. The source tally is reproduction evidence only and no
physical or numerical mass is claimed.

## Sensitivity and Counterexamples

Coordinate multipliers one, two, and three change kinetic and curvature
together while preserving their ratio. Pairing PG2's full cosine amplitude
with the quarter kinetic metric changes the generalized mass by four.
Retaining the cited trace coefficient makes the potential one quarter of
PG2's advertised expression; solving the equality requires four times that
coefficient. Sign handling distinguishes a Lagrangian term from the positive
potential.

## Framework Compatibility

The claim depends only on C-BRK-001 and C-CHI-001. It preserves Pauli trace,
field-coordinate, kinetic, sign, and prefactor conventions and leaves every
model parameter declared. It does not identify `F` with a measured decay
constant, import pending S2, or alter the normalized sine-Gordon root.

## Dependency and Consumer Replay

The direct dependencies are C-BRK-001 and C-CHI-001. GitNexus reports zero
upstream consumers of the reused kinetic helper and LOW overall additive
risk. Focused explicit-breaking and symmetry tests, both P061 verifiers,
governance, generated consumers, migration state, and the full workflow are
replayed before sealing. No convention debt remains.

## Competing Candidate Audit

Candidates B and C are jointly selected because mass interpretation requires
the potential and kinetic normalization together. Candidate A is rejected
because its passing check changes the cited coefficient, and Candidate D
prevents local shape agreement from selecting the mechanism. Selection is
structural and comparator-blind.

## Four-Axis Decision

The axes support a new exact conditional specialization and introduce no
challenge or supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: specialization of C-BRK-001 and C-CHI-001

## Promotion Transaction

Promotion adds C-CHI-002 with both dependencies to the registry and release
`v0.55.0`, archives exact and source evidence, qualifies PG2, regenerates
migration state, and synchronizes package exports, tests, generated docs, and
memory. The sensitive verifiers, focused and full replay, change detection,
and diff hygiene must pass.

## Continuation if Not Accepted

This clause is inactive because the exact coordinate theorem is accepted. A
physical pion claim still needs a derived chiral action, current, vacuum,
field normalization, spectral interpretation, and substrate map.

## Done Gate

The claim-level debt is empty after exact promotion replay and consumer
synchronization. The parent migration remains active.

## Cross-References

See P061, PG2, C-BRK-001, C-CHI-001, the primary provenance ledger,
`explicit_breaking.py`, focused tests, release `v0.55.0`, and the parent effort.
