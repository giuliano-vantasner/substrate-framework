---
description: Qualify SC1 through accepted Gordon geometry, canonical scalar stress, and the exact compatibility locus
author: vantasner-review
created: '2026-08-11T06:49:00Z'
updated: '2026-08-11T06:49:00Z'
tags: [substrate-framework, source-review, migration-SC1, gordon-metric]
category: decisions
confidence: established
status: archived
---
# SC1 Qualified Review

## Source Unit Under Review

SC1 executes five predicates and argues that a Gordon geometry cannot be
sourced nontrivially by its selected scalar ansatz, with two additional guard
calculations and a claimed handoff to SC2.

## Surviving Content

The component-ratio idea and vacuum endpoint survive only after replacing the
source's metric and stress by the accepted C-GOR-001 and C-STG-001 objects.
C-GOR-002 then proves the stronger exact statement: for a real canonical
scalar depending on `t,x`, the full covariant Einstein equations hold only on
the zero-gradient, zero-potential, reciprocal-affine index locus, and the
converse holds algebraically.

## Corrected Scope

SC1 uses the wrong mostly-plus Gordon coefficient, reproduces the rejected
`5/6` witness, and reverses the canonical potential sign. It omits `tx`,
divides by a velocity without treating rest, and stops before the remaining
curvature equation. With canonical stress, dropping `xx` gives
`U_x^2=-2V`; hence its Guard A positive family does not survive for a
nonnegative cosine potential. Guard B only reproduces the old G2 error.

## Verification and Compatibility

Primary, independent, and graph routes pass 35, 14, and 21 exact checks; 53
focused tests, the 29-check C-GOR-001 verifier, and the 1,514-test integrated
promotion boundary pass. G2, G3, SC1, and SC2
all run natively and contain no NumPy integration-name compatibility event,
so no version spelling affects a scientific verdict.

## Four-Axis Decision

The source receives a qualified evidence status rather than blanket acceptance.

- Verification: symbolic evidence for C-GOR-002; source reproduction evidence for SC1.
- Review: audited and qualified predicate by predicate.
- Compatibility: corrected through C-GOR-001, C-STG-001, and C-GOR-002.
- Epistemic: qualified source evidence, not blanket promotion of source prose.
- Release: v0.130.0 adds C-GOR-002 only.

## Closure

Qualify SC1 through C-GOR-001, C-STG-001, and C-GOR-002. Its original tensor
formulas, single-component blocker diagnosis, unrestricted-boost language,
breather embedding, material and physical-gravity readings, and assertion
that SC2 closes the alternative route remain unaccepted. SC2 stays pending
and receives no blanket authority.
