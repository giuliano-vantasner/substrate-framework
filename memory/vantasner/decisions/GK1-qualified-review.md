---
description: Qualify GK1 through exact gauge-dimension bookkeeping and accepted loop ceilings
author: vantasner-review
created: '2026-08-11T05:00:00Z'
updated: '2026-08-11T05:00:00Z'
tags: [substrate-framework, source-review, migration-GK1, gauge-kinetic]
category: decisions
confidence: established
status: archived
---
# GK1 Qualified Review

## Source Unit Under Review

GK1 compares EM5, YM1, and QCD1 algebra, presents eleven passing predicates,
and concludes a universal two-dimensional gauge-kinetic origin with propagated
couplings, physical sectors, and a substrate mechanism.

## Exact Surviving Content

The standard Pauli-half and Gell-Mann-half traces reproduce accepted
representation conventions. Antisymmetric rank-two component counts are one
in two dimensions and six in four dimensions, with zero and three magnetic
components respectively. In the canonical convention, a scale-free ansatz
`Pi_hat=g^2*c` with nonzero dimensionless `c` has kernel dimension two exactly
when `D=2`; C-DIM-009 owns that narrow result and its convention translation.

## Corrected Dimensional Scope

The narrow result is not a universal polarization theorem. A separately
supplied scale gives `g^2*M^(D-2)*c` dimension two in every dimension. In four
dimensions, `Q*f(Q/M^2)` is homogeneous for constant, rational, logarithmic,
and other dimensionless `f`, so dimensions select neither a logarithm nor a
loop coefficient. With `B=gA`, the identical density has coefficient
`kappa_B=kappa_A/g^2`; omitting that field-convention conversion creates a
false mismatch.

## Loop and Representation Scope

GK1 uses the fermion-shaped numerator `u(1-u)` for a declared complex scalar,
where accepted C-VAC-001 and C-NVP-001/002 require the scalar bubble--seagull
structure. Dividing a trace-weighted tensor by its own trace is an identity,
not a convention-preserving Abelian limit. Under generator rescaling,
`T(R)` changes quadratically and the coupling inversely, preserving `g^2 T(R)`.

## Physical and Substrate Scope

Local covariance, projector algebra, dimensional bookkeeping, and normalized
Riesz shape do not construct a kinetic normalization, propagating gauge boson,
unique total coupling, preferred dimension, dimensional lift, physical U1,
SU2, or SU3 sector, observable, or substrate dictionary. GK1's live-file
census is useful documentation regression but is not scientific authority.
Pending GK3D1 through GK3D4 must establish their own loop and matching claims.

## Verification and Dependency Replay

Primary, independent, and source-graph routes pass 50, 22, and 28 checks. The
14-node graph covers 168 predicate sites and 15 assertions. All nodes except
immutable YM2 and QCD2 run natively; those two use isolated `np.trapz` aliases
backed by `np.trapezoid`, so version compatibility causes no campaign failure.
The focused accepted-consumer replay passes 102 tests.
The controlled integrated workflow passes all 1,490 tests with 705 valid
memory records; an unchanged prior invocation is preserved as transport-
inconclusive because its detached session lost the terminal exit code.

## Four-Axis Decision

The source verdict and accepted claim state remain separate.

- Verification: exact evidence for trace, component-count, and conditional dimensional identities.
- Review: audited and qualified predicate by predicate.
- Compatibility: compatible only through C-DIM-009 and the cited accepted ceilings.
- Epistemic: qualified source evidence, not blanket promotion of GK1 prose.
- Release: v0.128.0 adds C-DIM-009 only.

## Closure

P176 adds the exact claim API and release while qualifying GK1 through
C-DIM-009, C-REP-002, C-LIE-001, C-VAC-001, C-NVP-001/002, and
C-KRN-001/002. The universal, logarithmic, physical-sector, coupling-
propagation, dimensional-lift, and substrate conclusions remain unaccepted.
