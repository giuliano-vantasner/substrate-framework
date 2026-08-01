---
description: Independent review of C-MIX-001
author: vantasner-review
created: '2026-08-01T17:17:53Z'
updated: '2026-08-01T17:17:53Z'
tags:
- substrate-framework
- claim-review
- matrix-decomposition
- basis-conventions
category: decisions
confidence: working
status: archived
---
# Review of C-MIX-001

## Claim Under Review

The claim gives the finite-dimensional complex singular-value decomposition in
one explicit column-basis convention, its Gram spectra and exceptional-space
freedoms, relative-basis unitarity, the corresponding row-transform
orientation, and the real symmetric two-by-two limit. It excludes every
physical flavor identification.

## Sourced Inputs

The review read `v0.29.0` at `b7d8fbc`, P034, the main and independent exact
routes, package APIs/tests, hash-pinned FG3 and its successful reproduction,
and the six-subclaim source adjudication. FG3's M1, SM2, SM3, W2, W3, W7, MH3,
and FG4 relationships were inventoried; none is an accepted dependency of the
mathematical claim.

## Independence

The main route combines exact SymPy examples with the reusable full NumPy SVD
and direct source inspection. The independent route uses a different exact
matrix, direct Gram actions, separately chosen rational rotations, a symbolic
off-diagonal derivation, and a continuously parameterized texture family. It
does not import the decomposition module, verifier constants, or FG3's bases.

## Verification Status

The finite-dimensional spectral construction, exact reconstruction, Gram
pairing, unitary identities, and two-by-two algebra support
`symbolic_verified`. NumPy results are regression coverage for the reusable
API, not the proof of the exact theorem. No numeric result is promoted as an
exact physical prediction.

## Sensitivity and Counterexamples

Changing a singular value, swapping only one paired basis, or scaling a basis
breaks the reconstruction verdict. A rational row-transform counterexample
separates `A_u A_d^dagger` from FG3's `A_u^dagger A_d` while leaving both
unitary, proving that unitarity-only checks miss the convention defect. Complex
textures are rejected by the real-symmetric angle API, and arbitrary texture
rotations produce continuously many relative angles.

## Framework Compatibility

The claim is native mathematical structure with no accepted scientific
dependency. It uses the standard complex inner product and explicitly states
matrix shapes, adjoint placement, zero and repeated singular-space freedoms,
and numerical precision limits. It supplies no fermion, mass, current, charge,
anomaly, or substrate map.

## Dependency and Consumer Replay

There are no accepted claim dependencies. Direct consumers are
`matrix_decompositions.py`, its exports/tests, P034, FG3's disposition, and
future matrix-algebra proposals such as FG4. The source's physical consumers
remain outside the claim graph. Focused replay passes with no debt.

## Competing Candidate Audit

Candidate A was selected because the corrected general convention closes
rectangular, deficient, repeated, and null cases; Candidate B is therefore too
narrow. Candidate C fails dependency closure and texture-variation tests, and
FG3's row-transform orientation error independently defeats its vertex claim.

## Four-Axis Decision

The axes apply only to the matrix theorem and convention map.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: standalone finite-dimensional matrix theorem

## Promotion Transaction

Promotion adds pure decomposition APIs, guarded tests, immutable P034,
qualified FG3 disposition, `v0.30.0`, generated records, and parent-effort
synchronization. The source's physical claims receive no accepted mapping.

## Continuation if Not Accepted

If general reconstruction had failed, Candidate B would retain only the
unitary-product and real-symmetric results. Physical flavor work must first
adjudicate representations, Yukawa structure, charged currents, and anomaly
coefficients, then state one field convention before composing them.

## Done Gate

The exact convention, spectra, exceptional cases, unitary-relative basis,
row-transform conversion, real limit, mutation sensitivity, physical boundary,
consumers, disposition, and debt closure are complete.

## Cross-References

See P034, FG3, `matrix_decompositions.py`, `v0.29.0`, and the parent migration
effort.
