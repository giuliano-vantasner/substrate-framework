---
description: Accepted review of exact supplied-multiplet charge claim C-REP-003
author: vantasner-review
created: '2026-08-10T20:15:00Z'
updated: '2026-08-10T20:15:00Z'
tags: [substrate-framework, claim-review, C-REP-003, multiplet-charges]
category: decisions
confidence: established
status: archived
---
# C-REP-003 Claim Review

## Claim Under Review

C-REP-003 states an exact supplied-data theorem. Named finite multiplet rows
carry positive spectator multiplicities, exact isospin weights, and one common
Abelian coordinate. The claim derives grouped charges, flattened traces, fixed-
input inversion, charge conjugation, and the covariant Abelian normalization
map while excluding selection of the table or a physical matter theory.

## Sourced Inputs

The review read release v0.125.0, C-REP-001, C-REP-002, their canonical modules,
both frozen P164 proposal records, hash-pinned SM2 and its dossier, all attempts,
the primary and independent derivations, source and predicate audits, dependency
and consumer records, impact analysis, and the fourteen-node graph. C-GSM-001
and C-PGA-001 were checked as scope boundaries rather than hidden premises.

## Independence

The canonical route composes the accepted flattened trace and normalization
APIs. The independent route writes fresh SymPy sums and linear systems, does not
import `multiplet_charges`, and separately derives every supplied spectrum,
trace, target inversion, coordinate rescaling, conjugate row, Yukawa sign, and
incomplete-table counterexample.

## Verification Status

All row values, spectra, traces, residuals, ranks, and rescalings are exact
SymPy expressions. The primary route passes 33 checks and the independent route
passes 18. The strongest verdict is symbolic verification of the finite
supplied-data theorem, not formal proof of a physical generation or gauge
theory.

## Sensitivity and Counterexamples

Inconsistent target separations reject a common row value; alternative targets
select a different exact value. Removing a row or adding a neutral singlet
changes the state count. Charge conjugation changes weights and charges but not
dimension. Holding the electric coefficient fixed breaks generator-rescaling
covariance. Properly conjugated Yukawa terms cancel while the naive source
shorthand does not.

## Framework Compatibility

The theorem is a compatible extension. C-REP-001 supplies exact flattened
charge traces and normalization covariance. C-REP-002 supplies the Pauli-half
specialization and its scalar commuting Abelian boundary. No accepted
normalization, representation, mass, product-algebra, or running API changes.

## Dependency and Consumer Replay

No pre-P164 production module imports the new API. GitNexus rates every public
function LOW risk with no affected execution flow. The focused suite passes 78
tests. The source graph replays 123 lexical and 123 runtime checks across
fourteen native sources with eighteen assertions and no legacy NumPy
integration reference.

## Competing Candidate Audit

Seven candidates were registered before renewed source audit. Accepted
composition lacked grouped multiplet provenance and conjugation. Anomaly and
physical-generation candidates depended on pending or supplied premises. The
generic ledger wins by exact closure, API novelty, parameter economy, and
mutation sensitivity—not by familiar charges or a fifteen-state comparator.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive composition of C-REP-001 with the C-REP-002 doublet specialization

## Promotion Transaction

Promotion adds the pure multiplet-charge module and tests, C-REP-003, release
v0.126.0, qualified SM2 disposition, P164 adjudication, regenerated queue and
documentation, and synchronized accepted memory. No anomaly, completeness,
conservation, global-group, or physical Standard Model claim is promoted.

## Done Gate

Acceptance requires the exact theorem, independent sensitivity, consumer
replay, registry and release closure, generated-state agreement, and an empty
debt ledger. Those gates do not extend the claim beyond supplied finite data.

## Cross-References

See P164, SM2, C-REP-001, C-REP-002, `multiplet_charges.py`, its focused tests,
the source audit, independent derivation, graph replay, and impact analysis.
