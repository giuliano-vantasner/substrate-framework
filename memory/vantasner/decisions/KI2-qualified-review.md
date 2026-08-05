---
description: Qualify KI2 as parameter-family freedom and reject its fixed-theory symmetry
author: vantasner-review
created: '2026-08-11T02:35:00Z'
updated: '2026-08-11T02:35:00Z'
tags:
- substrate-framework
- source-review
- migration-KI2
- parameter-family
category: decisions
confidence: established
status: archived
---
# KI2 Qualified Review

## Source Unit Under Review

KI2 claims that an explicit simultaneous scaling of the generalized-Skyrme BPS
couplings leaves every framework-derived quantity invariant while sweeping a
near-BPS epsilon through all positive values.

## Sourced Inputs

The review read v0.127.0, C-BPS-001/002/003, C-SK-001, canonical
`bps_energy.py`, P107's accepted evidence, P171's KI1 refutation, exact KI2 and
dossier bytes, their source history, the pinned Phase-34 Lean file, the typed
E3/E4/S4/NY1/NY2/KI1-KI4/MK1-MK3 graph, migration records, and local memory.
Untracked Phase-47 material is excluded from the governed predecessor baseline.

## Reproduction and Definitions

KI2 imports only SymPy and executes all six predicates. Its unique conditional
dimension tuple is `[F_pi,e,lambda,mu]=[1,0,-1,2]`; the displayed three vectors
form a basis of the dimension kernel; and their reciprocal product equals the
source's locally defined positive ratio. No coefficient fixes the normalization,
and no map identifies this expression with C-BPS-003's abstract epsilon.

## Fixed Theory Versus Parameter Family

The proposed flow sends both `lambda` and `mu` to `t` times themselves. Under
C-BPS-001, it scales the BPS energy density and Bogomolny square by `t^2`, the
saturation residual by `t`, and the bound by `t^2`. It therefore changes a fixed
theory. KI2.3's six-item invariant dictionary omits every one of those accepted
BPS objects.

Across the accepted family of positive parameter choices, the local ratio does
realize every positive target even with `F_pi,e` fixed. That is the valid
positive object. It compares distinct theories and is already implicit in
C-BPS-001's arbitrary positive inputs.

## Scope Corrections

Equal energy dimension does not prove that two scales are physically
independent; `lambda*mu=c*F_pi/e` is dimensionally allowed. Supplying a relation
for the product is enough to pin the local ratio, so importing both couplings
individually is not the unique weakest remedy. A finite registry cannot prove
that every future derived quantity is invariant.

Refuted KI1 supplies no premise. Pending MK1, MK2, and MK3 are counterrelations
only and select no accepted values. C-SK-001 remains a conditional scale
relation and does not individually select `F_pi` or `e`.

## Verification and Formal Scope

The primary, fresh independent, and typed graph routes pass 45, 21, and 59
checks. The independent route imports neither KI2 nor the primary verifier and
mutates all four dimension inputs, nontrivial flow powers, ratio normalization,
and a dimensionally allowed product relation. The twelve-node graph covers 81
predicates and ten assertions; KI1 alone fails at its governed refutation.

The pinned Lean capstone exits cleanly. Its exact encoding proves local ratio
scaling, a nontrivial ratio move, and invariance of `derivedScale := F/e`. It
contains no BPS energy density or bound and therefore cannot prove KI2's
headline interpretation.

## Four-Axis Decision

The four axes keep the source qualification separate from accepted claim state.

- KI2 verification: exact symbolic evidence for the qualified algebra and
  family statement; exact counterexample evidence against fixed-theory
  symmetry.
- KI2 review: audited and qualified, with individual predicate verdicts.
- KI2 compatibility: compatible as a parameter-family statement and in
  conflict as a fixed-theory invariance theorem.
- KI2 epistemic: qualified source evidence, not an accepted active claim.
- Accepted C-BPS-001, C-SK-001, and C-BPS-003 states: unchanged.
- Relationship: no challenge, supersession, physical epsilon, or new release.

## Closure

P172 updates only campaign, disposition, queue, proposal/review memory, and the
parent effort. No new claim or API survives nonduplication. The accepted set
remains 163 and the current release remains v0.127.0. Twenty-seven focused
consumers pass; the integrated workflow and explicit full suite each pass all
1,478 tests with 694 valid memory files.
