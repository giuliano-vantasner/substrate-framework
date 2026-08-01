---
description: Independent review of C-WIL-001
author: vantasner-review
created: '2026-08-01T16:01:23Z'
updated: '2026-08-01T16:01:23Z'
tags:
- substrate-framework
- claim-review
- wilson-loop
category: decisions
confidence: working
status: archived
---
# Review of C-WIL-001

## Claim Under Review

Conditional on a separately declared positive rectangular area-law expectation,
the large-time logarithmic extraction gives a linear potential. A separately
declared perimeter law instead gives an R-independent large-time contribution.

## Sourced Inputs

The review read `v0.24.0`, P028, exact and independent limit routes, package
APIs/tests, hash-pinned CF3, its source reproduction, and adjudication.

## Independence

The main route calls pure loop and extraction helpers. The independent route
works directly from the two logarithm exponents and takes both large-time
limits without importing the Wilson helper module.

## Verification Status

Exact logarithms, limits, and derivatives support `symbolic_verified`. The
status applies to the premise-to-conclusion implication, not to either premise
being realized by a physical gauge theory.

## Sensitivity and Counterexamples

Flipping the area exponent sign, replacing the product by a sum, or removing R
breaks the positive linear slope. The declared perimeter law retains the same
SU(3) center algebra but has zero separation derivative, so center alone cannot
select the area law.

## Framework Compatibility

This is a compatible premise-explicit mathematical extension with no accepted
scientific dependency. Positive R, T, and coefficients and the extraction rule
are all stated; no Wilson measure, physical tension, or confinement map enters.

## Dependency and Consumer Replay

The theorem deliberately has no dependency on the SU(3) center claim because
neither expression follows from center algebra. Consumers are
`wilson_loops.py`, package exports/tests, CF3's disposition, and pending
area-law audits. Focused tests pass and no claim debt remains.

## Competing Candidate Audit

Candidate A was selected over B because both exact conditional limits are
reusable and expose the premise boundary. Candidate C is rejected by the
same-center perimeter countermodel and CF3's own provenance labels.

## Four-Axis Decision

The axes describe the conditional implication only.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new conditional loop-law theorem

## Promotion Transaction

Promotion adds pure loop APIs/tests, registry entry, immutable P028, qualified
CF3 disposition, release/generated records, and parent synchronization.

## Continuation if Not Accepted

If the implication had no distinct consumer, Candidate B would retain the
positive center result alone. Physical law selection requires a new proposal.

## Done Gate

Premises, exact limits, mutations, countermodel, consumers, qualification, and
debt closure are complete.

## Cross-References

See P028, CF3, `wilson_loops.py`, and the parent migration effort.
