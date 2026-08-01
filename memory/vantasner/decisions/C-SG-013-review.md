---
description: Independent review of C-SG-013
author: vantasner-review
created: '2026-08-02T01:06:00Z'
updated: '2026-08-02T01:25:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- boundary-correlation
category: decisions
confidence: working
status: archived
---
# Review of C-SG-013

## Claim Under Review

The claim defines a full-field fixed-coordinate boundary sign correlation and
separately derives right-half-line topological charge change. It gives the
exact parity pullback, distinguishes a transformed outward-normal boundary
channel, evaluates convention-explicit sinusoidal traces, and proves that the
two boundary functionals do not imply one another. It includes the exact
zero-correlation limit of every fixed boundary of the accepted rest breather
and excludes physical parity violation or weak-sector dynamics.

## Sourced Inputs

The review read `v0.44.0`, `C-SG-001`, `C-SG-011`, `C-SG-012`, P050's frozen
proposal and passing attempt, the new pure APIs and tests, the 37-check primary
verifier, the eight-check independent boundary review, the cited predecessor
boundary equations, and hash-pinned NC3 at SHA-256 `dceed4b3...c9bd`. NC3's
cosine transcription, shared `W_Q` label, winding-discriminator implication,
parity-even-phase label, and G1/G2/NC4/W1/W3 physical imports remain outside
the claim delta.

## Independence

The primary route uses direct half-cycle integration, canonical APIs, explicit
counterexamples, and the accepted breather. The review route derives the
square-wave Fourier coefficient, applies the parity chain rule and half-line
fundamental theorem directly, and differentiates an independently written
closed breather expression. It does not call the new density, harmonic, or
charge-conversion helpers.

## Verification Status

The maximum status is `symbolic_verified`. SymPy proves the exact definition,
parity and normal-orientation transformations, harmonic phase law, half-line
charge conversion, functional independence, continuous nonquantization, and
rest-breather cancellation. No unresolved numerical, simulation, or empirical
predicate is promoted.

## Sensitivity and Counterexamples

Changing the coordinate parity sign from minus one to zero or plus one fails;
changing the harmonic factor four to two or pi fails; and changing the inverse
frequency to frequency power zero or plus one fails. Changing the half-line
orientation coefficient from minus one to zero, plus one, or minus two fails.
An unshifted cosine trace gives `-4*B*sin(delta)/omega`, catching NC3's prose
transcription. The source's own periodic trace has nonzero correlation and
zero winding, a separate `2*pi` field change has unit winding with zero
correlation, and continuous amplitude scaling gives a noninteger correlation.
The accepted rest breather has zero complete-period correlation at every fixed
boundary.

## Framework Compatibility

The result is a compatible extension using the normalized real field,
orientation, and scalar parity conventions of the accepted sine-Gordon sector.
It adds no boundary action, phase-to-chirality dictionary, coupling, fitted
constant, or pending dependency. Coordinate and outward-normal derivatives,
complete-period and impact-window integrals, observable and dynamics, and
state asymmetry and explicit symmetry breaking remain distinct.

## Dependency and Consumer Replay

The package export change has low graph impact with no affected indexed symbol
or execution flow; the remaining code is a new module. The targeted 61-test
boundary, sine-Gordon, topological-label, and U1 replay passes, as do the P001,
P048, and P049 verifiers with status zero. No consumer or scientific debt
remains.

## Competing Candidate Audit

Candidates A, B, and C and structural criteria were frozen before the full NC3
script was read. Candidate A is selected for the literal coordinate functional
and exact positive theorem. Candidate B is retained as a necessary domain-
orientation guard rather than substituted silently for NC3's object. Candidate
C is rejected by exact parity covariance, explicit functional-independence
counterexamples, and missing accepted boundary and weak dynamics.

## Four-Axis Decision

The four axes record an exact conditional boundary theorem while qualifying
the source's physical interpretation.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-SG-001, C-SG-011, and C-SG-012; challenges and supersedes none

## Promotion Transaction

Promotion adds separately named density, harmonic-correlation, and right-half-
line charge-change APIs, exact tests, immutable P050 evidence, `C-SG-013`, a
qualified NC3 mapping, a pinned v0.45 release, generated docs, and synchronized
accepted memory. The source's exact sine-convention formula remains mapped,
while its nomenclature and physical inferences remain explicitly excluded.

## Continuation if Not Accepted

If the coordinate theorem failed, Candidate B would proceed only with an
explicit domain and normal convention. A pending PDE correlation could be
reviewed later as numerical evidence but could not repair a false model-free
implication between two independent functionals.

## Done Gate

Accepted. The positive APIs, dependency closure, independent derivation,
sensitive mutations, counterexamples, exact breather limit, consumer replay,
canonical transaction, qualified source mapping, and empty debt ledger all
pass. The single repository promotion gate validated 62 accepted claims, 218
migration units with 170 pending, 224 memory records, the repo-local skill,
and 357 tests; `git diff --check` passes separately.

## Cross-References

See P050, NC3, `C-SG-001`, `C-SG-011`, `C-SG-012`, the boundary-correlation
module, P050 source adjudication and impact review, and the active corpus-
migration effort.
