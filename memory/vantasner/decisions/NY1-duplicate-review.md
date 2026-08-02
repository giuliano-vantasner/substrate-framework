---
description: Independent duplicate review of NY1's conditional Skyrme energy-unit equality
author: vantasner-review
created: '2026-08-04T00:18:00Z'
updated: '2026-08-04T00:18:00Z'
tags:
- substrate-framework
- source-review
- duplicate-evidence
- migration-NY1
category: decisions
confidence: working
status: archived
---
# Review of NY1 Duplicate Evidence

## Claims Under Review

The review asks whether NY1 changes C-SK-001 or C-DIM-003, whether its 25.69
MeV evaluation is a zero-import framework prediction, and whether it supplies
a nuclear or engine energy. The proposed disposition is `duplicate_evidence`.

## Sourced Inputs

The review reads v0.74.0, C-SK-001, C-DIM-003, their canonical modules and
tests, P008's accepted primary and independent evidence, P084's frozen
contract, the hash-pinned NY1 body and reproduction, source audit, candidate
comparison, primary provenance, literature audit, and impact map. B1, S2, and
NY2 are used only through generated queue status.

## Independence

The primary route composes accepted Skyrme APIs and audits the registry. The
independent route imports no Skyrme API or P008/P084 expression: it divides the
two monomials directly, derives the generic power family, constructs the
correction inverse, and checks the substituted closure in fresh SymPy algebra.

## Existing-Claim Decisions

C-SK-001 is unchanged because it already states the exact iff, shared linear
B1 cancellation, unequal-power ceiling, positive premises, and exclusion of
numerical comparators and physical prediction. C-DIM-003 is unchanged and used
only to confirm that reparameterizing a measured mass does not derive it.

## Verification Status

Twenty-eight primary and ten independent exact checks support the duplicate
classification. They add no verification status to either existing claim.
NY1's nine source checks reproduce, but only four are exact algebraic
restatements; the remainder are redundant substitutions or literal comparator
bands.

## Sensitivity and Counterexamples

Changing either prefactor or either B1 power breaks the advertised result. The
output has nonzero derivative with respect to E_e. A free dimensionless
`kappa` maps the same unit to every positive target, and the 34.1 MeV fit and
24 MeV engine values require different `kappa` values. The proton closure holds
for arbitrary positive B1 and E_e, proving it is not an independent oracle.

## Framework Compatibility

The conditional equality is compatible and already accepted. Neither mass
premise, the electron measurement, a universal quantum correction, a
multi-soliton binding coefficient, nuclear state identity, reaction energy, or
engine substitution is promoted. Primary literature's general 30% accuracy
statement is retained only as context.

## Dependency and Consumer Replay

NY1 has no new scientific consumer beyond C-SK-001's existing API and tests.
NY2 is later and pending. The migration queue is the only generated artifact
whose scientific disposition changes; release and generated claim records
remain v0.74.0.

## Competing Candidate Audit

Candidate B is selected as the strict duplicate. Candidates C--G supply
coefficient, provenance, empirical-input, arbitrary-target, and literature
ceilings. Candidate H finds no distinct claim. Candidate A is rejected because
the source lacks dependency closure and silently reclassifies an empirical
input as no import. Numerical proximity selected no candidate.

## Four-Axis Decision

No new claim receives four-axis promotion. Existing claim axes remain
unchanged, and NY1 is retained as noncanonical duplicate evidence for
C-SK-001.

## Promotion Transaction

There is no registry or release promotion. The transaction freezes P084,
records NY1's duplicate disposition and evidence, regenerates the source
queue, archives proposal memory, synchronizes the parent effort, and replays
the unchanged v0.74.0 boundary once.

## Continuation if Not Accepted

The positive P084 result is the complete premise, import, correction, and
duplication classification. The corpus migration continues to NY2 rather than
stopping at NY1's unsupported physical headline.

## Done Gate

The decision closes after exact primary and independent routes, every source
predicate, mutations, literature provenance, focused consumers, generated
queue, memory validation, integrated workflow, and diff check pass with empty
campaign debt.

## Cross-References

See P084, NY1, P008, C-SK-001, C-DIM-003, B1, S2, and NY2.
