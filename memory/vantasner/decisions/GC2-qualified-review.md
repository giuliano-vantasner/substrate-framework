---
description: Qualify GC2 as declared translated-well composition without a multisoliton or selected count
author: vantasner-review
created: '2026-08-05T23:16:00Z'
updated: '2026-08-05T23:16:00Z'
tags:
- substrate-framework
- source-review
- migration-GC2
- translated-localization
- multisoliton
category: decisions
confidence: established
status: archived
---
# GC2 Qualified Review

## Exact Surviving Content

GC2 correctly exposes that MH2 uses separately supplied translated external
wells with literal depth 12.0, width 0.7, spacing 4.0, and six centers. Their
exact ground states are isospectral under translation, have mean `R`, and have
centered variance `w^2*polygamma(1,s)/2`. C-OVL-002 owns this object.

The fixed external depth differs from C-QBL-005's quartic core depth
`6*kappa^2*sech(kappa*R)^2`; their ratio grows on the supplied ladder. This is
a comparison of declared models and derives neither well from the other.

## Multisoliton and Localization Correction

GC2 constructs one ground solve for each external Hamiltonian. It supplies no
common nonlinear field equation, simultaneous solution, interaction energy,
or stability theorem, so the wells are not established solitons. MH2 executes
six centers, not three.

The source quantity called a centroid is `E|x|`, and its convergence predicate
checks only that quantity. Exact translation replaces the incomplete numeric
oracle. Centered width divided by displacement tends to zero for any translated
fixed-width density and cannot by itself count physical objects.

## Spectrum and Count Correction

C-QBL-003's quartic translation tangent is an exact zero mode; the other
accepted level is negative and not a positive particle state. GC2's
exact-sine count three is copied from FG2's already rejected wall-contaminated
calculation. Only `p=2` among WM9's literal pure-sech trials `p=1,2,3` is a
quartic eigenfunction; the actual second mode is `sech*tanh`.

FG2 and FG4 both disclaim deriving observed count three, C-MIX-002 provides no
family map, and WM9 counts a literal tuple. The globals-name anti-fit guard is
also incomplete because it does not inspect reachable source strings.

## Verification and Decision

The primary and independent routes pass 37 and 20 checks. The terminal
14-node graph passes 39 checks over 107 predicates and 20 assertions, and 86
focused accepted-API tests pass. GC2 and its graph have no NumPy quadrature
compatibility surface.

GC2 is qualified through C-QBL-001, C-QBL-003, C-OVL-001, C-OVL-002,
C-MIX-002, and C-QBL-005. No multisoliton, selected count, exact-sine third
level, positive generation tower, stability, hierarchy, CP mechanism, or
physical map is accepted. v0.151.0 remains unchanged.
