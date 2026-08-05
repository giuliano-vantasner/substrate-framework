---
description: Qualify GK3D5 through the U1 current and radial Q-ball branch
author: vantasner
created: '2026-08-05T20:34:00Z'
updated: '2026-08-05T20:41:45Z'
tags:
- substrate-framework
- source-review
- GK3D5
- P202
category: decisions
confidence: established
status: active
---
# GK3D5 Qualified Review

GK3D5 is qualified through C-U1-001 and C-QBL-004. The corrected positive
object is a declared classical complex-scalar radial branch with exact
normalizations and resolution-bounded existence evidence, not the source's
genuine charged quantum loop particle.

The source does not check solver success, holds its domain and shooting
classifier fixed, truncates growing-tail roundoff, and imports unsupported
stability and dimensional-lift readings. Its fitted inverse tail length is not
a particle rest mass or propagator pole. Accepted determinant claims declare
their loop fields independently and supply no identification map.

Nine pinned source nodes cover 116 static checks and 13 assertions without
duplicate native execution. GK3D6 remains pending. EL2 retains only its prior
accepted mapping. Immutable GK3D5's lazy legacy NumPy fallback is compatibility
evidence only; canonical code uses `trapezoid_integral`, independent mutable
code uses `np.trapezoid`, and no version event affects the scientific verdict.

The integrated promotion gate validates all 829 memory files and passes all
1,815 repository tests in 172.62 seconds. P202 attempt 0006 records exit zero,
185.55 seconds total wall time, and 217,480 KiB peak RSS.
