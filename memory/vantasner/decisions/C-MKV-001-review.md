---
description: Accept the exact immigration-death process and dynamical nonuniqueness theorem
author: vantasner
created: '2026-08-05T19:00:00Z'
updated: '2026-08-05T19:03:19Z'
tags:
- substrate-framework
- claim-review
- C-MKV-001
- birth-death
- Markov-chain
category: decisions
confidence: established
status: active
---
# C-MKV-001 Review

C-MKV-001 is accepted as a symbolic compatible extension of C-CMB-003. A
separately declared immigration-death chain on the nonnegative integers has
rates `r*S` and `r*n`, zero boundary death rate, reversible factorial-one
stationary mass, local drift `r*(S-n)`, exact mean, PGF, and deterministic-
initial transition kernel.

The 54-check primary route, 37-check independent raw master-equation route, 25
new package tests, and 28 focused dependency regressions close the theorem.
Boundary outflow, the `n+1` detailed-balance index, rate scale, constant-death
mutation, static-ratio interpretation, and sample-path interpretation are load
bearing. A distinct reversible generator with the same stationary mass proves
that static weights do not determine dynamics.

The state space, generator, initial law, `S`, and `r` are model declarations.
The claim does not derive a material parameter, state preparation, granularity
map, participation law, physical growth, open or rescued channel, transition,
branching, isotope effect, reaction, rate, or substrate realization.

C-MKV-001 is pinned in v0.148.0 with dependency closure through C-CMB-003
only. The integrated promotion gate validates 817 memory files and passes all
1,804 repository tests in 178.70 seconds with exit zero; P199 attempt 0008
records the wall time and peak memory.
