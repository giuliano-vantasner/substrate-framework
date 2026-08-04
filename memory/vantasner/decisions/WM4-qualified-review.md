---
description: Terminal review of WM4's conditional common linear obstruction and overbroad physical identity
author: vantasner-review
created: '2026-08-08T19:00:00Z'
updated: '2026-08-08T19:00:00Z'
tags: [substrate-framework, source-review, renormalization, migration-WM4]
category: decisions
confidence: established
status: archived
---
# Review of WM4 Terminal Qualification

## Claim Under Review

WM4 asserts that a three-crossing scale range and WM3's weak-angle miss are the
same data-free one-loop near-miss, represented by one determinant D.

## Verification and Independence

Forty-four primary and thirty-four fresh independent checks agree. At the
declared rank-two slope triple, D spans the one-dimensional linear annihilator.
All finite signed crossing differences and the conditional inverse weak-
coordinate residual are beta-only multiples of D. The range is instead an
absolute piecewise projection, and the angle map contains supplied alpha_em.

The independent route rederived the determinant, nullspace, crossings, and
inverse residual without importing the primary verifier or canonical
renormalization helpers.

## Mutations and Preserved Failures

All-equal slopes produce D=0 with parallel disjoint lines. One equal pair keeps
rank two, two crossings, and the WM3 coefficient. Three distinct slopes can
still make the WM3 denominator zero. A nonlinear positive factor times D shares
its real zero locus without being a constant multiple. Reference shifts preserve
D, while coordinate normalization and Abelian rescaling expose its convention
dependence.

Four independent-verifier construction failures are preserved: determinant
orientation, unsimplified matrix equality, substitution order, and explicit
absolute-value normalization. Each repair strengthened the
oracle without changing the scientific target or tolerance.

## Source Oracle and Provenance

WM4, SM4, and WM3 reproduce 11, 8, and 10 checks. WM4 claims its coefficients
are imported and asserted equal, but it hard-codes them and never reads SM4's
beta attributes. Its bit-for-bit statement uses `math.isclose`; its data-free
angle dictionary explicitly multiplies by alpha_em.

## Four-Axis Decision

No new claim is accepted. WM4 is terminally qualified: its exact linear
compatibility content is symbolically verified, audited, native to C-IDN-001
and C-RGE-004, and qualified against the broader physical and invariant prose.
It neither challenges nor supersedes an accepted claim.

## Dependency, Consumers, and Promotion

Pending B1, M1, SM4, and WM6 grant no authority; WM2 is duplicate evidence;
WM3 contributes only C-RGE-004. No source unit declares WM4 as a dependency.
The transaction archives P128, updates the queue, and leaves v0.98.0, canonical
APIs, accepted claims, and release memory unchanged.

## Done Gate

Closure requires source and dependency reproduction, both exact routes, all
eleven predicate verdicts, rank and denominator counterexamples, input and
normalization ledgers, nonduplication, queue and memory synchronization, one
integrated repository gate, and empty debt.

## Cross-References

See C-LIN-001, C-IDN-001, C-RGE-004, P083, WM2-WM4, SM4, WM6, P128, and
v0.98.0.
