---
description: Independent claim-level review of exact cosine approximation and harmonic amplitude conventions
author: vantasner-review
created: '2026-08-05T16:55:00Z'
updated: '2026-08-05T17:02:00Z'
tags:
- substrate-framework
- claim-review
- C-OSC-002
- P194
category: decisions
confidence: established
status: active
---
# C-OSC-002 Claim Review

## Claim Under Review

Let `x` be real, `V(x)=1-cos(x)`, `Q(x)=x^2/2`, and `E(x)=Q(x)-V(x)`.
The proposal claims `0 <= E(x) <= x^4/24` globally. For nonzero `x`, this
implies `E/Q <= x^2/12`, so a positive tolerance `epsilon` is guaranteed on
`|x| <= sqrt(12*epsilon)`. It also claims that the cycle mean square of
`P*cos(omega*t+delta)` for real nonzero `omega` is `P^2/2`, with RMS
`|P|/sqrt(2)`.

## Exact Verification

The lower gap is the exact integral of
`(y-t)*(1-cos(t))` from zero to `y=|x|`. The upper complement is the exact
integral of `(y-t)^3*(1-cos(t))/6` on the same interval. Both kernels are
nonnegative, proving the two global inequalities without a grid or fitted
tolerance. Direct full-period integration independently gives `P^2/2`.

The 45-check primary route evaluates the canonical APIs and rejects changed
denominators, tolerance radii, and harmonic factors. The 25-check independent
route imports no candidate scientific API and reconstructs the integral
certificates, cycle average, signed-amplitude counterexample, and multi-mode
nonidentifiability families. Nineteen focused package tests pass.

## Domain and Convention Review

The relative error uses the quadratic approximation as denominator and is
stated only for `x != 0`; the continuous zero-coordinate limit is zero. The
radius is sufficient, not claimed maximal. `epsilon` is a caller-selected
positive accuracy requirement, not a fitted parameter.

Peak amplitude, RMS amplitude, and C-OSC-001's Fock coordinate `q_0` are not
interchangeable. If `A` means RMS, `S=A^2` is mean square and the conditional
limb boundary is `A=sqrt(n)`. If `A` means harmonic peak, mean square is
`A^2/2` and the boundary is `A=sqrt(2*n)`. No accepted claim identifies either
classical amplitude with `q_0`.

## Mutation and Limiting Review

At the cosine barrier `x=pi`, the exact relative-to-quadratic error is
`1-4/pi^2`, greater than 59 percent. This decisively rejects the barrier as a
universal small-error boundary. The exact bounds vanish with the correct
second- and fourth-order limits at the origin. A signed negative amplitude
breaks WN6's unqualified `A>sqrt(n)` equivalence even though its square exceeds
`n`, so positivity is load bearing.

## Nonduplication and Scope

C-SG-019 owns the entire cosine coefficient series but explicitly leaves
finite-approximation remainder control open. C-OSC-001 owns `q_0^2` and
factorial-one masses but no classical harmonic average. C-OSC-002 therefore
adds a distinct theorem and API. It derives no material amplitude, quantum
state, multimode displacement, density of states, topological winding,
probability, rate, reaction, or substrate realization.

## Recommendation

Accept C-OSC-002 as a symbolic-verified compatible extension depending on
C-SG-019 and C-OSC-001. Promote only the exact remainder, tolerance-domain,
harmonic mean-square, RMS conversion, and convention-separation statements.

