---
description: Independent review of the controlled near-BPS signed-difference expansion
author: vantasner-review
created: '2026-08-03T16:32:00Z'
updated: '2026-08-03T16:32:00Z'
tags:
- substrate-framework
- claim-review
- near-bps
- asymptotic-expansion
category: decisions
confidence: established
status: archived
---
# Review of C-BPS-003

## Claim Under Review

C-BPS-003 states that for positive integers `A,n`, dimensionless
`epsilon->0+`, finite fixed-degree corrections, and controlled expansions
`M_epsilon(D)=K*D+epsilon*Delta_D+r_D(epsilon)` at `D=A,nA`, the signed
difference is exactly
`epsilon*(n*Delta_A-Delta_nA)+n*r_A-r_nA`. If both remainders are
`o(epsilon)`, the difference has that leading coefficient plus `o(epsilon)`;
if they are `O(epsilon^2)`, the residual is `O(epsilon^2)`. The claim derives
no coefficient sign, magnitude, interpolation, or physical meaning.

## Sourced Inputs

The review reads C-BPS-002, C-RDIFF-001, P107's frozen asymptotic contract,
attempts 0001 through 0005, primary and independent verifiers, E4.5, the
uncontrolled-remainder and compacton-edge counterexamples, package tests,
consumer audit, and hash-pinned KI/MK sources only as noncanonical impact
evidence.

## Independence

The primary route calls the canonical ledger after independently deriving its
expected expression and limits. The independent reviewer constructs both mass
expansions from fresh symbols and subtracts them without importing the P107
BPS module. It separately derives the standard-potential compacton edge
behavior and the divergent naive L2 correction.

## Verification Status

The maximum verdict is `symbolic_verified`. Exact expansion cancels the common
degree-linear term and retains the correction and remainder combinations.
Symbolic limits verify the `O(epsilon^2)` specialization. The theorem's
asymptotic conclusion is conditional on stated remainder control; an
uninterpreted function name is not itself such control.

## Sensitivity and Counterexamples

Breaking degree conservation leaves a nonzero zeroth-order term. Correction
choices make the first-order coefficient positive, zero, or negative. A
remainder proportional to `sqrt(epsilon)` makes the ratio to `epsilon` diverge
and invalidates an `O(epsilon)` inference. For the exact standard
`V=1-cos(chi)` compacton, the independent route finds a simple pole with
coefficient two in the L2 edge integrand, so the naive first-order L2
correction diverges logarithmically even though the L4 edge factor remains
finite.

## Framework Compatibility

The claim is a controlled asymptotic composition of C-BPS-002 and
C-RDIFF-001. It does not assert that E4's L2+L4 deformation admits the required
expansion, that epsilon is numerically small, or that a formal order explains
a physical binding coefficient, reaction, or yield.

## Dependency and Consumer Replay

The claim depends on C-BPS-002 and C-RDIFF-001. KI3 cannot infer a global
continuous interpolant, sharp bracket, or inverse from a local controlled
expansion. MK4's pending compacton route is independently reproduced only as a
counterexample to E4's perturbative application. MK5 and later full-model
solves remain separate numerical obligations with coupling and convention
debts.

## Competing Candidate Audit

Candidate F was compared with E4's exact no-remainder ansatz, arbitrary
remainders, correction cancellation, and the standard compacton. The
controlled theorem was selected because it preserves the positive asymptotic
object while exposing every assumption. It is distinct from C-RDIFF-001
because it governs the limiting remainder needed by multiple pending
near-BPS consumers.

## Four-Axis Decision

The controlled asymptotic theorem is accepted on four independent axes.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-BPS-002 and C-RDIFF-001; challenges and supersedes none

## Promotion Transaction

Promotion adds C-BPS-003 with the shared near-BPS ledger, immutable P107
counterevidence, qualified E4 disposition, release v0.91.0, and synchronized
generated records. It does not promote the standard-potential compacton or any
pending coupling claim as a separate accepted object.

## Continuation if Not Accepted

If coefficient visibility, remainder control, degree balance, or consumer
ceilings fail, the claim returns for a new P107 attempt. E4's formal cancellation
cannot be relabeled physical smallness to bypass those gates.

## Done Gate

Acceptance requires exact expansion, independent derivation, remainder and
degree counterexamples, compacton application audit, importable API, tests,
synchronized records, one integrated boundary gate, and no debt.

## Cross-References

See P107, E4.5, C-BPS-001, C-BPS-002, C-RDIFF-001, KI3, MK4,
`bps_energy.py`, release v0.91.0, and the framework-migration effort.
