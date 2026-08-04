---
description: Independent review of C-RGE-005 exact gauge-only product-group coefficient ledger
author: vantasner-review
created: '2026-08-08T20:30:00Z'
updated: '2026-08-08T20:30:00Z'
tags:
- substrate-framework
- claim-review
- gauge-beta
- two-loop
- normalization-covariance
category: decisions
confidence: established
status: archived
---
# C-RGE-005 Review

## Claim Under Review

C-RGE-005 states an exact one- and two-loop gauge-only coefficient ledger for
separately supplied product-representation invariants, under explicit imported
modified-minimal-subtraction weights, and its Abelian coordinate covariance.

## Sourced Inputs

The review reads v0.98.0, C-LIE-001, C-REP-001, C-RGE-001, C-RGE-002,
C-RGE-004, the frozen P129 contract, every attempt, the canonical module and
tests, both exact verifiers, every campaign audit, and the primary formula
sources. WM5 is pinned at SHA-256
`8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc`.

WM5's eleven predicates are reviewed individually. Exact representation sums
survive with stronger input and convention typing. Claims to derive the field
content, upgrade pending SM4, produce the full two-loop Standard Model beta
function, use the comparison table only after the headline, or establish a
global running conclusion do not survive.

## Independence

The independent route imports none of `gauge_beta.py`. It freshly enumerates
six supplied multiplet rows, reconstructs spectator-degenerate Dynkin indices
and factor Casimirs, applies the audited loop weights, and derives the full
vector and matrix. It separately derives the Abelian scaling laws, substitutes
the inverse coupling change into the beta polynomial, and specializes the QCD
diagonal entry through Dirac pairs.

One failed review attempt omitted each row's generation multiplicity before
dividing its moments by three. The already correct vector and matrix exposed
that verifier-only aggregation mistake. The failure is preserved and the
independent moment oracle now uses the declared multiplicities.

## Verification Status

The verdict is symbolic verified. Twenty-eight primary and twelve independent
checks establish source and freeze hashes, executable provenance, hard-coded
inputs, comparator placement, exact coefficients, contribution decomposition,
scope omissions, Abelian covariance, beta covariance, and sensitive mutations.
Sixteen focused tests exercise the public API and invalid domains.

No quadrature, tolerance, sampled equality, or NumPy integration alias carries
the accepted claim. WM5 itself and three direct consumers reproduce 39 checks,
but consumer output promotes no pending running or boundary claim.

## Sensitivity and Counterexamples

Removing the scalar, changing generation multiplicity, deleting Q_L color,
perturbing a supplied charge, switching Weyl to Dirac counting, or transposing
the asymmetric matrix changes the verdict. Invalid factors, floating
invariants, wrong tuple lengths, negative invariants, zero multiplicities,
multiple Abelian factors, and non-Abelian rescalings are rejected.

The same exact table changes under an Abelian coordinate rescaling exactly as
`b'_a=rho_a^2*b_a` and `B'_ab=rho_a^2*rho_b^2*B_ab`; inverse coupling scaling
restores beta-vector covariance. Raw Abelian entries therefore cannot select a
normalization or embedding.

## Framework Compatibility

The claim is a compatible extension. It composes accepted convention-specific
SU3 facts, supplied-table and Abelian-coordinate ceilings, and existing RGE
conventions with an explicitly approved external perturbative formula. It does
not infer non-Abelian representations from C-REP-001 or grant authority to
pending SM2 and SM4.

The scope permits at most one Abelian factor and excludes its kinetic-mixing
generalization. The same-order Yukawa term, thresholds, matching, boundary
conditions, perturbative domain, physical field content, anomaly selection,
unification, observation, and substrate identity remain separate premises.

## Dependency and Consumer Replay

WM5 dynamically imports WM1, SM2, and SM4. Only WM1 has a qualified accepted
surface, and that surface explicitly withholds physical representation
semantics. QCD1, QCD3, SM3, WM2, and WM6 are prose dependencies in WM5.

WM6, WM7, and WM10 replay 28 checks from pinned hashes. Their coefficient use
is compatible with C-RGE-005, while their running, induction, comparator, and
closure conclusions remain pending. The campaign debt ledger is empty.

## Competing Candidate Audit

Literal reproduction, a generic ledger, fresh enumeration, provenance audit,
Abelian covariance, convention mutants, full-beta ceiling, field mutations,
and blinded comparison with global replay were frozen before source execution.
The generic ledger wins on exactness, explicit premises, parameter economy,
normalization covariance, reuse, and natural fit. Comparator closeness selects
nothing.

## Four-Axis Decision

The claim receives separate accepted axes after claim-level review.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: no challenge or supersession

## Promotion Transaction

Promotion adds `gauge_beta.py` and sixteen tests, exports its public records and
functions, archives P129, adds C-RGE-005 to the registry and v0.99.0 manifest,
qualifies WM5, regenerates the queue, and renders canonical documentation and
memory. One integrated repository gate runs after assembly; the terminal
attempt is finalized only after clean exit.

## Continuation if Not Accepted

If the promotion gate fails, P129 remains active and the exact API, independent
oracle, input typing, registry, release, generated consumer, or evidence layer
is repaired without weakening the scope or importing the rejected headline.

## Done Gate

C-RGE-005 is accepted only with an importable exact ledger, explicit formula
provenance and omissions, independent representation sums, sensitive
conventions and mutations, synchronized governance state, downstream replay,
and an empty debt ledger.

## Cross-References

See P024, P073, P083, P081, P129, QCD3, WM1, WM5, WM6, WM7, WM10,
C-LIE-001, C-REP-001, C-RGE-001, C-RGE-002, C-RGE-004, C-RGE-005, v0.98.0,
and the framework-migration effort.
