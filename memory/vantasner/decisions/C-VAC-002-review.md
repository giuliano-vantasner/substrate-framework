---
description: Independent review and acceptance decision for C-VAC-002
author: vantasner
created: '2026-08-11T11:57:00Z'
updated: '2026-08-11T11:57:00Z'
tags:
- substrate-framework
- claim-review
- P185
- C-VAC-002
category: decisions
confidence: established
status: active
---
# C-VAC-002 Review

## Claim Under Review

C-VAC-002 gives an exact conditional charged-Dirac one-loop polarization
ledger. It separates integration dimension from integer spinor trace, derives
the Ward contraction from the free inverse-propagator trace difference, and
states the general spacelike master, fermionic D=2 endpoint, fixed-trace
regulated D=4 Laurent and MS-bar family, below-threshold subtraction series,
and group-convention weight.

## Independence and Sensitivity

The primary route passes 27 exact checks. The independent route imports no
canonical Dirac-polarization module and passes 23 checks using generic matrix
algebra, fresh Gamma limits, six beta integrals, and 80-digit adaptive
quadrature. Wrong Ward sign, doubled spinor trace, shifted finite counterterm,
threshold crossing, and unpaired generator rescaling all change or invalidate
their load-bearing result. A metadata typo in the charge dimension was found
and repaired before promotion; code, equations, and tests already used the
correct squared-charge dimension `4-d`.

## Four-Axis Decision

C-VAC-002 is `symbolic_verified`, `accepted`, `compatible_extension`, and
`active`, with no challenge or supersession edge. It depends only on
C-GAU-001 and C-DIM-009. C-VAC-001 remains a separate complex-scalar D=2
bubble-plus-seagull theorem and is a comparator, not a dependency.

## Scope Decision

The theorem imports the charged Dirac field, determinant, loop order, charge,
mass, regulator, tensor and effective-action conventions, and subtraction
scheme. It fixes neither the arbitrary finite local counterterm nor any bare
or total kinetic coefficient. It derives no physical charged matter, gauge
group, preferred dimension, on-shell polarization count, dimensional lift,
observation, or substrate mechanism.

## Cross-References

See P185, GK3D1, the claim review, source adjudication, attempts 0004 through
0006, v0.137.0, C-GAU-001, C-DIM-009, C-VAC-001, and the framework-migration
effort.
