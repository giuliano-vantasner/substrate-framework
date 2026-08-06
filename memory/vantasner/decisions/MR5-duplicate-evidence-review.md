---
description: Terminal duplicate-evidence review of MR5 supplied-coupling stationary branches
author: vantasner-review
created: '2026-08-06T14:02:00Z'
updated: '2026-08-06T14:02:00Z'
tags:
- substrate-framework
- source-disposition
- MR5
category: decisions
confidence: established
status: archived
---
# MR5 Duplicate-Evidence Review

## Decision

MR5 is duplicate evidence for C-GSK-001 and C-RDIFF-001. Its supplied-point
stationary branches are useful regression evidence, but add no claim, API, or
release.

## Exact and numeric ceiling

The density, equation, opposite coupling scaling, and signed difference are
already owned. With accepted angular data and Robin boundaries, canonical
collocation gives `kappa=11.53644`, and fresh DOP853 shooting with Simpson
quadrature agrees. A bounded search locates one continuation-selected branch
minimum near `e=4.3263` on `[3,7]`. Neither result is a global profile minimum,
an all-positive-coupling floor, or a distinct invariant of the framework.

## Rejected extensions

MR4 supplies no accepted physical coupling. MR5 retains electron, pion, and
rho masses, `N_c=3`, and an ANW fit, while no accepted action/state map turns
degree into a baryon or light nucleus. Its mass, ratio, binding, convention-
bracket, and structural-falsification readings therefore lack closure. The
guard is refuted because executable E2, E3, MK5, ANW, and particle inputs evade
its selected needles.

## Verification and compatibility

Twenty-one primary, eleven fresh independent, and eight graph checks pass,
along with 87 focused tests. The preserved degree-four shooting residual is
repaired by tighter integration and amplitude-root resolution without relaxing
the threshold. MR5 and pending MR6 use current SciPy `trapezoid`; no version-
only event is a scientific failure.
