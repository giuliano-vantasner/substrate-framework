---
description: Independent review of C-OVL-001 normalized overlap and parameter ledgers
author: vantasner-review
created: '2026-08-03T05:50:00Z'
updated: '2026-08-03T06:10:00Z'
tags:
- substrate-framework
- claim-review
- normalized-overlap
category: decisions
confidence: established
status: archived
---
# C-OVL-001 Claim Review

## Claim Under Review

C-OVL-001 states normalized multiplier expectation bounds, the exact
matched-width positive-sech-power gamma ratio, the two actual C-QBL-003 mode
expectations and parity cross term, and the dimensions and free rescaling of a
separately declared overlap-times-scale product. The Cartesian measure,
matched-width premise, and physical ceiling are part of the claim.

## Sourced Inputs

The review reads release `v0.63.0`, C-QBL-001, C-QBL-003, the frozen P070
contract, hash-pinned MH1, all eight attempts, source audit and adjudication,
primary provenance, canonical module and tests, both exact verifier routes,
and the impact analysis. MH2 and MH3 remain pending and supply no premise.

## Independence

The independent review imports no `normalized_overlaps` API. It derives the
whole-line integral through a tanh beta substitution, proves the reduction
recurrence, normalizes both accepted mode shapes, derives expectation gaps as
weighted profile gaps, reconstructs dimension addition and rescaling, and
supplies a second positive functional against uniqueness.

## Verification Status

The maximum verdict is `symbolic_verified`. Every promoted statement is exact
beta/gamma algebra, normalization, parity, finite weighted-expectation algebra,
or dimensional/rescaling bookkeeping. All load-bearing SymPy expressions are
closed. No numerical quadrature, tolerance, data comparator, or simulation
enters the claim; the interrupted mismatched-width integral is preserved and
excluded rather than promoted.

## Sensitivity and Counterexamples

Mutations reject missing normalization and amplitude, wrong mode/profile
powers, negative and out-of-range expectations, replacement of the actual odd
mode by a pure sech power, hidden external scale, and a wrong dimension sum.
The actual same-profile odd/even ratio is `2/3`, not a hierarchy. Negative
profile amplitude reverses expectation sign. Independent amplitudes remain in
ratios, while reciprocal overlap/scale rescaling leaves the declared product
unchanged. A second positive functional proves that the Hessian no-go does not
select the overlap uniquely.

## Framework Compatibility

The claim is a compatible extension of C-QBL-003's exact conditional modes and
mass ceiling. It does not rename those modes as particles or modify the
quartic-Q-ball sector. The multiplier profile, matched width, amplitude,
external scale and dimensions remain inputs. Cartesian whole-line measure is
not generalized to radial or higher-dimensional problems.

## Dependency and Consumer Replay

The sole direct accepted dependency is C-QBL-003, whose closure includes
C-QBL-001. Consumers are the additive module, package exports, focused tests,
P070 primary verifier, governance, generated docs and memory, MH1 disposition,
and future overlap audits. The independent verifier deliberately shares no
canonical overlap API. Focused tests pass 21 tests, the primary route passes 51
checks, and the independent route passes 20 checks. The focused/governance
replay passes 38 tests and the full promotion workflow passes all 582 tests.
The stale graph index maps only `__all__`; direct search supplies the complete
additive consumer map.

## Competing Candidate Audit

Candidates B through E are selected because they jointly close normalization,
general exponent scope, the actual accepted modes, and parameter dimensions.
Candidate A is too weak and overinterpreted. Candidate F is already contained
in C-QBL-003 and cannot select a physical replacement. The source's
`9*pi/32` did not select a Yukawa or generation mechanism.

## Four-Axis Decision

The exact evidence and synchronized repository replay support acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-QBL-003 and challenges no accepted claim

## Promotion Transaction

Promotion adds C-OVL-001 to `v0.64.0`, qualifies MH1 through the disposition
source, regenerates the queue, and synchronizes implementation, tests, campaign,
registry, manifests, docs, and accepted memory. Staged impact detection, both
exact verifiers, focused tests, `scripts/validate.sh`, the full suite, and
`git diff --check` pass at the promotion boundary.

## Continuation if Not Accepted

If the gamma or actual-mode ledger fails, P070 continues with a direct beta
proof or narrower expectation candidate. Source failure alone cannot close the
campaign, and no physical flavor premise is imported to rescue it.

## Done Gate

The claim-level debt is empty after canonical synchronization and the 582-test
promotion replay. The parent migration remains active while units are pending.

## Cross-References

See P070, MH1, C-QBL-001, C-QBL-003, `normalized_overlaps.py`,
`test_normalized_overlaps.py`, release `v0.63.0`, and the parent effort.
