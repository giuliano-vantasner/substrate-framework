---
description: Qualify MD1 through exact scalar dispersion and continuum mode counting
author: vantasner
created: '2026-08-11T21:10:00Z'
updated: '2026-08-11T21:14:00Z'
tags:
- substrate-framework
- source-review
- MD1
- P196
category: decisions
confidence: established
status: active
---
# MD1 Qualified Review

MD1 is qualified through C-MED-003, C-SG-018, and C-DOS-001. Its 27 native
predicates reproduce, and its per-branch `d=3` density, continuum-ball count,
gap independence at fixed wave-number cutoff, and target-matching algebra are
exact under the explicitly declared continuum measure.

The source does not derive its physical interpretation. The accepted scalar
medium is one-dimensional; spatial dimension and polarization degeneracy are
independent inputs. A continuum integral is not an exact finite periodic
lattice-point count or dynamical-matrix rank. `V/a^3` requires cell topology,
integer divisibility, degrees of freedom, constraints, and boundary data, and
a target-matched cutoff is not a microscopic Brillouin-zone boundary.

Nine byte-pinned native records cover 224 checks, with MD2, MD4, and MD6 as
the exact pending reverse consumers. The graph contains no NumPy quadrature
surface, so no `np.trapz` compatibility event is present and no version-only
failure contributes to the scientific verdict.

The single promotion boundary validates 802 memory files and passes all 1,734
tests. The generated migration queue has 28 pending units after MD1.
