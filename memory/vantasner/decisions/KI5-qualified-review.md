---
description: Qualify KI5 through the accepted signed-difference and stationary-profile ceilings
author: vantasner-review
created: '2026-08-11T04:23:00Z'
updated: '2026-08-11T04:31:00Z'
tags:
- substrate-framework
- source-review
- migration-KI5
- variational-bound
category: decisions
confidence: established
status: archived
---
# KI5 Qualified Review

## Source Unit Under Review

KI5 says a signed energy difference inherits no one-sided variational bound and
uses selected profile degradations to draw profile-quality and physical lessons.

## Exact Surviving Content

For separately declared upper estimates with nonnegative slacks, the signed
difference error is exactly `alpha*(n*delta_initial-delta_final)`. It realizes
both signs, so independent upper estimates yield neither a universal upper nor
lower bound on their difference. C-RDIFF-001 already owns this theorem.

Additional premises matter. A relation between the two slacks can give a
conditional one-sided bound, while componentwise error control gives a
two-sided interval and convergence even when the signed estimate alternates
around truth. Improving component calculations is therefore meaningful; what
does not follow is monotone tightening of a one-sided kappa ceiling.

## Variational and Numerical Scope

C-RPROF-002 supplies resolution-bounded stationary branches and expressly
proves no local or global minimum, variational upper bound, or full
three-dimensional solution. KI5 checks eight width rescalings, consumes a
`solve_bvp` result without a success gate, and uses hard finite-wall data. An
exact counterfamily is positive at every sampled width and negative at an
unsampled width, so those probes cannot establish minimization.

The source reproduces stale `kappa=8.4574`; C-RDIFF-002 owns the corrected
conditional coordinate 8.482417318795285 and denies physical binding,
reaction, empirical, and variational-bound readings. Numerical convergence
inside an ansatz is not an ansatz-error bound to a full model.

## Comparator and Formal Scope

Comparator 0.929 enters both KI5.4 pass predicates, and changing only the
comparator flips the verdict. The B4 degradation is a valid example against a
universal monotone proximity rule, but it proves neither that proximity is
evidence of nothing under every error model nor that physical ninefold
overbinding stands. KI5.5 also assigns its final bound verdict `False`.

The unchanged Lean theorem proves positive and negative witnesses for the
abstract error `2*d2-d4`. It encodes no energy functional, trial space, solver,
minimizer, convergence, normalization, comparator, or physical interpretation.

## Verification and Dependency Replay

Primary, source-independent, and typed graph routes pass 39, 16, and 31 checks.
The six-node graph has 36 predicate sites and six assertions, reuses E1, E2,
E3, MK5, and MR5 executions, and freshly executes KI5. E1, E2, E3, and KI5 use
lazy current-first `numpy.trapezoid` dispatch; no version-only stop occurs.
Thirty-four focused accepted-consumer tests and both full 1,478-test executions
pass with 700 valid memory records.

## Four-Axis Decision

The source verdict and accepted claim state remain separate.

- Verification: exact evidence for signed-slack algebra and conditional error
  consequences; finite numeric evidence for selected profile perturbations.
- Review: audited and qualified predicate by predicate.
- Compatibility: compatible with C-RDIFF-001/002 and C-RPROF-002 at narrow scope.
- Epistemic: qualified source evidence, not a new accepted claim.
- Release: v0.127.0 unchanged.

## Closure

P175 changes campaign, KI5 disposition, queue, proposal and decision memory,
and parent effort only. MK5 and MR5 remain pending. No new API, accepted claim,
generated documentation, or release is created.
