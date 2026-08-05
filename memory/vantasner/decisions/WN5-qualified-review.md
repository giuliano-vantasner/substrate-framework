---
description: Qualify WN5 through accepted branching and factorial-one composition
author: vantasner
created: '2026-08-11T19:34:00Z'
updated: '2026-08-11T19:34:00Z'
tags:
- substrate-framework
- source-review
- WN5
- P193
category: decisions
confidence: established
status: active
---
# WN5 Qualified Review

WN5 is qualified through C-BRN-001 and C-OSC-001. Their exact composition gives
`B_gamma(n)=rho/(N*S^n/n!+rho)` and an adjacent difference with the sign of
`n+1-S`. Noninteger S therefore has one minimum at `floor(S)`, positive integer
S has the tied minima `S-1,S`, and subunit S has its minimum at order zero.
Relative odds against order one equal `N*S^(n-1)/n!` on positive orders.

The source's finite `S=25` first-argmin grid hides the integer tie and omits the
order-zero endpoint. Its population derivative is a fixed-weight partial, not
a universal population-dependent path statement. Its rho-free ratio retains N
and S and is not a physical suppression magnitude.

The mathematical turnover contrasts three declared weight functions only at
fixed N, rho, channel definitions, and order meaning. No measured branching
prediction follows without accepted rates, exhaustive channels, interactions,
spectral data, an order observable, cross-order controls, and parameter
provenance. C-BRN-002 remains reserved and unpromoted because existing claims
and APIs already own the complete warranted object. WN7, MD5, and MD6 remain
pending.
