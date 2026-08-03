---
description: Terminal review of GB4's fixed-weight allocation and unsupported regime-independent physical suppression
author: vantasner-review
created: '2026-08-08T14:45:00Z'
updated: '2026-08-08T14:45:00Z'
tags:
- substrate-framework
- source-review
- branching
- weighted-allocation
- migration-GB4
category: decisions
confidence: established
status: archived
---
# Review of GB4 Terminal Qualification

## Claim Under Review

GB4 claims a gamma fraction `rho/(w(n)N+rho)` that decreases with collective
occupation for every positive weight regime, together with a rho-free
suppression enhancement. The review separates the accepted fixed-weight
allocation theorem from coupled-weight and physical interpretations.

## Sourced Inputs

The review reads v0.98.0, C-BRN-001 and its canonical module, the qualified GB1,
GB3, PN2, and PN3 dispositions, P125's frozen contract, all attempts, both
verifiers, and all evidence. GB4 is pinned at SHA-256
`497ed6deda4a0f11562baeaef0ec7bc21cc20b38d3d11c69ed07728ed33faeb0`.

Queue formulas and weight-family names were exposed before freeze; predicate
detail and runtime output were not. No numerical value selected a candidate or
verdict.

## Independence

The independent route imports neither the primary verifier nor a canonical
branching helper. It normalizes fresh symbolic inputs, derives adjacent steps by
cross multiplication, constructs exact positive weight sequences, locates the
exponential turning point, fits target shares, and tests third-channel and gate
countermodels. Its twenty-nine checks agree with the forty-nine-check primary
route.

## Verification Status

C-BRN-001 exactly supplies both fractions, endpoints, odds, common scaling, the
weighted positive-integer specialization, fixed-weight positive-real
derivative, relative weighted odds, unequal-gate residual, and free-target
ceiling. A direct adjacent-integer derivation is strictly negative at fixed
positive weight.

For a coupled weight, the total derivative has sign opposite `w+Nw'`, and the
discrete step has sign opposite the change in `Nw`. The source's named regimes
therefore share one sign only under its executable fixed-n convention.

## Preserved Failures

Attempts 0003 through 0005 preserve three independent-oracle defects. Each used
structural equality for an algebraically equivalent SymPy normal form: first
the fixed-weight denominator, then the coupled denominator, then the factored
exponential derivative. Exact zero-residual repairs closed each route without
changing a candidate, premise, threshold, or verdict.

## Sensitivity and Counterexamples

Fixed-weight derivative sign, adjacent-integer difference, and same-baseline
normalization fail under load-bearing mutations. A positive `w=1/N` makes the
gamma fraction constant and a faster inverse weight makes it rise. For n=N and
`w=exp(-alpha*n)`, the sign reverses after `alpha*N=1`; an exact alpha=log(4)
example rises from N=1 to N=2. Linear and positive-power n=N examples retain
the decline.

The source's one-point helper accepts a mutant that declines at its selected
N=3 sample and rises at N=4. Hidden rho dependence inside a modeled weight
evades its free-symbol test. Unequal gates and an omitted third channel change
the fraction, and zero coupling removes physical rates.

## Framework Compatibility

C-BRN-001 already covers the reusable exact surface and explicitly withholds a
weight law or physical channel. The adjacent-integer corollary has no distinct
governed consumer, while coupled-weight counterexamples qualify the source
rather than requiring a new API.

## Dependency and Consumer Replay

GB1 maps to C-BRN-001. GB3, PN2, and PN3 supply no physical rate or weight law.
All fourteen source-consumer hashes remain identical to P122's 576-check
replay. Reusing that durable boundary avoids rerunning an unchanged pending WN
cycle. GitNexus reports LOW risk, zero affected processes, and no canonical
change; all fifteen focused branching tests pass.

## Four-Axis Decision

The review accepts no new claim and terminally qualifies GB4.

- Verification: exact accepted fixed-weight algebra and exact coupled counterexamples
- Review: GB4 terminal disposition `qualified`
- Compatibility: native reuse of C-BRN-001
- Epistemic: qualified source evidence, not an accepted physical suppression claim
- Relationship: challenges and supersedes none

## Promotion Transaction

The transaction records GB4 as qualified, regenerates the source queue,
archives proposal memory, and checkpoints the parent effort. The registry,
v0.98.0, accepted docs and memory, and package APIs remain unchanged.

## Done Gate

Terminal qualification requires native reproduction, both exact routes, all
twenty-three predicate verdicts, fixed and coupled derivative and integer
mutations, weight and normalization countermodels, dependency and consumer
closure, synchronized queue state, one integrated workflow pass, and an empty
debt ledger.

## Cross-References

See GB4, GB1/P122, GB3/P124, PN2/P110, PN3/P111, C-BRN-001, P125, v0.98.0,
and the framework-migration effort.
