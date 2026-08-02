---
description: Independent review of C-PDE-007
author: vantasner-review
created: '2026-08-02T08:20:00Z'
updated: '2026-08-02T08:20:00Z'
tags:
- substrate-framework
- claim-review
- radial-sine-gordon
- energy-spectrum
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-007

## Claim Under Review

The claim states the exact half-period selection rule for canonical energy
density of a finite odd-cosine radial field, extends the rule through any
time-independent radial linear functional, gives the complete local
single-mode twice-frequency coefficient, and applies the accepted spherical
second-moment identity. It expressly does not assert that the twice-frequency
coefficient is nonzero, lowest, dominant, radiating, or sourced by an exact
full-PDE solution.

## Sourced Inputs

The review read base release `v0.46.0`, `C-PDE-001`, `C-MOM-003`,
`C-PDE-005`, `C-PDE-006`, the P053 contract, all attempts 0001 through 0007,
both verifier implementations, the canonical observable module and tests, and
hash-pinned QB2 at SHA-256 `f7ff064a...22bbff`. QB2's standalone shooting
branch, physical radiation vocabulary, P3D3 comparison, and nonzero-line
conclusion stay outside this exact claim.

## Independence

The primary route uses direct symbolic sign reversal, explicit periodic sums,
and the canonical APIs. The independent route reconstructs the density
without the new observable functions, integrates phase with Gauss-Legendre
and radius with Simpson, and separately builds a cancellation example and a
spectrally pure non-solution. The spherical STF result is also checked by
direct tensor subtraction and an anisotropic mutation.

## Verification Status

The maximum status is `symbolic_verified`. Half-period antisymmetry, evenness
of canonical energy density, Fourier cancellation, the Bessel coefficient,
and isotropic angular integration decide the stated identities exactly.
Float64 transforms are mutation and regression evidence, not the source of
the exact verdict.

## Sensitivity and Counterexamples

Adding an even field harmonic breaks half-period antisymmetry. Omitting or
doubling the physical time-derivative frequency fails the full local
coefficient. Known cosine and sine signals rederive the real-transform
normalization and phase. The complete local formula includes the gradient
term omitted from QB2's conclusion. A real one-mode choice at amplitude one
and frequency 0.97 cancels the twice-frequency coefficient while leaving a
nonzero fourth harmonic, proving that the selection rule does not order or
populate the allowed bins. An arbitrary radial non-solution keeps exact even
purity but has PDE residual RMS 0.132448. A declared anisotropic tensor breaks
the spherical STF null.

The independent numerical odd coefficients are assessed relative to the DC
scale after 96/192/384 Gauss refinement. Attempt 0005's unjustified absolute
`2e-10` bound is preserved as failed; the repaired ratios are between
`5e-15` and `6e-14`. This roundoff regression is not used to weaken or replace
the separate exact Fourier cancellation.

## Framework Compatibility

The theorem is native to the C-PDE-005 odd-harmonic convention and imports the
already accepted C-MOM-003 spherical identity. It introduces no fitted value,
wall, solver, empirical comparator, nonspherical source, gravity premise,
physical unit, or ontology. It strengthens interpretation by separating an
allowed harmonic from a guaranteed line.

## Dependency and Consumer Replay

The direct dependencies are `C-PDE-005` and `C-MOM-003`, whose closures reach
the accepted radial model and moment conventions. The new pure module and its
tests pass alongside radial harmonic-balance, radial IVP, and moment tests.
The claim is consumed by `C-PDE-008` and the qualified QB2 mapping. Later QB3
and QB4 remain pending evidence and acquire no accepted result automatically.
No claim debt remains.

## Competing Candidate Audit

Candidates A, B, and C and structural criteria were frozen before QB2's
reported values were opened. Literal Candidate A contains the correct parity
idea but overstates nonzero amplitude and radiation. Candidate B is selected
because its exact rule follows from accepted symmetries with no new dynamical
premise. Candidate C is unnecessary for this scalar theorem and remains the
separate regular route if a nonspherical STF object is later requested.

## Four-Axis Decision

The four axes record an exact native theorem and do not upgrade its numerical
application.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-PDE-005 and C-MOM-003; challenges and supersedes none

## Promotion Transaction

Promotion adds the pure observable APIs and exact tests, immutable P053
evidence, registry entry `C-PDE-007`, a pinned release, generated docs and
accepted memory, and the qualified QB2 mapping. The separate finite-box line
is reviewed as `C-PDE-008`.

## Continuation if Not Accepted

If parity or the energy convention failed, the numerical spectrum could
remain attempt evidence but no exact selection theorem could be promoted. A
different invariant observable would need its own preregistered derivation and
counterexamples.

## Done Gate

Accepted. Exact dependency closure, sign and normalization mutations,
cancellation and non-solution counterexamples, importable APIs, downstream
replay, synchronized canonical records, and empty claim debt pass at the
single promotion boundary.

## Cross-References

See P053, QB2, `C-PDE-005`, `C-MOM-003`, `C-PDE-008`, the observable module,
the source adjudication, the impact review, and the parent migration effort.
