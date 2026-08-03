---
description: Independent review of the all-order classical cosine mixed-coordinate coefficient theorem
author: vantasner-review
created: '2026-08-07T19:30:00Z'
updated: '2026-08-07T19:30:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- mixed-taylor-coefficients
category: decisions
confidence: established
status: archived
---
# Review of C-SG-019

## Claim Under Review

C-SG-019 states the exact coefficient theorem for the declared classical local
function `A*(1-cos(phi0+a_H*H+a_L*L))`. For nonnegative integer orders `j,k`,
the coefficient of `H^j*L^k` is the `(j+k)`th derivative of `A*(1-cos(phi))`
at `phi0`, multiplied by `a_H^j*a_L^k/(j!*k!)`. At zero background the
constant and positive odd-total coefficients vanish, while positive even-total
coefficients have the displayed alternating sign. The one-high specialization,
factorial decay, coordinate dependence, and finite-truncation ceiling are part
of the claim. Quantum-process meanings are explicitly excluded.

## Sourced Inputs

The review reads release v0.91.0, C-SG-012 and C-BRK-001, P109's frozen
contract, PN1 at SHA-256
`f2fcd58c97b9e9aa0b92e0ece9d92ff6c7ddaddec1b385b10a68a156ac3df985`,
all append-only attempts, primary and independent verifiers, package module,
focused tests, source and predicate audits, dependency ledger, and the eight
pinned scientific or interpretive consumers plus the PN4 honesty-scan edge.

## Independence

The primary route differentiates the declared function and cross-checks a
two-dimensional coefficient grid. The independent reviewer imports no
canonical coefficient helper. It starts from complex exponentials, derives the
derivative cycle afresh, and reconstructs mixed terms with the binomial
theorem. It independently exposes the first omitted truncation term.

## Verification Status

The maximum verdict is `symbolic_verified`. Exact SymPy identities and direct
integer/factorial algebra cover arbitrary-order formulas symbolically and
finite grids operationally. Entire convergence and the limit `1/n! -> 0` are
mathematical imports with explicit exact checks. No numerical or simulation
evidence is inflated into an exact or physical verdict.

## Sensitivity and Counterexamples

Wrong sign, wrong parity, missing factorial, changed amplitude, and changed
coordinate-scale mutations break relevant predicates. Expanding at `pi/2`
exchanges positive-order parity support and preserves a nonzero constant,
disproving a background-free parity reading. A degree-eight polynomial has a
nonzero degree-ten remainder. Attempts 0002 through 0004 preserve one wrong
test expectation and two independent-oracle defects; all were repaired without
changing the theorem or weakening a check.

## Framework Compatibility

The claim is a compatible extension of C-SG-012's declared classical
potential. It changes no accepted invariant, solver, field ontology, or scale.
C-BRK-001 remains the univariate sixth-order surface. The new theorem adds the
all-order mixed coordinate formula and makes normalization and background
dependence explicit.

## Dependency and Consumer Replay

The only accepted dependency is C-SG-012. FS1, NC1, and NC2 provide no mode
split or quantization. PN2, WN1, WN2, WN3, WN6, MD3, and the PN4/PN6 scan or
coverage edges remain pending. They may reuse the exact classical coefficient
but inherit no operator, state, weight, rate, resonance, kinematic channel, or
material interpretation.

## Competing Candidate Audit

Literal reproduction, entire-series, mixed-derivative, background, coordinate-
rescaling, convergence, quantum-ceiling, and nonduplication candidates were
frozen before source execution. Exact closure, independent agreement,
sensitivity, and consumer reach selected B through H; no empirical value or
later physical conclusion selected the claim.

## Four-Axis Decision

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: challenges and supersedes none

## Promotion Transaction

Promotion adds C-SG-019, the pure `cosine_vertices.py` API and tests, immutable
P109 evidence, qualified PN1 disposition, release v0.92.0, generated docs and
memory, and the parent migration checkpoint. The integrated gate runs once at
the final scientific boundary.

## Continuation if Not Accepted

If a sign, factorial, background, normalization, truncation, dependency, or
consumer gate fails, the claim returns to P109 for an append-only repair and
PN1 remains pending. Missing quantum premises do not weaken the exact classical
theorem and do prevent promotion of PN1's broader headline.

## Done Gate

Acceptance requires both derivations, sensitive mutations, exact package APIs,
focused tests, complete predicate and consumer audits, synchronized records,
and an empty claim ledger.

## Cross-References

See P109, PN1, C-SG-012, C-BRK-001, `cosine_vertices.py`, release v0.92.0,
and the framework-migration effort.
