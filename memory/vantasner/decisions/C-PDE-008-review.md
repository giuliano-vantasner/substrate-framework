---
description: Independent review of C-PDE-008
author: vantasner-review
created: '2026-08-02T08:20:00Z'
updated: '2026-08-02T08:20:00Z'
tags:
- substrate-framework
- claim-review
- radial-sine-gordon
- finite-box-spectrum
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-008

## Claim Under Review

The claim records one declared core radial second-energy-moment spectrum on
the accepted finite-box branch `C-PDE-006`. It promotes a converged dominant
twice-frequency coefficient while preserving harmonic truncation, core
cutoff, wall, scalar-moment, finite-box, and numerical epistemic limits.

## Sourced Inputs

The review read release `v0.46.0`, exact proposed `C-PDE-007`, accepted
`C-PDE-006`, P053's frozen proposal, all source and numerical evidence,
attempts 0001 through 0007, the 38-check primary result, the 22-check
independent result, and hash-pinned QB2. The source's amplitude-three N=1
branch, P3D3 closeness, nonzero universal coefficient, eigenfunction purity,
and radiating-line meaning are excluded.

## Independence

The primary route reconstructs the accepted N=1 through N=9 branch with the
canonical periodic DFT and trapezoid-dispatched radial observable. The
independent route uses a separately written observable reconstruction,
96/192/384-node Gauss-Legendre phase quadrature, Simpson radial integration,
and no new observable API. It reproduces the main coefficient within 0.003
percent and rejects time-derivative, Fourier-normalization, radial-measure,
PDE-purity, and anisotropy false oracles.

## Verification Status

The maximum status is `numeric_evidence`. Every accepted BVP completes with
finite state and resolved collocation residual. The coefficient is a finite-
precision result for one finite cutoff, finite harmonic set, and finite wall.
The exact parity dependency decides only odd-bin absence and does not turn the
line amplitude or branch into an exact full-PDE fact.

## Sensitivity and Counterexamples

The N=1, 3, 5, 7, and 9 coefficients converge from 666.330281099 to
591.470484284 as the full nonlinear core remainder falls from 0.105185 to
`1.366e-5`. Full-box energy variation falls from 0.058154 to `9.687e-7`,
providing a residual-sensitive conservation diagnostic. Temporal
256/512/1024 and radial 1201/2401/4801 refinements converge; initial meshes
200/300/400 span less than 0.005; and tighter tolerance plus 512 projection
samples changes the coefficient by 0.007 while reducing collocation residual
tenfold.

Walls 30, 40, 50, and 60 yield core coefficients from 590.990 to 598.370 and
a full-box variance resonance near wall 50. Thus bounded core behavior does
not imply wall independence. The independent coefficient is 591.468056462.
Its initial absolute odd-bin threshold failed and is preserved; phase-node
refinement shows scale-relative roundoff below `6e-14`. A spectrally pure
non-solution, a local twice-frequency cancellation, the radial-measure
mutation, and the spherical STF null prevent the numerical line from serving
as a PDE, universal-amplitude, or radiation oracle.

## Framework Compatibility

The result is a compatible extension of `C-PDE-006` through the exact
observable meanings of `C-PDE-007`. All branch coordinates, cutoff, wall,
harmonics, grids, tolerances, coefficient normalization, and error metrics are
declared. It imports no P3D1 or source frequency, FS2 width, gravity constant,
absolute scale, or nonspherical deformation.

## Dependency and Consumer Replay

The direct dependencies are `C-PDE-006` and `C-PDE-007`. The new observable
tests, accepted harmonic-balance and radial-model tests, moment tests, primary
verifier, and independent review pass. QB2 is the adjudicated source
consumer. QB3 and QB4 remain pending and may use only the finite-box scalar
meaning unless their own governed campaigns establish more. No debt remains.

## Competing Candidate Audit

Candidates were frozen before comparator inspection. Candidate A reproduces
the source tally but fails branch identity, solver-status, refinement,
coefficient-completeness, and radiation-meaning gates. Candidate B is selected
for the positive object because it consumes accepted branch data, declares
the observable and error hierarchy, and requires independent normalization.
Candidate C would answer a different nonspherical question and cannot be
smuggled into the scalar evidence.

## Four-Axis Decision

The axes preserve the numerical and finite-box ceiling.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: depends on C-PDE-006 and C-PDE-007; challenges and supersedes none

## Promotion Transaction

Promotion adds importable observable APIs and tests, immutable P053 evidence,
registry entry `C-PDE-008`, a pinned release, generated docs and memory, and a
qualified QB2 mapping. It does not promote a radiating STF source, an exact
periodic PDE solution, or the source's standalone shooting branch.

## Continuation if Not Accepted

If the coefficient failed convergence, Candidate B would continue with a
different cutoff, basis, or radiative-tail treatment under a new frozen
contract. Physical radiation would still require Candidate C or another
regular nonspherical construction with its own source and gravity oracles.

## Done Gate

Accepted. The positive scalar spectrum, exact dependency closure, independent
normalization, residual and convergence hierarchy, wall counterexample,
consumer replay, synchronized canonical records, and empty claim debt pass at
the single promotion boundary.

## Cross-References

See P053, QB2, `C-PDE-006`, `C-PDE-007`, the numerical audit, independent
review, source adjudication, impact review, and parent migration effort.
