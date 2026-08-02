---
description: Independent review of C-OVL-003 overlap-compression ledgers
author: vantasner-review
created: '2026-08-03T08:10:00Z'
updated: '2026-08-03T08:10:00Z'
tags:
- substrate-framework
- claim-review
- overlap-compression
category: decisions
confidence: established
status: archived
---
# C-OVL-003 Claim Review

## Claim Under Review

C-OVL-003 states the exact finite compression of a bounded real multiplication
operator, its Hermiticity, Rayleigh bounds, common-basis covariance, parity
blocks, commuting-Hermitian simultaneous-diagonalization criterion, and
phase/order/degeneracy ceiling. It includes the conditional asymmetric
compression of C-QBL-003's actual modes and explicitly excludes a physical
flavor interpretation.

## Sourced Inputs

The review reads release `v0.65.0`, C-QBL-003, C-MIX-001, C-MIX-002,
C-OVL-001, C-OVL-002, the frozen P072 contract, hash-pinned MH3, all attempts,
the source audit and adjudication, candidate comparison, primary provenance,
canonical module and tests, both verifier routes, and the impact analysis.
Pending later units supply no premise.

## Independence

The independent review imports no `overlap_compressions` API. It reconstructs
the sesquilinear conjugation, basis-change expansion, gamma-function mode
norms, even and odd multiplier pieces, actual and source-proxy matrices,
two-by-two commutator scalar, asymmetry dependence, and phase, permutation,
and degenerate-block counterexamples from fresh SymPy expressions.

## Verification Status

The maximum verdict is `symbolic_verified`. All promoted matrix entries,
width cancellations, parity identities, commutators, and covariance
statements are exact. A soluble Fourier compression checks the Rayleigh
interval and makes omitted conjugation fail. No numerical integration or
version-specific NumPy quadrature API appears in the claim route.

## Sensitivity and Counterexamples

Mutations reject omitted conjugation, an even multiplier's opposite-parity
cross entry, width-only texture changes, matrix difference as an eigenbasis
oracle, and nonidentity or unitarity as a basis-invariant verdict. Independent
phase and ordering choices produce nonidentity relative representatives for
equal operators, while a degenerate identity block admits arbitrary unitary
rotations. Different diagonal matrices provide the commuting counterexample
to “different texture implies misalignment.” A final diff audit also caught
and repaired the distinction between `dim U(m)-1` and the claimed extra
freedom `dim U(m)-dim U(1)^m=m^2-m`; attempt 0003 preserves that correction.

## Framework Compatibility

The claim is a compatible extension of the accepted overlap and matrix
ledgers. It uses one declared Hilbert space, measure, ordered orthonormal
basis, conjugation convention, and multiplier. The actual quartic mode matrix
does not rewrite C-QBL-003. Its odd multiplier term is a new visible
conditional premise and setting it to zero restores C-OVL-001's parity block.
No fermion, Yukawa, generation, up/down sector, charged current, CKM, Cabibbo,
mass, or hierarchy object is imported.

## Source Adjudication

MH3's exact source-proxy matrix is `pi*A/16` times
`[[4,sqrt(3)*b],[sqrt(3)*b,3]]`. Every common-width factor cancels. The source
changes `b` independently from `1/3` to `1/4`, so the changed texture and
commutator cannot be attributed to widths `1/2` and `2/3`. It also substitutes
`sech` for C-QBL-003's accepted even `sech^2` mode and uses a row transform as
though it were a column eigenbasis. The narrow asymmetric compression and
equal-input guard survive; its hierarchy and physical-mixing readings do not.

## Dependency and Consumer Replay

The direct dependencies are C-QBL-003, C-MIX-001, C-MIX-002, and C-OVL-001.
Consumers are the additive module and export, focused tests, campaign
verifiers, governance, generated artifacts, MH3 disposition, and future
compression audits. Direct search supplies the additive consumer map; no
canonical symbol is renamed. Focused tests pass 28 tests, the primary route
passes 42 checks, the independent route passes 23 checks, the focused
implementation/governance replay passes 45 tests, and the full promotion
workflow passes all 637 tests.

## Competing Candidate Audit

Candidates B through E supply the general positive theorem and its invariant
ceiling. Candidate F supplies the minimum asymmetric counterexample while
retaining its new free parameter. Candidate A is retained only as source
reproduction evidence. Comparator language selected no profile, basis, map,
or physical claim.

## Four-Axis Decision

The exact evidence supports acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-QBL-003, C-MIX-001, C-MIX-002, and C-OVL-001; challenges no accepted claim

## Promotion Transaction

Promotion adds C-OVL-003 to `v0.66.0`, qualifies MH3 through the disposition
source, regenerates the queue, and synchronizes implementation, tests,
campaign, registry, manifests, docs, and accepted memory. The exact focused,
governance, and full promotion tallies pass at the single workflow gate.

## Done Gate

The claim-level debt is empty after canonical synchronization and the 637-test
promotion replay. The parent migration remains active while source units are
pending.

## Cross-References

See P072, MH3, C-QBL-003, C-MIX-001, C-MIX-002, C-OVL-001, C-OVL-002,
`overlap_compressions.py`, `test_overlap_compressions.py`, and release
`v0.65.0`.
