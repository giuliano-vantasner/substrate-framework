---
description: Independent disposition review of MD1 density of states and mode counting
author: vantasner-review
created: '2026-08-11T20:58:00Z'
updated: '2026-08-11T21:04:00Z'
tags:
- substrate-framework
- source-review
- MD1
- P196
category: decisions
confidence: established
status: active
---
# MD1 Disposition Review

## Object Under Review

P196 reviews MD1's d3 DOS, claim of exact finite rank `3V/a^3`, Debye cutoff,
gap-independent count, and assertion that no spectrum is needed for WN6's
participating-mode problem.

## Exact Result

The conditional continuum mathematics survives and is generalized by
C-DOS-001. The source's per-branch d3 formula and cutoff are exact corollaries
only after dimension, branch degeneracy, measure, and target count are supplied.

## Corrected Boundaries

Dimension is not polarization or component count. Continuum phase volume is
not exact finite rank. A target-matched cutoff is not microscopic lattice
geometry. Total modes do not select participating modes, couplings, states, or
rates. The accepted scalar model supplies no d3 lift.

## Compatibility and Consumers

MD1 and its nine-node graph have no legacy quadrature event. The graph covers
224 native checks. MD2, MD4, and MD6 reproduce but remain pending and receive
no blanket promotion.

## Recommendation

Accept C-DOS-001 and qualify MD1 through C-MED-003, C-SG-018, and C-DOS-001.
Reject the derived-medium, branch, exact-rank, cell, microscopic-cutoff, and
participation overreads.

