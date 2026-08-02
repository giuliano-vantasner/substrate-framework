---
description: Independent duplicate review of AS4's over-determination-v2 system
author: vantasner-review
created: '2026-08-02T19:02:40Z'
updated: '2026-08-02T19:08:02Z'
tags:
- substrate-framework
- source-review
- duplicate-evidence
- migration-AS4
category: decisions
confidence: working
status: archived
---
# Review of AS4 Duplicate Evidence

## Claims Under Review

The review asks whether AS4 changes C-LIN-001 or C-IDN-001, whether it
instantiates C-GLS-001, and whether its physical over-determination narrative
warrants a distinct accepted claim. The proposed source-unit disposition is
`duplicate_evidence`.

## Sourced Inputs

The review reads `v0.68.0`, C-LIN-001, C-IDN-001, C-GLS-001, C-RGE-003,
C-GRV-001, their canonical APIs and tests, P075's frozen contract, attempts
0001 through 0003, the hash-pinned AS4 body and clean reproduction, the source
audit, candidate comparison, provenance inventory, and impact map. Every cited
pending source remains noncanonical.

## Independence

The primary route uses accepted diagnostics. The independent route imports no
linear-system or scale-constraint API: it row-reduces the matrix, constructs
two explicit left-null vectors, solves the compatible system, restores
nuisances, differentiates the baseline-plus-induced gravity law, and derives
weighted normal equations directly in SymPy.

## Existing-Claim Decisions

C-LIN-001 is unchanged because it already distinguishes coefficient rank,
augmented consistency, uniqueness, and equation count. C-IDN-001 is unchanged
because its accepted P065 evidence explicitly derives AS4's two coefficient
directions and two compatibility relations while denying physical provenance
or absolute scale. C-GLS-001 is unchanged and not instantiated because AS4
provides no covariance or stochastic model.

## Verification Status

Twenty-eight primary and sixteen independent exact checks support the
duplicate classification after one preserved harness failure and one preserved
two-predicate representation failure. They do not add verification status to
the existing claims. The source's seven-check tally omits augmented rank,
accepts several coefficient mutations, and contains a guard whose passing
predicate contradicts its prose.

## Sensitivity and Counterexamples

Perturbing either dependent right-hand side raises augmented rank. Mutating
three omitted x coefficients leaves AS4.1 green while changing compatibility.
Wrong prediction coefficients pass AS4.4's symbol-occurrence test. The stated
free-length matrix has nullity zero, while a corrected proportional row has
nullity one. Free sector coefficients reopen a mixed scale-coupling direction,
an additive inverse-G baseline removes the constant gravity log slope, and
different declared covariances change the residual ledger without changing
coefficient rank.

## Framework Compatibility

The narrow exact linear algebra is native and already accepted. The source's
physical rows, independence, scale emergence, predictions, and deferral expiry
exceed accepted AS1-AS3 and sector ceilings. Keeping supplied quantities
symbolic does not make them derived, and dimensionless nuisance coefficients
remain load-bearing parameters.

## Dependency and Consumer Replay

AS4 has no distinct scientific consumer beyond C-LIN-001 and C-IDN-001's
existing generic APIs. P075 adds no package helper, formal theorem, registry
entry, or release. The affected 78 canonical tests pass, and the migration
queue is the only generated consumer changed by the final transaction.

## Competing Candidate Audit

Candidate B is selected as the exact duplicate specialization, Candidate C as
its left-null restatement, and Candidates D-F as counterexample and scope
audits. Candidate A is rejected because the source lacks dependency closure,
observations, covariance, provenance evidence, and sensitive headline checks.
No empirical comparator or source tally selected the disposition.

## Four-Axis Decision

No new claim receives four-axis promotion. Existing claim axes remain
unchanged, C-GLS-001 remains uninstantiated, and AS4 is retained as
noncanonical duplicate evidence.

## Promotion Transaction

There is no registry or release promotion. The transaction freezes P075,
changes AS4's authoritative migration disposition with structured duplicate
reason and durable evidence, regenerates the source queue, archives proposal
memory, synchronizes the parent effort, and replays the unchanged `v0.68.0`
accepted boundary.

## Continuation if Not Accepted

This source adds no claim, but the positive campaign object is the exact
terminal classification and durable source mapping. The parent migration
continues to AS5 rather than stopping at AS4's failed physical interpretation.

## Done Gate

The duplicate decision closes only after both exact routes, source
reproduction, mutation audit, nuisance and covariance ceilings, queue
regeneration, memory validation, integrated workflow validation, and diff
checks pass with no campaign debt.

## Cross-References

See P075, AS4, P022, P065, C-LIN-001, C-IDN-001, C-GLS-001, C-RGE-003,
C-GRV-001, and the parent migration effort.
