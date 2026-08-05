---
description: Accept the conditional complex-scalar D4 and affine kinetic-boundary theorem
author: vantasner
created: '2026-08-11T12:54:00Z'
updated: '2026-08-11T12:54:00Z'
tags:
- substrate-framework
- claim-review
- C-VAC-003
- vacuum-polarization
- renormalization
category: decisions
confidence: established
status: active
---
# C-VAC-003 Review

C-VAC-003 is accepted as a symbolic compatible extension. Conditional on a
separately declared free complex charged scalar, its scalar-QED determinant,
bubble and seagull, one-loop tensor convention, common shift-invariant gauge-
preserving dimensional regulator, and subtraction prescription, it derives
the exact general-dimensional parameter master and the D4 Laurent residue,
MS-bar finite family, and logarithmic slopes. In the convention of C-VAC-002,
the Dirac slope is exactly four times the complex-scalar slope.

For the connection field `B=e*A`, separately supplied invariant scalar and
Dirac weights compose as `b=W_s/3+4*W_f/3`. The resulting inverse-kinetic flow
has the full affine family
`Z(mu)=Z_ref+b*log(mu_ref/mu)/(8*pi^2)`. A reference-scale change must be paired
with the corresponding `Z_ref` coordinate change. The finite local term and
matching offset remain independent coordinates.

The zero-matching solution is accepted only as a separately declared branch.
Rung25 supplies no kinetic coefficient, charged threshold, counterterm, or
matching surface. C-MAX-001 proves that deleting the kinetic term yields the
current constraint, not that every connection is pure gauge. Therefore no
accepted premise fixes `Z_ref`, the reference scale, total normalization,
physical matter content, group, coupling, dimension, or substrate sector.

The decision is supported by 31 primary and 28 independent exact checks plus
80 focused regression tests. Wrong seagull, parameter-weight, statistics,
counterterm, boundary, scale-order, and reference-coordinate mutations change
the relevant verdict. External papers are normalization comparators only and
do not select the claim.

See `campaigns/P186-gk3d2-induced-kinetic-normalization-audit` and the accepted
v0.138.0 manifest.
