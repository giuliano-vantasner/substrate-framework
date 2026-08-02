---
description: Independent review of C-PDE-005
author: vantasner-review
created: '2026-08-02T02:00:00Z'
updated: '2026-08-02T02:00:00Z'
tags:
- substrate-framework
- claim-review
- radial-sine-gordon
- harmonic-balance
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-005

## Claim Under Review

The claim gives the exact odd-cosine projection of the dimensionless
three-dimensional radial sine-Gordon equation, its regular-origin curvature
law, and its linear far-field classification into evanescent, threshold, and
radiative one-over-r channels. It states conditionally that a nonzero
radiative channel has infinite integrated radial energy and that a finite
Dirichlet wall on such a channel is a standing-wave box condition, not proof
of an infinite-domain localized breather.

## Sourced Inputs

The review read release `v0.45.0`, `C-PDE-001`, its dependency `C-SG-001`, the
canonical radial equation, P052's frozen proposal and revision 0001, attempts
0001 through 0011, both verifier implementations, and hash-pinned QB1 at
SHA-256 `1f387c14...e2dc7a`. QB1's fitted amplitude, numerical branch,
frequency comparator, lifetime language, and any unique or exact eigenstate
interpretation remain outside this exact claim.

## Independence

The primary verifier reconstructs the periodic DFT projection and uses SymPy
for radial tails and origin identities. The independent route uses a 96-point
Gauss-Legendre projection and direct asymptotic energy calculations without
calling the new projection, channel-classification, or solver APIs. It also
compares the single-harmonic projection against independently available
Jacobi-Anger Bessel coefficients.

## Verification Status

The maximum status is `symbolic_verified`. Fourier orthogonality, the radial
origin limit, and the far-field ODEs decide the claimed identities exactly.
Numerical examples serve as mutation and regression evidence only; no
finite-grid fact is smuggled into the theorem.

## Sensitivity and Counterexamples

An even-harmonic insertion breaks half-period antisymmetry. Replacing the DFT
factor two by either one or minus two fails against Jacobi-Anger coefficients.
Replacing the three-dimensional origin factor three by one, two, or four
fails the regular series identity. Evanescent and radiative one-over-r
profiles have opposite radial-Laplacian eigenvalue signs, while a nonzero
radiative tail has a positive asymptotic energy density per radial length.
At the audited sub-gap fundamental, all retained harmonics from n=3 upward are
explicit counterexamples to the idea that `omega<1` localizes every channel.

## Framework Compatibility

The theorem is native to `C-PDE-001` and uses its dimensionless equation,
mass threshold one, radial geometry, and even-origin convention. It imports no
fitted constant, empirical comparator, outer boundary, lifetime law, gravity,
particle label, or substrate premise. Its conditional nonzero-tail statement
does not assert that every formal solution must have a radiative coefficient.

## Dependency and Consumer Replay

The dependency is `C-PDE-001`, whose closure reaches `C-SG-001`. The new pure
module has no import-time solve. Exact and API tests pass inside a 38-test
targeted replay, and P044's 28-check radial authority verifier passes. The
new theorem is consumed by `C-PDE-006` and the QB1 disposition; pending QB2
through QB4 are not treated as accepted consumers. No debt remains.

## Competing Candidate Audit

Candidates A, B, and C and structural criteria were frozen before QB1 values
were opened. Candidate A preserves the correct projected equation but not its
physical ceiling. Candidate B supplies the finite-box numerical object.
Candidate C supplies the necessary channel-aware interpretation and is
selected for the exact theorem because its asymptotics follow from the
accepted linearized equation rather than numerical proximity to P3D1.

## Four-Axis Decision

The four axes record an exact native theorem without upgrading its numerical
application.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-PDE-001; challenges and supersedes none

## Promotion Transaction

Promotion adds importable projection, reconstruction, residual, and channel
APIs; exact tests and sensitive mutations; immutable P052 evidence; registry
entry `C-PDE-005`; a pinned v0.46 release; generated docs and accepted memory;
and a qualified QB1 mapping. The numerical branch is reviewed separately as
`C-PDE-006`.

## Continuation if Not Accepted

If the channel classification failed, the finite-box branch could remain
attempt evidence but could not be promoted as a localized object. A different
asymptotic formulation would have to be preregistered and independently
derived before any infinite-domain statement.

## Done Gate

Accepted. The exact dependency closure, normalization rederivation, sign and
origin mutations, counterexamples, canonical APIs, consumer replay, and empty
claim debt pass. The single repository-wide transaction gate validated 64
accepted claims, 232 memory records, the repo-local skill, and 372 tests.

## Cross-References

See P052, QB1, `C-PDE-001`, `C-PDE-006`, the radial harmonic-balance module,
the source adjudication, the impact review, and the parent migration effort.
