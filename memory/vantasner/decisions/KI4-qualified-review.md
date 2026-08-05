---
description: Qualify KI4 as same-datum inverse reconstruction and reject its zero-information and cycle overclaims
author: vantasner-review
created: '2026-08-11T03:50:00Z'
updated: '2026-08-11T04:01:00Z'
tags:
- substrate-framework
- source-review
- migration-KI4
- inverse-reconstruction
category: decisions
confidence: established
status: archived
---
# KI4 Qualified Review

## Source Unit Under Review

KI4 calls back-solving epsilon from a supplied coefficient formally circular,
zero-information, and a directed dependency cycle.

## Exact Surviving Content

For each of three declared injective maps and a target in its open range,
substitution of the exact inverse reconstructs the same target. This is exact
same-datum inverse reconstruction. C-IDN-002 already states that such a zero
residual is not an independent overdetermination test, while C-XOV-001 owns the
conditional inverse-domain semantics.

## Scope Corrections

The source declares only positive `y`, omitting `y<K`. For `y=2K` its inverses
are negative or complex. After observing `y=K/2` through the fixed Pade map,
the compatible epsilon set is `{1}`, not the positive prior. KI4's alleged
posterior is instead assigned equal to the prior after eleven samples and is a
pre-observation output-support union.

Ordinary calibration and residual evaluation is a DAG. KI4 obtains a cycle only
by inserting `kappa_predicted -> kappa_emp`, treating a fixed observed input as
though the reconstruction modifies it. A non-independent same-datum check need
not be a computational cycle. Calibration can legitimately predict and be
refuted by a distinct held-out observable.

KI4 uses stale 8.4563 and comparator 0.929 in `disagreement > 5`; changing only
the comparator flips the predicate. Disagreement does not prove derivation
provenance. Its final guard also assigns `backsolve_is_a_derivation=False`
rather than deriving that verdict.

## Verification and Formal Scope

Primary, fresh independent, and proportional graph routes pass 37, 15, and 32
checks. The graph has seven nodes, 41 predicate sites, and seven assertions;
hash-identical executions are reused and only MK3 and MR5 are freshly replayed.
Forty-seven focused tests and both full 1,478-test executions pass with 698
valid memory records. No NumPy compatibility event occurs.
One post-gate narrow-command shape failure is preserved and repaired through
one-path memory validation and schema-aware generated-queue inspection.

The unchanged Lean theorem proves one Pade inverse identity and equality of a
prior-intersected reachable-output set with the open range. It defines no
observed-target parameter posterior, information measure, graph, or held-out
prediction. Its prior clean execution is reused.

## Four-Axis Decision

The source verdict and accepted claim state remain separate.

- Verification: exact evidence for qualified inverse reconstruction and exact
  counterexamples to stronger conditioning and graph claims.
- Review: audited and qualified predicate by predicate.
- Compatibility: compatible with C-IDN-002/C-XOV-001 at narrow scope.
- Epistemic: qualified source evidence, not a new accepted claim.
- Release: v0.127.0 unchanged.

## Closure

P174 changes campaign, KI4 disposition, queue, proposal and decision memory,
and parent effort only. MK3, MK5, and MR5 remain pending. No new API, accepted
claim, generated documentation, or release is created.
