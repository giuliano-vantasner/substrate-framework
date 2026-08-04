---
description: Independent review of the conditional Maxwell action and point-source theorem C-MAX-001
author: vantasner-review
created: '2026-08-09T02:30:00Z'
updated: '2026-08-09T02:30:00Z'
tags: [substrate-framework, claim-review, maxwell, green-function, point-source]
category: decisions
confidence: established
status: archived
---
# Review of C-MAX-001

## Claim Under Review

C-MAX-001 states the exact consequences of an independently declared flat
Maxwell action with positive kinetic coefficient and supplied conserved current.
It derives the sourced Euler equation, Bianchi and current-compatibility
identities, source-normalized static point-charge branches in every positive
integer spatial dimension, and a separately conditional test-charge force. It
does not derive the action, current, dimension, boundary data, charge ontology,
photon, or physical electromagnetic sector.

## Sourced Inputs

The review reads v0.101.0, C-GAU-001 and C-KRN-001, the frozen P134 proposal,
hash-pinned EM3 and its dossier, attempts 0001 through 0010, the source,
dependency, consumer, compatibility, impact, nonduplication, candidate and
predicate audits, the canonical module and focused tests, and both exact
verifiers. C-U1-001 and C-FLX-001 are comparison surfaces only; pending G1,
G2, G3 and all pending consumers grant no premise.

## Independence

The primary route calls the new canonical APIs and accepted Riesz helper. The
independent route imports neither `maxwell.py` nor `momentum_kernels.py`: it
rebuilds the component action, Euler operator, gauge-source boundary identity,
antisymmetric double divergence, sphere areas, flux-normalized potentials,
lower-dimensional branches, energy gradient, and countermodels directly.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary verifier passes 31
exact/source checks, the fresh route passes 24 exact checks, and 24 focused
Maxwell/gauge/kernel tests pass. The 227-predicate immutable source-graph replay
is consumer regression only. EM3's polyfit, finite differences, and CODATA
calculation cannot upgrade or select the exact theorem.

## Sensitivity and Counterexamples

Doubling the kinetic coefficient halves potential, field, energy, and force.
Reversing source charge reverses field and force; reversing only the probe
leaves the field fixed and reverses force. Zero source and zero probe are
separate limits. The source's `A_0=-phi` mutation reverses the action-derived
Poisson sign. Exact `d=4`, `d=5`, and `d=6` solutions decay while changing the
force power. The logarithmic branch refuses an omitted reference radius. A
zero-net-charge dipole has nonzero field, and a zero source-only action permits
a non-pure connection, breaking both source guards at their overclaimed scope.

## Framework Compatibility

The claim is a compatible extension. C-GAU-001 supplies only the connection and
curvature convention; C-KRN-001 supplies the general Riesz kernel without
source or force. C-MAX-001 declares the missing action, coefficient, current,
source, dimension, boundary, and force premises rather than retrofitting them
into either accepted claim. The explicit `(+,-,...,-)` diagonal controls signs;
the source's ambiguous “mostly-plus” name is not used.

## Dependency and Consumer Replay

The accepted dependencies are C-GAU-001 and C-KRN-001. GitNexus reports LOW
additive impact and zero affected processes for the reused helpers and tracked
diff. Fifteen reverse source consumers and three pending declared dependencies
replay 227 predicates with clean exits and tallies. G1 uses a direct immutable
legacy alias; YM2 and QCD2 use eagerly evaluated dynamic legacy defaults. The
shared AST preflight detects all three and their alias-only replays pass. No
consumer imports EM3 executably, and no pending result gains authority.

## Competing Candidate Audit

Candidates B, C, and D are selected because the action variation, full
dimension family, and force close under the frozen structural criteria.
Candidate F supplies decisive countermodels. Literal Candidate A is retained
only where its exact equations survive. Candidate E alone is insufficient:
C-KRN-001 and C-FLX-001 do not contain the action, continuity condition, source
normalization, or lower-dimensional boundary cases. Comparator agreement plays
no role.

## Four-Axis Decision

The claim earns four independent accepted axes.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new conditional action and source theorem depending on C-GAU-001 and C-KRN-001

## Promotion Transaction

Promotion adds the pure Maxwell module and exports, focused tests, C-MAX-001,
release v0.102.0, generated claim/release records, qualified EM3 disposition,
and immutable P134 evidence. The workflow compatibility improvement adds the
AST preflight and updates AGENTS, the physics skill, four applicable task
templates, tests, and durable memory without changing scientific equations.

## Continuation if Not Accepted

This clause is inactive because the conditional theorem passes. Failure would
retain C-GAU-001/C-KRN-001 and qualify EM3 without a new claim. A physical
electromagnetic realization still requires a separately governed construction
of the action coefficient, conserved charged matter, dimension, boundary
conditions, source ontology, and observational dictionary.

## Done Gate

Action variation, signs, current compatibility, source normalization, all
dimension branches, force, mutations, countermodels, independent derivation,
dependencies, consumers, compatibility, novelty, implementation, and
transactional debt are closed for C-MAX-001.

## Cross-References

See P014, P027, P030, P064, P134, EM3, C-U1-001, C-GAU-001,
C-FLX-001, C-KRN-001, `maxwell.py`, `test_maxwell.py`, and the parent migration
effort.
