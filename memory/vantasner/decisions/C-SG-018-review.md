---
description: Independent review of C-SG-018
author: vantasner-review
created: '2026-08-03T10:02:28Z'
updated: '2026-08-03T10:02:28Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- dispersion
category: decisions
confidence: working
status: archived
---
# Review of C-SG-018

## Claim Under Review

Conditional on `C-MED-003`, the claim gives the exact physical vacuum
linearization, positive real-wavenumber dispersion and velocities, the
real-frequency exterior-tail trichotomy, and the absence of nonzero
whole-line `L2` separated modes for the homogeneous constant-coefficient
linear equation. It distinguishes these statements from nonlinear breather
existence, outgoing radiation, transient traveling packets, defects,
finite-box modes, and material selection.

## Sourced Inputs

The review read release `v0.81.0`, accepted `C-MED-003`, `C-SG-017`,
`C-SG-011`, `C-LAT-001`, and `C-PDE-005`, their canonical modules and tests,
P096's frozen contract, attempts, source audit, predicate ledger, consumer map,
and hash-pinned MC2 source. It separately inspected MC3, MC4, MD1, MD2, and
four engineering consumers; all material, simulation, 3-D measure, cutoff,
lifetime, and design subclaims remain outside the delta.

## Independence

The primary route calls the new exact APIs after deriving their expected
quantities from the accepted physical residual. The independent route imports
none of those APIs: it differentiates the nonlinear residual at a vacuum,
performs a fresh Fourier substitution and time separation, constructs and
solves the half-line matching system, evaluates oscillatory norm per period,
computes directed flux, and constructs a finite-energy d'Alembert packet.

## Verification Status

The status is `symbolic_verified`. Exact SymPy identities establish the
linearization, spectrum, velocity relations and limits, tail coefficient,
matching determinant, threshold behavior, repeated-period norm, flux
distinction, nonlinear-tail cross-check, and gapless traveling-packet
counterexample. No unevaluated integral or numeric tolerance carries the
verdict. MC2's twenty-one source checks are reproduction evidence only.

## Sensitivity and Counterexamples

Mass-sign, gradient-sign, inertia, band-term, tail-sign, rate-factor,
frequency-factor, and derivative-matching mutations fail. The cusp derivative
jump counters the global absolute-value exponential. A standing above-gap wave
has zero mean flux while a directed wave on the same dispersion has nonzero
flux. `sech(x-c*t)` is an exact localized finite-energy gapless packet, so the
broad no-localized-dynamics reading fails without weakening the precise
real-frequency separated-mode theorem.

## Framework Compatibility

The claim is a compatible extension of `C-MED-003` and preserves its exact
positive coefficient and physical-coordinate conventions. Its normalized
limit agrees with `C-SG-011`, its nonlinear exterior rate agrees with
`C-SG-017`, and it does not merge continuum, lattice, or radial spectra. The
canonical branch name is `oscillatory`, not `radiative`, because flux and
boundary data are separate premises.

## Dependency and Consumer Replay

The dependency is `C-MED-003`; `C-SG-017` is a cross-check rather than a premise
for the spectrum derivation. Direct consumers are the dimensional
sine-Gordon module, public exports, tests, and P096 verifiers. Normalized
sine-Gordon, lattice scalar, and radial-tail tests are replayed. All later
material and engineering consumers remain pending or noncanonical, so no debt
is transferred into this claim.

## Competing Candidate Audit

Candidates A through J were frozen before full source inspection and execution.
Candidates B-E supply the theorem, F is a nonlinear cross-check, G-H impose
counterexample and radiation ceilings, and I-J enforce consumer and
nonduplication closure. Exact boundary/norm consistency selects the result;
the source tally and sampled signs do not.

## Four-Axis Decision

The exact conditional spectrum and classification are accepted with explicit
domain, norm, boundary, and solution-class conditions.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-MED-003, uses C-SG-017 only as a cross-check, and challenges or supersedes no accepted claim

## Promotion Transaction

Promotion adds `C-SG-018`, importable spectrum/tail/wave APIs and tests,
immutable P096 evidence, qualified MC2 disposition, release `v0.82.0`,
generated docs and accepted memory, and parent-effort continuation. Registry
membership and release closure are validated together.

## Continuation if Not Accepted

This section is not invoked because the exact conditional theorem is accepted.
Material gaps, nonlinear existence beyond `C-SG-017`, outgoing scattering,
finite-box modes, 3-D density of states, and engineering uses remain separate
objectives rather than hidden claim debt.

## Done Gate

The positive theorem, dependency closure, independent rederivation, mutations,
counterexamples, exact limits, importable APIs/tests, source ceiling, and
consumer map close with an empty campaign ledger. The corpus effort continues
to MC3.

## Cross-References

See P096, MC2, `C-MED-003`, `C-SG-017`, the dimensional sine-Gordon module,
and the framework-migration effort.
