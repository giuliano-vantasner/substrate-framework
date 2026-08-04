---
description: Qualified review of QCD5 dimensional-overdetermination bridge
author: vantasner-review
created: '2026-08-10T18:42:00Z'
updated: '2026-08-10T18:45:00Z'
tags: [substrate-framework, source-review, migration-QCD5, dimensional-identifiability]
category: decisions
confidence: established
status: archived
---
# QCD5 Qualified Review

## Decision

QCD5 is qualified through C-LIE-003, C-NVP-002, C-KRN-001, C-KRN-002, and
C-LIN-001 with no new claim, API, or release. Its exact shared Riesz exponent
and fixed-input substitutions survive; its independent three-sector
overdetermination headline does not.

## Corrected Positive Object

For supplied `s`, inverse-square behavior gives the accepted family
`d=2s+1`. At `s=1`, one equation uniquely gives `d=3`. Three named copies have
the same coefficient row, rank one, and two dependencies; they are a repeated
conditional specialization, not three independent constraints.

## Retained and Rejected Content

The standard SU3 half-trace metric, shared exponent, fixed-`s` uniqueness, and
`s=3/4 -> d=5/2` conditionality witness are retained in accepted scope. Sector
labels and amplitudes never enter the rows. A fabricated nonzero `kappa(d)`
does not change the radial exponent, so its source guard is off target. No
endpoint selection, geometry, dimensional lift, physical gauge sector, or
substrate dimension is promoted.

## Compatibility and Closure

Native QCD5 passes all seven predicates and has no NumPy integration surface.
Immutable YM2 and QCD2 use isolated compatibility aliases backed only by
`np.trapezoid`. Primary, independent, focused accepted-API, and frozen-graph
routes pass 32, 14, 46, and 20 checks or tests. The graph records 91 lexical
check sites and 99 runtime executions across eight units. No accepted consumer
or release changes.

## Cross-References

See P162, C-KRN-001, C-KRN-002, C-LIN-001, the predicate and source audits,
independent rank review, semantic graph, impact analysis, and v0.124.0.
