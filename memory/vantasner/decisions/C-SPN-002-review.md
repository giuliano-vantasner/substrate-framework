---
description: Independent review of the normalized permutation-symmetric two-state ladder theorem
author: vantasner-review
created: '2026-08-07T22:30:00Z'
updated: '2026-08-07T22:30:00Z'
tags:
- substrate-framework
- claim-review
- symmetric-spin
- collective-ladder
category: decisions
confidence: established
status: archived
---
# Review of C-SPN-002

## Claim Under Review

C-SPN-002 states the exact raising and lowering coefficients on normalized
permutation-symmetric k-excitation vectors of N declared two-state factors.
It fixes the tensor-product inner product, binomial normalization, local
operator sum, real common scale, maximal-spin coordinates, edge cases,
central-rung scaling, and the projection and norm ledger for unequal complex
ground-state couplings. It explicitly states that a squared ladder
coefficient is not a physical rate.

## Sourced Inputs

The review reads release v0.92.0, all accepted registry entries, C-SPN-001 and
C-TH-001 at their canonical records, P111's frozen contract, PN3 at SHA-256
`da472079f418368926e27d22567cdf3ad8f32c836146ed8107ae2874f377b58b`,
both append-only attempts, primary and independent verifiers, the package
module and tests, predicate and source audits, dependency and candidate
ledgers, and all ten direct plus seventeen transitive pinned consumers.

PN3's normalized ground-edge formula and N=1 limit fall inside the claim. Its
rate, Rabi, superradiant, nuclear Dicke, phonon, supertransfer, material, and
observed-process readings remain outside the claim delta.

## Independence

The primary route calls the canonical API, reconstructs normalized tensor
states, and checks explicit matrices. The independent reviewer imports no
canonical symmetric-spin implementation. It builds computational vectors from
bitmasks, derives the coefficient from a fresh binomial ratio, constructs
irreducible matrices independently, and checks their commutator and Casimir.

## Verification Status

The maximum verdict is `symbolic_verified`. Exact finite-dimensional linear
algebra proves every displayed identity; exhaustive small tensor products
exercise the construction, while symbolic binomial and representation routes
establish the general formula. No unevaluated integral, numerical solver,
floating comparator, or simulation is used. The fourteen source tests are
regression and predicate evidence, not independent proof of the stronger
claim.

## Sensitivity and Counterexamples

Removing one rung factor, removing the square root, replacing the collective
sum by an average, changing operator normalization, using unnormalized Dicke
vectors, or changing coupling phases breaks the relevant verdict. The exact
central-rung limit disproves universal square-root amplitude scaling. Opposite
phases produce a zero symmetric projection with nonzero total image norm.
Zero interaction and zero on-shell spectral density preserve the ladder while
making a conditional Golden-rule expression vanish.

## Framework Compatibility

The theorem is an additive finite-dimensional mathematical surface and
changes no accepted invariant. C-SPN-001 concerns a distinct pure spin-one
orbit classification. C-TH-001 concerns a supplied two-state partition
function and explicitly supplies no amplitude or causal mechanism. No
accepted claim supplies physical constituents, state preparation, or an
interaction, so the physical ceiling is necessary and natural.

## Dependency and Consumer Replay

The claim has no accepted scientific dependency beyond approved standard
finite-dimensional mathematics. Ten direct and seventeen transitive queue
units are pinned by hash and remain separate pending candidates. None gains a
nuclear state, common phonon mode, equal site coupling, coherent preparation,
Hamiltonian, resonance, spectral density, linewidth, decoherence, or material
map from C-SPN-002.

## Competing Candidate Audit

Literal reproduction, normalized combinatorics, irreducible representation,
unequal coupling, physical-rate completion, consumer closure, and
nonduplication candidates were frozen before PN3 execution. Structural
closure selects the exact theorem, not familiarity with the textbook formula
or agreement with a quoted rate label.

## Four-Axis Decision

The four axes accept only the exact normalized algebraic theorem.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: challenges and supersedes none

## Promotion Transaction

Promotion adds C-SPN-002, the pure symmetric-spin API and tests, immutable P111
evidence, qualified PN3 disposition, release v0.93.0, generated documentation
and accepted memory, regenerated source ledger, and the parent migration
checkpoint. The integrated workflow runs once at the complete scientific
boundary.

## Continuation if Not Accepted

If normalization, all-rung, representation, unequal-coupling, physical-
ceiling, dependency, or consumer closure fails, the claim returns to P111 for
an append-only repair and PN3 remains pending. Failure of the physical rate
reading does not weaken the exact vector-space theorem and does prevent its
use as a rate premise.

## Done Gate

Acceptance requires both exact derivations, sensitive mutations, pure package
APIs, focused tests, complete predicate and consumer reviews, synchronized
registry, release, generated records, source disposition, and an empty claim
ledger.

## Cross-References

See P111, PN3, C-SPN-001, C-TH-001, `symmetric_spin.py`, release v0.93.0, and
the framework-migration effort.
