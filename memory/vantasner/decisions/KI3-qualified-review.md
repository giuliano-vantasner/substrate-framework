---
description: Qualify KI3's explicit interpolants and reject its universal sharp bracket
author: vantasner-review
created: '2026-08-11T03:20:00Z'
updated: '2026-08-11T03:20:00Z'
tags:
- substrate-framework
- source-review
- migration-KI3
- interpolation-range
category: decisions
confidence: established
status: archived
---
# KI3 Qualified Review

## Source Unit Under Review

KI3 claims that zero and a classical coefficient are the endpoints of one
physical interpolation, that their closed bracket is exactly the attainable
set, and that the unspecified interpolation creates a second free object.

## Sourced Inputs

The review read v0.127.0, C-BPS-002/003, C-RDIFF-001/002, C-XOV-001,
P107 and P172 adjudications, canonical `crossovers.py`, exact KI3 and dossier
bytes, source history, the pinned Phase-34 Lean file, and the typed
E3/E4/KI2-KI4/MK4-MK6/MR6 graph. Pending later sources are evidence only.

## Exact Surviving Content

KI3's Pade, exponential, tanh, and algebraic functions each approach zero at
positive epsilon tending to zero, approach `kappa_cl` at infinity, and are
strictly increasing. Their exact ranges are open. Their inverse values at a
comparator-free normalized level one-half are `1`, `log(2)`, `atanh(1/2)`, and
`1/sqrt(3)`, so endpoint data alone do not select an inverse function.

C-XOV-001 already owns the generic exact range and inverse theorem when
continuity, strict monotonicity, actual range, and endpoint typing are supplied.
The four KI3 functions have no accepted physical selection or consumer that
would justify a new claim or interpolant API.

## Rejected Universal Bracket

Continuity and endpoint limits imply interior inclusion, not outside exclusion
or uniqueness. The exact map
`epsilon(epsilon+5)/(epsilon+1)^2` preserves the zero and one limits, passes the
source's derivative test at epsilon one-half, reaches three-halves at epsilon
one, and reaches six-fifths at two distinct positive inputs. Reversing its bump
produces minus one-half while preserving the limits. KI3's declared codomain
already assumes the exclusion it claims to derive.

On the source's strictly positive domain its four examples do not attain either
endpoint, so their exact ranges are `(0,kappa_cl)`, not the closed bracket.
C-BPS-003 supplies no global interpolation or nonzero first-order coefficient;
C-RDIFF-002 is a conditional coordinate, not a ceiling or BPS limit; and P172's
KI2 result ranges across distinct theories without identifying a physical
epsilon. The source also uses stale 8.4563 input instead of accepted 8.4824.

## Comparator and Formal Scope

The source's 0.929 comparator enters `ratio`, four back-solves, their spread,
and the `spread > 1.05` pass condition. A small comparator-level mutation flips
that verdict. The exact inverse ambiguity survives only after replacing this
with a symbolic or rational interior level.

The hash-identical Lean capstone was compiled in P172 and was not rerun as
ceremony. Its exact theorem proves surjectivity and inverse substitution for one
locally defined Pade function; it does not quantify over arbitrary continuous
maps or encode the missing physical premises.

## Four-Axis Decision

The source verdict and unchanged accepted claim state are recorded separately.

- KI3 verification: exact symbolic evidence for four witnesses and exact
  counterexample evidence against the universal inference.
- KI3 review: audited and qualified with individual predicate verdicts.
- KI3 compatibility: compatible as generic witness evidence and in conflict as
  a framework-wide exact-bracket theorem.
- KI3 epistemic: qualified source evidence, not an accepted active claim.
- Accepted C-XOV-001, C-BPS-003, and C-RDIFF-002 states: unchanged.
- Relationship: no challenge, supersession, physical interpolation, or release.

## Closure

P173 updates campaign, KI3 disposition, generated queue, proposal and decision
memory, and parent effort. KI4 and later MK/MR consumers remain pending. No
accepted claim, canonical API, generated documentation, or release changes.
Twenty-four focused tests and both full 1,478-test executions pass with 696
valid memory records.
