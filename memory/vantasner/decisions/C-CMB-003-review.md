---
description: Accept the exact factorial-one shape generating moment and tail theorem
author: vantasner
created: '2026-08-11T19:07:00Z'
updated: '2026-08-11T19:07:00Z'
tags:
- substrate-framework
- claim-review
- C-CMB-003
- factorial-one
category: decisions
confidence: established
status: active
---
# C-CMB-003 Review

C-CMB-003 is accepted as a symbolic compatible extension of C-OSC-001. For
the normalized all-nonnegative mass `p_S(n)=exp(-S)S^n/n!`, it gives the exact
strict log-concavity quotient `(n+1)/n` while retaining the adjacent modes
`S-1,S` at positive integer S. It derives the PGF `exp(S(t-1))`, every
falling-factorial moment `S^r`, exact eventual geometric point and upper-tail
majorants, and decay faster than every fixed inverse power.

The 115-check primary oracle evaluates the package APIs and load-bearing
mutations. The 47-check independent route reconstructs raw coefficients,
modes, generating series, derivatives, and tail bounds without importing a
candidate or accepted scientific API. Thirty-seven focused tests and the
seventeen-node 662-predicate source graph support the exact boundary.

The theorem is mathematical only. A normalized Poisson mass does not derive a
Poisson process, occurrence rate, time variable, phase-space or energy-gap
law, power-law interpolation, subdivision mechanism, medium mean, branching
channel, or material prediction. The only direct claim dependency is
C-OSC-001; WN5 through WN7 and MD1 through MD6 remain pending.
