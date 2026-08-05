---
description: Qualify BX1 through exact radial spectral typing and accepted averaged-operator ceilings
author: vantasner-review
created: '2026-08-11T06:02:00Z'
updated: '2026-08-11T06:02:00Z'
tags: [substrate-framework, source-review, migration-BX1, finite-box]
category: decisions
confidence: established
status: archived
---
# BX1 Qualified Review

## Source Unit Under Review

BX1 presents eight passing predicates and concludes that QB3's time-averaged
l=2 object is a Dirichlet-box artifact, that no l=2 bound state exists for its
profile, and that the only genuine internal mode is l=0.

## Surviving Content

Native and instrumented runs succeed. The R=80 fixed-guess branch is above the
unit threshold and multi-node. The lowest self-adjoint l=2 level for the
source-defined averaged potential is resolution stable, approaches the vacuum
spherical-Bessel wall level from above, has inverse-wall-square gap, and fills
a fixed fraction of the ball. A pure-vacuum standing wave passes QB3's
localization test after the outer tail is imposed as zero.

## Corrected Spectral Scope

The fixed-guess wall scan selects different multi-node branches and does not
prove that every continuously tracked level lacks a limit. Robust node
filtering changes several counts, and no linear-growth predicate runs. The
source claims five to forty-two nodes and an l=0 family endpoint 0.4015 while
its pinned execution reports five to forty-one and 0.459073.

The Rayleigh implication is exact only if the displayed excess potential is
nonnegative almost everywhere. Sampling 8,000 points on a finite interval
does not prove that premise. P054 independently established the narrower
accepted-background fact: its time-averaged R=40 level is above threshold,
wall sensitive, and outer-norm filled.

## Averaged and Physical Scope

The l=0 control belongs to a source-defined time-averaged operator. C-PDE-009
requires a separate Floquet construction before it can be called a genuine
full-periodic mode. No all-channel scan supports “only genuine internal mode.”
The finite-wall result supplies no nonlinear triaxial deformation, conserved
gravitational source, physical radiation, absolute scale, particle identity,
corpus-wide replacement mechanism, or substrate realization.

## Verification and Compatibility

Primary, independent, and graph routes pass 39, 22, and 24 checks; 103 focused
tests pass. The graph replays 72 source predicates and 15 assertions. BX1 runs
natively. Immutable P3D2, QB3, QB4, and TX1 receive isolated `np.trapz`
aliases backed by `np.trapezoid`, so their version spelling causes no campaign
failure or change in scientific status.

## Four-Axis Decision

- Verification: exact evidence for C-PDE-012; numeric evidence for scoped finite-wall behavior.
- Review: audited and qualified predicate by predicate.
- Compatibility: native through C-PDE-003/005/009/012.
- Epistemic: qualified source evidence, not blanket promotion of BX1 prose.
- Release: v0.129.0 adds C-PDE-012 only.

## Closure

Qualify BX1 through C-PDE-003, C-PDE-005, C-PDE-009, and C-PDE-012. SC2 and
TX1 through TX3 remain pending and inherit no accepted route-closure premise.
