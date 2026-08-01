---
description: Independent review of C-SG-011
author: vantasner-review
created: '2026-08-01T22:02:00Z'
updated: '2026-08-01T22:02:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- topological-current
category: decisions
confidence: working
status: archived
---
# Review of C-SG-011

## Claim Under Review

The claim gives the exact off-shell and on-shell balances of the two naive
sine-Gordon characteristic derivatives, the convention-fixed identically
conserved topological current, its boundary and integer-vacuum charge, and its
spatial-parity transformation. It states that parity exchanges opposite
winding sectors while preserving the field equation and explicitly excludes a
derived physical V-A or intrinsic parity-violation mechanism.

## Sourced Inputs

The review read `v0.42.0`, `C-SG-001`, `C-TOP-001`, P048's frozen proposal,
both attempts, canonical sine-Gordon APIs and tests, the 31-check primary
verifier, the seven-check independent review, and hash-pinned NC1 at SHA-256
`b7206df0...010f5`. NC1's physical weak-sector conclusion, pending W1/W3/W7
dependencies, and massless-free-limit language remain outside the claim.

## Independence

The primary route differentiates canonical current definitions in `(t,x)` and
applies the accepted equation. The review route independently changes to
`u=t+x`, `v=t-x`, constructs the antisymmetric orientation matrix directly,
uses the fundamental theorem at the boundary, and defines its own kink
profile. It does not call the new characteristic-balance, topological-current,
charge, kink, or parity helpers.

## Verification Status

The maximum status is `symbolic_verified`. SymPy establishes exact differential
identities, boundary algebra, profile residuals, parity covariance, and the
small-amplitude limit. There is no unresolved numeric, simulation, or empirical
predicate, so numerical evidence would be weaker and unnecessary.

## Sensitivity and Counterexamples

Changing the on-shell source coefficient to zero, plus one, or minus two fails.
Changing the light-cone half to one, two, or one quarter fails. Replacing the
topological flux sign minus one by zero or plus one breaks conservation, and
changing the charge denominator from `2*pi` to `pi` or `4*pi` breaks unit kink
winding. The exact small-amplitude limit retains source `-f`, countering NC1's
massless chiral-free reading. The equation's exact parity invariance counters
the inference that sector exchange itself is parity violation.

## Framework Compatibility

The claim is native to the normalized real sine-Gordon convention and does not
borrow the independent complex-field U1 current. Smoothness, orientation, and
boundary hypotheses are explicit; no fitted constants or empirical values
appear. Integer charge is restricted to vacuum boundaries. The claim preserves
the distinction between an axial transformation law, selection of a sector,
and a parity-violating interaction.

## Dependency and Consumer Replay

The canonical sine-Gordon module has low impact: direct package consumers are
the package export surface and `u1_charge`, with indirect quartic-Q-ball
consumers. Targeted sine-Gordon, topological-label, U1, quartic, and exact-sine
tests pass, as do the P001 and P019 scientific verifiers. NC2-NC4 and earlier
weak-sector source units may consume only the exact statement and ceilings.
No claim debt remains.

## Competing Candidate Audit

Candidates A, B, and C were frozen before the full NC1 script was read.
Candidate A is selected because it supplies the minimal exact positive object.
The stress-tensor alternative is broader and reserved for NC2. Candidate C is
rejected structurally by parity invariance and missing accepted weak-interaction
dependencies, not by numerical comparison.

## Four-Axis Decision

The four axes record an exact native mathematical claim without promoting the
source's physical narrative.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-SG-001; challenges and supersedes none

## Promotion Transaction

Promotion adds the current, balance, charge, kink, and parity APIs, exact tests,
immutable P048 record, claim registry entry, qualified NC1 mapping, v0.43
release manifest, generated docs, and synchronized accepted memory. The source
remains qualified with its rejected physical and free-limit remainder recorded
in durable evidence.

## Continuation if Not Accepted

If the current or parity identities failed, Candidate B would supply an exact
stress-energy construction without importing NC2 as authority. No weak-sector
narrative could repair a failed exact identity.

## Done Gate

The exact positive object, dependency closure, independent derivation,
mutations, limits, compatibility, consumers, source qualification, canonical
transaction, empty campaign debt ledger, and 342-test repository gate pass.

## Cross-References

See P048, NC1, `C-SG-001`, `C-TOP-001`, the canonical sine-Gordon module, the
P048 source adjudication, and the active corpus-migration effort.
