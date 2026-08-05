---
description: Qualify GK3D4 through accepted product-carrier trace, affine-kinetic, trace-coupling, and anomaly ceilings
author: vantasner-review
created: '2026-08-11T14:48:00Z'
updated: '2026-08-11T14:53:00Z'
tags:
- substrate-framework
- source-review
- migration-GK3D4
- product-gauge
- kinetic-normalization
category: decisions
confidence: established
status: archived
---
# GK3D4 Qualified Review

## Source Unit Under Review

GK3D4 claims that equal fundamental trace factors extend one Abelian D4 loop
construction to physical U(1), SU(2), and SU(3) sectors and upgrade a supplied
three-eighths trace coordinate to a physical four-dimensional weak angle.

## Exact Surviving Content

The standard Pauli-half and Gell-Mann-half fundamental metrics separately equal
one-half times the identity, and that trace factor is a dimensionless rational.
On the accepted `C^3 tensor C^2` carrier, spectator dimensions instead give
color metric `I_8`, isospin metric `(3/2)I_3`, Abelian entry `6 y^2`, and zero
cross blocks. This is the exact product-sector trace ledger.

The source ratio is a conditional specialization. For independent factor
families `Z_a=z_a+b_a L_a/(8 pi^2)`, its exact residual is
`b_i z_j-b_j z_i+b_i b_j(L_j-L_i)/(8 pi^2)`. Only separately zero boundaries
and a common logarithm remove it. Scale matching does not erase the boundaries.

## Trace, Coupling, and Anomaly Scope

The supplied fifteen-state table has trace coordinate `3/8`, but C-REP-001
makes equality with a coupling coordinate equivalent to a separately common
inverse-trace coefficient. Equal independent couplings yield `1/2`, and paired
Abelian rescaling moves the coordinate to `3/23` at scale two. C-ANO-001's
three anomaly-free branches and free overall normalization refute the claimed
unique anomaly selection.

## Verification and Consumer Replay

The primary and independent exact routes pass 28 and 21 checks, and 131 focused
accepted-API tests pass. GK3D4, GK3D5, GK3D6, EL2, and HE5 run natively with 52
source checks. GK3D6 directly repeats the ratio and three-eighths overclaim;
GK3D5 refers only to the candidate excitation, and EL2/HE5 are transitive.

GK3D4, GK3D6, EL2, HE5, and mutable P188 contain no legacy trapezoidal access.
Immutable GK3D5 selects its current-first lazy branch under NumPy 2.5.1, where
the current API exists and the legacy API does not. No alias or version-only
scientific failure occurs.

## Four-Axis Decision

The source verdict and the unchanged accepted-claim states remain distinct.

- Verification: exact evidence for carrier traces, affine residuals, trace iff,
  normalization covariance, and anomaly branches.
- Review: audited and qualified predicate by predicate.
- Compatibility: compatible with the ten accepted mapped claims at their
  existing narrow scopes.
- Epistemic: qualified source evidence, not a new accepted claim.
- Release: v0.139.0 unchanged.

## Closure

P188 changes campaign, GK3D4 disposition, generated queue, proposal and
decision memory, and the parent effort only. C-VAC-005 stays reserved and
unpromoted. No canonical API, test, accepted claim, generated documentation,
release, physical three-sector construction, weak angle, or substrate
mechanism is accepted. The integrated gate validates all 768 memory records and
passes all 1,633 tests. GK3D5 and GK3D6 remain pending.
