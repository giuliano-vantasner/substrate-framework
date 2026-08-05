---
description: Independent claim-level review of conditional continuum density of states and mode counting
author: vantasner-review
created: '2026-08-11T20:58:00Z'
updated: '2026-08-11T21:04:00Z'
tags:
- substrate-framework
- claim-review
- C-DOS-001
- P196
category: decisions
confidence: established
status: active
---
# C-DOS-001 Claim Review

## Claim Under Review

For a separately supplied positive integer spatial dimension `d`, positive
integer branch degeneracy `b`, positive `V` and `c`, nonnegative gap
`omega_0`, and continuum phase-space measure `V*d^d k/(2*pi)^d`, the isotropic
dispersion `omega(k)=sqrt(omega_0^2+c^2*k^2)` has the proposed open-band DOS.
The claim includes its exact radial-ball integral, fixed-cutoff gap
independence, and positive cutoff solving a separately supplied target count.

## Sourced Inputs

The review read v0.144.0, C-MED-003, C-SG-018, C-KRN-001, P196's frozen
formula and attempts, canonical implementation and tests, both verifiers, the
hash-pinned MD1 source, all five source dependencies, and the three direct
reverse consumers. None supplies an accepted d3 scalar-medium lift, branch
count, finite cell complex, microscopic cutoff, or participating-mode map.

## Independence

The primary route derives the canonical formula from radial shell area and the
inverse-dispersion Jacobian. The independent route imports no candidate API
and reconstructs sphere factors, threshold limits, four frequency integrals,
the d3 corollary, and finite-rank counterexamples directly in SymPy.

## Verification Status

The claim earns symbolic verification. Forty primary and 28 independent checks
pass with clean exit; every integral simplifies to a closed expression with no
unevaluated Integral, condition, or numerical tolerance. Seventeen focused
package tests pass. The oracle matches the exact algebraic obligation.

## Sensitivity and Counterexamples

Changing the sphere surface, Fourier denominator, or branch multiplier breaks
the count. The d1 DOS has the correct integrable open-band divergence, d2 has
a finite edge, and d3 vanishes at threshold. Gapless limits retain the correct
dimension-dependent power. A finite periodic one-dimensional box has three
wavevectors at a boundary where the continuum count is two, proving the exact
finite-rank overread false. Scalar and vector fields in the same d3 space have
different component ranks, and equal total mode counts admit different active
coupling supports.

## Framework Compatibility

The theorem is a native compatible extension because every new input is typed
and declared. It does not lift C-MED-003 out of one spatial coordinate or use
QCD5 as dimension authority. The exact target inversion is not a microscopic
Brillouin-zone derivation. No material, cell topology, integer divisibility,
polarization, interaction, coupling, occupation, rate, or observation enters.

## Dependency and Consumer Replay

The claim is logically self-contained and has no accepted-claim dependency.
Its source comparisons remain individually governed. MD2, MD4, and MD6 have no
legacy quadrature surface and reproduce 26, 34, and 40 checks respectively;
they remain pending and inherit no physical conclusion.

## Competing Candidate Audit

Candidates A through E and structural criteria were frozen before renewed MD1
execution. General-d continuum Candidate A and typed d3 corollary C win on
exactness and assumption economy. Exact finite lattice Candidate B needs a
different supplied object. Nonduplication Candidate D fails because C-SG-018
explicitly excludes DOS, and foundational Candidate E has no independent
inconsistency trigger.

## Four-Axis Decision

The four axes support claim-level promotion without adopting MD1 wholesale.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new claim; no challenge or supersession

## Promotion Transaction

Accept C-DOS-001 with `mode_counting.py`, its package exports and tests, both
exact routes, this individual review, the MD1 qualified disposition, a new
release, regenerated docs and accepted memory, regenerated source queue, one
integrated validation boundary, and an empty debt ledger.

## Continuation if Not Accepted

This clause is inactive because the exact conditional theorem is accepted for
promotion. A discrete lattice-rank theorem remains a distinct future objective
rather than hidden debt.

## Done Gate

Promotion is recommended once the source graph, generated records, release,
and terminal validation transaction close without debt.

## Cross-References

The authoritative artifacts are P196, C-SG-018, C-KRN-001, the canonical
module and tests, MD1's source audit, and the three pending consumer records.

