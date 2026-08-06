---
description: Accepted review of C-GSK-001 exact generalized radial model
author: vantasner-review
created: '2026-08-06T11:41:41Z'
updated: '2026-08-06T11:41:41Z'
tags:
- substrate-framework
- claim-review
- C-GSK-001
category: decisions
confidence: established
status: archived
---
# C-GSK-001 Review

## Decision

C-GSK-001 is accepted as an exact conditional reduced-model claim. Fresh
symbolic variation establishes the L2+L4+L6+L0 Euler-Lagrange equation,
nonnegativity, Derrick weights, endpoint linearization, the C-RPROF-001 limit,
and the C-VEC-002 lambda-convention conversion.

## Scope

Degree, angular integral, and both dimensionless coefficients are separately
supplied. The claim derives no coefficient value, physical action, rational
map, existence theorem, minimizer, full field, particle, nucleus, binding
energy, observation, or substrate interpretation. Its dependencies are
C-RMAP-001, C-RPROF-001, C-BPS-001, and C-VEC-002.

## Evidence

Twenty-seven primary checks, twelve fresh independent checks, load-bearing
angular, sextic, tail, and convention mutations, 65 focused tests, and the
twenty-node source graph support the exact claim. The reusable implementation
is `src/substrate_framework/generalized_skyrme_radial.py`; P218 preserves the
full derivation and review record.
