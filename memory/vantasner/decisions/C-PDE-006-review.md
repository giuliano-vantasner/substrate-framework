---
description: Independent review of C-PDE-006
author: vantasner-review
created: '2026-08-02T02:00:00Z'
updated: '2026-08-02T02:00:00Z'
tags:
- substrate-framework
- claim-review
- radial-sine-gordon
- finite-box
category: decisions
confidence: working
status: archived
---
# Review of C-PDE-006

## Claim Under Review

The claim records one nontrivial, parameter-explicit finite-radius
odd-harmonic Galerkin branch of `C-PDE-005`: central fundamental 2.5,
origin cutoff 1e-3, wall radius 40, a decaying fundamental Robin condition,
radiative-mode Dirichlet box conditions, and continuation through N=9. It
promotes resolved core convergence while explicitly excluding uniqueness,
infinite-domain localization, exact periodicity, eternal lifetime, and an
equation-only recovery of the P3D1 comparator.

## Sourced Inputs

The review read release `v0.45.0`, `C-PDE-001`, proposed `C-PDE-005`, P052's
contract and claim split, every preserved attempt, the primary numerical audit,
the 41-check verifier result, the independent 14-check result, and hash-pinned
QB1. The source's amplitude-fitted 0.921 value and all physical quasibreather,
particle, gravity, and substrate interpretations remain outside the claim.

## Independence

The primary route uses the canonical periodic-DFT BVP with a logistic sub-gap
frequency parameter. The independent route uses DOP853 event shooting for the
fundamental, Gauss-Legendre projection with a separately written collocation
system, and centered finite differences with nonlinear least squares and an
explicit second-order zero-spacing extrapolation. It does not call the
canonical harmonic-balance APIs or copy the source's frequency target.

## Verification Status

The maximum status is `numeric_evidence`. Every SciPy solve used in the final
evidence has a successful status, finite state, declared tolerance, and
resolved residual. The evidence supports one finite-grid, finite-harmonic,
finite-wall branch. Neither tight tolerances nor method agreement turns it
into an exact or infinite-domain object.

## Sensitivity and Counterexamples

The N=1, 3, 5, 7, and 9 frequency sequence converges from 0.976908657117 to
0.976873921394, while the full core nonlinear remainder decreases from
0.105422 to 1.3719e-5. Initial meshes 200/300/400, temporal samples 256/512,
and tolerances 1e-8/1e-9 preserve the branch. Changing the central amplitude
from 2.5 to 2.0 or 3.0 changes the fitted frequency, proving that amplitude is
a load-bearing free coordinate rather than a predicted constant. Walls at
30, 40, 50, and 60 keep the frequency within about 6.5e-5 but produce a more
than twentyfold third-harmonic tail resonance near radius 50. Frequency-only
convergence is therefore an explicit false oracle for localization.

The independent Gauss N=9 frequency is 0.976873921630 and its core remainder
is 1.3759e-5. Three finite-difference grids converge, and their second-order
extrapolated N=5 frequency 0.976871246116 agrees with the Gauss value
0.976873950083. Earlier cold solves, an incorrect raw-grid tolerance, and
status-zero least-squares results were rejected and preserved rather than
counted.

## Framework Compatibility

The branch is a compatible extension of the exact `C-PDE-005` formulation.
All values are dimensionless, every free parameter and outer condition is
declared, and no accepted IVP frequency is fitted or imported. The radiative
box walls are numerical model data, not asymptotic localization. The result
is compatible with `C-PDE-001`'s finite-time ceiling but is not identified
with that distinct Gaussian IVP trajectory.

## Dependency and Consumer Replay

The direct dependency is `C-PDE-005`. The optional parameter extension to the
shared BVP helper leaves the existing vortex route parameter-free; 38 targeted
tests and P044's 28-check verifier pass. Primary and independent P052
verifiers pass 41 and 14 checks. QB1 is the only adjudicated source consumer;
later QB units remain pending. No claim debt remains.

## Competing Candidate Audit

Candidates A, B, and C and their structural ranking were frozen before source
values and the comparator were opened. Candidate A reproduces the source but
fails the residual, domain, and calibration interpretation gates. Candidate B
is selected for the positive numerical object because its free coordinate,
origin series, residual hierarchy, and refinement policy are explicit.
Candidate C supplies the exact tail ceiling; an outgoing-tail solution would
be a different future object, not a silent reinterpretation of this box branch.

## Four-Axis Decision

The four axes preserve the numerical and finite-box limits of the accepted
object.

- Verification: numeric_evidence
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: qualified
- Relationship: depends on C-PDE-005; challenges and supersedes none

## Promotion Transaction

Promotion adds the parameterized BVP evidence extension, the pure harmonic-
balance solver and residual APIs, focused tests, all immutable P052 attempts,
registry entry `C-PDE-006`, v0.46, generated documentation and accepted
memory, and the qualified QB1 disposition. It does not promote the source's
target-fitted amplitude or localized-eigenstate headline.

## Continuation if Not Accepted

If the finite-box branch failed refinement, Candidate B would continue with a
different continuation representation. An outgoing or matched radiative-tail
candidate would require its own declared tail data, residual and flux oracle,
and independent method; failure here could not authorize lowering those gates.

## Done Gate

Accepted. The positive branch, exact dependency closure, multiple numerical
methods, convergence and mutation evidence, finite-box interpretation,
consumer replay, and empty claim debt pass. The single repository-wide
transaction gate validated 64 accepted claims, 232 memory records, the repo-
local skill, and 372 tests.

## Cross-References

See P052, QB1, `C-PDE-001`, `C-PDE-005`, the numerical audit, independent
review, source adjudication, impact review, and the parent migration effort.
