---
description: Accept the exact isotropic continuum density-of-states theorem
author: vantasner
created: '2026-08-11T21:10:00Z'
updated: '2026-08-11T21:14:00Z'
tags:
- substrate-framework
- claim-review
- C-DOS-001
- mode-counting
category: decisions
confidence: established
status: active
---
# C-DOS-001 Review

C-DOS-001 is accepted as a self-contained symbolic compatible extension. For
separately supplied positive spatial dimension `d`, branch degeneracy `b`,
volume `V`, speed `c`, and nonnegative gap `omega_0`, it derives the exact
isotropic continuum density of states under the declared phase-space measure.
Its integral to wave-number cutoff `K` is
`b*V*S_(d-1)*K^d/(d*(2*pi)^d)` and is independent of the gap. Inverting a
separately supplied positive target gives the unique positive matching cutoff.

The 40-check primary symbolic route, 28-check independent raw-SymPy route, 17
focused package tests, and threshold, normalization, mutation, and numerical
quadrature probes close the theorem. The `d=3` per-branch formula and the
`b=3`, `N=3*V/a^3` cutoff are retained only as conditional corollaries.

The claim does not identify spatial dimension with branch count, a continuum
ball integral with exact finite lattice rank, a supplied target with a derived
cell count, or a matching cutoff with a microscopic Brillouin-zone boundary.
It derives no participating-mode count, coupling, state, channel, rate,
material parameter, or substrate realization.

The promotion boundary validates 802 memory files and passes all 1,734 tests.
