---
description: Qualify GK3D2 through the scalar D4 and affine-boundary theorem
author: vantasner
created: '2026-08-11T12:54:00Z'
updated: '2026-08-11T12:54:00Z'
tags:
- substrate-framework
- source-review
- GK3D2
- P186
category: decisions
confidence: established
status: active
---
# GK3D2 Qualified Review

GK3D2 is qualified. Its complex-scalar logarithmic slope, exact factor four
against the Dirac slope, conditional one-third and four-thirds invariant
weights, affine flow equation, common-scale invariance, and explicitly imposed
zero-boundary specialization survive through C-VAC-003.

Its headline normalization does not survive. The source's scalar helper omits
the determinant, bubble, seagull, regulator scale, Laurent pole, and
counterterm. More importantly, rung25 constructs exact-connection witnesses
but defines no kinetic coefficient or matching surface. Introducing charged
matter and the local loop operator changes the theory and operator basis, so a
no-matter absence statement cannot erase the new theory's affine integration
constant.

The governed result retains `Z_ref`, local and finite matching coordinates,
matter weights, and scale mapping. `Z_ref=0` is one separately declared
compositeness or matching model. Scale ordering controls the sign only on that
branch; it does not select the general total or a physical gauge coupling.

GK3D3, GK3D4, and GK3D6 directly consume the rejected boundary reading, and
GK3D5 consumes it transitively. They remain pending and may inherit only the
conditional slopes, matter-weight formula, affine family, and explicitly
assumed zero-matching branch. Existing qualified GK3D1, EL2, and out-of-scope
HE5 gain no additional authority.

No NumPy compatibility event occurred in GK3D2 or its canonical implementation.
The pending GK3D5 source uses the current trapezoidal name first with a lazy
legacy fallback; any future compatibility stop remains version-only evidence,
not a physics failure.
