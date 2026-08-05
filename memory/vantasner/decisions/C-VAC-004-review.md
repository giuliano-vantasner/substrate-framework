---
description: Accept the conditional scale-matched affine kinetic composition theorem
author: vantasner
created: '2026-08-11T13:50:00Z'
updated: '2026-08-11T13:50:00Z'
tags:
- substrate-framework
- claim-review
- C-VAC-004
- dimensional-transmutation
- kinetic-matching
category: decisions
confidence: established
status: active
---
# C-VAC-004 Review

C-VAC-004 is accepted as a symbolic compatible extension. For independently
supplied positive lengths `ell0`, `ell1` and inverse-length energy conversions
`K0`, `K1`, the exact reference-to-evaluation energy ratio is
`(ell1/ell0)/(K1/K0)`. Composing its logarithm with C-VAC-003 preserves the
full affine family `Z=Z_ref+b*L/(8*pi^2)`.

On C-RGE-003's consistently paired formal one-loop branch,
`ell1/ell0=(K1/K0)*exp(8*pi^2/(b0*g^2))`. The conversions therefore cancel
without requiring equality, and the general result is
`Z=Z_ref+b/(b0*g^2)`. Only a separately imposed zero-matching branch with
positive `b` has the inverse kinetic coordinate `b0*g^2/b`.

The theorem selects no physical scale labels, conversion factors, one-loop
inputs, matter weights, matching boundary, gauge group, field normalization,
or physical coupling. Common length rescaling leaves relative data unchanged
while shifting both absolute energies. An unpaired soliton coefficient changes
the logarithm. Power zero is a constant, and exact rational functions of
`log(y)` refute the source's logarithm-uniqueness claim.

The decision is supported by 31 primary and 20 independent exact checks plus
51 focused tests. Conversion, orientation, affine-boundary, rescaling,
soliton-factor, zero-matter, power-zero, and hidden-float mutations exercise
the load-bearing paths. See
`campaigns/P187-gk3d3-transmutation-logarithm-audit` and v0.139.0.
