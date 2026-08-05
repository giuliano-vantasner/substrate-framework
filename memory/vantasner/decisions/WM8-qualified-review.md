---
description: Qualify WM8 as an exact conditional weighted-boundary inverse-running specialization
author: vantasner-review
created: '2026-08-05T22:20:00Z'
updated: '2026-08-05T22:20:00Z'
tags:
- substrate-framework
- source-review
- migration-WM8
- gauge-running
- inverse-inference
category: decisions
confidence: established
status: archived
---
# WM8 Qualified Review

## Exact surviving content

WM8 specializes C-RGE-006's exact zero-matrix boundary solver. With supplied
boundary ratios `S`, one-loop vector `b`, low constraints `C*a=d`, and
`a=A*S+q*b`, the nonsingular columns `C*S` and `C*b` uniquely determine `A`
and `q`. The selected one-scalar inputs give positive coordinates, zero
residuals, and readout `0.216221801107...`.

## Scalar-count correction

The source varies `N_H` only in `S` while retaining one-scalar beta
coefficients. Its exact boundary-only readout is
`19*(91299*N_H+1325644)/(452766*(7*N_H+268))` and gives `0.232261554419...`
at three scalars.

A coherent count change also updates the beta vector. Its exact readout is
`(236383*N_H+2211064)/(452766*(N_H+24))` and gives `0.238878442809...` at
three scalars. The paths agree only at one scalar. Numerical proximity cannot
select a multiplicity that accepted claims do not derive.

## Interpretation and verification

The two low coordinates, reference scale, boundary ratios, normalization, and
zero matching offsets are supplied. Comparator absence from the solve is real,
but WM8's named perturbation repeats identical arguments. Matching offsets,
targets, boundaries, and coherent beta changes move the readout. No physical
input provenance, uncertainty, threshold, matching, Yukawa, scheme,
perturbative-domain, unification, observation, or substrate conclusion follows.

The source reproduces ten checks. Primary and independent routes pass 37 and
19 checks after three preserved construction repairs. The 13-node graph passes
39 checks over 118 predicates and 15 assertions, and twelve focused API tests
pass. WM8 and mutable P205 have no quadrature surface; immutable S2's legacy
syntax is alias-only compatibility evidence.

## Four-axis decision

- Verification: exact symbolic evidence for design, solution, readout,
  sensitivity, and coherent counterfactuals.
- Review: audited predicate by predicate and qualified.
- Compatibility: accepted composition of C-MIX-002, C-REP-001, C-REP-003,
  C-RGE-004, C-RGE-005, C-RGE-006, and C-VAC-003.
- Epistemic: qualified source evidence, not a new claim.
- Release: v0.150.0 unchanged.

## Closure

C-RGE-008 remains reserved and unpromoted. No package or release surface
changes. WM8's terminal disposition, queue, campaign, and durable memory are
the complete governed delta.
