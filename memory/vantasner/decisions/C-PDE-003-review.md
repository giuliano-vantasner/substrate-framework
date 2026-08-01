---
description: Independent review of C-PDE-003
author: vantasner-review
created: '2026-08-01T20:50:36Z'
updated: '2026-08-01T20:50:36Z'
tags:
- substrate-framework
- claim-review
- sine-gordon-l2
- symbolic-verification
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-003

## Claim Under Review

The claim gives the exact full-field residual of P3D3's multiplicative P2
deformation and the exact regular l=2 linearized equation about any radial
solution of the declared 3+1 sine-Gordon model. It fixes the angular convention,
origin behavior, transformed variable, and nonlinear harmonic-mixing ceiling.

## Sourced Inputs

The review read `v0.40.0`, `C-PDE-001`, `C-MOM-003`, P046's frozen proposal,
all attempts, importable l-mode module and tests, primary and independent
verifiers, and hash-pinned P3D3. P3D3's prescribed moment, coarse 2D run,
frequency line, FS2 recovery, and gravity language were audited separately and
are not inputs to the exact derivation.

## Independence

The primary route substitutes the finite multiplicative ansatz into the full
spherical-coordinate PDE and expands it with SymPy. The independent review
starts from `v=r*P` and `z=r*psi`, differentiates both transformations directly,
and rederives the barrier coefficient without importing the residual API.

## Verification Status

The strongest earned status is `symbolic_verified`. Exact algebra fixes the
finite residual, its first-order coefficient, the correct l=2 equation,
regular `r^2/r^3` origin behavior, and the P4 term from `P2^2`. Numeric API
evaluations are sensitivity regressions rather than the authority for these
identities.

## Sensitivity and Counterexamples

The source ansatz gives a concrete nonzero residual away from trivial zeros,
and its l=2 coefficient is nonzero at the origin. Angular barrier mutations 2
and 12 fail the solid-harmonic test that coefficient 6 passes. Centered
finite-amplitude differences reproduce the exact Taylor coefficient. Deleting
nonlinear mixing misses the exact P4 contribution at second order.

## Framework Compatibility

The result is native to `C-PDE-001`'s dimensionless 3+1 model and adds no
constant, fit, comparator, or gravity premise. It corrects the candidate
representation rather than modifying the accepted radial equation. The exact
statement allows trivial special zeros and does not overstate generic
nonvanishing as a global no-solution theorem.

## Dependency and Consumer Replay

The accepted dependency is `C-PDE-001`. Direct consumers are the new l-mode
module, its tests, `C-PDE-004`, and P046. Prospective P3D4/QB2/QB3/BX1
consumers must use the regular equation and cannot import the rejected product
ansatz. P044/P045 replay verifies no regression in accepted radial and moment
paths.

## Competing Candidate Audit

Candidate A is selected because the exact corrected sector exists and the
numeric gates also close. Candidate B's exact-only scope would be required if
the numeric route failed, but it did not. Candidate C is rejected before
comparison values because its exact full-PDE residual is generically nonzero.

## Four-Axis Decision

The exact claim keeps its four axes distinct.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-PDE-001 and challenges only P3D3's unaccepted construction

## Promotion Transaction

Promotion adds the pure residual, P2, regular-seed, transformed-operator APIs,
tests, immutable P046 evidence, claim registry entry, qualified P3D3 mapping,
release, generated docs, and accepted memory.

## Continuation if Not Accepted

If the exact identity failed, Candidate C would remain rejected and the next
route would rederive the angular sector in Cartesian harmonics. No numerical
closeness could replace the missing equation.

## Done Gate

The full residual, Taylor orders, regularity, transformation, mutations,
dependencies, consumers, and scope are closed with no exact-claim debt.

## Cross-References

See P046, P3D3, `C-PDE-001`, `C-PDE-004`, the l-mode module, and the parent
migration effort.
