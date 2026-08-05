---
description: Accept the exact population-dependent weighted-allocation derivative criterion
author: vantasner
created: '2026-08-05T19:25:00Z'
updated: '2026-08-05T19:30:00Z'
tags:
- substrate-framework
- claim-review
- C-BRN-002
- branching
- monotonicity
category: decisions
confidence: established
status: active
---
# C-BRN-002 Review

C-BRN-002 is accepted as a symbolic compatible extension of C-BRN-001. For a
separately declared positive differentiable weight `w(N)` and comparison ratio
`rho>0`, the exact derivative of `rho/(N*w(N)+rho)` has sign opposite
`w+N*w'`. This supplies the complete decreasing, stationary, and increasing
trichotomy and preserves the constant-weight C-BRN-001 specialization.

The 19-check primary route, 12-check independent raw-function route, 21
focused branching tests, and 19-check source graph close the theorem. Removing
the `N*w'` term is load bearing; the positive weights `N^(-1/2)`, `N^(-1)`, and
`N^(-2)` realize all three verdicts. Integer-only counts require adjacent
ordering of `N*w(N)` rather than an undeclared continuous derivative.

The weight law, common rate dimensions, exhaustive channel set, and physical
meaning remain independent premises. The claim derives no material population
law, isotope map, state preparation, interaction, reaction, branching
observable, rate, yield, heat, or substrate realization. It is pinned in
v0.149.0 with dependency closure through C-BRN-001 only.

The integrated promotion gate validates all 822 memory files and passes all
1,810 repository tests in 167.99 seconds with exit zero. P200 attempt 0010
records 181.00 seconds wall time and 218,320 KiB peak RSS.
