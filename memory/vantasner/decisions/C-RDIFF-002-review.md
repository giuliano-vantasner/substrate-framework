---
description: Independent review of the corrected conditional B2-B4 energy-difference coefficient
author: vantasner-review
created: '2026-08-07T16:55:00Z'
updated: '2026-08-07T16:55:00Z'
tags:
- substrate-framework
- claim-review
- energy-difference
- numerical-evidence
category: decisions
confidence: established
status: archived
---
# Review of C-RDIFF-002

## Claim Under Review

C-RDIFF-002 specializes C-RDIFF-001 to multiplicity two, declared
normalization `3*pi^2`, and C-RPROF-002's B=2 and B=4 stationary-branch energy
coefficients. It reports the normalized difference, scaled coefficient, and a
two-method rectangular sensitivity envelope. It is not a physical mass,
binding energy, variational bound, state assignment, reaction, or yield.

## Sourced Inputs

The review reads release v0.89.0, C-RDIFF-001, C-RPROF-002, P105 attempts 0005
and 0006 with pinned SHA-256 hashes, P106's exact and independent verifiers,
attempts 0001 through 0004, source and numerical audits, dependency and
consumer ledgers, focused package tests, and E3's reproduction. The source's
biased 8.457 value and empirical 23.86 MeV literal are comparators only.

## Independence

The primary route loads hash-pinned P105 canonical and independent snapshots,
derives the combination symbolically, and then evaluates it. The independent
review imports neither the primary verifier nor canonical API: it reads the
same immutable P105 evidence, rebuilds the mass and binding expressions with
fresh symbols, and computes the monotone interval endpoints separately.

## Verification Status

The maximum verdict is `numeric_evidence`. P105's canonical binary64 values
give normalized difference `0.2864828542962012` and coefficient
`8.482417318795285`; its independent collocation values give
`8.482414868843847`. The rectangular cross-method envelope is
`[8.482414867768218, 8.482417319870914]`. The exact transformation is owned by
C-RDIFF-001, while these inputs and decimals retain C-RPROF-002's
resolution-bounded status.

## Sensitivity and Counterexamples

Both P105 methods lie in the declared monotone envelope and its lower endpoint
is positive. The envelope width is below `3e-6`, but it is explicitly a
two-method sensitivity construction rather than a statistical confidence
interval or rigorous discretization enclosure. E3's 7.5-to-9.5 band accepts
both 0.9 and 1.1 normalization mutations and therefore cannot validate this
coefficient. Factor, multiplicity, sign, and branch-value mutations change the
result. One-ULP differences between finite-decimal and binary64 evaluation are
bounded as numeric regression, not mistaken for exact equality.

## Framework Compatibility

C-RPROF-002 supplies conditional stationary-branch coefficients only. The
`3*pi^2` normalization remains a declared mathematical input to this claim,
not an accepted physical multi-soliton mass map. The result is a compatible
conditional coordinate and carries no action, global minimum, baryon,
deuteron, helium, quantum correction, reaction, empirical scale, or BPS model.

## Dependency and Consumer Replay

The claim depends only on C-RDIFF-001 and C-RPROF-002. C-SK-001 is
compatibility context, not a multi-degree derivation. Later KI, MK, and MR
consumers must replace 8.46 with this corrected anchor if they use the accepted
surface, but receive no automatic promotion of their interpolation, coupling,
solver, mass, or physical conclusions. Focused package and campaign checks
exercise the actual transform without rerunning P105's already accepted BVPs.

## Competing Candidate Audit

The accepted-input composition and independent method envelope were frozen as
structural criteria before post-freeze source execution. Source reproduction,
fresh algebra, interval propagation, bound counterexamples, physical audit,
and nonduplication were compared without selecting by empirical proximity.
Proposal revision 0001 separated this numeric status from the exact theorem.

## Four-Axis Decision

The conditional specialization is accepted on four independent axes.

- Verification: `numeric_evidence`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `qualified`
- Relationship: depends on C-RDIFF-001 and C-RPROF-002; challenges and supersedes none

## Promotion Transaction

Promotion adds C-RDIFF-002 beside C-RDIFF-001, reuses the minimal package API
and tests, freezes P106 evidence, qualifies E3, creates release v0.90.0,
regenerates canonical docs and memory, and updates the parent effort. No source
consumer or empirical literal is mutated.

## Continuation if Not Accepted

If snapshot provenance, interval monotonicity, method agreement, or dependency
closure fails, the numeric claim returns for a new P106 attempt while the exact
C-RDIFF-001 review remains separate. A failed physical interpretation does not
convert this conditional coefficient into campaign completion.

## Done Gate

Acceptance requires both pinned P105 methods, transparent status-preserving
propagation, mutation sensitivity, independent construction, importable API,
source and consumer ceilings, synchronized canonical records, one final full
gate, and no debt.

## Cross-References

See P106, E3, C-RDIFF-001, C-RPROF-002, P105 attempts 0005/0006,
`energy_differences.py`, release v0.90.0, and the framework-migration effort.
